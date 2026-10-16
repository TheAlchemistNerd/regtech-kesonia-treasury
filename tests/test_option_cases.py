"""Economic identities, independent benchmarks and numerical recovery tests."""
import itertools
import json
import math
import unittest

from research_lab.option_cases import (
    calibrate_rate_tree, cpr_to_smm, scheduled_principal_fraction,
    mortgage_pool, solve_oas, optimal_mortgage_value, swap_pv, par_swap_rate,
    finite_difference_risk, hedge_selection_case, collateral_case, option_examples,
    merton_terminal_debt, recover_merton_assets,
)


class RateAndMortgageTests(unittest.TestCase):
    def tree(self, months=36, sigma=.015, zero=.085):
        return calibrate_rate_tree([math.exp(-zero * i / 12) for i in range(months + 1)], sigma=sigma)

    def test_curve_reprices_every_maturity_including_negative_rates(self):
        for zero in (.085, -.01):
            tree = self.tree(zero=zero)
            for prices, target in zip(tree.state_prices, tree.input_discount_factors):
                self.assertAlmostEqual(sum(prices), target, places=13)
                self.assertGreaterEqual(min(prices), 0)

    def test_zero_volatility_tree_is_deterministic_forward_curve(self):
        tree = self.tree(sigma=0)
        for rates in tree.rates:
            for rate in rates:
                self.assertAlmostEqual(rate, .085, places=12)

    def test_invalid_calibration_inputs_fail(self):
        for discounts, dt, sigma in (([1, 0], 1/12, .01), ([.99, .9], 1/12, .01),
                                    ([1, .9], 0, .01), ([1, .9], 1/12, -.1),
                                    ([1, float('nan')], 1/12, .01)):
            with self.assertRaises(ValueError):
                calibrate_rate_tree(discounts, dt, sigma)

    def test_cpr_conversion_preserves_annual_survival(self):
        for cpr in (0, .04, .60, 1):
            self.assertAlmostEqual((1 - cpr_to_smm(cpr)) ** 12, 1 - cpr, places=14)
        with self.assertRaises(ValueError):
            cpr_to_smm(1.1)

    def test_principal_cash_conservation_in_every_month(self):
        result = mortgage_pool(self.tree())
        self.assertAlmostEqual(result['expected_principal_paid'], 1e6, places=6)
        self.assertAlmostEqual(result['final_expected_balance'], 0, places=7)
        for row in result['monthly_cashflows_under_Q']:
            self.assertAlmostEqual(row['principal_reconciliation_residual'], 0, places=7)
            self.assertGreaterEqual(row['prepayment'], 0)
            self.assertGreaterEqual(row['closing_expected_balance'], 0)

    def test_no_prepay_matches_independent_deterministic_discounted_schedule(self):
        tree = self.tree()
        balance, direct = 1e6, 0.0
        monthly = .14 / 12
        payment = balance * monthly / (1 - (1 + monthly) ** -36)
        for i in range(1, 37):
            interest = balance * monthly
            principal = balance if i == 36 else payment - interest
            direct += (interest + principal) * tree.input_discount_factors[i]
            balance -= principal
        result = mortgage_pool(tree, base_cpr=0, response=0, cpr_cap=0)
        self.assertAlmostEqual(result['pv'], direct, places=6)

    def test_node_aggregation_matches_independent_path_enumeration(self):
        tree, months = self.tree(months=6), 6
        enumerated = 0.0
        for path in itertools.product((0, 1), repeat=months):
            balance, discount, cash_pv, j = 1e6, 1.0, 0.0, 0
            for i, move in enumerate(path):
                rate = tree.rates[i][j]
                interest = balance * .14 / 12
                payment = balance * (.14 / 12) / (1 - (1 + .14 / 12) ** -(months - i))
                scheduled = min(balance, payment - interest)
                cpr = min(.6, .04 + 6 * max(.14 - rate - .025, 0))
                prepay = (balance - scheduled) * (1 - (1 - cpr) ** (1/12))
                discount *= math.exp(-(rate + .0175) / 12)
                cash_pv += (interest + scheduled + prepay) * discount
                balance -= scheduled + prepay
                j += move
            enumerated += cash_pv / 2 ** months
        self.assertAlmostEqual(mortgage_pool(tree, spread=.0175)['pv'], enumerated, places=6)

    def test_oas_recovers_positive_and_negative_known_spreads(self):
        tree = self.tree()
        for spread in (-.025, 0, .0175, .12):
            target = mortgage_pool(tree, spread=spread)['pv']
            recovered = solve_oas(tree, target)
            self.assertAlmostEqual(recovered['spread'], spread, places=11)
            self.assertLessEqual(abs(recovered['price_residual']), 1e-7)

    def test_oas_monotonicity_and_bad_bracket(self):
        tree = self.tree()
        prices = [mortgage_pool(tree, spread=s)['pv'] for s in (-.03, 0, .02, .10)]
        self.assertTrue(all(a > b for a, b in zip(prices, prices[1:])))
        with self.assertRaises(ValueError):
            solve_oas(tree, 3e6)

    def test_zero_coupon_and_full_prepayment_edges(self):
        result = mortgage_pool(self.tree(), coupon=0, base_cpr=1, cpr_cap=1, response=0)
        self.assertAlmostEqual(result['monthly_cashflows_under_Q'][0]['scheduled_principal'], 1e6/36)
        self.assertAlmostEqual(result['monthly_cashflows_under_Q'][0]['closing_expected_balance'], 0)
        self.assertAlmostEqual(result['pv'], 1e6 * self.tree().input_discount_factors[1], places=7)

    def test_optimal_borrower_option_cannot_increase_lender_value(self):
        tree = self.tree()
        optimal = optimal_mortgage_value(tree)
        noncallable = optimal_mortgage_value(tree, allow_prepayment=False)
        scheduled = mortgage_pool(tree, base_cpr=0, response=0, cpr_cap=0)
        self.assertAlmostEqual(noncallable['pv'], scheduled['pv'], places=6)
        self.assertLess(optimal['pv'], noncallable['pv'])
        self.assertGreater(optimal['exercise_node_count'], 0)

    def test_no_borrower_exercise_when_coupon_zero_and_rates_positive(self):
        result = optimal_mortgage_value(self.tree(sigma=0), coupon=0)
        self.assertEqual(result['exercise_node_count'], 0)


class HedgeAndCollateralTests(unittest.TestCase):
    def test_par_swaps_reprice_and_payer_gains_on_upward_parallel_shift(self):
        for tenor in (2, 5):
            fixed = par_swap_rate(tenor)
            self.assertAlmostEqual(swap_pv(tenor, 1e6, fixed), 0, places=7)
            self.assertGreater(swap_pv(tenor, 1e6, fixed, .01, .01), 0)
            self.assertLess(swap_pv(tenor, 1e6, fixed, -.01, -.01), 0)

    def test_finite_difference_has_independent_exponential_benchmark(self):
        price = lambda shift: 1e6 * math.exp(-(.085 + shift) * 3)
        risk = finite_difference_risk(price)
        self.assertAlmostEqual(risk['d_pv_per_bp'], -3 * price(0) * 1e-4, places=4)
        self.assertLess(abs(risk['second_derivative_kes_per_rate_squared'] / (9 * price(0)) - 1), 2e-7)

    def test_selected_hedge_obeys_joint_cash_and_fee_limits_and_grid_optimality(self):
        result = hedge_selection_case()
        chosen = result['selected']
        self.assertLessEqual(chosen['transaction_fee'], 2000)
        self.assertLessEqual(chosen['initial_cash_use'], 70000)
        objective = chosen['objective_worst_absolute_scenario_pnl_after_fee']
        self.assertEqual(objective, min(c['objective_worst_absolute_scenario_pnl_after_fee'] for c in result['candidates'] if c['feasible']))
        self.assertLess(objective, result['candidates'][0]['objective_worst_absolute_scenario_pnl_after_fee'])

    def test_basis_stress_changes_swap_pv_even_when_asset_does_not_change(self):
        result = hedge_selection_case()
        stress = next(s for s in result['selected']['scenarios'] if s['label'].startswith('projection_basis'))
        self.assertAlmostEqual(stress['asset_pnl'], 0)
        self.assertGreater(abs(stress['hedge_pnl']), 0)

    def test_finite_difference_risk_converges(self):
        result = hedge_selection_case()
        self.assertLess(abs(result['selected_risk']['d_pv_per_bp'] - result['risk_at_half_bump']['d_pv_per_bp']), .001)

    def test_funding_and_net_wealth_identities_for_both_legal_settlement_treatments(self):
        for mode in ('bilateral', 'cleared'):
            result = collateral_case(mode)
            for row in result['events']:
                self.assertAlmostEqual(row['funding_identity_residual'], 0, places=7)
                self.assertAlmostEqual(row['net_wealth_identity_residual'], 0, places=7)
                self.assertGreaterEqual(row['available_cash'], -1e-8)
            self.assertGreater(result['peak_borrowing'], 0)

    def test_bilateral_call_is_pending_until_next_weekday_morning(self):
        result = collateral_case()
        call, settled = result['events'][1:3]
        self.assertGreater(call['vm_pending_market_value'], 0)
        self.assertEqual(call['vm_collateral_posted_market_value'], 0)
        self.assertAlmostEqual(settled['vm_collateral_posted_market_value'], call['vm_pending_market_value'])
        self.assertEqual(settled['vm_pending_market_value'], 0)

    def test_haircut_grossup_and_netting(self):
        row = collateral_case()['events'][-1]
        self.assertAlmostEqual(row['im_collateral_market_value'] * .98, row['im_required'], places=7)
        self.assertAlmostEqual(row['vm_collateral_posted_market_value'] * .98, row['vm_required_before_haircut'], places=7)
        self.assertGreater(row['gross_out_of_money_marks_without_netting'], -row['net_derivative_mark_before_settlement'])

    def test_minimum_transfer_threshold_controls_calls(self):
        rows = collateral_case(mta=1e9)['events']
        self.assertTrue(all(r['vm_collateral_posted_market_value'] == 0 for r in rows))
        self.assertGreater(rows[-1]['gap_after_posted_vm'], 0)

    def test_cleared_final_variation_is_not_double_counted_as_collateral(self):
        for row in collateral_case('cleared')['events']:
            self.assertEqual(row['vm_collateral_posted_market_value'], 0)
            self.assertEqual(row['restricted_collateral_asset'], row['im_collateral_market_value'])
            self.assertAlmostEqual(row['cumulative_final_variation_settlement_paid'], -row['net_derivative_mark_before_settlement'])

    def test_hedge_reduces_value_movement_while_increasing_cash_demand(self):
        result = collateral_case('cleared')
        final = result['events'][-1]
        self.assertLess(abs(final['combined_economic_change']), abs(final['asset_value_change']))
        self.assertGreater(final['funding_borrowing'], result['events'][0]['funding_borrowing'])
        self.assertGreater(final['cumulative_funding_expense'], 0)

    def test_examples_are_json_serializable_without_nonfinite_numbers(self):
        json.dumps(option_examples(), allow_nan=False)


class StructuralCreditTests(unittest.TestCase):
    def test_debt_equity_identity_and_credit_discount_bounds(self):
        for value in (500_000, 1_000_000, 1_500_000, 5_000_000):
            result = merton_terminal_debt(value, 1e6, .30, .085, 3)
            self.assertAlmostEqual(result['debt_value'] + result['equity_value'], value, places=7)
            self.assertGreaterEqual(result['put_credit_discount'], -1e-8)
            self.assertLessEqual(result['debt_value'], min(value, result['risk_free_debt_pv']) + 1e-8)
            self.assertTrue(0 <= result['terminal_default_probability_Q'] <= 1)

    def test_synthetic_observations_recover_asset_value_and_volatility(self):
        observed = merton_terminal_debt(1.5e6, 1e6, .30, .085, 3)
        fit = recover_merton_assets(observed['equity_value'], observed['equity_volatility'], 1e6, .085, 3)
        self.assertAlmostEqual(fit['asset_value'], 1.5e6, places=5)
        self.assertAlmostEqual(fit['asset_volatility'], .30, places=11)
        self.assertLess(abs(fit['equity_value_residual']), 1e-7)

    def test_terminal_payoffs_and_zero_volatility_limit(self):
        for value in (500_000, 1_500_000):
            terminal = merton_terminal_debt(value, 1e6, .3, .085, 0)
            self.assertEqual(terminal['debt_value'], min(value, 1e6))
            self.assertEqual(terminal['equity_value'], max(value - 1e6, 0))
            deterministic = merton_terminal_debt(value, 1e6, 0, .085, 3)
            self.assertAlmostEqual(deterministic['debt_value'], min(value, 1e6 * math.exp(-.085*3)))

    def test_riskier_assets_increase_equity_option_and_reduce_debt_value(self):
        low = merton_terminal_debt(1.5e6, 1e6, .15, .085, 3)
        high = merton_terminal_debt(1.5e6, 1e6, .5, .085, 3)
        self.assertGreater(high['equity_value'], low['equity_value'])
        self.assertLess(high['debt_value'], low['debt_value'])

    def test_invalid_calibration_domain_rejected(self):
        with self.assertRaises(ValueError):
            recover_merton_assets(1e6, .3, 1e6, .085, 0)
        with self.assertRaises(ValueError):
            merton_terminal_debt(-1, 1e6, .3, .085, 3)


if __name__ == '__main__':
    unittest.main()
