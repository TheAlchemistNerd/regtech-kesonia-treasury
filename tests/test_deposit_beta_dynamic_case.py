"""Independent identities, economic direction and limiting cases for the dynamic case."""
from copy import deepcopy
import math
import unittest
from research_lab.deposit_beta_dynamic_case.model import assumptions,run_case,source_models,static_bridge,reserve,pd_for_capacity,benchmark_schedule

class DynamicCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=assumptions();cls.fit=source_models()['fit']
        cls.cases={s:run_case(s,cfg=cls.cfg,fitted=cls.fit) for s in cls.cfg['scenarios']}

    def test_static_bridge_matches_independent_arithmetic(self):
        x=static_bridge()
        self.assertEqual(x['initial_nii'],8800000)
        self.assertEqual(x['repricing_gain'],1240000)
        self.assertEqual(x['replacement_cost'],584000)
        self.assertEqual(x['extra_expected_loss'],900000)
        self.assertEqual(x['net_change'],-244000)

    def test_all_period_accounting_identities(self):
        for result in self.cases.values():
            for r in result['monthly']:
                for k,v in r.items():
                    if k.endswith('_residual'):self.assertLess(abs(v),1e-5,(r['scenario'],r['month'],k))
                self.assertAlmostEqual(r['total_assets'],r['cash']+r['gross_loans']+r['workout_gross']+r['interest_receivable']-r['allowance'],places=6)

    def test_cash_is_independently_reconstructed(self):
        for result in self.cases.values():
            for r in result['monthly']:
                incoming=sum(r[k] for k in ('loan_interest_received','cash_interest','principal_received','recoveries','new_deposits','wholesale_issued'))
                outgoing=sum(r[k] for k in ('external_withdrawals','deposit_interest','wholesale_interest','wholesale_maturity','operating_cost','originations'))
                self.assertAlmostEqual(r['opening_cash']+incoming-outgoing,r['cash'],places=6)

    def test_allowance_and_writeoffs_are_not_double_counted(self):
        for result in self.cases.values():
            s=result['summary']
            self.assertAlmostEqual(s['impairment_expense'],s['closing_allowance']-s['opening_allowance']+s['writeoffs'],places=6)
            self.assertAlmostEqual(s['profit'],s['nii']-24*self.cfg['monthly_operating_cost']-s['impairment_expense'],places=6)
            self.assertAlmostEqual(s['closing_equity'],s['opening_equity']+s['profit'],places=6)

    def test_default_recovery_and_writeoff_timings(self):
        rows=self.cases['joint_stress']['monthly'];lag=self.cfg['recovery_lag_months']
        for i,r in enumerate(rows):
            transfer=rows[i-lag]['default_transfer'] if i>=lag else 0
            self.assertAlmostEqual(r['recoveries'],transfer*(1-self.cfg['lgd']),places=6)
            self.assertAlmostEqual(r['writeoffs'],transfer*self.cfg['lgd'],places=6)

    def test_original_cohort_depletes_without_new_money(self):
        rows=self.cases['rates_up']['monthly'];original=sum(x['balance'] for x in self.cfg['deposits'])
        for r in rows:
            original-=r['original_cohort_withdrawals']
            self.assertAlmostEqual(original,r['original_deposits_remaining'],places=5)
            self.assertLessEqual(original,r['deposits']+1e-7)

    def test_migration_is_internal_and_does_not_move_bank_cash(self):
        for r in self.cases['rates_up']['monthly']:
            self.assertGreaterEqual(r['internal_migration'],0)
            self.assertLess(abs(r['deposit_residual']),1e-6)

    def test_deposit_interest_matches_cohort_rate_and_opening_balance(self):
        for result in self.cases.values():
            for r in result['monthly']:
                expected=sum(d['opening']*d['paid_rate']*r['days']/365 for d in result['deposits'] if d['month']==r['month'])
                self.assertAlmostEqual(expected,r['deposit_interest'],places=6)

    def test_term_rate_remains_fixed_until_renewal(self):
        d=[x for x in self.cases['rates_up']['deposits'] if x['cohort_id']=='original_term']
        for row in d[:6]:self.assertAlmostEqual(row['paid_rate'],self.cfg['deposits'][2]['rate'])
        self.assertGreater(d[6]['paid_rate'],d[5]['paid_rate'])

    def test_repricing_lags_and_contract_resets(self):
        rows=self.cases['rates_up']['monthly']
        self.assertGreater(rows[3]['savings_rate'],rows[2]['savings_rate'])
        loans=[r for r in self.cases['rates_up']['loans'] if r['cohort_id']=='trade_0']
        self.assertFalse(loans[2]['reset']);self.assertTrue(loans[6]['reset'])
        self.assertGreater(loans[6]['loan_rate'],loans[2]['loan_rate'])

    def test_interest_receivable_separates_accrual_and_cash(self):
        rows=self.cases['baseline']['monthly']
        self.assertEqual(rows[0]['loan_interest_received'],0)
        for a,b in zip(rows,rows[1:]):self.assertAlmostEqual(a['loan_interest_accrued'],b['loan_interest_received'])
        s=self.cases['baseline']['summary']
        self.assertAlmostEqual(s['nii']-s['cash_nii'],s['closing_interest_receivable'],places=6)

    def test_lower_capacity_increases_pd_at_fixed_rate(self):
        a=pd_for_capacity(.03,1.2,1.2,4,0);b=pd_for_capacity(.03,.9,1.2,4,0)
        self.assertAlmostEqual(a,.03);self.assertGreater(b,a)
        self.assertGreater(self.cases['credit_stress']['summary']['default_transfer'],self.cases['baseline']['summary']['default_transfer'])

    def test_survival_and_declining_exposure_in_reserve(self):
        self.assertAlmostEqual(reserve(100,1,.12,.45),100*.45*(1-.88**(1/12)))
        self.assertLess(reserve(100,12,.12,.45),100*.12*.45)
        self.assertEqual(reserve(0,12,.12,.45),0)
        self.assertEqual(reserve(100,0,.12,.45),0)

    def test_funding_limit_constrains_lending(self):
        c=deepcopy(self.cfg);c['wholesale_limit']=self.cfg['opening_wholesale'];c['new_lending_per_month']=10000000
        x=run_case('joint_stress',cfg=c,fitted=self.fit)
        self.assertGreater(x['summary']['lending_deferred'],0)
        self.assertLessEqual(x['summary']['peak_wholesale'],c['wholesale_limit']+1e-6)
        for r in x['monthly']:self.assertLessEqual(r['originations'],r['lending_requested'])

    def test_capital_limit_constrains_new_lending(self):
        c=deepcopy(self.cfg);c['capital_floor']=.20
        x=run_case('joint_stress',cfg=c,fitted=self.fit)
        self.assertGreater(x['summary']['lending_deferred'],0)
        self.assertEqual(x['monthly'][0]['originations'],0)

    def test_prefunding_is_explicit_cash_and_liability(self):
        x=run_case('joint_stress','term_prefunding',self.cfg,self.fit)
        self.assertEqual(x['events'][0]['month'],2)
        self.assertEqual(x['events'][0]['amount'],10000000)
        self.assertLess(x['summary']['maximum_reconciliation_error'],1e-5)

    def test_paired_retention_changes_cost_and_volume(self):
        x=run_case('joint_stress','retain_deposits',self.cfg,self.fit)
        standard=self.cases['joint_stress']['summary']
        self.assertLess(x['summary']['external_withdrawals'],standard['external_withdrawals'])
        self.assertGreater(x['summary']['deposit_interest'],standard['deposit_interest'])

    def test_zero_lending_is_a_true_runoff_book(self):
        c=deepcopy(self.cfg);c['new_lending_per_month']=0
        x=run_case(cfg=c,fitted=self.fit)
        self.assertEqual(x['summary']['originations'],0)
        self.assertLess(x['summary']['closing_gross_loans'],self.cases['baseline']['summary']['closing_gross_loans'])

    def test_calendar_and_leap_year(self):
        c=deepcopy(self.cfg);c['start_date']='2028-01-01';c['months']=2
        x=benchmark_schedule(c,c['scenarios']['baseline'])
        self.assertEqual([r['days'] for r in x],[31,29])

    def test_deterministic_repeat(self):
        a=run_case('rates_down',cfg=self.cfg,fitted=self.fit)
        self.assertEqual(a,self.cases['rates_down'])

    def test_invalid_inputs_fail_early(self):
        for k,v in [('months',0),('lgd',1.1),('cash_floor',-1),('interest_settlement_lag_months',4),('market_rate',float('nan'))]:
            c=deepcopy(self.cfg);c[k]=v
            with self.assertRaises(ValueError):run_case(cfg=c,fitted=self.fit)

if __name__=='__main__':unittest.main()
