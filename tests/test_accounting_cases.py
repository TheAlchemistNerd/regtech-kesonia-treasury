import unittest
from decimal import Decimal as D
from research_lab.accounting_cases import (accounting_examples, cash_hedge_measure,
    Designation, discontinue_cash_hedge, journal)


class AccountingCaseTests(unittest.TestCase):
    def test_all_journals_balance_and_cash_reconciles(self):
        result = accounting_examples()
        for name in ('fair_value_hedge', 'cash_flow_hedge'):
            for entry in result[name]['journals']:
                self.assertLessEqual(abs(sum(map(D, entry['signed_debits'].values()))), D('1e-8'))
        cash = result['cash_flow_hedge']
        self.assertEqual(cash['total_profit_or_loss_cost'], cash['net_cash_cost'])
        self.assertEqual(cash['ending_reserve'], '0')

    def test_fair_value_adjustment_amortises_at_recalculated_eir(self):
        fv = accounting_examples()['fair_value_hedge']
        self.assertLess(abs(D(fv['terminal_carrying_residual'])), D('1e-20'))
        self.assertLess(D(fv['net_ineffectiveness_gain']), 0)
        self.assertAlmostEqual(float(fv['adjusted_carrying_amount']), 50/1.06+1050/1.06**2)

    def test_lower_of_is_cumulative_and_underhedge_is_not_spurious_loss(self):
        self.assertEqual(cash_hedge_measure(8, -10)['ineffectiveness'], 0)
        self.assertEqual(cash_hedge_measure(-12, 10)['ineffectiveness'], -2)
        rows = accounting_examples()['cash_flow_hedge']['measurements']
        self.assertEqual(rows[1]['period_ineffectiveness_gain'], '-1')
        with self.assertRaises(ValueError): cash_hedge_measure(12, 10)
        with self.assertRaises(ValueError): cash_hedge_measure(float('nan'), 10)

    def test_discontinuation_and_rebalancing_are_distinct(self):
        self.assertEqual(discontinue_cash_hedge(16, forecast_expected=True)['retained_oci'], '16')
        self.assertEqual(discontinue_cash_hedge(16, forecast_expected=False)['immediate_pl_reclassification'], '16')
        d = Designation('D1', D(1000), D(1000), 'objective')
        with self.assertRaises(ValueError): d.rebalance(900, objective_unchanged=False, effectiveness_reviewed=True)
        self.assertEqual(d.hedge_units, D(1000))
        with self.assertRaises(ValueError): journal('unbalanced', cash=10, income=-9)
        with self.assertRaises(ValueError): discontinue_cash_hedge('NaN', forecast_expected=True)
