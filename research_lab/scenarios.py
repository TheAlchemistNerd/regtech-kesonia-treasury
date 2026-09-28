"""Separate cash, profit, discounted shortfall and value-risk teaching cases."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal as D, localcontext
import math


@dataclass(frozen=True)
class BalanceSheet:
    cash: D
    loans: D
    collateral_receivable: D
    deposits: D
    wholesale: D
    equity: D

    def residual(self) -> D:
        # Preserve ledger precision even when callers use Python's default context.
        with localcontext() as ctx:
            ctx.prec = 40
            return self.cash + self.loans + self.collateral_receivable - self.deposits - self.wholesale - self.equity


@dataclass(frozen=True)
class Period:
    start: date
    end: date
    loan_rate: D
    cash_rate: D
    deposit_rate: D
    wholesale_rate: D
    principal_repaid: D
    new_draws: D
    deposit_withdrawals: D
    chargeoff: D
    recovered_cash: D
    operating_cash: D
    distribution: D
    collateral_posted: D


def step(opening: BalanceSheet, p: Period, minimum_cash: D, unused_facility: D) -> tuple[BalanceSheet, dict]:
    """Simple synthetic balance sheet; interest on opening balances, end-period events.

    All scheduled interest is received/paid. Charge-off is recognised at period
    end; recovered cash relates to balances already charged off (including the
    current period). Posted collateral is an asset, not an expense. Replacement
    funding is drawn at period end and starts accruing next period. The model
    excludes impairment allowances, taxes, fair-value accounting and regulatory
    capital: it is a realised cash/equity bridge, not IFRS reporting software.
    """
    values = list(opening.__dict__.values()) + [v for v in p.__dict__.values() if isinstance(v, D)] + [minimum_cash, unused_facility]
    if any(not v.is_finite() for v in values) or abs(opening.residual()) > D('1e-20'):
        raise ValueError('Finite, balanced opening ledger required')
    if p.end <= p.start or minimum_cash < 0 or unused_facility < 0:
        raise ValueError('Invalid period or funding limit')
    movements = [p.principal_repaid, p.new_draws, p.deposit_withdrawals, p.chargeoff,
                 p.recovered_cash, p.operating_cash, p.distribution, p.collateral_posted]
    if any(v < 0 for v in movements):
        raise ValueError('Movements are nonnegative, with signs determined by event type')
    if p.principal_repaid > opening.loans or p.deposit_withdrawals > opening.deposits:
        raise ValueError('Cannot repay or withdraw more than outstanding')
    with localcontext() as ctx:
        ctx.prec = 40
        dt = D((p.end - p.start).days) / 365
        income = (opening.loans * p.loan_rate + opening.cash * p.cash_rate) * dt
        expense = (opening.deposits * p.deposit_rate + opening.wholesale * p.wholesale_rate) * dt
        nii = income - expense
        profit = nii - p.chargeoff + p.recovered_cash - p.operating_cash
        provisional_cash = (opening.cash + nii + p.principal_repaid - p.new_draws - p.deposit_withdrawals
                            + p.recovered_cash - p.operating_cash - p.distribution - p.collateral_posted)
        funding = max(D(0), minimum_cash - provisional_cash)
        if funding > unused_facility:
            raise ValueError('Unfunded cash shortfall exceeds evidenced facility limit')
        loans = opening.loans - p.principal_repaid + p.new_draws - p.chargeoff
        if loans < 0:
            raise ValueError('Charge-off exceeds gross loans')
        closing = BalanceSheet(provisional_cash + funding, loans,
            opening.collateral_receivable + p.collateral_posted,
            opening.deposits - p.deposit_withdrawals, opening.wholesale + funding,
            opening.equity + profit - p.distribution)
        if abs(closing.residual()) > D('1e-20'):
            raise ArithmeticError('Closing balance sheet does not reconcile')
        return closing, {'start': p.start.isoformat(), 'end': p.end.isoformat(), 'days': (p.end - p.start).days,
                         'opening': {k: str(v) for k, v in opening.__dict__.items()},
                         'interest_received': str(income), 'interest_paid': str(expense),
                         'net_interest_income': str(nii), 'realised_profit': str(profit),
                         'replacement_funding': str(funding), 'cash_before_replacement': str(provisional_cash),
                         'closing': {k: str(v) for k, v in closing.__dict__.items()},
                         'balance_sheet_residual': str(closing.residual()),
                         'events': {k: str(v) for k, v in p.__dict__.items() if k not in ('start', 'end')}}


def marginal_defaults(hazards: list[float]) -> tuple[list[float], float]:
    survival = 1.0
    events = []
    for hazard in hazards:
        if not math.isfinite(hazard) or not 0 <= hazard <= 1:
            raise ValueError('Conditional hazards must lie between zero and one')
        events.append(survival * hazard)
        survival *= 1 - hazard
    return events, survival


def discounted_shortfall(report_date: date, contractual: list[tuple[date, float]],
                         scenarios: list[tuple[float, list[tuple[date, float]]]], annual_eir: float) -> dict:
    """Scenario-weighted shortfalls in a specified original-EIR teaching case.

    Stage, default definition, SICR and floating-rate EIR updates are inputs to
    the accounting policy, not inferred by this arithmetic helper.
    """
    if not math.isfinite(annual_eir) or annual_eir <= -1:
        raise ValueError('Annual EIR must exceed -100%')
    if not scenarios or abs(sum(p for p, _ in scenarios) - 1) > 1e-12:
        raise ValueError('Mutually exclusive exhaustive scenarios must sum to one')
    if any(not math.isfinite(p) or not 0 <= p <= 1 for p, _ in scenarios):
        raise ValueError('Invalid scenario probability')
    def pv(flows):
        if any(t < report_date or not math.isfinite(cash) for t, cash in flows):
            raise ValueError('Invalid future cash flow')
        return sum(cash / (1 + annual_eir) ** ((day - report_date).days / 365) for day, cash in flows)
    contract_pv = pv(contractual)
    expected_pv = sum(probability * pv(flows) for probability, flows in scenarios)
    return {'contractual_present_value': contract_pv, 'expected_receipts_present_value': expected_pv,
            'expected_discounted_shortfall': contract_pv - expected_pv, 'annual_eir': annual_eir}


def constrained_hedge_example() -> dict:
    """Exhaustive finite choice on TWO sensitivity axes and a cash budget.

    Hypothetical two-node PV01 vectors in currency/bp; risk reduction is first
    order. The collateral cash requirement is an assumption, not a swap price
    or margin model. No dealer quotations, capital relief or hedge accounting.
    """
    asset = (800.0, 1200.0)
    instruments = [(100.0, 10.0), (10.0, 200.0)]
    choices = []
    for short_units in range(11):
        for long_units in range(11):
            residual = tuple(asset[i] - short_units * instruments[0][i] - long_units * instruments[1][i] for i in range(2))
            cost = short_units * 100 + long_units * 200
            cash = short_units * 500 + long_units * 1500
            if cash > 10000:
                continue
            # Nondimensionalise both terms; the relative policy weight is explicit.
            pv01_scale = 1000.0  # currency per basis point
            cost_scale = 1000.0  # currency
            cost_penalty_weight = .001
            objective = sum((v / pv01_scale) ** 2 for v in residual) + cost_penalty_weight * cost / cost_scale
            choices.append({'short_units': short_units, 'long_units': long_units,
                            'residual_pv01': residual, 'cost': cost, 'collateral_cash': cash,
                            'objective': objective})
    best = min(choices, key=lambda r: (r['objective'], r['cost'], r['short_units'], r['long_units']))
    return {'before_pv01': asset, 'cash_budget': 10000, 'feasible_choices': len(choices), 'selected': best,
            'objective_note': 'Dimensionless objective = sum((residual PV01 / 1000 currency-per-bp)^2) + 0.001 * cost / 1000 currency. Relative weights are illustrative policy choices, not universal economic utility.'}


def scenario_examples() -> dict:
    opening = BalanceSheet(*map(D, ['200', '800', '0', '900', '0', '100']))
    periods = [
        Period(date(2026, 1, 1), date(2026, 2, 1), *map(D, ['.10', '.06', '.035', '.10', '80', '20', '90', '30', '5', '2', '1', '5'])),
        Period(date(2026, 2, 1), date(2026, 3, 1), *map(D, ['.10', '.08', '.045', '.11', '70', '30', '180', '10', '3', '2', '0', '8'])),
        Period(date(2026, 3, 1), date(2026, 4, 1), *map(D, ['.10', '.08', '.045', '.11', '60', '40', '80', '15', '4', '2', '0', '0'])),
    ]
    rows = []
    unused = D('150')
    for period in periods:
        opening, row = step(opening, period, D('60'), unused)
        unused -= D(row['replacement_funding'])
        rows.append(row)
    shortfall = discounted_shortfall(date(2026, 1, 1), [(date(2027, 1, 1), 1060)],
        [(.9, [(date(2027, 1, 1), 1060)]), (.1, [(date(2028, 1, 1), 300)])], .06)
    return {'scenario_label': 'Synthetic bank, KES millions; cash-flow timing and opening-balance interest explicitly assumed',
            'bank_path': rows, 'unused_facility': str(unused),
            'separate_discounted_shortfall_case': shortfall,
            'hazards_not_marginals': {'hazards': [.1, .2], 'result': marginal_defaults([.1, .2])},
            'separate_hedge_choice_case': constrained_hedge_example()}
