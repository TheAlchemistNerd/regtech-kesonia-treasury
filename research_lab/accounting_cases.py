"""Synthetic, pre-qualified IFRS 9 hedge-accounting journal examples.

Fair values and designation eligibility are inputs. No eligibility or journal
authorisation is inferred from a passing arithmetic check. Money is KES.
"""
from dataclasses import dataclass
from decimal import Decimal as D
import math


def journal(label, **signed_debits):
    entries = {key: D(str(value)) for key, value in signed_debits.items()}
    if any(not x.is_finite() for x in entries.values()):
        raise ValueError('Finite journal amounts required')
    if abs(sum(entries.values())) > D('0.00000001'):
        raise ValueError('Debits must equal credits')
    return {'event': label, 'signed_debits': {k: str(v) for k, v in entries.items()},
            'debit_credit_residual': str(sum(entries.values()))}


def cash_hedge_measure(derivative_gain, hypothetical_item_change):
    """Cumulative amounts since designation, for an offsetting relationship.

    The hypothetical item's sign is opposite the instrument; same-sign gains
    are rejected instead of treating their magnitudes as an economic offset.
    """
    derivative_gain, hypothetical_item_change = map(D, map(str, (derivative_gain, hypothetical_item_change)))
    if any(not x.is_finite() for x in (derivative_gain, hypothetical_item_change)):
        raise ValueError('Finite cumulative fair-value changes required')
    if derivative_gain * hypothetical_item_change > 0:
        raise ValueError('This scoped example requires offsetting changes')
    effective = min(abs(derivative_gain), abs(hypothetical_item_change))
    reserve = effective if derivative_gain >= 0 else -effective
    return {'derivative': derivative_gain, 'reserve': reserve,
            'ineffectiveness': derivative_gain - reserve}


@dataclass(frozen=True)
class Designation:
    version: str
    hedged_units: D
    hedge_units: D
    objective: str

    def rebalance(self, hedge_units, *, objective_unchanged, effectiveness_reviewed):
        hedge_units = D(str(hedge_units))
        if not objective_unchanged or not effectiveness_reviewed:
            raise ValueError('Rebalancing requires unchanged objective and prior measurement')
        if not hedge_units.is_finite() or hedge_units <= 0 or self.hedged_units <= 0:
            raise ValueError('Positive hedge quantities required')
        return Designation(self.version + '.rebalance', self.hedged_units, hedge_units, self.objective)


def discontinue_cash_hedge(reserve, *, forecast_expected):
    reserve = D(str(reserve))
    if not reserve.is_finite() or not isinstance(forecast_expected, bool):
        raise ValueError('Finite reserve and explicit forecast decision required')
    return {'retained_oci': str(reserve if forecast_expected else D(0)),
            'immediate_pl_reclassification': str(D(0) if forecast_expected else reserve),
            'reason': 'Forecast remains expected' if forecast_expected else 'Forecast is no longer expected'}


def fair_value_case():
    # Remaining contractual receipts: 50 in year 1 and 1,050 in year 2.
    # The supplied benchmark-only rate change is 5% -> 6%.
    value = D(50) / D('1.06') + D(1050) / D('1.06') ** 2
    loss = D(1000) - value
    derivative_gain = D(18)
    journals = [journal('Hedged benchmark loss', hedge_loss=loss, asset_adjustment=-loss),
                journal('Derivative fair-value gain', derivative=derivative_gain, hedge_gain=-derivative_gain),
                journal('Derivative settlement on discontinuation', cash=derivative_gain, derivative=-derivative_gain)]
    carrying = value
    roll = []
    for period, receipt in enumerate((D(50), D(1050)), 1):
        income = carrying * D('.06')
        next_value = carrying + income - receipt
        journals.append(journal(f'Effective interest after discontinuation, year {period}', asset_adjustment=income, interest_income=-income))
        journals.append(journal(f'Coupon/principal receipt, year {period}', cash=receipt, asset_adjustment=-receipt))
        roll.append({'year': period, 'opening_carrying': str(carrying), 'recalculated_eir': '.06',
                     'interest_income': str(income), 'receipt': str(receipt), 'closing_carrying': str(next_value)})
        carrying = next_value
    return {'adjusted_carrying_amount': str(value), 'hedged_item_loss': str(loss),
            'derivative_gain': '18', 'net_ineffectiveness_gain': str(derivative_gain - loss),
            'recalculated_eir': '.06', 'post_discontinuation_amortisation': roll,
            'terminal_carrying_residual': str(carrying), 'journals': journals}


def cash_flow_case():
    rows, journals = [], []
    prior = {'derivative': D(0), 'reserve': D(0), 'ineffectiveness': D(0)}
    for when, derivative, item in [('2027-03-31', 12, -10), ('2027-06-30', 17, -16), ('2027-09-30', 20, -19)]:
        now = cash_hedge_measure(derivative, item)
        delta = {key: now[key] - prior[key] for key in now}
        journals.append(journal('Remeasure ' + when, derivative=delta['derivative'],
                                oci_reserve=-delta['reserve'], ineffectiveness_gain=-delta['ineffectiveness']))
        rows.append({'date': when, 'hypothetical_item_change': str(item),
                     **{key: str(value) for key, value in now.items()},
                     'period_ineffectiveness_gain': str(delta['ineffectiveness'])})
        prior = now
    journals += [journal('Pay contractual interest', interest_expense=100, cash=-100),
                 journal('Settle derivative', cash=20, derivative=-20),
                 journal('Reclassify effective reserve with hedged interest', oci_reserve=19, interest_expense=-19)]
    return {'measurements': rows, 'journals': journals, 'gross_interest_expense': '100',
            'net_interest_expense_after_oci': '81', 'separate_ineffectiveness_gain': '1',
            'total_profit_or_loss_cost': '80', 'net_cash_cost': '80', 'ending_reserve': '0',
            'discontinued_at_june_forecast_expected': discontinue_cash_hedge(16, forecast_expected=True),
            'discontinued_at_june_forecast_not_expected': discontinue_cash_hedge(16, forecast_expected=False)}


def accounting_examples():
    original = Designation('D1', D(1000), D(1000), 'Manage benchmark cash-flow variability')
    changed = original.rebalance(900, objective_unchanged=True, effectiveness_reviewed=True)
    return {'units': 'KES; debit-positive signed journal lines; illustrative pre-qualified designations',
            'fair_value_hedge': fair_value_case(), 'cash_flow_hedge': cash_flow_case(),
            'separate_prospective_rebalancing_example': {
                'original': {'version': original.version, 'hedged_units': '1000', 'hedge_units': '1000'},
                'new': {'version': changed.version, 'hedged_units': '1000', 'hedge_units': '900'},
                'prior_ineffectiveness_preserved': True,
                'scope': 'Separate quantity/designation control; fair-value measurement after rebalancing requires a fresh instrument valuation.'}}
