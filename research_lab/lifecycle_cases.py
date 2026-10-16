"""Elected balance/accrual, evidence and partial-settlement reference cases.

This teaching profile buys/withdraws principal at a compounded benchmark index.
It accrues margin simply on funded principal and carries benchmark return in the
index account. It is not a universal loan convention or a CBK interpretation.
The operational extension consumes already approved order terms; no external
order, identity provider, bank ledger or supervisory system is contacted.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, datetime, time, timezone
from decimal import Decimal as D, localcontext, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile

from .benchmark import Calendar, Fixing, schedule, select_fixing


def _decimal(value):
    value = D(str(value))
    if not value.is_finite():
        raise ValueError("Finite decimal required")
    return value


def _time(value):
    value = datetime.fromisoformat(value) if isinstance(value, str) else value
    if not isinstance(value, datetime) or value.utcoffset() is None:
        raise ValueError("Information timestamps require a timezone")
    return value


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _hash(value):
    return hashlib.sha256(_canonical(value).encode()).hexdigest()


def _cash(value):
    return str(value.quantize(D(".01"), rounding=ROUND_HALF_UP))


@dataclass(frozen=True)
class BalanceEvent:
    event_id: str
    effective_date: str
    available_at: str
    principal_change: str


@dataclass(frozen=True)
class MarginReset:
    reset_id: str
    effective_date: str
    available_at: str
    margin: str
    authority_id: str
    approved_contract_version: str


@dataclass(frozen=True)
class AccountProfile:
    contract_id: str = "SYNTHETIC-INDEX-ACCOUNT-1"
    contract_version: str = "v1"
    convention_id: str = "benchmark_index_account_simple_margin_v1"
    margin: str = ".03"
    fixing_floor: str | None = None
    fixing_cap: str | None = None
    day_basis: int = 365
    lookback_business_days: int = 0
    margin_convention: str = "simple_on_funded_principal"
    balance_convention: str = "benchmark_index_account"
    contract_timezone: str = "UTC"


def accrue_account(start, end, opening_principal, fixings, cutoff, profile=None,
                   balance_events=(), margin_resets=(), calendar=None):
    """Replay one specified index-account contract at an information cutoff.

    V is benchmark-index account value, P is funded principal. A principal event
    changes both by the same signed amount. Between events V grows by J(e)/J(s).
    For a source fixing span, J(t)/J(span_start)=1+r*elapsed_days/basis. This ratio
    preserves the original weekend/holiday factor when an event splits its span.
    Margin is P*k*days/basis, accrued separately and never capitalised here.

    Balance changes occur at interval starts. Positive changes are draws into
    the account; negative changes withdraw principal. Withdrawal of accrued
    return is outside this profile. A reset must reference this contract version
    and an authority identifier available by 00:00 UTC on its effective date.
    Exact-midnight approval is allowed; later intraday approval cannot authorise
    an already-started date-only accrual interval.
    """
    start = date.fromisoformat(start) if isinstance(start, str) else start
    end = date.fromisoformat(end) if isinstance(end, str) else end
    cutoff = _time(cutoff)
    profile = profile or AccountProfile()
    calendar = calendar or Calendar()
    if (not profile.contract_id or not profile.contract_version or not profile.convention_id
            or profile.margin_convention != "simple_on_funded_principal"
            or profile.balance_convention != "benchmark_index_account"
            or profile.contract_timezone != "UTC"
            or profile.day_basis <= 0 or profile.lookback_business_days < 0):
        raise ValueError("Unsupported or incomplete elected contract profile")
    opening_principal = _decimal(opening_principal)
    if opening_principal < 0:
        raise ValueError("Opening principal cannot be negative")
    floor = None if profile.fixing_floor is None else _decimal(profile.fixing_floor)
    cap = None if profile.fixing_cap is None else _decimal(profile.fixing_cap)
    if floor is not None and cap is not None and floor > cap:
        raise ValueError("Fixing floor exceeds cap")
    initial_margin = _decimal(profile.margin)
    events, resets, seen = {}, {}, set()
    for event in balance_events:
        day = date.fromisoformat(event.effective_date)
        available = _time(event.available_at)
        if not event.event_id or event.event_id in seen:
            raise ValueError("Balance-event identity is missing or duplicated")
        seen.add(event.event_id)
        if not start <= day < end:
            raise ValueError("Balance event outside half-open accrual period")
        _decimal(event.principal_change)
        if available <= cutoff:
            events.setdefault(day, []).append(event)
    reset_ids = set()
    for reset in margin_resets:
        day = date.fromisoformat(reset.effective_date)
        available = _time(reset.available_at)
        if not reset.reset_id or reset.reset_id in reset_ids or day in resets:
            raise ValueError("Reset identity/date is missing or duplicated")
        reset_ids.add(reset.reset_id)
        if not start <= day < end:
            raise ValueError("Reset outside accrual period")
        effective_at = datetime.combine(day, time.min, tzinfo=timezone.utc)
        if (not reset.authority_id or reset.approved_contract_version != profile.contract_version
                or available > effective_at):
            raise ValueError("Reset needs authority by 00:00 UTC on its effective date for this contract version")
        _decimal(reset.margin)
        if available <= cutoff:
            resets[day] = reset
    rows = schedule(start, end, calendar, profile.lookback_business_days, False)
    ledger, fixing_evidence = [], []
    with localcontext() as ctx:
        ctx.prec = 40
        principal = opening_principal
        value = opening_principal
        margin = initial_margin
        total_margin = D(0)
        net_principal = D(0)
        for row in rows:
            fixing = select_fixing(row.observation, fixings, cutoff)
            effective_rate = fixing.rate
            if floor is not None: effective_rate = max(floor, effective_rate)
            if cap is not None: effective_rate = min(cap, effective_rate)
            if 1 + effective_rate * row.weight_days / profile.day_basis <= 0:
                raise ValueError("Nonpositive span factor")
            fixing_evidence.append({"observation": fixing.observation.isoformat(),
                                    "available_at": fixing.available_at.isoformat(),
                                    "version": fixing.version, "source": fixing.source,
                                    "raw_rate": str(fixing.rate), "applied_rate": str(effective_rate)})
            boundaries = sorted({row.start, row.end} |
                                {d for d in events if row.start < d < row.end} |
                                {d for d in resets if row.start < d < row.end})
            for left, right in zip(boundaries, boundaries[1:]):
                delta = sum((_decimal(e.principal_change) for e in events.get(left, [])), D(0))
                principal += delta
                value += delta
                net_principal += delta
                if principal < 0 or value < 0:
                    raise ValueError("Principal withdrawal exceeds available principal/account value")
                if left in resets:
                    margin = _decimal(resets[left].margin)
                elapsed_left = D((left - row.start).days)
                elapsed_right = D((right - row.start).days)
                left_index = 1 + effective_rate * elapsed_left / profile.day_basis
                right_index = 1 + effective_rate * elapsed_right / profile.day_basis
                factor = right_index / left_index
                opening_value = value
                benchmark_increment = value * (factor - 1)
                margin_increment = principal * margin * D((right - left).days) / profile.day_basis
                value += benchmark_increment
                total_margin += margin_increment
                ledger.append({"start": left.isoformat(), "end": right.isoformat(),
                    "principal_event_ids": [e.event_id for e in events.get(left, [])],
                    "principal_change": str(delta), "principal": str(principal),
                    "opening_account_value_after_events": str(opening_value),
                    "subinterval_index_ratio": str(factor), "fixing_version": fixing.version,
                    "observation": row.observation.isoformat(), "applied_fixing_rate": str(effective_rate),
                    "margin_rate": str(margin), "reset_id": resets[left].reset_id if left in resets else None,
                    "benchmark_increment": str(benchmark_increment), "margin_increment": str(margin_increment),
                    "closing_account_value": str(value)})
        benchmark = value - opening_principal - net_principal
        total = benchmark + total_margin
        identity = {"profile": asdict(profile), "start": start.isoformat(), "end": end.isoformat(),
                    "opening_principal": str(opening_principal),
                    "visible_balance_events": [asdict(e) for d in sorted(events) for e in events[d]],
                    "visible_margin_resets": [asdict(resets[d]) for d in sorted(resets)]}
        return {"profile": asdict(profile), "input_contract_and_events_hash": _hash(identity),
                "calculation_cutoff": cutoff.isoformat(), "opening_principal": str(opening_principal),
                "net_principal_change": str(net_principal), "closing_principal": str(principal),
                "closing_benchmark_account_value": str(value), "benchmark_interest": str(benchmark),
                "simple_margin_interest": str(total_margin), "total_interest": str(total),
                "rounded_interest": _cash(total), "fixing_evidence": fixing_evidence,
                "result_hash": _hash({"contract": identity, "cutoff": cutoff.isoformat(),
                                      "fixings": fixing_evidence, "ledger": ledger}),
                "ledger": ledger, "scope": "Elected synthetic index-account profile; benchmark return carried, simple margin separate"}


def correction_case(original, revised, correction_id):
    """Produce an adjustment proposal, never automatically amend or post."""
    if not correction_id or original["input_contract_and_events_hash"] != revised["input_contract_and_events_hash"]:
        raise ValueError("A fixing-only correction must preserve contract and visible balance/reset events")
    if _time(revised["calculation_cutoff"]) <= _time(original["calculation_cutoff"]):
        raise ValueError("Revised cutoff must follow original cutoff")
    before, after = D(original["rounded_interest"]), D(revised["rounded_interest"])
    return {"correction_id": correction_id, "kind": "fixing_correction_proposal",
            "contract_version": original["profile"]["contract_version"],
            "original_result_hash": original["result_hash"], "revised_result_hash": revised["result_hash"],
            "original_posted_interest": str(before), "revised_interest": str(after),
            "proposed_adjustment": str(after-before),
            "unrounded_interest_change": str(D(revised["total_interest"])-D(original["total_interest"])),
            "reconciliation_residual": str(before+(after-before)-after),
            "requires_result_specific_approval": True, "contract_amendment": False, "posted": False}


def freshness_gate(evidence, cutoff, maximum_age_days, requested_action="refresh_assumption"):
    """Keep last verified rights when a source is unavailable; do not change PD/terms.

    Evidence records carry effective_at, available_at, verified_at, result,
    version and owner. 'unavailable' is evidence about access, not deterioration.
    """
    cutoff = _time(cutoff)
    if not isinstance(maximum_age_days, int) or maximum_age_days < 0:
        raise ValueError("Nonnegative governed age limit required")
    visible = []
    for e in evidence:
        effective, available = _time(e["effective_at"]), _time(e["available_at"])
        if not e.get("version") or not e.get("owner") or e["result"] not in {"confirmed", "changed", "unavailable"}:
            raise ValueError("Evidence requires version, owner and known result type")
        verified = _time(e["verified_at"]) if e.get("verified_at") else None
        if verified and verified < available:
            raise ValueError("Verification cannot precede evidence availability")
        if available <= cutoff and effective <= cutoff:
            visible.append(e)
    visible.sort(key=lambda e: (_time(e["available_at"]), e["version"]))
    verified = [e for e in visible if e.get("verified_at") and _time(e["verified_at"]) <= cutoff
                and e["result"] in {"confirmed", "changed"}]
    current = verified[-1] if verified else None
    latest = visible[-1] if visible else None
    age = (cutoff - _time(current["verified_at"])).total_seconds()/86400 if current else None
    source_unavailable = latest is not None and latest["result"] == "unavailable"
    review_pending = latest is not None and latest["result"] == "changed" and latest not in verified
    stale = age is None or age > maximum_age_days
    status = "request_evidence" if current is None or source_unavailable else "review_pending" if review_pending else "stale" if stale else "review_verified_change" if current["result"] == "changed" else "confirmed_no_change"
    return {"cutoff": cutoff.isoformat(), "status": status, "last_verified_version": current["version"] if current else None,
            "last_verified_at": current.get("verified_at") if current else None, "age_days": age,
            "source_unavailable": source_unavailable, "stale": stale, "review_pending": review_pending,
            "owner": latest["owner"] if latest else None, "requested_action": requested_action,
            "current_verified_recovery_assumption": current.get("recovery_fraction") if current else None,
            "analytical_refresh_allowed": bool(current and not stale and not source_unavailable and not review_pending),
            "contract_change_authorised": False, "borrower_pd_changed_by_this_gate": False}


class AccrualPostingBook:
    """Append-only local approval/adjustment fixture, in rounded money units.

    A correction references the immediately preceding posted result. Its delta
    is revised rounded balance less already posted rounded balance. Approval is
    bound to the exact calculation JSON; real authentication is outside scope.
    """
    def __init__(self, path):
        self.db = sqlite3.connect(str(path))
        self.db.execute("CREATE TABLE IF NOT EXISTS accrual_approvals (approval_id TEXT PRIMARY KEY, result_hash TEXT UNIQUE, result_json TEXT, maker TEXT, checker TEXT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS accrual_postings (event_id TEXT PRIMARY KEY, contract_key TEXT, result_hash TEXT, predecessor_hash TEXT, delta TEXT, receipt TEXT)")
        self.db.commit()

    def close(self): self.db.close()

    def approve(self, result, approval_id, maker, checker):
        if not approval_id or not maker or not checker or maker == checker:
            raise PermissionError("Independent checker and approval identity required")
        encoded = _canonical(result)
        row = self.db.execute("SELECT result_hash,result_json,maker,checker FROM accrual_approvals WHERE approval_id=?",(approval_id,)).fetchone()
        values = (result["result_hash"],encoded,maker,checker)
        if row:
            if row != values: raise ValueError("Approval identity reused for a different result or actor")
            return
        with self.db:
            self.db.execute("INSERT INTO accrual_approvals VALUES (?,?,?,?,?)",(approval_id,*values))

    def post(self, event_id, approval_id, predecessor_hash=None):
        if not event_id: raise ValueError("Posting business identity required")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT result_hash,result_json FROM accrual_approvals WHERE approval_id=?",(approval_id,)).fetchone()
            if not row: raise PermissionError("Result-specific approval required before posting")
            result_hash, encoded = row
            result = json.loads(encoded)
            key = result["input_contract_and_events_hash"]
            prior_event = self.db.execute("SELECT result_hash,predecessor_hash,receipt FROM accrual_postings WHERE event_id=?",(event_id,)).fetchone()
            if prior_event:
                if prior_event[:2] != (result_hash,predecessor_hash): raise ValueError("Posting identity reused with changed economic event")
                self.db.commit()
                return {**json.loads(prior_event[2]),"duplicate":True}
            previous = self.db.execute("SELECT result_hash FROM accrual_postings WHERE contract_key=? ORDER BY rowid DESC LIMIT 1",(key,)).fetchone()
            if predecessor_hash != (previous[0] if previous else None):
                raise ValueError("Correction must reference the current posted result")
            if self.db.execute("SELECT 1 FROM accrual_postings WHERE contract_key=? AND result_hash=?",(key,result_hash)).fetchone():
                raise ValueError("This result is already posted; reuse original posting identity")
            if previous:
                previous_json = self.db.execute("SELECT result_json FROM accrual_approvals WHERE result_hash=?",(previous[0],)).fetchone()[0]
                if _time(result["calculation_cutoff"]) <= _time(json.loads(previous_json)["calculation_cutoff"]):
                    raise ValueError("Correction calculation must use a later information cutoff")
            booked = sum((D(row[0]) for row in self.db.execute("SELECT delta FROM accrual_postings WHERE contract_key=?",(key,))),D(0))
            delta = D(result["rounded_interest"]) - booked
            receipt = {"event_id":event_id,"approval_id":approval_id,"result_hash":result_hash,
                       "predecessor_hash":predecessor_hash,"adjustment_money":str(delta),
                       "closing_accrual_money":result["rounded_interest"],"contract_key":key,
                       "contract_amendment":False,"duplicate":False}
            self.db.execute("INSERT INTO accrual_postings VALUES (?,?,?,?,?,?)",(event_id,key,result_hash,predecessor_hash,str(delta),_canonical(receipt)))
            self.db.commit()
            return receipt
        except Exception:
            self.db.rollback(); raise

    def ledger(self):
        return [json.loads(row[0]) for row in self.db.execute("SELECT receipt FROM accrual_postings ORDER BY rowid")]


class PartialSettlementBook:
    """Durable extension downstream of the approved-terms STP handoff.

    Amounts are integer minor currency units. Position = confirmed fills;
    settlement payable = fills less actual settled cash; order capacity is
    separate. Approval/cancellation/amendment assertions in this local fixture
    are checked for maker/checker separation and exact economic terms. They
    are not authentication of real people or external venue acknowledgement.
    """
    def __init__(self, path, currency="KES", instrument="synthetic_deposit_placement"):
        if not isinstance(currency, str) or not currency.strip() or not isinstance(instrument, str) or not instrument.strip():
            raise ValueError("Book currency and instrument are required")
        self.currency, self.instrument = currency, instrument
        self.db = sqlite3.connect(str(path))
        self.db.execute("CREATE TABLE IF NOT EXISTS book_scope (singleton INTEGER PRIMARY KEY CHECK(singleton=1), currency TEXT NOT NULL, instrument TEXT NOT NULL)")
        existing = self.db.execute("SELECT currency,instrument FROM book_scope WHERE singleton=1").fetchone()
        if existing is not None and existing != (currency, instrument):
            self.db.close()
            raise ValueError("Persisted book currency/instrument cannot be changed on restart")
        if existing is None:
            self.db.execute("INSERT INTO book_scope VALUES (1,?,?)", (currency, instrument))
        self.db.execute("CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
        self.db.commit()

    def close(self):
        self.db.close()

    @staticmethod
    def _positive(amount):
        if type(amount) is not int or amount <= 0:
            raise ValueError("Positive integer minor units required")
        return amount

    @staticmethod
    def _approval(payload):
        approval = payload.get("approval", {})
        if (not approval.get("id") or not approval.get("maker") or not approval.get("checker")
                or approval["maker"] == approval["checker"] or approval.get("terms_hash") != _hash(payload["terms"])):
            raise PermissionError("Exact terms and independent checker approval required")

    def _replay(self, events):
        state = {"currency": self.currency, "instrument": self.instrument,
                 "orders": {}, "settlements": {}, "cash_paid_minor": 0, "position_minor": 0, "approval_terms": {}}
        def record_approval(p):
            self._approval(p)
            identity, terms_hash = p["approval"]["id"], _hash(p["terms"])
            if identity in state["approval_terms"] and state["approval_terms"][identity] != terms_hash:
                raise ValueError("Approval identity reused for changed terms")
            state["approval_terms"][identity] = terms_hash
        for e in events:
            kind, p = e["kind"], e["payload"]
            if kind == "ORDER":
                record_approval(p)
                if not p.get("order_id") or p["order_id"] in state["orders"]:
                    raise ValueError("Order identity already exists; unknown acknowledgement never authorises resending")
                self._positive(p["terms"]["notional_minor"])
                if not p["terms"].get("currency") or not p["terms"].get("instrument"):
                    raise ValueError("Currency and instrument required")
                if (p["terms"]["currency"], p["terms"]["instrument"]) != (self.currency, self.instrument):
                    raise ValueError("Order currency/instrument differs from this book's aggregation scope")
                state["orders"][p["order_id"]] = {"terms": p["terms"], "terms_hash": _hash(p["terms"]),
                    "approval_id": p["approval"]["id"], "status": "SENT", "acknowledgement": "UNKNOWN",
                    "fills": {}, "filled_minor": 0, "settled_minor": 0}
                continue
            if p.get("order_id") not in state["orders"]:
                raise ValueError("Unknown order")
            order = state["orders"][p["order_id"]]
            if kind == "ACK":
                if p.get("state") not in {"UNKNOWN", "ACKNOWLEDGED"}:
                    raise ValueError("Invalid external acknowledgement status")
                order["acknowledgement"] = p["state"]
            elif kind == "AMEND":
                record_approval(p)
                self._positive(p["terms"]["notional_minor"])
                if order["status"] == "CANCELLED" or p["terms"]["notional_minor"] < order["filled_minor"]:
                    raise ValueError("Cannot amend cancelled order or below already confirmed fills")
                if {k:v for k,v in p["terms"].items() if k != "notional_minor"} != {k:v for k,v in order["terms"].items() if k != "notional_minor"}:
                    raise ValueError("This fixture only amends unfilled quantity; other term changes need a new lifecycle")
                order.update(terms=p["terms"], terms_hash=_hash(p["terms"]), approval_id=p["approval"]["id"], acknowledgement="UNKNOWN")
                order["status"] = ("FILLED" if order["filled_minor"] == p["terms"]["notional_minor"]
                                   else "PART_FILLED" if order["filled_minor"] else "SENT")
            elif kind == "CANCEL":
                cancel_terms = {"order_id":p["order_id"],"terms_hash":order["terms_hash"],"action":"cancel_unfilled"}
                record_approval({"terms":cancel_terms,"approval":p.get("approval",{})})
                if p.get("terms_hash") != order["terms_hash"] or not p.get("external_confirmation_id"):
                    raise ValueError("Cancellation requires current terms, authority and external cancellation evidence")
                order["status"] = "CANCELLED"
            elif kind == "FILL":
                amount = self._positive(p["amount_minor"])
                if order["status"] == "CANCELLED" or not p.get("fill_id") or p["fill_id"] in order["fills"]:
                    raise ValueError("Cancelled order or duplicate/missing fill identity")
                if p.get("terms_hash") != order["terms_hash"] or order["filled_minor"] + amount > order["terms"]["notional_minor"]:
                    raise ValueError("Stale/unapproved terms or overfill")
                order["fills"][p["fill_id"]] = {"amount_minor": amount, "settled_minor": 0}
                order["filled_minor"] += amount
                state["position_minor"] += amount
                order["acknowledgement"] = "ACKNOWLEDGED"
                order["status"] = "FILLED" if order["filled_minor"] == order["terms"]["notional_minor"] else "PART_FILLED"
            elif kind == "SETTLE":
                amount = self._positive(p["amount_minor"])
                if p.get("fill_id") not in order["fills"] or not p.get("settlement_id") or p["settlement_id"] in state["settlements"]:
                    raise ValueError("Unknown fill or duplicate/missing settlement business identity")
                fill = order["fills"][p["fill_id"]]
                if fill["settled_minor"] + amount > fill["amount_minor"]:
                    raise ValueError("Cumulative settlement exceeds confirmed fill")
                fill["settled_minor"] += amount
                order["settled_minor"] += amount
                state["cash_paid_minor"] += amount
                state["settlements"][p["settlement_id"]] = {"order_id": p["order_id"], "fill_id": p["fill_id"], "amount_minor": amount}
            else:
                raise ValueError("Unsupported lifecycle event")
        state["settlement_payable_minor"] = state["position_minor"] - state["cash_paid_minor"]
        state["cash_change_minor"] = -state["cash_paid_minor"]
        state["balance_residual_minor"] = state["position_minor"] + state["cash_change_minor"] - state["settlement_payable_minor"]
        for order in state["orders"].values():
            order["unfilled_minor"] = order["terms"]["notional_minor"] - order["filled_minor"]
            order["live_unfilled_minor"] = 0 if order["status"] == "CANCELLED" else order["unfilled_minor"]
            order["unsettled_filled_minor"] = order["filled_minor"] - order["settled_minor"]
        return state

    def snapshot(self):
        events = [json.loads(row[0]) for row in self.db.execute("SELECT payload FROM events ORDER BY rowid")]
        return self._replay(events)

    def apply(self, event_id, kind, payload):
        if not event_id:
            raise ValueError("Durable event identity required")
        event = {"kind": kind, "payload": payload}
        encoded = _canonical(event)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            prior = self.db.execute("SELECT payload FROM events WHERE event_id=?", (event_id,)).fetchone()
            if prior:
                if prior[0] != encoded:
                    raise ValueError("Idempotency key reused with changed content")
                self.db.commit()
                return {"duplicate": True, "state": self.snapshot()}
            events = [json.loads(row[0]) for row in self.db.execute("SELECT payload FROM events ORDER BY rowid")]
            state = self._replay(events + [event])
            self.db.execute("INSERT INTO events VALUES (?,?)", (event_id, encoded))
            self.db.commit()
            return {"duplicate": False, "state": state}
        except Exception:
            self.db.rollback()
            raise


def _approval(terms, identity="APPROVAL-1"):
    return {"id": identity, "maker": "maker", "checker": "checker", "terms_hash": _hash(terms)}


def lifecycle_examples():
    fixings = [Fixing(date(2025, 9, day), datetime.fromisoformat(f"2025-09-{available:02d}T09:00:00+03:00"),
                     D(rate), f"original-{day}") for day,available,rate in [(1,2,".08"),(2,3,".09"),(3,4,".10"),(4,5,".11"),(5,8,".12")]]
    fixings.append(Fixing(date(2025,9,5), datetime.fromisoformat("2025-09-09T09:00:00+03:00"), D(".13"), "corrected-5"))
    events = [BalanceEvent("DRAW-1", "2025-09-03", "2025-09-03T00:00:00+03:00", "200000"),
              BalanceEvent("REPAY-1", "2025-09-06", "2025-09-06T00:00:00+03:00", "-300000")]
    resets = [MarginReset("RESET-1", "2025-09-04", "2025-09-03T10:00:00+03:00", ".04", "EXECUTED-SCHEDULE-1", "v1")]
    profile = AccountProfile(fixing_floor="0", fixing_cap=".20")
    original = accrue_account("2025-09-01","2025-09-08","1000000",fixings,"2025-09-08T10:00:00+03:00",profile,events,resets)
    revised = accrue_account("2025-09-01","2025-09-08","1000000",fixings,"2025-09-09T10:00:00+03:00",profile,events,resets)
    evidence = [
        {"version":"E1","effective_at":"2025-09-01T00:00:00+03:00","available_at":"2025-09-01T09:00:00+03:00","verified_at":"2025-09-01T10:00:00+03:00","result":"confirmed","owner":"recovery-reviewer","recovery_fraction":.60},
        {"version":"E2","effective_at":"2025-09-02T00:00:00+03:00","available_at":"2025-09-02T09:00:00+03:00","verified_at":None,"result":"unavailable","owner":"recovery-reviewer"},
        {"version":"E3","effective_at":"2025-09-03T00:00:00+03:00","available_at":"2025-09-03T09:00:00+03:00","verified_at":"2025-09-04T10:00:00+03:00","result":"changed","owner":"recovery-reviewer","recovery_fraction":.30}]
    terms = {"currency":"KES","instrument":"synthetic_deposit_placement","notional_minor":1000000,"rate_bps":800}
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary)/"partial.sqlite3"
        accrual = AccrualPostingBook(Path(temporary)/"accrual.sqlite3")
        accrual.approve(original,"ACCRUAL-APPROVAL-1","maker","checker")
        accrual.post("ACCRUAL-POST-1","ACCRUAL-APPROVAL-1")
        accrual.approve(revised,"ACCRUAL-APPROVAL-2","maker","checker")
        accrual.post("ACCRUAL-POST-2","ACCRUAL-APPROVAL-2",original["result_hash"])
        accrual_replay = accrual.post("ACCRUAL-POST-2","ACCRUAL-APPROVAL-2",original["result_hash"])
        accrual_ledger = accrual.ledger()
        accrual.close()
        book = PartialSettlementBook(path)
        book.apply("ORDER-E","ORDER",{"order_id":"ORDER-1","terms":terms,"approval":_approval(terms)})
        book.apply("UNKNOWN-E","ACK",{"order_id":"ORDER-1","state":"UNKNOWN"})
        book.apply("FILL-E","FILL",{"order_id":"ORDER-1","fill_id":"FILL-1","amount_minor":600000,"terms_hash":_hash(terms)})
        book.apply("SETTLE-1-E","SETTLE",{"order_id":"ORDER-1","fill_id":"FILL-1","settlement_id":"SETTLE-1","amount_minor":200000})
        partial = book.snapshot()
        cancel_terms = {"order_id":"ORDER-1","terms_hash":_hash(terms),"action":"cancel_unfilled"}
        book.apply("CANCEL-E","CANCEL",{"order_id":"ORDER-1","terms_hash":_hash(terms),"approval":_approval(cancel_terms,"CANCEL-APPROVAL-1"),"external_confirmation_id":"CANCEL-CONFIRM-1"})
        payload = {"order_id":"ORDER-1","fill_id":"FILL-1","settlement_id":"SETTLE-2","amount_minor":400000}
        book.apply("SETTLE-2-E","SETTLE",payload)
        book.close()
        book = PartialSettlementBook(path)
        replay = book.apply("SETTLE-2-E","SETTLE",payload)
        final = book.snapshot()
        book.close()
    return {"case_id":"KESONIA-LIFECYCLE-001","status":"Synthetic reproducible reference cases",
            "original_accrual":original,"corrected_accrual":revised,
            "correction":correction_case(original,revised,"FIXING-CORRECTION-1"),
            "approved_correction_ledger":accrual_ledger,"duplicate_correction":accrual_replay["duplicate"],
            "evidence_views":[freshness_gate(evidence,f"2025-09-0{day}T12:00:00+03:00",5) for day in (1,2,3,4)],
            "partial_settlement":{"after_first_cash":partial,"final":final,"duplicate_after_restart":replay["duplicate"]}}
