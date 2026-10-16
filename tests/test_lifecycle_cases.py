import copy
from datetime import date, datetime
from decimal import Decimal as D, localcontext
import json
from pathlib import Path
import tempfile
import unittest

from research_lab.benchmark import Calendar, Fixing, schedule, compound
from research_lab.lifecycle_cases import (
    AccountProfile, BalanceEvent, MarginReset, accrue_account, correction_case,
    freshness_gate, AccrualPostingBook, PartialSettlementBook, lifecycle_examples,
    _approval, _hash,
)


class AccrualLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.start, self.end = date(2025,9,5), date(2025,9,8)
        self.cutoff = datetime.fromisoformat("2025-09-09T12:00:00+03:00")
        self.fixings = [Fixing(self.start,datetime.fromisoformat("2025-09-08T09:00:00+03:00"),D(".10"),"original")]

    def calculate(self, **kwargs):
        return accrue_account(self.start,self.end,"1000000",self.fixings,self.cutoff,**kwargs)

    def test_unchanged_balance_matches_existing_weighted_weekend_reference(self):
        actual = self.calculate()
        reference = compound(schedule(self.start,self.end,Calendar()),self.fixings,self.cutoff,D("1000000"),D(".03"))
        self.assertAlmostEqual(D(actual["benchmark_interest"]),D(reference["benchmark_cash"]),places=25)
        self.assertEqual(actual["rounded_interest"],reference["total_cash_rounded"])

    def test_zero_balance_event_does_not_create_extra_weekend_compounding(self):
        event = BalanceEvent("ZERO","2025-09-06","2025-09-06T00:00:00+03:00","0")
        actual = self.calculate(balance_events=[event])
        self.assertAlmostEqual(D(actual["benchmark_interest"]),D(self.calculate()["benchmark_interest"]),places=25)
        self.assertEqual(len(actual["ledger"]),2)

    def test_mid_span_withdrawal_matches_independent_index_units_solution(self):
        event = BalanceEvent("REPAY","2025-09-06","2025-09-06T00:00:00+03:00","-300000")
        actual = self.calculate(balance_events=[event])
        with localcontext() as ctx:
            ctx.prec=40
            index_mid=1+D(".10")/365
            index_end=1+D(".10")*3/365
            terminal=(D(1000000)-D(300000)/index_mid)*index_end
            expected_interest=terminal-D(700000)
            expected_margin=(D(1000000)+2*D(700000))*D(".03")/365
        self.assertAlmostEqual(D(actual["benchmark_interest"]),expected_interest,places=25)
        self.assertAlmostEqual(D(actual["simple_margin_interest"]),expected_margin,places=25)
        self.assertEqual(D(actual["closing_principal"]),D(700000))

    def test_fixing_floor_and_cap_apply_before_factor_not_to_whole_customer_rate(self):
        floored=self.calculate(profile=AccountProfile(fixing_floor=".11",fixing_cap=".12"))
        capped=self.calculate(profile=AccountProfile(fixing_cap=".08"))
        self.assertAlmostEqual(D(floored["benchmark_interest"]),D(1000000)*D(".11")*3/365,places=20)
        self.assertAlmostEqual(D(capped["benchmark_interest"]),D(1000000)*D(".08")*3/365,places=20)
        self.assertEqual(floored["simple_margin_interest"],capped["simple_margin_interest"])
        with self.assertRaises(ValueError): self.calculate(profile=AccountProfile(fixing_floor=".2",fixing_cap=".1"))

    def test_margin_reset_preserves_benchmark_and_requires_effective_authority(self):
        reset=MarginReset("RESET","2025-09-06","2025-09-05T12:00:00+03:00",".04","TERMS-1","v1")
        result=self.calculate(margin_resets=[reset])
        self.assertAlmostEqual(D(result["benchmark_interest"]),D(self.calculate()["benchmark_interest"]),places=25)
        expected=D(1000000)*(D(".03")+2*D(".04"))/365
        self.assertAlmostEqual(D(result["simple_margin_interest"]),expected,places=20)
        with self.assertRaises(ValueError): self.calculate(margin_resets=[MarginReset("R","2025-09-06","2025-09-07T00:00:00+03:00",".04","A","v1")])
        with self.assertRaises(ValueError): self.calculate(margin_resets=[MarginReset("R","2025-09-06","2025-09-05T00:00:00+03:00",".04","","v1")])

    def test_invalid_and_duplicate_principal_events_fail(self):
        event=BalanceEvent("E","2025-09-06","2025-09-06T00:00:00+03:00","0")
        with self.assertRaises(ValueError): self.calculate(balance_events=[event,event])
        with self.assertRaises(ValueError): self.calculate(balance_events=[BalanceEvent("X","2025-09-06","2025-09-06T00:00:00+03:00","-1000001")])
        with self.assertRaises(ValueError): self.calculate(profile=AccountProfile(margin_convention="compounded"))

    def test_margin_reset_authority_uses_full_utc_instant_at_start_of_effective_day(self):
        for available in ("2025-09-06T23:00:00+00:00", "2025-09-06T00:00:01+00:00",
                          "2025-09-05T23:30:00-01:00"):
            with self.subTest(available=available), self.assertRaises(ValueError):
                self.calculate(margin_resets=[MarginReset("R","2025-09-06",available,".04","A","v1")])
        for available in ("2025-09-06T00:00:00+00:00", "2025-09-06T03:00:00+03:00",
                          "2025-09-05T23:59:59+00:00"):
            with self.subTest(available=available):
                result=self.calculate(margin_resets=[MarginReset("R","2025-09-06",available,".04","A","v1")])
                expected=D(1000000)*(D(".03")+2*D(".04"))/365
                self.assertAlmostEqual(D(result["simple_margin_interest"]),expected,places=20)
        with self.assertRaises(ValueError):
            self.calculate(profile=AccountProfile(contract_timezone="Africa/Nairobi"))

    def test_late_reported_principal_is_not_known_at_earlier_cutoff(self):
        event=BalanceEvent("LATE","2025-09-06","2025-09-10T00:00:00+03:00","10000")
        actual=self.calculate(balance_events=[event])
        self.assertEqual(actual["closing_principal"],"1000000")

    def test_fixing_correction_keeps_contract_and_rounded_delta_reconciles(self):
        old=accrue_account(self.start,self.end,"1000000",self.fixings,"2025-09-08T10:00:00+03:00")
        updated=self.fixings+[Fixing(self.start,datetime.fromisoformat("2025-09-09T09:00:00+03:00"),D(".12"),"corrected")]
        new=accrue_account(self.start,self.end,"1000000",updated,self.cutoff)
        correction=correction_case(old,new,"CORR")
        self.assertEqual(D(correction["original_posted_interest"])+D(correction["proposed_adjustment"]),D(correction["revised_interest"]))
        self.assertFalse(correction["contract_amendment"])
        self.assertTrue(correction["requires_result_specific_approval"])
        changed=accrue_account(self.start,self.end,"1000000",updated,self.cutoff,AccountProfile(margin=".04"))
        with self.assertRaises(ValueError): correction_case(old,changed,"NOT-A-FIXING-CORRECTION")


class EvidenceGateTests(unittest.TestCase):
    def setUp(self):
        self.evidence=[{"version":"E1","owner":"reviewer","effective_at":"2025-09-01T00:00:00+03:00","available_at":"2025-09-01T09:00:00+03:00","verified_at":"2025-09-01T10:00:00+03:00","result":"confirmed","recovery_fraction":.6},
            {"version":"E2","owner":"reviewer","effective_at":"2025-09-02T00:00:00+03:00","available_at":"2025-09-02T09:00:00+03:00","verified_at":None,"result":"unavailable"},
            {"version":"E3","owner":"reviewer","effective_at":"2025-09-03T00:00:00+03:00","available_at":"2025-09-03T09:00:00+03:00","verified_at":"2025-09-04T10:00:00+03:00","result":"changed","recovery_fraction":.3}]

    def test_outage_preserves_last_verified_assumption_and_verification_clock(self):
        result=freshness_gate(self.evidence,"2025-09-02T12:00:00+03:00",5)
        self.assertEqual(result["last_verified_version"],"E1")
        self.assertEqual(result["current_verified_recovery_assumption"],.6)
        self.assertTrue(result["source_unavailable"])
        self.assertFalse(result["analytical_refresh_allowed"])
        self.assertFalse(result["borrower_pd_changed_by_this_gate"])

    def test_unverified_change_waits_then_verified_change_is_analytical_only(self):
        pending=freshness_gate(self.evidence,"2025-09-03T12:00:00+03:00",5)
        verified=freshness_gate(self.evidence,"2025-09-04T12:00:00+03:00",5)
        self.assertTrue(pending["review_pending"])
        self.assertEqual(pending["current_verified_recovery_assumption"],.6)
        self.assertEqual(verified["current_verified_recovery_assumption"],.3)
        self.assertTrue(verified["analytical_refresh_allowed"])
        self.assertFalse(verified["contract_change_authorised"])

    def test_stale_known_evidence_cannot_authorise_refresh(self):
        result=freshness_gate(self.evidence,"2025-09-20T12:00:00+03:00",5)
        self.assertTrue(result["stale"])
        self.assertFalse(result["analytical_refresh_allowed"])
        self.assertEqual(freshness_gate([],"2025-09-02T12:00:00+03:00",5)["status"],"request_evidence")


class DurableOperationsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/"partial.sqlite3"
        self.book=PartialSettlementBook(self.path)
        self.terms={"notional_minor":10000,"currency":"KES","instrument":"synthetic_deposit_placement","rate_bps":800}
        self.order={"order_id":"O","terms":self.terms,"approval":_approval(self.terms)}
        self.book.apply("O-E","ORDER",self.order)

    def tearDown(self):
        self.book.close();self.temp.cleanup()

    def fill(self, amount=6000):
        return self.book.apply("F-E","FILL",{"order_id":"O","fill_id":"F","terms_hash":_hash(self.terms),"amount_minor":amount})

    def settle(self, event, business, amount):
        return self.book.apply(event,"SETTLE",{"order_id":"O","fill_id":"F","settlement_id":business,"amount_minor":amount})

    def test_partial_settlement_cash_and_payable_reconcile(self):
        self.fill(); self.settle("S1-E","S1",2000)
        state=self.book.snapshot()
        self.assertEqual((state["position_minor"],state["cash_change_minor"],state["settlement_payable_minor"]),(6000,-2000,4000))
        self.assertEqual(state["balance_residual_minor"],0)
        self.assertEqual(state["orders"]["O"]["live_unfilled_minor"],4000)
        with self.assertRaises(ValueError): self.settle("EXCESS-E","EXCESS",4001)
        self.assertEqual(self.book.snapshot(),state)

    def test_restart_and_retry_do_not_duplicate_settlement(self):
        self.fill(); self.settle("S1-E","S1",2000)
        self.book.close();self.book=PartialSettlementBook(self.path)
        self.assertTrue(self.settle("S1-E","S1",2000)["duplicate"])
        with self.assertRaises(ValueError): self.settle("NEW-TRANSPORT-ID","S1",2000)
        with self.assertRaises(ValueError): self.settle("S1-E","S1",3000)
        self.assertEqual(self.book.snapshot()["cash_paid_minor"],2000)

    def test_unknown_acknowledgement_does_not_allow_new_order(self):
        self.book.apply("UNKNOWN","ACK",{"order_id":"O","state":"UNKNOWN"})
        with self.assertRaises(ValueError): self.book.apply("RESENT-ORDER","ORDER",self.order)
        self.assertTrue(self.book.apply("O-E","ORDER",self.order)["duplicate"])
        self.fill()
        self.assertEqual(self.book.snapshot()["orders"]["O"]["acknowledgement"],"ACKNOWLEDGED")

    def test_cancellation_releases_only_unfilled_order_and_keeps_payable(self):
        self.fill()
        cancel_terms={"order_id":"O","terms_hash":_hash(self.terms),"action":"cancel_unfilled"}
        self.book.apply("CANCEL","CANCEL",{"order_id":"O","terms_hash":_hash(self.terms),"approval":_approval(cancel_terms,"C1"),"external_confirmation_id":"EX-C1"})
        self.assertEqual(self.book.snapshot()["orders"]["O"]["live_unfilled_minor"],0)
        self.assertEqual(self.book.snapshot()["settlement_payable_minor"],6000)
        self.settle("FINAL","FINAL",6000)
        self.assertEqual(self.book.snapshot()["settlement_payable_minor"],0)
        with self.assertRaises(ValueError): self.book.apply("F2-E","FILL",{"order_id":"O","fill_id":"F2","terms_hash":_hash(self.terms),"amount_minor":1})

    def test_amendment_requires_new_exact_approval_and_cannot_undo_fill(self):
        self.fill()
        amended={**self.terms,"notional_minor":8000}
        with self.assertRaises(PermissionError): self.book.apply("BAD-AMEND","AMEND",{"order_id":"O","terms":amended,"approval":_approval(self.terms)})
        with self.assertRaises(ValueError): self.book.apply("RECYCLED-APPROVAL","AMEND",{"order_id":"O","terms":amended,"approval":_approval(amended)})
        self.book.apply("AMEND","AMEND",{"order_id":"O","terms":amended,"approval":_approval(amended,"A2")})
        with self.assertRaises(ValueError): self.book.apply("STALE-FILL","FILL",{"order_id":"O","fill_id":"F2","amount_minor":2000,"terms_hash":_hash(self.terms)})
        self.book.apply("F2-E","FILL",{"order_id":"O","fill_id":"F2","amount_minor":2000,"terms_hash":_hash(amended)})
        too_small={**amended,"notional_minor":7999}
        with self.assertRaises(ValueError): self.book.apply("UNDO-FILL","AMEND",{"order_id":"O","terms":too_small,"approval":_approval(too_small,"A3")})

    def test_self_approval_and_boolean_minor_units_rejected(self):
        invalid=copy.deepcopy(self.order);invalid["order_id"]="OTHER";invalid["approval"]["checker"]="maker"
        with self.assertRaises(PermissionError): self.book.apply("SELF","ORDER",invalid)
        with self.assertRaises(ValueError): self.fill(True)

    def test_book_rejects_other_currency_or_claim_and_preserves_scope_on_restart(self):
        before=self.book.snapshot()
        for field,value in (("currency","USD"),("instrument","synthetic_swap")):
            terms={**self.terms,field:value}
            with self.assertRaises(ValueError):
                self.book.apply("OTHER-"+field,"ORDER",{"order_id":"OTHER-"+field,"terms":terms,"approval":_approval(terms,"A-"+field)})
        self.assertEqual(before,self.book.snapshot())
        self.book.close()
        with self.assertRaises(ValueError): PartialSettlementBook(self.path,currency="USD")
        self.book=PartialSettlementBook(self.path)
        self.assertEqual(self.book.snapshot()["currency"],"KES")
        self.assertEqual(self.book.snapshot()["instrument"],self.terms["instrument"])

    def test_enlarging_filled_order_restores_partial_status_and_residual_capacity(self):
        self.fill(10000)
        self.assertEqual(self.book.snapshot()["orders"]["O"]["status"],"FILLED")
        amended={**self.terms,"notional_minor":12000}
        self.book.apply("ENLARGE","AMEND",{"order_id":"O","terms":amended,"approval":_approval(amended,"A2")})
        state=self.book.snapshot()
        self.assertEqual(state["orders"]["O"]["status"],"PART_FILLED")
        self.assertEqual(state["orders"]["O"]["live_unfilled_minor"],2000)
        self.assertEqual(state["position_minor"],10000)
        self.book.apply("F2-E","FILL",{"order_id":"O","fill_id":"F2","amount_minor":2000,"terms_hash":_hash(amended)})
        self.assertEqual(self.book.snapshot()["orders"]["O"]["status"],"FILLED")
        self.assertEqual(self.book.snapshot()["position_minor"],12000)

    def test_approved_fixing_adjustment_durable_ledger_and_stale_predecessor(self):
        examples=lifecycle_examples()
        original,revised=examples["original_accrual"],examples["corrected_accrual"]
        path=Path(self.temp.name)/"accrual.sqlite3"
        accrual=AccrualPostingBook(path)
        with self.assertRaises(PermissionError): accrual.post("P0","MISSING")
        with self.assertRaises(PermissionError): accrual.approve(original,"A0","maker","maker")
        accrual.approve(original,"A1","maker","checker")
        first=accrual.post("P1","A1")
        accrual.approve(revised,"A2","maker","checker")
        with self.assertRaises(ValueError): accrual.post("P2","A2","NOT-PREDECESSOR")
        adjustment=accrual.post("P2","A2",original["result_hash"])
        self.assertEqual(D(first["adjustment_money"])+D(adjustment["adjustment_money"]),D(revised["rounded_interest"]))
        accrual.close();accrual=AccrualPostingBook(path)
        self.assertTrue(accrual.post("P2","A2",original["result_hash"])["duplicate"])
        with self.assertRaises(ValueError): accrual.post("REPOST-OLD","A1",revised["result_hash"])
        self.assertEqual(len(accrual.ledger()),2)
        accrual.close()

    def test_examples_are_deterministic_and_json_serializable(self):
        first=lifecycle_examples();second=lifecycle_examples()
        self.assertEqual(first,second)
        json.dumps(first,allow_nan=False)
        self.assertTrue(first["duplicate_correction"])
        self.assertTrue(first["partial_settlement"]["duplicate_after_restart"])


if __name__ == "__main__": unittest.main()
