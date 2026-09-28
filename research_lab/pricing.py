"""Money-to-rate reconciliation and a narrowly defined dated cash-flow yield."""
from datetime import date
from decimal import Decimal as D, localcontext
import math


def margin_bridge(exposure_years: D, benchmark_income: D, fees: D,
                  external_funding: D, operating_cost: D, principal_loss: D,
                  capital_hurdle_money: D) -> dict:
    """Solve benchmark + k*H + fees - funding - cost - loss = hurdle.

    Every input except H is money for the SAME entity and horizon. H is the
    expected collectible interest-bearing balance integrated over year fractions.
    Principal loss excludes an interest shortfall already absent from income.
    No discounting, tax, regulatory capital or APR interpretation is implicit.
    """
    values = [exposure_years, benchmark_income, fees, external_funding, operating_cost, principal_loss, capital_hurdle_money]
    if any(not isinstance(v, D) or not v.is_finite() for v in values) or exposure_years <= 0:
        raise ValueError('Finite money inputs and positive currency-years required')
    with localcontext() as ctx:
        ctx.prec = 40
        charge = external_funding + operating_cost + principal_loss + capital_hurdle_money - fees - benchmark_income
        margin = charge / exposure_years
        income = benchmark_income + margin * exposure_years + fees
        before_capital = income - external_funding - operating_cost - principal_loss
        return {'exposure_currency_years': str(exposure_years), 'required_margin_rate': str(margin),
                'margin_income': str(charge), 'total_income_including_fees': str(income),
                'return_before_capital_hurdle': str(before_capital),
                'economic_surplus_after_hurdle': str(before_capital - capital_hurdle_money)}


def cashflow_yield(flows: list[tuple[date, float]]) -> dict:
    """One initial negative cash flow and later nonnegative receipts, ACT/365.

    Monotonicity ensures a unique root. Other sign patterns are rejected instead
    of silently picking among multiple IRRs. Not a statutory APR implementation.
    """
    if len(flows) < 2 or flows[0][1] >= 0 or any(c < 0 for _, c in flows[1:]):
        raise ValueError('Require one initial outflow followed by nonnegative receipts')
    if any(not math.isfinite(c) for _, c in flows) or sum(c for _, c in flows[1:]) <= 0:
        raise ValueError('Finite flows and a positive receipt required')
    if any(a[0] >= b[0] for a, b in zip(flows, flows[1:])):
        raise ValueError('Dates must be strictly increasing')
    anchor = flows[0][0]
    terms = [((day - anchor).days / 365, cash) for day, cash in flows]
    def npv(rate):
        return sum(cash * math.exp(-time * math.log1p(rate)) for time, cash in terms)
    low, high = -.999, 1.
    if npv(low) < 0:
        raise ValueError('Yield below declared numerical search domain')
    while npv(high) > 0 and high < 1e6:
        high = high * 2 + 1
    if npv(high) > 0:
        raise ValueError('Yield above declared numerical search domain')
    for iterations in range(200):
        midpoint = (low + high) / 2
        residual = npv(midpoint)
        if abs(residual) < 1e-8:
            return {'annual_effective_yield': midpoint, 'present_value_residual': residual,
                    'iterations': iterations + 1, 'day_basis': 'ACT/365'}
        if residual > 0:
            low = midpoint
        else:
            high = midpoint
    raise ArithmeticError('Cash-flow yield failed residual tolerance')


def pricing_examples() -> dict:
    result = margin_bridge(*map(D, ['1000000', '90000', '5000', '100000', '20000', '15000', '10000']))
    result['allocated_capital'] = '50000'
    result['one_year_pre_tax_raroc'] = str(D(result['return_before_capital_hurdle']) / D(50000))
    return {'margin_case': result,
            'fee_yield_case': cashflow_yield([(date(2026, 1, 1), -990000), (date(2027, 1, 1), 1140000)]),
            'fee_yield_contract': 'Synthetic KES1m, 14% one-year bullet interest, KES10k upfront fee; other fees/costs absent. Cash-flow yield is not labelled statutory APR.'}
