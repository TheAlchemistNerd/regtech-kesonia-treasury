"""Typed synthetic cash handoffs; optional frozen evidence from owning projects.

This fixture demonstrates interfaces and conservation. It is not a second
implementation of Mwendo's canonical waterfall or an IFRS 17 engine.
"""
from dataclasses import dataclass, asdict
from datetime import date
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path


@dataclass(frozen=True)
class EconomicQuantity:
    value: D
    unit: str
    currency: str
    entity: str
    claim: str
    period: str
    scenario: str
    source_version: str

    def __post_init__(self):
        if not isinstance(self.value, D) or not self.value.is_finite():
            raise ValueError('Finite Decimal value required; unknown is not zero')
        if any(not isinstance(v, str) or not v for k, v in asdict(self).items() if k != 'value'):
            raise ValueError('Every quantity requires complete dimensions')

    def add(self, other):
        left, right = asdict(self), asdict(other)
        if any(left[k] != right[k] for k in left if k != 'value'):
            raise ValueError('Incompatible quantity dimensions')
        return EconomicQuantity(self.value + other.value, **{k: v for k, v in left.items() if k != 'value'})


def cash_ledger(opening, events):
    balances = {k: D(str(v)) for k, v in opening.items()}
    if not balances or any(not v.is_finite() or v < 0 for v in balances.values()):
        raise ValueError('Finite nonnegative opening balances required')
    total = sum(balances.values())
    seen, rows = {}, []
    previous_date = ''
    for event in events:
        when, identity, payer, recipient, amount, purpose = event
        date.fromisoformat(when)
        payload = tuple(event)
        if identity in seen:
            if seen[identity] != payload:
                raise ValueError('Changed payload under the same event ID')
            continue
        if when < previous_date or payer == recipient:
            raise ValueError('Ordered events and distinct entities required')
        amount = D(str(amount))
        if not amount.is_finite() or amount <= 0:
            raise ValueError('Positive finite cash amount required')
        if payer not in balances or recipient not in balances:
            raise ValueError('Unknown entity')
        if balances[payer] < amount:
            raise ValueError('Unfunded payment; no silent cash creation')
        balances[payer] -= amount
        balances[recipient] += amount
        if sum(balances.values()) != total:
            raise ArithmeticError('Inter-entity cash conservation failed')
        rows.append({'date': when, 'event_id': identity, 'payer': payer, 'recipient': recipient,
                     'amount': str(amount), 'purpose': purpose,
                     'balances': {k: str(v) for k, v in balances.items()}, 'cash_residual': '0'})
        seen[identity] = payload
        previous_date = when
    return {'rows': rows, 'closing': {k: str(v) for k, v in balances.items()}, 'cash_residual': '0'}


def connected_finance_case():
    # Same borrower cash as Underwrite's on-time 60-day reference; SPV funding
    # and originator costs below are new, explicit interface assumptions.
    opening = {'borrower': 250000, 'bank_originator': 600000, 'spv': 0,
               'class_a': 375000, 'class_b': 75000, 'class_c': 60000,
               'customers': 1000000, 'suppliers': 0, 'servicer': 0,
               'bank_operations': 0, 'tax_authority': 0, 'bank_parent': 0}
    events = [
        ('2026-10-01', 'A-fund', 'class_a', 'spv', 375000, 'Class A asset funding'),
        ('2026-10-01', 'B-fund', 'class_b', 'spv', 75000, 'Class B asset funding'),
        ('2026-10-01', 'C-fund', 'class_c', 'spv', 60000, '50,000 Class C asset funding plus 10,000 funded reserve'),
        ('2026-10-01', 'loan', 'bank_originator', 'borrower', 500000, 'Borrower draw; bank loan asset initially recognised'),
        ('2026-10-01', 'sale', 'spv', 'bank_originator', 500000, 'Assumed transfer at par; accounting derecognition requires separate assessment'),
        ('2026-10-01', 'fee', 'borrower', 'bank_originator', 10000, 'Originator fee retained under assumed contract'),
        ('2026-10-01', 'customer-1', 'customers', 'borrower', 200000, 'Trading receipts'),
        ('2026-10-01', 'stock', 'borrower', 'suppliers', 600000, 'Stock/operating payment'),
        ('2026-10-31', 'operating-1', 'borrower', 'suppliers', 120000, 'Operating payment'),
        ('2026-11-30', 'customer-2', 'customers', 'borrower', 800000, 'Trading receipts'),
        ('2026-11-30', 'operating-2', 'borrower', 'suppliers', 100000, 'Operating payment'),
        ('2026-11-30', 'debt', 'borrower', 'spv', 515000, '500,000 principal and 15,000 interest to claim holder'),
        ('2026-11-30', 'servicing', 'spv', 'servicer', 2000, 'Senior servicing fee'),
        ('2026-11-30', 'coupon-A', 'spv', 'class_a', 6000, 'Assumed Class A coupon money'),
        ('2026-11-30', 'coupon-B', 'spv', 'class_b', 1500, 'Assumed Class B coupon money'),
        ('2026-11-30', 'principal-A', 'spv', 'class_a', 375000, 'Class A repayment'),
        ('2026-11-30', 'principal-B', 'spv', 'class_b', 75000, 'Class B repayment'),
        ('2026-11-30', 'principal-C', 'spv', 'class_c', 50000, 'Class C asset capital repayment'),
        ('2026-11-30', 'residual', 'spv', 'class_c', 15500, '10,000 reserve release plus 5,500 residual after senior claims; no remaining pool'),
        ('2026-11-30', 'bank-cost', 'bank_originator', 'bank_operations', 8000, 'Originator operating cost'),
        ('2026-11-30', 'bank-tax', 'bank_originator', 'tax_authority', 600, 'Assumed 30% on 2,000 fee contribution'),
        ('2026-12-15', 'permitted-remittance', 'bank_originator', 'bank_parent', 800, 'After 600 retained earnings under assumed distribution policy'),
    ]
    result = cash_ledger(opening, events)
    result['economics'] = {'borrower_finance_cost': '25000', 'borrower_closing_cash': '405000',
        'originator_fee': '10000', 'spv_loan_interest': '15000', 'spv_residual_after_cost_and_coupons': '5500',
        'originator_after_tax_profit': '1400', 'originator_retained_profit': '600', 'parent_remittance': '800',
        'class_c_distribution': '65500', 'class_c_return_of_capital': '60000', 'class_c_profit_before_investor_tax': '5500'}
    result['scope'] = 'Interface example, all KES; borrower assumptions reused; small 75/15/10 asset stack plus separately funded reserve. No bank regulatory capital or legal true-sale conclusion inferred.'
    return result


def refund_case():
    # Premium 1,200, one-year coverage, cancellation at end of month 3.
    # Pro-rata refund 900 is an elected contractual assumption, accepted then
    # settled at a later date. Service allocation is not IFRS17 revenue.
    return {'contract_premium': '1200', 'assumed_service_allocation_3_of_12_months': '300',
            'accepted_refund': '900', 'loan_before_refund': '1000',
            'events': [
                {'date': '2027-03-31', 'event': 'cancellation_and_refund_acceptance',
                 'insurer_refund_payable': '900', 'lender_collection_right': '900',
                 'cash_received_by_spv': '0', 'loan_principal_outstanding': '1000'},
                {'date': '2027-04-15', 'event': 'insurer_settlement_to_authorised_spv_account',
                 'insurer_refund_payable': '0', 'lender_collection_right': '0',
                 'cash_received_by_spv': '900', 'loan_principal_outstanding': '100'}],
            'cash_events': cash_ledger({'insurer': 1200, 'spv': 0}, [
                ('2027-04-15', 'refund-1', 'insurer', 'spv', 900, 'Settlement extinguishes the accepted right')]),
            'principal_allocation_residual': '0',
            'scope': 'Cash and rights interface only. Insurer IFRS17 contract grouping, LRC/LIC, onerous measurement, claims and journals remain with the insurance accounting model.'}


def owner_case():
    normalised = D(1590000) - D(300000) - D(180000) - D(120000)
    unrestricted_cash, near_claims, buffer = D(200000), D(80000), D(100000)
    parent_day_early = D(100) - D(300)
    parent_after_late_remittance = parent_day_early + D(800)
    parent_ledger = cash_ledger({'parent':100, 'bridge_lender':200, 'bank_remittance':800, 'parent_creditor':0}, [
        ('2026-12-01','bridge-draw','bridge_lender','parent',200,'Explicit temporary funding'),
        ('2026-12-01','parent-bill','parent','parent_creditor',300,'Dated obligation'),
        ('2026-12-15','net-remittance','bank_remittance','parent',800,'Already net of bank tax/cost/retention'),
        ('2026-12-15','bridge-repay','parent','bridge_lender',200,'Assumed zero-fee temporary bridge repayment')])
    return {'normalisation': {'reported_owner_benefit': '1590000', 'replacement_labour': '300000',
             'maintenance': '180000', 'required_working_capital': '120000', 'normalised_earning_power': str(normalised)},
            'business_distribution_capacity_today': str(max(D(0), unrestricted_cash-near_claims-buffer)),
            'parent_2026_12_01_cash_before_bridge': str(parent_day_early),
            'parent_2026_12_15_cash_after_remittance_if_200_bridge_available': str(parent_after_late_remittance),
            'required_temporary_parent_financing': '200',
            'dated_parent_cash_ledger': parent_ledger,
            'scope': 'The 800 remittance is already net of bank costs, tax and retention. Positive eventual cash does not fund the earlier 200 shortfall; bridge repayment reduces the later 800 receipt.'}


def cross_project_snapshot():
    path = Path(__file__).parent / 'data/cross_project_reference_2026-10-01.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'status': 'No frozen snapshot supplied'}


def connected_examples():
    q = EconomicQuantity(D(100), 'currency', 'KES', 'originator', 'fee', '2026-10-01/2026-11-30', 'connected-base', 'fixture-v1')
    return {'typed_quantity': {k: str(v) for k, v in asdict(q).items()},
            'connected_finance': connected_finance_case(), 'refund_timing': refund_case(),
            'owner_and_parent': owner_case(), 'owning_project_evidence': cross_project_snapshot()}
