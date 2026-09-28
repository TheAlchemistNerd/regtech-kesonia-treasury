"""Independent arithmetic identities, estimation recovery and state-machine tests."""
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest

try:
    from research_lab.operations import (AccrualSlice, ftp_lifecycle, ftp_examples,
        synthetic_deposit_panel, fit_deposit_passthrough, evaluate_deposit_model,
        deposit_cohort_flows, retention_bounds_from_panel,
        constrained_replication_ladder, STPWorkflow, stp_example)
except ModuleNotFoundError:  # Scratch payload verification before installation.
    from operations import (AccrualSlice, ftp_lifecycle, ftp_examples,
        synthetic_deposit_panel, fit_deposit_passthrough, evaluate_deposit_model,
        deposit_cohort_flows, retention_bounds_from_panel,
        constrained_replication_ladder, STPWorkflow, stp_example)


class FTPTests(unittest.TestCase):
    def test_fixed_one_year_eliminates_internal_transfers(self):
        x = ftp_examples()["fixed"]
        self.assertEqual(x["customer_income"], 150000)
        self.assertEqual(x["total_internal_ftp"], 90000)
        self.assertEqual(x["business_unit_margin"], 60000)
        self.assertEqual(x["treasury_margin"], 10000)
        self.assertEqual(x["consolidated_margin"], 70000)
        self.assertEqual(x["consolidation_residual_unrounded"], 0)

    def test_amortisation_uses_actual_exposure_days(self):
        x = ftp_examples()["amortising"]
        exposure_days = 1000000 * 90 + 750000 * 91 + 500000 * 92 + 250000 * 92
        expected = Fraction(exposure_days, 365)
        self.assertAlmostEqual(x["drawn_exposure_years"], float(expected))
        self.assertEqual(x["customer_income"], round(float(expected * Fraction(15, 100)), 2))
        self.assertLess(x["consolidated_margin"], ftp_examples()["fixed"]["consolidated_margin"])

    def test_floating_reset_and_liquidity_horizon_are_distinct(self):
        x = ftp_examples()["floating"]
        self.assertEqual(x["rows"][1]["reset_date"], "2027-04-01")
        self.assertEqual(x["rows"][1]["liquidity_horizon"], "2028-01-01")
        expected_external = Fraction(1000000, 365) * (90 * Fraction(8, 100) + 91 * Fraction(9, 100) + 92 * Fraction(10, 100) + 92 * Fraction(85, 1000))
        self.assertEqual(x["total_external_funding_cost"], round(float(expected_external), 2))
        self.assertEqual(x["business_unit_margin"], 55000)
        self.assertEqual(x["treasury_margin"], 5000)

    def test_revolver_commitment_cost_is_separate_from_drawn_interest(self):
        x = ftp_examples()["revolving"]
        undrawn_days = 600000 * 90 + 200000 * 91 + 400000 * 92 + 100000 * 92
        expected_commitment = Fraction(undrawn_days, 365) * Fraction(2, 100)
        self.assertEqual(x["totals"]["internal_commitment_cost"], round(float(expected_commitment), 2))
        self.assertGreater(x["totals"]["external_commitment_cost"], 0)
        self.assertAlmostEqual(x["business_unit_margin"] + x["treasury_margin"], x["consolidated_margin"], places=2)
        self.assertNotEqual(ftp_examples()["revolving_actual_minus_plan"]["consolidated_margin"], 0)

    def test_transfer_rate_changes_allocation_not_consolidation(self):
        base = AccrualSlice("2027-01-01", "2028-01-01", 1000, 1000, .15, .09, .08, "2027-01-01", "2028-01-01")
        from dataclasses import replace
        changed = replace(base, ftp_rate=.12)
        a, b = ftp_lifecycle([base]), ftp_lifecycle([changed])
        self.assertEqual(a["consolidated_margin"], b["consolidated_margin"])
        self.assertEqual(a["business_unit_margin"] - b["business_unit_margin"], 30)
        self.assertEqual(b["treasury_margin"] - a["treasury_margin"], 30)

    def test_leap_year_actual_days_and_missing_intervals(self):
        first = AccrualSlice("2028-01-01", "2029-01-01", 365, 365, .10, .05, .04, "2028-01-01", "2030-01-01")
        self.assertEqual(ftp_lifecycle([first])["customer_income"], 36.60)
        from dataclasses import replace
        with self.assertRaises(ValueError):
            ftp_lifecycle([first, replace(first, start="2029-01-02", end="2030-01-01")])
        with self.assertRaises(ValueError):
            ftp_lifecycle([replace(first, drawn=366)])


class DepositTests(unittest.TestCase):
    def test_closed_form_recovers_known_immediate_and_lag_parameters(self):
        movements = [(20, 0), (-20, 20), (0, -20), (40, -10), (-30, 50), (10, 30), (-10, -40), (0, 20), (50, 10), (-50, -20)]
        rows = []
        for i, (now, lag) in enumerate(movements):
            y = 2 + .3 * max(now, 0) + .2 * min(now, 0) + .1 * max(lag, 0) + .05 * min(lag, 0)
            rows.append({"date": f"2024-{i+1:02d}-01", "month": i+1, "segment": "test", "market_change_bps": now,
                         "lagged_market_change_bps": lag, "paid_change_bps": y})
        fit = fit_deposit_passthrough(rows)["test"]
        for key, expected in zip(("intercept_bps", "beta_up", "beta_down", "lag_beta_up", "lag_beta_down"), (2, .3, .2, .1, .05)):
            self.assertAlmostEqual(fit["coefficients"][key], expected, places=10)
        self.assertAlmostEqual(fit["cumulative_up_beta"], .4, places=10)

    def test_future_holdout_exposes_unseen_regime_and_serialisation_is_safe(self):
        panel = synthetic_deposit_panel()
        training = [r for r in panel if r["date"] < "2025-01-01"]
        holdout = [r for r in panel if r["date"] >= "2025-01-01"]
        fit = fit_deposit_passthrough(training)
        validated = evaluate_deposit_model(fit, holdout)
        self.assertEqual(validated, evaluate_deposit_model(json.loads(json.dumps(fit, sort_keys=True)), holdout))
        for segment in fit:
            self.assertGreater(validated[segment]["rmse_bps"], fit[segment]["training_rmse_bps"] * 5)
            self.assertEqual(fit[segment]["train_end"], "2024-12-01")
        with self.assertRaises(ValueError):
            evaluate_deposit_model(fit, training)

    def test_singular_rate_history_is_rejected(self):
        rows = [{"date": f"2024-{i:02d}-01", "month": i, "segment": "s", "market_change_bps": 0,
                 "lagged_market_change_bps": 0, "paid_change_bps": 0} for i in range(1, 9)]
        with self.assertRaises(ValueError):
            fit_deposit_passthrough(rows)

    def test_cohort_and_product_balances_reconcile_without_inflow_masking(self):
        panel = synthetic_deposit_panel()
        for row in panel:
            self.assertAlmostEqual(row["opening_cohort_balance"] - row["cohort_withdrawal"] - row["cohort_migration"], row["closing_cohort_balance"])
            self.assertAlmostEqual(row["opening_product_balance"] + row["new_inflow"] - row["cohort_withdrawal"] - row["cohort_migration"], row["closing_product_balance"])
        summary = deposit_cohort_flows(panel)
        for segment, result in summary.items():
            self.assertAlmostEqual(result["cohort_reconciliation_residual"], 0, places=7)
            self.assertGreater(result["tagged_cohort_remaining_at_bank"], result["retained_in_original_product"])
            self.assertGreater(result["closing_original_product_total"], result["retained_in_original_product"])
        self.assertGreater(summary["rate_sensitive"]["migrated_to_other_bank_product"], summary["operating"]["migrated_to_other_bank_product"])

    def test_ladder_obeys_retention_and_policy_not_beta(self):
        panel = [r for r in synthetic_deposit_panel() if r["date"] < "2025-01-01"]
        bounds = retention_bounds_from_panel(panel)
        ladder = constrained_replication_ladder(2000000, bounds)
        self.assertAlmostEqual(sum(r["weight"] for r in ladder["rungs"]), 1)
        self.assertGreaterEqual(ladder["rungs"][0]["weight"], .2)
        self.assertLessEqual(ladder["average_maturity_months"], 6)
        for horizon, retention in bounds.items():
            locked = sum(r["weight"] for r in ladder["rungs"] if r["months"] > horizon)
            self.assertLessEqual(locked, retention * .9 + 1e-12)
        stressed = constrained_replication_ladder(2000000, {1: .3, 3: .2, 6: .1, 12: .05})
        self.assertLess(stressed["weighted_yield"], ladder["weighted_yield"])
        overnight = constrained_replication_ladder(100, bounds, maximum_average_months=0)
        self.assertEqual(overnight["annualised_income_run_rate"], 4)
        with self.assertRaises(ValueError):
            constrained_replication_ladder(100, {1: .9, 3: .95, 12: .7})
        with self.assertRaises(ValueError):
            constrained_replication_ladder(float("nan"), bounds)
        tighter = constrained_replication_ladder(2000000, bounds, retention_haircut=.25)
        self.assertEqual(tighter["rungs"][0]["weight"], .3)
        self.assertLess(tighter["weighted_yield"], ladder["weighted_yield"])


class STPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "test.sqlite3"
        self.flow = STPWorkflow(self.path)
        self.terms = {"currency": "KES", "notional_cents": 10000, "rate_bps": 500,
                      "start": "2027-01-01", "end": "2027-04-01", "instrument": "fixed_deposit_placement",
                      "counterparty": "SYNTHETIC", "curve_version": "v1", "snapshot_id": "s1"}
        self.flow.apply("p", "PROPOSE", "maker", {"proposal_id": "P", "terms": self.terms})

    def tearDown(self):
        self.flow.close()
        self.temp.cleanup()

    def act(self, event, kind, actor, **payload):
        return self.flow.apply(event, kind, actor, {"proposal_id": "P", **payload})

    def booked(self):
        self.act("a", "APPROVE", "approver")
        self.act("o", "ORDER", "dealer", order_id="O")
        self.act("c", "CONFIRM", "operations", order_id="O", trade_id="T", confirmation_id="C", terms=self.terms)
        self.act("b", "BOOK", "operations", trade_id="T")

    def test_wrong_role_and_self_approval_are_rejected(self):
        with self.assertRaises(PermissionError):
            self.act("a", "APPROVE", "dealer")
        self.flow.actors["maker"] = "approver"
        with self.assertRaises(PermissionError):
            self.act("a2", "APPROVE", "maker")
        self.assertEqual(self.flow.recompute()["event_count"], 1)

    def test_rejection_prevents_execution(self):
        self.act("r", "REJECT", "approver", reason="Illustrative limit decision")
        with self.assertRaises(ValueError):
            self.act("o", "ORDER", "dealer", order_id="O")
        self.assertEqual(self.flow.recompute()["journal_lines"], 0)

    def test_approval_limit_and_wrong_settlement_amount_do_not_post(self):
        self.flow.limit = 9999
        with self.assertRaises(ValueError):
            self.act("a", "APPROVE", "approver")
        self.assertEqual(self.flow.recompute()["event_count"], 1)
        self.flow.limit = 10000
        self.booked()
        with self.assertRaises(ValueError):
            self.act("s", "SETTLE", "operations", settlement_id="S", cash_cents=-10001)
        self.assertEqual(self.flow.recompute()["journal_lines"], 2)

    def test_confirmation_changed_economic_terms_is_rejected(self):
        self.act("a", "APPROVE", "approver")
        self.act("o", "ORDER", "dealer", order_id="O")
        changed = {**self.terms, "rate_bps": 501}
        with self.assertRaises(ValueError):
            self.act("c", "CONFIRM", "operations", order_id="O", trade_id="T", confirmation_id="C", terms=changed)
        self.assertEqual(self.flow.recompute()["event_count"], 3)

    def test_idempotent_booking_survives_process_restart(self):
        self.booked()
        self.flow.close()
        self.flow = STPWorkflow(self.path)
        replay = self.act("b", "BOOK", "operations", trade_id="T")
        self.assertTrue(replay["duplicate"])
        self.assertEqual(self.flow.recompute()["journal_lines"], 2)
        with self.assertRaises(ValueError):
            self.act("b", "BOOK", "operations", trade_id="DIFFERENT")
        with self.assertRaises(ValueError):
            self.act("b2", "BOOK", "operations", trade_id="T")

    def test_failed_settlement_retry_and_independent_journal_reconstruction(self):
        self.booked()
        self.act("f", "SETTLEMENT_FAILED", "operations", reason="Outage")
        self.assertNotIn("cash", self.flow.recompute()["account_balances_cents"])
        with self.assertRaises(ValueError):
            self.act("s", "SETTLE", "operations", settlement_id="S", cash_cents=-10000, retry_of="wrong")
        self.act("s", "SETTLE", "operations", settlement_id="S", cash_cents=-10000, retry_of="f")
        expected = {"placement_asset": 10000, "settlement_payable": 0, "cash": -10000}
        ledger = self.flow.recompute()
        self.assertEqual(ledger["account_balances_cents"], expected)
        self.assertEqual(ledger["trial_balance_residual_cents"], 0)
        self.assertTrue(ledger["ledger_matches_events"])
        with self.assertRaises(ValueError):
            self.act("r", "RECONCILE", "auditor", statement_id="ST", bank_cash_cents=-9999, position_cents=10000)
        self.assertEqual(self.act("r", "RECONCILE", "auditor", statement_id="ST", bank_cash_cents=-10000, position_cents=10000)["status"], "RECONCILED")

    def test_balanced_but_tampered_journal_is_detected(self):
        self.booked()
        self.act("s", "SETTLE", "operations", settlement_id="S", cash_cents=-10000)
        self.flow.db.execute("UPDATE journal SET signed_cents=signed_cents*2")
        self.flow.db.commit()
        ledger = self.flow.recompute()
        self.assertEqual(ledger["trial_balance_residual_cents"], 0)
        self.assertFalse(ledger["ledger_matches_events"])
        with self.assertRaises(ValueError):
            self.act("r", "RECONCILE", "auditor", statement_id="ST", bank_cash_cents=-10000, position_cents=10000)

    def test_example_settlement_replay_preserves_exactly_one_cash_posting(self):
        example = stp_example()
        self.assertTrue(example["duplicate_after_restart"]["duplicate"])
        self.assertEqual(example["ledger_after_restart"], example["ledger"])
        self.assertEqual(example["ledger"]["event_count"], 8)
        self.assertEqual(example["ledger"]["journal_lines"], 4)


if __name__ == "__main__":
    unittest.main()
