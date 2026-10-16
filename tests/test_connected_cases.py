import unittest
from decimal import Decimal as D
from research_lab.connected_cases import EconomicQuantity, cash_ledger, connected_examples


class ConnectedTests(unittest.TestCase):
    def test_all_entities_conserve_cash_and_borrower_matches_reference(self):
        result = connected_examples()['connected_finance']
        self.assertEqual(result['closing']['borrower'], '405000')
        self.assertEqual(result['closing']['spv'], '0')
        self.assertEqual(result['closing']['class_c'], '65500')
        self.assertEqual(result['closing']['bank_originator'], '600600')
        self.assertTrue(all(r['cash_residual'] == '0' for r in result['rows']))
        economics = result['economics']
        self.assertEqual(D(economics['borrower_finance_cost']), D(economics['originator_fee'])+D(economics['spv_loan_interest']))

    def test_refund_acceptance_is_not_cash_or_second_recovery(self):
        r = connected_examples()['refund_timing']
        self.assertEqual(r['events'][0]['cash_received_by_spv'], '0')
        self.assertEqual(r['events'][-1]['loan_principal_outstanding'], '100')
        self.assertEqual(r['cash_events']['closing']['spv'], '900')

    def test_replay_and_overdraft_failures(self):
        event = ('2026-10-01','x','a','b',10,'purpose')
        self.assertEqual(cash_ledger({'a':10,'b':0}, [event,event])['closing']['b'], '10')
        with self.assertRaises(ValueError): cash_ledger({'a':9,'b':0}, [event])
        with self.assertRaises(ValueError): cash_ledger({'a':20,'b':0}, [event, (*event[:4],11,event[5])])
        with self.assertRaises(ValueError): cash_ledger({'a':'NaN','b':0}, [])
        with self.assertRaises(ValueError): cash_ledger({'a':-5,'b':0}, [])

    def test_owner_earnings_and_cash_are_different_endpoints(self):
        r = connected_examples()['owner_and_parent']
        self.assertEqual(r['normalisation']['normalised_earning_power'], '990000')
        self.assertEqual(r['business_distribution_capacity_today'], '20000')
        self.assertEqual(r['parent_2026_12_01_cash_before_bridge'], '-200')
        self.assertEqual(r['parent_2026_12_15_cash_after_remittance_if_200_bridge_available'], '600')
        self.assertEqual(r['dated_parent_cash_ledger']['closing']['parent'], '600')

    def test_incompatible_units_and_missing_metadata_rejected(self):
        q = EconomicQuantity(D(10),'currency','KES','a','loan','one-year','base','v1')
        self.assertEqual(q.add(q).value, D(20))
        with self.assertRaises(ValueError): q.add(EconomicQuantity(D(10),'annual_rate','KES','a','loan','one-year','base','v1'))
        with self.assertRaises(ValueError): EconomicQuantity(D(10),'currency','KES','','loan','one-year','base','v1')
