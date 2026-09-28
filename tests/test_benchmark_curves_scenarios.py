import math
import unittest
from datetime import date, datetime, timedelta
from decimal import Decimal as D
from dataclasses import replace
from research_lab.benchmark import Calendar, Fixing, Interval, schedule, compound, published_index_ratio, benchmark_examples
from research_lab.curves import Curve, bootstrap_annual_par, quote_repricing, floating_note_pv, key_rate_dv01
from research_lab.scenarios import BalanceSheet, Period, step, marginal_defaults, discounted_shortfall, scenario_examples, constrained_hedge_example


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar()
        self.cutoff = datetime.fromisoformat('2025-09-08T09:00:00+03:00')
        self.fixing = Fixing(date(2025, 9, 5), self.cutoff, D('.094618'), 'v1')
        self.rows = schedule(date(2025, 9, 5), date(2025, 9, 8), self.calendar)

    def test_published_weekend_index_independent_check(self):
        result = compound(self.rows, [self.fixing], self.cutoff, D('1000000'), D('.03'))
        self.assertEqual(result['total_cash_rounded'], '1024.26')
        index = published_index_ratio(D('100.10451025'), D('100.18235974'))
        self.assertLess(abs(D(result['benchmark_cash']) - index * D('1000000')), D('.0001'))
        # A weekend span uses one linear factor; three separate daily products differ.
        self.assertNotEqual(D(result['factor']), (1 + D('.094618') / 365) ** 3 - 1)

    def test_clipped_weekend_and_calendar_holiday(self):
        rows = schedule(date(2025, 9, 6), date(2025, 9, 7), self.calendar)
        self.assertEqual(rows, [Interval(date(2025, 9, 6), date(2025, 9, 7), date(2025, 9, 5), 1)])
        examples = benchmark_examples()
        self.assertEqual(examples['five_business_day_no_shift']['weight_days'], 7)
        self.assertEqual(examples['five_business_day_shift']['weight_days'], 6)
        self.assertNotEqual(examples['five_business_day_shift']['factor'], examples['five_business_day_no_shift']['factor'])

    def test_unavailable_fixing_does_not_leak_future_information(self):
        with self.assertRaises(LookupError):
            compound(self.rows, [self.fixing], self.cutoff - timedelta(seconds=1), D(100))

    def test_correction_is_selected_by_availability(self):
        later = replace(self.fixing, rate=D('.10'), available_at=self.cutoff + timedelta(days=1), version='v2')
        old = compound(self.rows, [later, self.fixing], self.cutoff, D(100))
        revised = compound(self.rows, [later, self.fixing], later.available_at, D(100))
        self.assertEqual(old['ledger'][0]['version'], 'v1')
        self.assertEqual(revised['ledger'][0]['version'], 'v2')
        with self.assertRaises(ValueError):
            compound(self.rows, [self.fixing, self.fixing], self.cutoff, D(100))

    def test_fallback_requires_recorded_authorization(self):
        fallback = replace(self.fixing, source='CBR')
        with self.assertRaises(ValueError):
            compound(self.rows, [fallback], self.cutoff, D(100))
        approved = replace(fallback, fallback_authorization='synthetic-contract-clause-v1')
        self.assertEqual(compound(self.rows, [approved], self.cutoff, D(100))['ledger'][0]['source'], 'CBR')

    def test_negative_rate_valid_but_nonpositive_factor_rejected(self):
        result = compound(self.rows, [replace(self.fixing, rate=D('-.01'))], self.cutoff, D(100))
        self.assertLess(D(result['factor']), 0)
        with self.assertRaises(ValueError):
            compound(self.rows, [replace(self.fixing, rate=D('-200'))], self.cutoff, D(100))

    def test_gap_overlap_and_invalid_input_fail(self):
        for bad in [self.rows + self.rows, [replace(self.rows[0], weight_days=0)]]:
            with self.assertRaises(ValueError):
                compound(bad, [self.fixing], self.cutoff, D(100))
        with self.assertRaises(ValueError):
            compound(self.rows, [replace(self.fixing, rate=D('NaN'))], self.cutoff, D(100))


class CurveTests(unittest.TestCase):
    def test_sensitivities_reject_nonfinite_cashflows(self):
        c = bootstrap_annual_par(.10, [.12])
        for flow in [(1, float('nan')), (float('inf'), 1)]:
            with self.assertRaises(ValueError): key_rate_dv01(c, [flow])

    def test_quotes_reprice_and_closed_form_matches(self):
        c = bootstrap_annual_par(.10, [.12, .13])
        self.assertAlmostEqual(c.df(1), 10 / 11, places=13)
        self.assertAlmostEqual(c.df(2), 175 / 220, places=13)
        for row in quote_repricing(c, .10, [.12, .13]):
            self.assertLess(abs(row['residual_to_unit_price']), 1e-12)

    def test_log_discount_interpolation_and_no_extrapolation(self):
        c = bootstrap_annual_par(.10, [.12, .13])
        self.assertAlmostEqual(c.df(1.5), math.sqrt(c.df(1) * c.df(2)), places=13)
        with self.assertRaises(ValueError): c.df(4)
        with self.assertRaises(ValueError): Curve(((0., 1.), (1., 0.)), 'invalid')

    def test_floating_telescoping_identity_and_basis(self):
        d = bootstrap_annual_par(.10, [.12, .13])
        p = bootstrap_annual_par(.11, [.13, .14])
        self.assertAlmostEqual(floating_note_pv(d, d, [1, 2, 3]), 1.0, places=12)
        self.assertGreater(floating_note_pv(p, d, [1, 2, 3]), 1.0)

    def test_negative_rates_do_not_force_decreasing_discount_factors(self):
        c = bootstrap_annual_par(-.01, [-.01])
        self.assertGreater(c.df(1), 1)

    def test_key_rate_sensitivity_converges_and_aggregates(self):
        c = bootstrap_annual_par(.10, [.12, .13])
        flows = [(1, 100.), (2, 100.), (3, 1100.)]
        a = key_rate_dv01(c, flows, 1e-4)
        b = key_rate_dv01(c, flows, 5e-5)
        exact_parallel = sum(t * cash * c.df(t) * 1e-4 for t, cash in flows)
        self.assertAlmostEqual(sum(r['dv01'] for r in b), exact_parallel, places=8)
        self.assertLess(abs(sum(r['dv01'] for r in b) - exact_parallel), abs(sum(r['dv01'] for r in a) - exact_parallel))


class ScenarioTests(unittest.TestCase):
    def test_currency_unit_scaling_preserves_multiperiod_ledger(self):
        scale = D('1000000')
        opening = BalanceSheet(*[D(v) * scale for v in ('200','800','0','900','0','100')])
        unused = D('150') * scale
        for reference in scenario_examples()['bank_path']:
            e = reference['events']
            rates = [D(e[k]) for k in ('loan_rate','cash_rate','deposit_rate','wholesale_rate')]
            cash = [D(e[k]) * scale for k in ('principal_repaid','new_draws','deposit_withdrawals','chargeoff','recovered_cash','operating_cash','distribution','collateral_posted')]
            p = Period(date.fromisoformat(reference['start']), date.fromisoformat(reference['end']), *rates, *cash)
            opening, result = step(opening, p, D('60') * scale, unused)
            unused -= D(result['replacement_funding'])
            self.assertLess(abs(opening.residual()), D('1e-20'))
            self.assertAlmostEqual(float(opening.equity / scale), float(reference['closing']['equity']), places=12)

    def test_every_period_reconciles_and_changes_following_costs(self):
        results = scenario_examples()['bank_path']
        self.assertAlmostEqual(float(results[0]['net_interest_income']), 60.5 * 31 / 365, places=12)
        self.assertEqual(D(results[0]['closing']['loans']), D(710))
        for row in results:
            self.assertLess(abs(D(row['balance_sheet_residual'])), D('1e-20'))
            self.assertGreaterEqual(D(row['closing']['cash']), D(60))
        self.assertGreater(D(results[1]['replacement_funding']), 0)
        self.assertGreater(D(results[2]['opening']['wholesale']), 0)

    def test_cash_is_not_equity_and_margin_is_not_expense(self):
        row = scenario_examples()['bank_path'][0]
        opening, closing = row['opening'], row['closing']
        self.assertEqual(D(closing['collateral_receivable']) - D(opening['collateral_receivable']), D(5))
        self.assertAlmostEqual(float(D(closing['equity']) - D(opening['equity'])), float(D(row['realised_profit']) - 1), places=12)

    def test_shortfall_fails_without_available_funding(self):
        bs = BalanceSheet(*map(D, ['10', '100', '0', '100', '0', '10']))
        p = Period(date(2026, 1, 1), date(2026, 2, 1), *map(D, ['0','0','0','0','0','0','100','0','0','0','0','0']))
        with self.assertRaises(ValueError): step(bs, p, D(0), D(50))

    def test_hazards_probability_mass_and_delayed_recovery(self):
        pd, survived = marginal_defaults([.1, .2])
        self.assertAlmostEqual(pd[1], .18)
        self.assertAlmostEqual(sum(pd) + survived, 1)
        r = scenario_examples()['separate_discounted_shortfall_case']
        expected = .1 * (1000 - 300 / 1.06 ** 2)
        self.assertAlmostEqual(r['expected_discounted_shortfall'], expected, places=10)
        with self.assertRaises(ValueError): marginal_defaults([1.1])

    def test_hedge_choice_obeys_cash_limit(self):
        r = constrained_hedge_example()
        self.assertLessEqual(r['selected']['collateral_cash'], r['cash_budget'])
        self.assertLess(sum(v*v for v in r['selected']['residual_pv01']), sum(v*v for v in r['before_pv01']))


if __name__ == '__main__':
    unittest.main()
