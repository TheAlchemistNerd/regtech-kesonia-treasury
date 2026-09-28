import unittest
from datetime import date
from decimal import Decimal as D
from research_lab.pricing import margin_bridge, cashflow_yield, pricing_examples

class PricingTests(unittest.TestCase):
    def test_money_to_margin_reconciles_and_capital_not_charged_twice(self):
        r = pricing_examples()['margin_case']
        self.assertEqual(D(r['required_margin_rate']), D('.05'))
        self.assertEqual(D(r['return_before_capital_hurdle']), D(10000))
        self.assertEqual(D(r['one_year_pre_tax_raroc']), D('.2'))
        self.assertEqual(D(r['economic_surplus_after_hurdle']), D(0))

    def test_unfunded_exposure_denominator_fails(self):
        with self.assertRaises(ValueError): margin_bridge(*map(D, ['0', '90', '5', '100', '20', '15', '10']))

    def test_fee_yield_against_direct_one_year_solution(self):
        r = pricing_examples()['fee_yield_case']
        self.assertAlmostEqual(r['annual_effective_yield'], 114 / 99 - 1, places=12)
        self.assertLess(abs(r['present_value_residual']), 1e-8)

    def test_multi_sign_irr_rejected(self):
        with self.assertRaises(ValueError):
            cashflow_yield([(date(2026,1,1), -100), (date(2027,1,1), 230), (date(2028,1,1), -132)])

if __name__ == '__main__': unittest.main()
