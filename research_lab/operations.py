"""Dated FTP, synthetic deposit behaviour and a local, durable STP laboratory.

Standard library only. All example terms/data are invented; no Kenyan market
calibration, accounting compliance, live trade or vendor integration is claimed.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import math
from pathlib import Path
import sqlite3
import tempfile


def decimal(value) -> Decimal:
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError("Amounts and rates must be finite")
    return result


def money(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


@dataclass(frozen=True)
class AccrualSlice:
    """Half-open, constant-balance ACT/365 slice; annual decimal rates.

    Every balance/reset event must start a new slice. Reset date and liquidity
    horizon are distinct: a quarterly rate reset need not terminate commitment.
    """
    start: str
    end: str
    drawn: float
    limit: float
    customer_rate: float
    ftp_rate: float
    external_rate: float
    reset_date: str
    liquidity_horizon: str
    customer_commitment_fee: float = 0.0
    internal_liquidity_rate: float = 0.0
    external_liquidity_rate: float = 0.0


def ftp_lifecycle(slices: list[AccrualSlice]) -> dict:
    """Accrual attribution, not a discounted valuation or principal-cash ledger.

    Decimal accumulation precedes two-decimal output rounding. Treasury receives
    both internal charges. Its externally incurred commitment cost is separate
    from the drawn funding cost, so consolidation eliminates internal FTP once.
    """
    if not slices:
        raise ValueError("At least one dated slice is required")
    keys = ("customer_interest", "customer_commitment_fee", "drawn_ftp",
            "internal_commitment_cost", "external_drawn_cost", "external_commitment_cost")
    totals = dict.fromkeys(keys, Decimal(0))
    exposure_time = Decimal(0)
    undrawn_time = Decimal(0)
    rows = []
    previous_end = None
    for item in slices:
        start, end = date.fromisoformat(item.start), date.fromisoformat(item.end)
        reset, horizon = date.fromisoformat(item.reset_date), date.fromisoformat(item.liquidity_horizon)
        if end <= start or (previous_end is not None and start != previous_end):
            raise ValueError("Slices must be positive, chronological and contiguous")
        if reset > start or horizon < end:
            raise ValueError("Reset must be known by slice start; liquidity horizon must cover slice")
        previous_end = end
        drawn, limit = decimal(item.drawn), decimal(item.limit)
        if not 0 <= drawn <= limit:
            raise ValueError("Drawn balance must be between zero and limit")
        rate_names = ("customer_rate", "ftp_rate", "external_rate", "customer_commitment_fee",
                      "internal_liquidity_rate", "external_liquidity_rate")
        rates = {name: decimal(getattr(item, name)) for name in rate_names}
        if any(rates[name] < 0 for name in rate_names[3:]):
            raise ValueError("Commitment fee/cost rates cannot be negative in this laboratory")
        years = Decimal((end - start).days) / 365
        drawn_years, undrawn_years = drawn * years, (limit - drawn) * years
        exposure_time += drawn_years
        undrawn_time += undrawn_years
        values = dict(zip(keys, (
            drawn_years * rates["customer_rate"], undrawn_years * rates["customer_commitment_fee"],
            drawn_years * rates["ftp_rate"], undrawn_years * rates["internal_liquidity_rate"],
            drawn_years * rates["external_rate"], undrawn_years * rates["external_liquidity_rate"],
        )))
        for key in keys:
            totals[key] += values[key]
        rows.append({"start": item.start, "end": item.end, "days": (end - start).days,
                     "drawn": float(drawn), "undrawn": float(limit - drawn),
                     "reset_date": item.reset_date, "liquidity_horizon": item.liquidity_horizon,
                     **{key: money(value) for key, value in values.items()}})
    income = totals["customer_interest"] + totals["customer_commitment_fee"]
    internal = totals["drawn_ftp"] + totals["internal_commitment_cost"]
    external = totals["external_drawn_cost"] + totals["external_commitment_cost"]
    unit, treasury = income - internal, internal - external
    residual = unit + treasury - (income - external)
    return {
        "basis": "ACT/365; start included, end excluded; undiscounted accrual; synthetic terms",
        "rows": rows, "totals": {key: money(value) for key, value in totals.items()},
        "drawn_exposure_years": float(exposure_time), "undrawn_exposure_years": float(undrawn_time),
        "exposure_weighted_drawn_ftp_rate": float(totals["drawn_ftp"] / exposure_time) if exposure_time else None,
        "customer_income": money(income), "total_internal_ftp": money(internal),
        "total_external_funding_cost": money(external), "business_unit_margin": money(unit),
        "treasury_margin": money(treasury), "consolidated_margin": money(income - external),
        "consolidation_residual_unrounded": float(residual),
    }


def ftp_examples() -> dict:
    dates = ["2027-01-01", "2027-04-01", "2027-07-01", "2027-10-01", "2028-01-01"]
    result = {}
    for name, balances in (("fixed", [1_000_000] * 4),
                           ("amortising", [1_000_000, 750_000, 500_000, 250_000]),
                           ("floating", [1_000_000] * 4),
                           ("revolving", [400_000, 800_000, 600_000, 900_000])):
        slices = []
        for index, drawn in enumerate(balances):
            floating = name in {"floating", "revolving"}
            external = [.08, .09, .10, .085][index] if floating else .08
            slices.append(AccrualSlice(
                dates[index], dates[index + 1], drawn,
                1_000_000 if name == "revolving" else drawn,
                external + .06 if floating else .15,
                external + .005 if floating else .09, external,
                dates[index] if floating else dates[0], dates[-1],
                .01 if name == "revolving" else 0,
                .02 if name == "revolving" else 0,
                .0075 if name == "revolving" else 0,
            ))
        result[name] = ftp_lifecycle(slices)
    planned = [AccrualSlice(dates[i], dates[i + 1], 600_000, 1_000_000,
                            .14, .085, .08, dates[i], dates[-1], .01, .02, .0075)
               for i in range(4)]
    result["revolving_ex_ante"] = ftp_lifecycle(planned)
    result["revolving_actual_minus_plan"] = {
        key: round(result["revolving"][key] - result["revolving_ex_ante"][key], 2)
        for key in ("customer_income", "total_internal_ftp", "total_external_funding_cost",
                    "business_unit_margin", "treasury_margin", "consolidated_margin")
    }
    return result


def _inverse(matrix: list[list[float]]) -> list[list[float]]:
    """Pivoted Gauss-Jordan inverse for the small, full-rank OLS design."""
    n = len(matrix)
    augmented = [list(row) + [float(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda i: abs(augmented[i][col]))
        if abs(augmented[pivot][col]) < 1e-10:
            raise ValueError("Rate design is singular; more independent rate movements are needed")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [value / scale for value in augmented[col]]
        for row in range(n):
            if row != col:
                factor = augmented[row][col]
                augmented[row] = [a - factor * b for a, b in zip(augmented[row], augmented[col])]
    return [row[n:] for row in augmented]


def _features(row: dict) -> list[float]:
    current, lag = row["market_change_bps"], row["lagged_market_change_bps"]
    return [1.0, max(current, 0), min(current, 0), max(lag, 0), min(lag, 0)]


def synthetic_deposit_panel(months: int = 36) -> list[dict]:
    """Two labelled segments, observed monthly; holdout regime changes at month24.

    Balance flows follow their own known data-generating process. Migration is
    to another product in the same bank; withdrawal leaves the bank. New inflows
    never replenish the tagged original cohort. Month0 is its opening snapshot.
    """
    if not 24 <= months <= 120:
        raise ValueError("Use 24 to 120 monthly intervals")
    changes = [25, 50, 0, -25, 75, -50, -25, 10, 0, -10, 40, -20]
    rows = []
    for segment, initial_coefficients in (("operating", [.15, .10, .10, .05]),
                                           ("rate_sensitive", [.50, .40, .20, .15])):
        market, paid, cohort, product, migrated = .08, .02, 1_000_000.0, 1_000_000.0, 0.0
        lag = 0
        for month in range(months + 1):
            asof = date(2023 + month // 12, month % 12 + 1, 1).isoformat()
            delta = 0 if month == 0 else changes[(month - 1) % len(changes)]
            coefficients = list(initial_coefficients)
            if month >= 24:
                coefficients[0] += .15  # A deliberately unseen repricing regime.
            noise = 0 if month == 0 else [.10, -.20, .15, .05, -.10][month % 5]
            features = [max(delta, 0), min(delta, 0), max(lag, 0), min(lag, 0)]
            paid_change = 0 if month == 0 else sum(a * b for a, b in zip(coefficients, features)) + noise
            market += delta / 10_000
            paid += paid_change / 10_000
            opening, opening_product = cohort, product
            withdrawal = 0 if month == 0 else cohort * (.008 + .002 * (month % 3))
            migration = 0 if month == 0 else cohort * (.004 if segment == "operating" else .014)
            inflow = 0 if month == 0 else 8_000 + 1_000 * (month % 2)
            cohort -= withdrawal + migration
            product += inflow - withdrawal - migration
            migrated += migration
            rows.append({
                "date": asof, "month": month, "segment": segment, "synthetic": True,
                "market_rate": market, "paid_rate": paid, "market_change_bps": delta,
                "lagged_market_change_bps": lag, "paid_change_bps": paid_change,
                "opening_cohort_balance": opening, "cohort_withdrawal": withdrawal,
                "cohort_migration": migration, "closing_cohort_balance": cohort,
                "opening_product_balance": opening_product, "new_inflow": inflow,
                "closing_product_balance": product, "migrated_balance_same_bank": migrated,
            })
            lag = delta
    return sorted(rows, key=lambda row: (row["date"], row["segment"]))


def fit_deposit_passthrough(training_panel: list[dict]) -> dict:
    """OLS in basis-point changes: intercept + up/down immediate/one-month lag.

    Diagnostic standard errors assume homoskedastic uncorrelated residuals;
    they are not time-series robust uncertainty estimates for real portfolios.
    """
    if not training_panel:
        raise ValueError("Training observations are required")
    fitted = {}
    names = ["intercept_bps", "beta_up", "beta_down", "lag_beta_up", "lag_beta_down"]
    for segment in sorted({row["segment"] for row in training_panel}):
        rows = [row for row in training_panel if row["segment"] == segment and row["month"] > 0]
        if len(rows) <= 5:
            raise ValueError("Each segment needs more observations than fitted coefficients")
        if len({row["date"] for row in rows}) != len(rows):
            raise ValueError("Duplicate segment-date observation")
        x, y = [_features(row) for row in rows], [row["paid_change_bps"] for row in rows]
        if any(not math.isfinite(v) for values in x for v in values) or any(not math.isfinite(v) for v in y):
            raise ValueError("Rate observations must be finite")
        xtx = [[sum(row[i] * row[j] for row in x) for j in range(5)] for i in range(5)]
        xty = [sum(row[i] * target for row, target in zip(x, y)) for i in range(5)]
        inverse = _inverse(xtx)
        coefficients = [sum(a * b for a, b in zip(row, xty)) for row in inverse]
        errors = [target - sum(a * b for a, b in zip(row, coefficients)) for row, target in zip(x, y)]
        sse = sum(error * error for error in errors)
        variance = sse / (len(rows) - 5)
        fitted[segment] = {
            "n": len(rows), "train_start": min(row["date"] for row in rows),
            "train_end": max(row["date"] for row in rows),
            "coefficients": dict(zip(names, coefficients)),
            "standard_errors_iid_only": dict(zip(names, [math.sqrt(max(0, variance * inverse[i][i])) for i in range(5)])),
            "training_rmse_bps": math.sqrt(sse / len(rows)),
            "cumulative_up_beta": coefficients[1] + coefficients[3],
            "cumulative_down_beta": coefficients[2] + coefficients[4],
        }
    return fitted


def evaluate_deposit_model(fitted: dict, holdout: list[dict]) -> dict:
    if not holdout:
        raise ValueError("Holdout observations are required")
    results = {}
    for segment in sorted({row["segment"] for row in holdout}):
        model = fitted[segment]
        rows = [row for row in holdout if row["segment"] == segment]
        if any(row["date"] <= model["train_end"] for row in rows):
            raise ValueError("Holdout must be strictly later than the training cutoff")
        c = [model["coefficients"][name] for name in
             ("intercept_bps", "beta_up", "beta_down", "lag_beta_up", "lag_beta_down")]
        errors = [row["paid_change_bps"] - sum(a * b for a, b in zip(_features(row), c)) for row in rows]
        results[segment] = {"n": len(rows), "start": min(row["date"] for row in rows),
                            "end": max(row["date"] for row in rows),
                            "rmse_bps": math.sqrt(sum(e * e for e in errors) / len(errors)),
                            "mae_bps": sum(abs(e) for e in errors) / len(errors),
                            "mean_error_bps": sum(errors) / len(errors)}
    return results


def deposit_cohort_flows(panel: list[dict]) -> dict:
    summaries = {}
    for segment in sorted({row["segment"] for row in panel}):
        rows = sorted((row for row in panel if row["segment"] == segment), key=lambda r: r["date"])
        opening = rows[0]["opening_cohort_balance"]
        withdrawal, migration = (sum(row[key] for row in rows) for key in ("cohort_withdrawal", "cohort_migration"))
        retained = rows[-1]["closing_cohort_balance"]
        summaries[segment] = {
            "opening_tagged_cohort": opening, "withdrawn_from_bank": withdrawal,
            "migrated_to_other_bank_product": migration, "retained_in_original_product": retained,
            "retained_fraction_original_product": retained / opening,
            "tagged_cohort_remaining_at_bank": retained + migration,
            "new_inflows": sum(row["new_inflow"] for row in rows),
            "closing_original_product_total": rows[-1]["closing_product_balance"],
            "cohort_reconciliation_residual": opening - withdrawal - migration - retained,
        }
    return summaries


def retention_bounds_from_panel(panel: list[dict], horizons=(1, 3, 6, 12)) -> dict[int, float]:
    initial = sum(row["closing_cohort_balance"] for row in panel if row["month"] == 0)
    segments = {row["segment"] for row in panel}
    if not initial:
        raise ValueError("Opening cohort observations are required")
    result = {}
    for horizon in horizons:
        observed = [row for row in panel if row["month"] == horizon]
        if {row["segment"] for row in observed} != segments or len(observed) != len(segments):
            raise ValueError("Each horizon needs a complete, unique set of cohort observations")
        result[horizon] = sum(row["closing_cohort_balance"] for row in observed) / initial
    return result


def constrained_replication_ladder(total: float, retained_bounds: dict[int, float],
                                   liquidity_buffer=.20, retention_haircut=.10,
                                   maximum_average_months=6.0) -> dict:
    """Small finite-grid yield maximisation with nested runoff constraints.

    Maturities 0/3/6/12 months; weights in 5% increments; no beta input. Money
    still locked after each observed horizon cannot exceed haircut retention.
    This synthetic policy uses terminal rungs, not continuously rolling buckets.
    """
    if not all(math.isfinite(v) for v in (total, liquidity_buffer, retention_haircut, maximum_average_months)):
        raise ValueError("Funding and policy inputs must be finite")
    if total <= 0 or not 0 <= liquidity_buffer <= 1 or not 0 <= retention_haircut < 1:
        raise ValueError("Invalid funding/policy inputs")
    if maximum_average_months < 0 or not retained_bounds:
        raise ValueError("Maturity cap and observed retention bounds are required")
    ordered = sorted(retained_bounds.items())
    if any(h <= 0 or not 0 <= r <= 1 for h, r in ordered):
        raise ValueError("Retention bounds must be fractions at positive horizons")
    if any(b > a + 1e-12 for (_, a), (_, b) in zip(ordered, ordered[1:])):
        raise ValueError("Original-cohort retention cannot increase")
    if max(retained_bounds) < 12:
        raise ValueError("The twelve-month rung requires an observed twelve-month horizon")
    tenors, rates = (0, 3, 6, 12), (.04, .05, .055, .06)
    best = None
    for overnight in range(21):
        for three in range(21 - overnight):
            for six in range(21 - overnight - three):
                twelve = 20 - overnight - three - six
                weights = [v / 20 for v in (overnight, three, six, twelve)]
                average = sum(w * t for w, t in zip(weights, tenors))
                if weights[0] + 1e-12 < liquidity_buffer or average > maximum_average_months + 1e-12:
                    continue
                if any(sum(w for w, t in zip(weights, tenors) if t > h) > retention * (1 - retention_haircut) + 1e-12
                       for h, retention in retained_bounds.items()):
                    continue
                income_rate = sum(w * rate for w, rate in zip(weights, rates))
                score = (round(income_rate, 12), -average)
                if best is None or score > best[0]:
                    best = (score, weights, average, income_rate)
    if best is None:
        raise ValueError("No ladder satisfies the stated constraints")
    _, weights, average, income_rate = best
    return {
        "total": total, "grid_step": .05, "policy_liquidity_buffer": liquidity_buffer,
        "policy_retention_haircut": retention_haircut, "policy_maximum_average_months": maximum_average_months,
        "observed_retention_bounds": retained_bounds, "average_maturity_months": average,
        "weighted_yield": income_rate, "annualised_income_run_rate": total * income_rate,
        "rungs": [{"months": t, "weight": w, "amount": total * w, "yield": rate}
                  for t, w, rate in zip(tenors, weights, rates)],
        "scope": "Synthetic constrained cash-maturity ladder; not deposit duration, regulatory liquidity classification or empirical investment advice",
    }


def _json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


class STPWorkflow:
    """Durable local fixed-deposit placement workflow, with integer minor units.

    Actor mapping is a simulation boundary, not authentication. SQLite commits
    event, position state and journal together. Only complete fills are supported.
    """
    DEFAULT_ROLES = {"maker": "proposer", "approver": "approver", "dealer": "dealer",
                     "operations": "backoffice", "auditor": "reconciler"}
    REQUIRED = {"PROPOSE": "proposer", "APPROVE": "approver", "REJECT": "approver",
                "ORDER": "dealer", "CONFIRM": "backoffice", "BOOK": "backoffice",
                "SETTLEMENT_FAILED": "backoffice", "SETTLE": "backoffice", "RECONCILE": "reconciler"}

    def __init__(self, db_path: str | Path, actors: dict | None = None, approval_limit_cents=100_000_000):
        self.actors = dict(actors or self.DEFAULT_ROLES)
        self.limit = approval_limit_cents
        self.db = sqlite3.connect(str(db_path))
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
          CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT UNIQUE NOT NULL, fingerprint TEXT NOT NULL, kind TEXT NOT NULL,
            actor TEXT NOT NULL, payload TEXT NOT NULL, result TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS proposals(proposal_id TEXT PRIMARY KEY, maker TEXT NOT NULL,
            terms TEXT NOT NULL, status TEXT NOT NULL, order_id TEXT UNIQUE, trade_id TEXT UNIQUE,
            confirmation_id TEXT UNIQUE, settlement_id TEXT UNIQUE, failed_event_id TEXT);
          CREATE TABLE IF NOT EXISTS journal(event_id TEXT NOT NULL, line INTEGER NOT NULL,
            proposal_id TEXT NOT NULL, account TEXT NOT NULL, signed_cents INTEGER NOT NULL,
            PRIMARY KEY(event_id,line));
        """)

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    @staticmethod
    def _identifier(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("A nonempty durable identifier is required")
        return value

    @staticmethod
    def _terms(terms):
        if set(terms) != {"currency", "notional_cents", "start", "end", "rate_bps", "instrument", "counterparty", "curve_version", "snapshot_id"}:
            raise ValueError("Terms must contain exactly the supported economic/evidence fields")
        if type(terms["notional_cents"]) is not int or terms["notional_cents"] <= 0:
            raise ValueError("Notional must be positive integer minor units")
        if type(terms["rate_bps"]) is not int or terms["rate_bps"] < 0:
            raise ValueError("Rate must be a nonnegative integer number of basis points")
        if terms["currency"] not in {"KES", "USD"} or terms["instrument"] != "fixed_deposit_placement":
            raise ValueError("Unsupported currency or illustrative instrument")
        if date.fromisoformat(terms["end"]) <= date.fromisoformat(terms["start"]):
            raise ValueError("Placement dates must be ordered")
        for key in ("counterparty", "curve_version", "snapshot_id"):
            STPWorkflow._identifier(terms[key])

    def _post(self, event_id, proposal_id, entries):
        if sum(value for _, value in entries) != 0:
            raise ValueError("Unbalanced journal")
        self.db.executemany("INSERT INTO journal VALUES(?,?,?,?,?)",
                            [(event_id, i, proposal_id, account, value) for i, (account, value) in enumerate(entries)])

    def apply(self, event_id: str, kind: str, actor: str, payload: dict) -> dict:
        self._identifier(event_id)
        encoded = _json(payload)
        fingerprint = hashlib.sha256(_json([kind, actor, payload]).encode()).hexdigest()
        self.db.execute("BEGIN IMMEDIATE")
        try:
            prior = self.db.execute("SELECT * FROM events WHERE event_id=?", (event_id,)).fetchone()
            if prior:
                if prior["fingerprint"] != fingerprint:
                    raise ValueError("Event ID reused with a different payload, actor or event type")
                result = json.loads(prior["result"])
                self.db.commit()
                return {**result, "duplicate": True}
            if kind not in self.REQUIRED or self.actors.get(actor) != self.REQUIRED[kind]:
                raise PermissionError("Actor is not authorised for this event type")
            proposal_id = self._identifier(payload.get("proposal_id"))
            row = self.db.execute("SELECT * FROM proposals WHERE proposal_id=?", (proposal_id,)).fetchone()
            if kind == "PROPOSE":
                if row:
                    raise ValueError("Proposal already exists; amendments require a new proposal")
                terms = payload["terms"]
                self._terms(terms)
                self.db.execute("INSERT INTO proposals(proposal_id,maker,terms,status) VALUES(?,?,?,?)",
                                (proposal_id, actor, _json(terms), "PROPOSED"))
                status = "PROPOSED"
            else:
                if row is None:
                    raise ValueError("Unknown proposal")
                terms, status = json.loads(row["terms"]), row["status"]
                amount = terms["notional_cents"]
                permitted = {"APPROVE": {"PROPOSED"}, "REJECT": {"PROPOSED"}, "ORDER": {"APPROVED"},
                             "CONFIRM": {"ORDERED"}, "BOOK": {"CONFIRMED"},
                             "SETTLEMENT_FAILED": {"BOOKED"}, "SETTLE": {"BOOKED", "SETTLEMENT_FAILED"},
                             "RECONCILE": {"SETTLED"}}
                if status not in permitted[kind]:
                    raise ValueError(f"{kind} not allowed from {status}")
                if kind in {"APPROVE", "REJECT"}:
                    if actor == row["maker"]:
                        raise PermissionError("Proposer cannot approve or reject own proposal")
                    if kind == "APPROVE" and amount > self.limit:
                        raise ValueError("Approval limit exceeded")
                    if kind == "REJECT":
                        self._identifier(payload.get("reason"))
                    status = "APPROVED" if kind == "APPROVE" else "REJECTED"
                elif kind == "ORDER":
                    order = self._identifier(payload.get("order_id"))
                    self.db.execute("UPDATE proposals SET order_id=? WHERE proposal_id=?", (order, proposal_id))
                    status = "ORDERED"
                elif kind == "CONFIRM":
                    if payload.get("order_id") != row["order_id"] or payload.get("terms") != terms:
                        raise ValueError("Confirmation does not match the approved order and frozen terms")
                    trade = self._identifier(payload.get("trade_id"))
                    confirmation = self._identifier(payload.get("confirmation_id"))
                    self.db.execute("UPDATE proposals SET trade_id=?,confirmation_id=? WHERE proposal_id=?",
                                    (trade, confirmation, proposal_id))
                    status = "CONFIRMED"
                elif kind == "BOOK":
                    if payload.get("trade_id") != row["trade_id"]:
                        raise ValueError("Booking must identify the confirmed trade")
                    self._post(event_id, proposal_id, [("placement_asset", amount), ("settlement_payable", -amount)])
                    status = "BOOKED"
                elif kind == "SETTLEMENT_FAILED":
                    self._identifier(payload.get("reason"))
                    self.db.execute("UPDATE proposals SET failed_event_id=? WHERE proposal_id=?", (event_id, proposal_id))
                    status = "SETTLEMENT_FAILED"
                elif kind == "SETTLE":
                    if type(payload.get("cash_cents")) is not int or payload["cash_cents"] != -amount:
                        raise ValueError("Settlement cash must match the full approved placement")
                    if status == "SETTLEMENT_FAILED" and payload.get("retry_of") != row["failed_event_id"]:
                        raise ValueError("Settlement retry must reference the recorded failed event")
                    settlement = self._identifier(payload.get("settlement_id"))
                    self.db.execute("UPDATE proposals SET settlement_id=? WHERE proposal_id=?", (settlement, proposal_id))
                    self._post(event_id, proposal_id, [("settlement_payable", amount), ("cash", -amount)])
                    status = "SETTLED"
                elif kind == "RECONCILE":
                    self._identifier(payload.get("statement_id"))
                    if any(type(payload.get(key)) is not int for key in ("bank_cash_cents", "position_cents")):
                        raise ValueError("Statement amounts must be integer minor units")
                    if payload.get("bank_cash_cents") != -amount or payload.get("position_cents") != amount:
                        raise ValueError("External cash/position statement mismatch")
                    if not self.recompute()["ledger_matches_events"]:
                        raise ValueError("Ledger differs from independent event reconstruction")
                    status = "RECONCILED"
                self.db.execute("UPDATE proposals SET status=? WHERE proposal_id=?", (status, proposal_id))
            result = {"event_id": event_id, "proposal_id": proposal_id, "status": status, "duplicate": False}
            self.db.execute("INSERT INTO events(event_id,fingerprint,kind,actor,payload,result) VALUES(?,?,?,?,?,?)",
                            (event_id, fingerprint, kind, actor, encoded, _json(result)))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise

    def recompute(self) -> dict:
        """Reconstruct expected postings from accepted events, independently of journal."""
        amounts, expected = {}, []
        for event in self.db.execute("SELECT * FROM events ORDER BY seq"):
            payload = json.loads(event["payload"])
            proposal = payload["proposal_id"]
            if event["kind"] == "PROPOSE":
                amounts[proposal] = payload["terms"]["notional_cents"]
            if event["kind"] in {"BOOK", "SETTLE"}:
                amount = amounts[proposal]
                entries = [("placement_asset", amount), ("settlement_payable", -amount)] if event["kind"] == "BOOK" else [("settlement_payable", amount), ("cash", -amount)]
                expected.extend((event["event_id"], i, proposal, account, value) for i, (account, value) in enumerate(entries))
        actual = [tuple(row) for row in self.db.execute("SELECT event_id,line,proposal_id,account,signed_cents FROM journal")]
        balances = {}
        for _, _, _, account, value in actual:
            balances[account] = balances.get(account, 0) + value
        return {"event_count": self.db.execute("SELECT count(*) FROM events").fetchone()[0],
                "journal_lines": len(actual), "account_balances_cents": balances,
                "trial_balance_residual_cents": sum(balances.values()),
                "ledger_matches_events": sorted(expected) == sorted(actual)}


def stp_example() -> dict:
    terms = {"currency": "KES", "notional_cents": 25_000_000, "rate_bps": 500,
             "start": "2027-01-01", "end": "2027-04-01", "instrument": "fixed_deposit_placement",
             "counterparty": "SYNTHETIC-BANK", "curve_version": "synthetic-curve-v1", "snapshot_id": "scenario-001"}
    events = [
        ("e01", "PROPOSE", "maker", {"terms": terms}),
        ("e02", "APPROVE", "approver", {}),
        ("e03", "ORDER", "dealer", {"order_id": "order-001"}),
        ("e04", "CONFIRM", "operations", {"order_id": "order-001", "trade_id": "trade-001", "confirmation_id": "confirm-001", "terms": terms}),
        ("e05", "BOOK", "operations", {"trade_id": "trade-001"}),
        ("e06", "SETTLEMENT_FAILED", "operations", {"reason": "Illustrative payment-network outage"}),
        ("e07", "SETTLE", "operations", {"settlement_id": "settlement-001", "cash_cents": -25_000_000, "retry_of": "e06"}),
        ("e08", "RECONCILE", "auditor", {"statement_id": "statement-001", "bank_cash_cents": -25_000_000, "position_cents": 25_000_000}),
    ]
    with tempfile.TemporaryDirectory(prefix="kesonia-stp-") as temp:
        db = Path(temp) / "workflow.sqlite3"
        with STPWorkflow(db) as flow:
            results = [flow.apply(event, kind, actor, {"proposal_id": "proposal-001", **payload}) for event, kind, actor, payload in events]
            ledger = flow.recompute()
        with STPWorkflow(db) as restarted:
            duplicate = restarted.apply("e07", "SETTLE", "operations", {"proposal_id": "proposal-001", **events[6][3]})
            after_restart = restarted.recompute()
    return {"scope": "Local SQLite simulation; no API, market order or external money movement",
            "terms": terms, "events": results, "ledger": ledger,
            "duplicate_after_restart": duplicate, "ledger_after_restart": after_restart}


def operations_examples() -> dict:
    panel = synthetic_deposit_panel()
    training = [row for row in panel if row["date"] < "2025-01-01"]
    holdout = [row for row in panel if row["date"] >= "2025-01-01"]
    fitted = fit_deposit_passthrough(training)
    return {
        "evidence": "Synthetic deterministic demonstration; no empirical Kenyan claims",
        "ftp": ftp_examples(),
        "deposits": {"panel": panel, "training_cutoff": "2024-12-01", "fit": fitted,
                     "future_holdout": evaluate_deposit_model(fitted, holdout),
                     "cohort_flows": deposit_cohort_flows(training),
                     "replication_ladder": constrained_replication_ladder(2_000_000, retention_bounds_from_panel(training)),
                     "replication_ladder_tighter_retention_policy": constrained_replication_ladder(
                         2_000_000, retention_bounds_from_panel(training), retention_haircut=.25)},
        "stp": stp_example(),
    }
