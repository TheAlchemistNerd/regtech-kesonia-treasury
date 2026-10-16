import json
import math
import unittest

from research_lab.regulatory_cases import (
    IRTrade, LiquidAsset, girr_correlation, girr_delta, liquidity_coverage,
    liquidity_example, reduced_ba_cva, regulatory_examples, sa_ccr_ir,
    stable_funding, supervisory_duration, unilateral_cva, wrong_way_example,
    balance_sheet_interest_case, reverse_cash_stress,
)


class LiquidityCases(unittest.TestCase):
    def test_both_caps_are_simultaneously_enforced(self):
        x = liquidity_example()["lcr"]
        self.assertAlmostEqual(x["hqla"], 100/.6)
        self.assertAlmostEqual(x["accepted_level2b"], 25)
        self.assertLessEqual(x["accepted_level2a"]+x["accepted_level2b"], .4*x["hqla"]+1e-10)
        self.assertAlmostEqual(x["inflows_recognised"], 142.5)
        self.assertAlmostEqual(x["net_outflows"], 47.5)
        self.assertAlmostEqual(x["lcr"], (100/.6)/47.5)

    def test_cap_feasibility_across_grid(self):
        for l1 in (0, 5, 100):
            for a in (0, 25, 100):
                for b in (0, 10, 90):
                    x = liquidity_coverage([LiquidAsset("a", l1, "L1"),
                                            LiquidAsset("b", a/.85, "L2A"),
                                            LiquidAsset("c", b/.5, "L2B_CORPORATE")], [], [])
                    self.assertGreaterEqual(x["hqla"], l1)
                    self.assertLessEqual(x["accepted_level2a"], a+1e-10)
                    self.assertLessEqual(x["accepted_level2b"], b+1e-10)
                    self.assertLessEqual(x["accepted_level2b"], .15*x["hqla"]+1e-10)
                    self.assertAlmostEqual(l1+x["accepted_level2a"]+x["accepted_level2b"], x["hqla"])

    def test_encumbrance_and_operational_unavailability(self):
        x = liquidity_coverage([LiquidAsset("pledged", 100, "L1", encumbered=True),
                                LiquidAsset("trapped", 100, "L1", operationally_available=False)],
                               [("out", 10, 1)], [])
        self.assertEqual(x["hqla"], 0)
        self.assertEqual(x["lcr"], 0)

    def test_double_counting_and_sft_fail_closed(self):
        with self.assertRaises(ValueError):
            liquidity_coverage([LiquidAsset("security", 100, "L1")], [], [("security", 100, 1)])
        with self.assertRaises(ValueError):
            liquidity_coverage([], [], [], short_sft_unwind_required=True)

    def test_no_outflow_ratio_is_explicitly_undefined(self):
        x = liquidity_coverage([LiquidAsset("cash", 100, "L1")], [], [("receipt", 40, 1)])
        self.assertIsNone(x["lcr"])
        self.assertEqual(x["inflows_recognised"], 0)

    def test_stable_funding_uses_gross_carrying_values_not_lcr_haircuts(self):
        x = liquidity_example()["nsfr"]
        self.assertEqual(x["asf"], 810)
        self.assertEqual(x["rsf_assets"], 551.5)
        self.assertEqual(x["rsf_commitments"], 5)
        self.assertEqual(x["rsf"], 556.5)
        self.assertEqual(x["balance_sheet_residual"], 0)
        self.assertAlmostEqual(x["nsfr"], 810/556.5)

    def test_cash_and_equity_reconcile_at_every_event(self):
        x = liquidity_example()
        self.assertEqual(x["cash_without_monetisation_on_3_oct"], -170)
        self.assertEqual(x["closing_cash"], 175)
        self.assertEqual(x["closing_equity"], 80)
        self.assertEqual(x["realised_sale_loss"], 20)
        self.assertEqual(x["cash_bridge_residual"], 0)
        for row in x["timeline"]:
            self.assertEqual(row["balance_residual"], 0)
            self.assertGreaterEqual(row["cash"], 0)

    def test_ratios_invariant_to_currency_scale(self):
        a = liquidity_coverage([LiquidAsset("cash", 100, "L1")], [("deposits", 400, .1)], [("loan", 20, .5)])
        b = liquidity_coverage([LiquidAsset("cash", 1e8, "L1")], [("deposits", 4e8, .1)], [("loan", 2e7, .5)])
        self.assertAlmostEqual(a["lcr"], b["lcr"])
        self.assertAlmostEqual(b["hqla"], a["hqla"]*1e6)

    def test_invalid_factors_and_nonfinite_inputs(self):
        with self.assertRaises(ValueError):
            stable_funding([("x", 10, 1.01)], [], [])
        with self.assertRaises(ValueError):
            liquidity_coverage([LiquidAsset("x", float("nan"), "L1")], [], [])

    def test_eve_nii_use_same_book_and_zero_shock_identity(self):
        x = balance_sheet_interest_case(0)
        self.assertEqual(x["opening_asset_balance"], 1000)
        self.assertEqual(x["opening_liability_balance"], 900)
        self.assertEqual(x["delta_eve"], 0)
        self.assertEqual(x["delta_nii"], 0)
        self.assertAlmostEqual(x["base_nii"], 88.6)
        for row in x["rows"]:
            if row["maturity_years"] and row["maturity_years"] == int(row["maturity_years"]):
                self.assertAlmostEqual(row["base_pv"], row["opening_carrying_value"])

    def test_nii_hand_repricing_bridge_and_linear_shocks(self):
        x = balance_sheet_interest_case(.02)
        asset_bump = 350*.02*(1-19/365)
        funding_bump = (400*.5+200*.8+200+50)*.02
        self.assertAlmostEqual(x["delta_nii"], asset_bump-funding_bump)
        y = balance_sheet_interest_case(-.02)
        self.assertAlmostEqual(x["delta_nii"], -y["delta_nii"])
        self.assertLess(x["delta_eve"], 0)
        self.assertGreater(y["delta_eve"], 0)

    def test_eve_cashflows_repay_each_principal_once(self):
        for row in balance_sheet_interest_case()["rows"]:
            if row["maturity_years"]:
                self.assertAlmostEqual(sum(cf["redemption"] for cf in row["cashflows"]), row["opening_carrying_value"])
                self.assertEqual(row["cashflows"][-1]["time"], row["maturity_years"])

    def test_reverse_cash_boundary_and_breach(self):
        x = reverse_cash_stress()
        for response in x["responses"]:
            w = response["withdrawal_multiplier_exhausting_cash"]
            available = response["opening_cash_plus_sales"]
            self.assertAlmostEqual(available-170*w-20, 0)
            self.assertLess(available-170*(w+1e-6)-20, 0)
        self.assertEqual(x["responses"][0]["baseline_funding_shortfall"], 170)
        self.assertEqual(x["responses"][1]["additional_collateral_call_capacity_at_baseline"], 0)
        self.assertEqual(x["responses"][2]["additional_collateral_call_capacity_at_baseline"], 35)


class CounterpartyCases(unittest.TestCase):
    def trade(self, **kwargs):
        values = dict(name="t", notional=1_000_000, start_years=0., end_years=3.,
                      maturity_years=3., delta=1, market_value=20_000)
        values.update(kwargs)
        return IRTrade(**values)

    def test_single_trade_independent_hand_formula(self):
        x = sa_ccr_ir([self.trade()])
        sd = (1-math.exp(-.15))/.05
        addon = 1_000_000*sd*.005
        self.assertAlmostEqual(x["addon"], addon)
        self.assertEqual(x["replacement_cost"], 20_000)
        self.assertEqual(x["multiplier"], 1)
        self.assertAlmostEqual(x["ead"], 1.4*(20_000+addon))

    def test_opposite_identical_trades_cancel(self):
        x = sa_ccr_ir([self.trade(), self.trade(name="offset", delta=-1, market_value=-20_000)])
        self.assertEqual(x["addon"], 0)
        self.assertEqual(x["ead"], 0)

    def test_netting_benefit_and_daily_margin(self):
        x = regulatory_examples()["sa_ccr"]
        self.assertGreater(x["without_netting_ead"], x["unmargined"]["ead"])
        self.assertLess(x["margined"]["ead"], x["unmargined"]["ead"])
        self.assertAlmostEqual(x["margined"]["trades"][0]["maturity_factor"], .3)
        self.assertEqual(x["margined"]["replacement_cost"], 0)

    def test_maturity_floors_and_margin_cap(self):
        short = self.trade(end_years=1/250, maturity_years=1/250)
        x = sa_ccr_ir([short])
        self.assertEqual(x["trades"][0]["maturity_factor"], .2)
        y = sa_ccr_ir([short], mpor_days=10, threshold=1_000_000)
        self.assertTrue(y["margin_cap_applied"])
        self.assertEqual(y["ead"], y["unmargined_ead_same_collateral"])
        with self.assertRaises(ValueError):
            sa_ccr_ir([short], mpor_days=5)

    def test_nica_and_multiplier_floor(self):
        x = sa_ccr_ir([self.trade()], collateral=1_000_000, mpor_days=10, threshold=30_000,
                      minimum_transfer=5_000, nica=10_000)
        self.assertEqual(x["replacement_cost"], 25_000)
        self.assertGreaterEqual(x["multiplier"], .05)
        self.assertLess(x["multiplier"], .051)

    def test_duration_forward_start_and_small_interval(self):
        self.assertAlmostEqual(supervisory_duration(2, 5), math.exp(-.1)*supervisory_duration(0, 3))
        self.assertEqual(supervisory_duration(0, 1e-9), 10/250)
        with self.assertRaises(ValueError):
            supervisory_duration(3, 2)

    def test_ccr_scale_homogeneity(self):
        x = sa_ccr_ir([self.trade()], collateral=15_000)
        y = sa_ccr_ir([self.trade(notional=10_000_000, market_value=200_000)], collateral=150_000)
        self.assertAlmostEqual(y["ead"], 10*x["ead"])


class CvaAndMarketCases(unittest.TestCase):
    def test_cva_closed_form_flat_profile(self):
        x = unilateral_cva([1, 2, 3], [100, 100, 100], .02, .4, 0)
        self.assertAlmostEqual(x["cva"], .6*100*(1-math.exp(-.02/.6*3)))
        self.assertAlmostEqual(sum(r["marginal_default_probability"] for r in x["rows"]), 1-math.exp(-.1))
        self.assertEqual(unilateral_cva([1], [100], 0, .4, .09)["cva"], 0)

    def test_analytic_cs01_agrees_with_shrinking_bump(self):
        args = ([1, 2, 3], [600_000, 900_000, 400_000])
        x = unilateral_cva(*args, .02, .4, .09)
        errors = []
        for bump in (1e-4, 5e-5):
            up = unilateral_cva(*args, .02+bump, .4, .09)["cva"]
            down = unilateral_cva(*args, .02-bump, .4, .09)["cva"]
            errors.append(abs((up-down)/(2*bump)*1e-4-x["cs01"]))
        self.assertLess(errors[1], errors[0]/3)
        self.assertLess(errors[1], 1e-5)

    def test_wrong_way_comparator_preserves_marginals(self):
        x = wrong_way_example()
        self.assertGreater(x["joint_cva"], x["independent_cva_same_marginals"])
        for j, row in enumerate(x["independent_marginals"]):
            self.assertAlmostEqual(row["marginal_default_probability"], sum(s["weight"]*s["rows"][j]["marginal_default_probability"] for s in x["states"]))

    def test_reduced_ba_cva_single_counterparty_and_diversification(self):
        row = {"name": "one", "risk_weight": .03, "netting_sets": [(140_000, 3)]}
        x = reduced_ba_cva([row])
        # Alpha cancels 140,000/1.4 to 100,000, M*DF=(1-exp(-.15))/.05.
        expected = .65*.03*100_000*(1-math.exp(-.15))/.05
        self.assertAlmostEqual(x["capital"], expected)
        self.assertAlmostEqual(x["rwa"], 12.5*expected)
        y = reduced_ba_cva([row, {**row, "name": "two"}])
        self.assertAlmostEqual(y["capital"], expected*math.sqrt(2.5))

    def test_girr_correlation_table_and_floor(self):
        self.assertAlmostEqual(girr_correlation(1, 5), math.exp(-.12))
        self.assertEqual(girr_correlation(.25, 30), .4)
        self.assertEqual(girr_correlation(.25, 30, "low"), .30000000000000004)
        self.assertEqual(girr_correlation(1, 2, "high"), 1.)

    def test_single_factor_and_exact_offset(self):
        x = girr_delta([("KES", 5, -100_000)])
        self.assertAlmostEqual(x["girr_delta_component"], 1100)
        y = girr_delta([("KES", 5, 100_000), ("KES", 5, -100_000)])
        self.assertEqual(y["girr_delta_component"], 0)

    def test_two_tenor_hand_calculation_and_cross_currency(self):
        x = girr_delta([("KES", 1, 100_000), ("KES", 5, -100_000)])
        rho = math.exp(-.12)
        expected = math.sqrt(1600**2+1100**2-2*rho*1600*1100)
        self.assertAlmostEqual(x["scenarios"]["medium"]["capital_component"], expected)
        y = girr_delta([("KES", 5, 100_000), ("USD", 5, 100_000)])
        self.assertAlmostEqual(y["scenarios"]["medium"]["capital_component"], 1100*math.sqrt(3))
        self.assertEqual(y["worst_scenario"], "high")

    def test_girr_scale_sign_and_order_invariance(self):
        entries = [("KES", 1, -20_000), ("KES", 5, 80_000), ("USD", 10, -10_000)]
        x = girr_delta(entries)
        y = girr_delta([(c, t, -7*s) for c, t, s in reversed(entries)])
        self.assertAlmostEqual(y["girr_delta_component"], 7*x["girr_delta_component"])

    def test_zero_coupon_sensitivities_are_independent_derivatives(self):
        for p in regulatory_examples()["frtb_girr_delta"]["synthetic_positions"]:
            n, t, r = p["signed_reporting_notional"], p["tenor"], p["continuous_zero_rate"]
            bump = 1e-6
            fd = (n*math.exp(-(r+bump)*t)-n*math.exp(-(r-bump)*t))/(2*bump)
            self.assertAlmostEqual(fd/p["analytic_sensitivity_per_decimal"], 1, places=9)
            forward_bp = (n*math.exp(-(r+.0001)*t)-n*math.exp(-r*t))/.0001
            self.assertAlmostEqual(forward_bp/p["regulatory_one_bp_sensitivity_per_decimal"], 1, places=10)

    def test_cases_serialise_without_nonfinite_values(self):
        json.dumps(regulatory_examples(), allow_nan=False)


if __name__ == "__main__":
    unittest.main()
