"""Deterministic synthetic option, priced hedge and collateral teaching cases.

No market observations or empirical borrower calibration are implied. All monetary
amounts are KES; rates are annual decimals. Importing this module performs no work.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
import math


def _finite(*values):
    if not all(math.isfinite(v) for v in values):
        raise ValueError('Finite numeric inputs required')


@dataclass(frozen=True)
class RateTree:
    dt: float
    rates: tuple[tuple[float, ...], ...]
    state_prices: tuple[tuple[float, ...], ...]
    input_discount_factors: tuple[float, ...]


def calibrate_rate_tree(discounts, dt=1 / 12, sigma=.015):
    """Fit every discount factor using additive binomial rates and Q branch p=1/2.

    Rates at i,j are a_i+(2j-i)*sigma*sqrt(dt). The time-dependent shift a_i
    is solved analytically from discounted state prices. Volatility is assumed.
    """
    discounts = tuple(discounts)
    _finite(dt, sigma, *discounts)
    if dt <= 0 or sigma < 0 or len(discounts) < 2 or discounts[0] != 1:
        raise ValueError('Positive dt, nonnegative sigma, and D(0)=1 required')
    if min(discounts) <= 0:
        raise ValueError('Discount factors must be positive')
    q, rates, state = [1.0], [], [(1.0,)]
    for i, target in enumerate(discounts[1:]):
        offsets = [(2 * j - i) * sigma * math.sqrt(dt) for j in range(i + 1)]
        a = math.log(sum(qj * math.exp(-o * dt) for qj, o in zip(q, offsets)) / target) / dt
        row = tuple(a + o for o in offsets)
        nxt = [0.0] * (i + 2)
        for j, (qj, rate) in enumerate(zip(q, row)):
            discounted = .5 * qj * math.exp(-rate * dt)
            nxt[j] += discounted
            nxt[j + 1] += discounted
        rates.append(row)
        state.append(tuple(nxt))
        q = nxt
    return RateTree(dt, tuple(rates), tuple(state), discounts)


def cpr_to_smm(cpr):
    _finite(cpr)
    if not 0 <= cpr <= 1:
        raise ValueError('CPR must lie in [0,1]')
    return 1 - (1 - cpr) ** (1 / 12)


def scheduled_principal_fraction(coupon, remaining_months):
    """Share of opening balance amortized this month for identical surviving loans."""
    _finite(coupon)
    if coupon < 0 or not isinstance(remaining_months, int) or remaining_months <= 0:
        raise ValueError('Nonnegative coupon and positive integer term required')
    monthly = coupon / 12
    payment = 1 / remaining_months if monthly == 0 else monthly / (1 - (1 + monthly) ** -remaining_months)
    return min(1.0, max(0.0, payment - monthly))


def mortgage_pool(tree, principal=1_000_000.0, coupon=.14, spread=0.0,
                  base_cpr=.04, response=6.0, refinance_markup=.025, cpr_cap=.60):
    """Exact node aggregation of path-dependent homogeneous pool balances.

    Prepayment occurs after scheduled principal at the period end, using the
    rate known at its start. CPR is an explicit valuation-measure assumption.
    Separate probability-weighted and discounted balances preserve rate/balance
    dependence; discounting average cashflows at average rates is not used.
    """
    _finite(principal, coupon, spread, base_cpr, response, refinance_markup, cpr_cap)
    if principal <= 0 or coupon < 0 or response < 0 or not 0 <= base_cpr <= cpr_cap <= 1:
        raise ValueError('Invalid mortgage/policy inputs')
    if abs(tree.dt - 1 / 12) > 1e-14:
        raise ValueError('Mortgage schedule requires monthly tree')
    expected, discounted = [principal], [principal]
    pv, rows = 0.0, []
    months = len(tree.rates)
    for i, rates in enumerate(tree.rates):
        sched = scheduled_principal_fraction(coupon, months - i)
        enext, dnext = [0.0] * (i + 2), [0.0] * (i + 2)
        row = dict(month=i + 1, opening_expected_balance=sum(expected), interest=0.0,
                   scheduled_principal=0.0, prepayment=0.0, discounted_cash=0.0)
        for j, rate in enumerate(rates):
            cpr = min(cpr_cap, base_cpr + response * max(coupon - (rate + refinance_markup), 0))
            prepay = (1 - sched) * cpr_to_smm(cpr)
            residual = max(0.0, 1 - sched - prepay)
            disc = math.exp(-(rate + spread) * tree.dt)
            cash_fraction = coupon / 12 + sched + prepay
            row['interest'] += expected[j] * coupon / 12
            row['scheduled_principal'] += expected[j] * sched
            row['prepayment'] += expected[j] * prepay
            row['discounted_cash'] += discounted[j] * cash_fraction * disc
            for k in (j, j + 1):
                enext[k] += .5 * expected[j] * residual
                dnext[k] += .5 * discounted[j] * residual * disc
        row['closing_expected_balance'] = sum(enext)
        row['principal_reconciliation_residual'] = row['opening_expected_balance'] - row['scheduled_principal'] - row['prepayment'] - row['closing_expected_balance']
        pv += row['discounted_cash']
        rows.append(row)
        expected, discounted = enext, dnext
    return {'pv': pv, 'monthly_cashflows_under_Q': rows,
            'final_expected_balance': sum(expected),
            'expected_principal_paid': sum(r['scheduled_principal'] + r['prepayment'] for r in rows)}


def solve_oas(tree, target_price, lower=-.05, upper=.20, price_tolerance=1e-7, **pool_inputs):
    """Bracketed bisection with explicit failure; output spread is annual decimal."""
    _finite(target_price, lower, upper, price_tolerance)
    if target_price <= 0 or lower >= upper or price_tolerance <= 0 or 'spread' in pool_inputs:
        raise ValueError('Positive target/tolerance and increasing spread bracket required')
    def price(s):
        return mortgage_pool(tree, spread=s, **pool_inputs)['pv']
    p_low, p_high = price(lower), price(upper)
    if not p_high <= target_price <= p_low:
        raise ValueError('Target price lies outside the explicit spread bracket')
    for iteration in range(1, 101):
        middle = (lower + upper) / 2
        value = price(middle)
        if abs(value - target_price) <= price_tolerance:
            return {'spread': middle, 'spread_bp': middle * 10_000, 'model_price': value,
                    'target_price': target_price, 'price_residual': value - target_price,
                    'iterations': iteration}
        if value > target_price:
            lower = middle
        else:
            upper = middle
    raise ArithmeticError('OAS bisection did not meet the price tolerance')


def optimal_mortgage_value(tree, principal=1_000_000.0, coupon=.14, allow_prepayment=True):
    """Separate frictionless borrower-exercise limit; call at start of months 2..N.

    Homogeneous scheduled balances are deterministic for surviving whole loans.
    The lender receives min(continuation value, outstanding par) at call dates.
    No immediate time-zero refinancing, credit default, fees or borrower frictions.
    """
    _finite(principal, coupon)
    if principal <= 0 or coupon < 0 or abs(tree.dt - 1 / 12) > 1e-14:
        raise ValueError('Positive principal, nonnegative coupon and monthly tree required')
    months = len(tree.rates)
    balances, cash = [principal], []
    for i in range(months):
        fraction = scheduled_principal_fraction(coupon, months - i)
        cash.append(balances[-1] * (coupon / 12 + fraction))
        balances.append(balances[-1] * (1 - fraction))
    values, exercise = [0.0] * (months + 1), []
    for i in reversed(range(months)):
        nxt = []
        for j, rate in enumerate(tree.rates[i]):
            continuation = math.exp(-rate * tree.dt) * (cash[i] + .5 * (values[j] + values[j + 1]))
            call = allow_prepayment and i > 0 and continuation > balances[i]
            nxt.append(min(continuation, balances[i]) if allow_prepayment and i > 0 else continuation)
            if call:
                exercise.append({'month_start': i + 1, 'up_moves': j, 'outstanding_par': balances[i],
                                 'continuation_value': continuation})
        values = nxt
    return {'pv': values[0], 'exercise_node_count': len(exercise), 'exercise_nodes': exercise}


def _discount(t, zero=.085, parallel=0.0, slope=0.0):
    return math.exp(-(zero + parallel + slope * (t - 3) / 3) * t)


def swap_pv(tenor, notional, fixed_rate, discount_shift=0.0, projection_shift=0.0, slope=0.0):
    """Annual pay-fixed/receive-floating swap; synthetic continuous zero curves.

    Projection baseline 9%, discount baseline 8.5%; t in years. Coupon accruals
    are one year. No principal exchange. Curves are fully specified functions.
    """
    _finite(notional, fixed_rate, discount_shift, projection_shift, slope)
    if not isinstance(tenor, int) or tenor <= 0 or notional < 0:
        raise ValueError('Positive integer tenor and nonnegative notional required')
    result = 0.0
    for t in range(1, tenor + 1):
        def dp(s):
            return _discount(s, zero=.09, parallel=projection_shift, slope=slope)
        forward = dp(t - 1) / dp(t) - 1
        result += notional * (forward - fixed_rate) * _discount(t, parallel=discount_shift, slope=slope)
    return result


def par_swap_rate(tenor):
    annuity = sum(_discount(t) for t in range(1, tenor + 1))
    return swap_pv(tenor, 1, 0) / annuity


def bond_pv(parallel=0.0, slope=0.0):
    return sum((110_000 + (1_000_000 if t == 3 else 0)) * _discount(t, parallel=parallel, slope=slope) for t in range(1, 4))


def finite_difference_risk(price, bump=1e-4):
    _finite(bump)
    if bump <= 0:
        raise ValueError('Positive sensitivity bump required')
    base, up, down = price(0), price(bump), price(-bump)
    return {'pv': base, 'd_pv_per_bp': (up - down) / (2 * bump) * 1e-4,
            'second_derivative_kes_per_rate_squared': (up - 2 * base + down) / bump ** 2,
            'second_order_pnl_at_100bp': .5 * (up - 2 * base + down) / bump ** 2 * .01 ** 2}


def hedge_selection_case():
    scenarios = [dict(label='parallel_up_100bp', discount=.01, projection=.01, slope=0),
                 dict(label='parallel_down_100bp', discount=-.01, projection=-.01, slope=0),
                 dict(label='projection_basis_up_100bp', discount=0, projection=.01, slope=0),
                 dict(label='curve_twist', discount=0, projection=0, slope=.01)]
    base = bond_pv()
    fixed = {t: par_swap_rate(t) for t in (2, 5)}
    candidates = []
    for n2 in (0, 250_000, 500_000, 750_000, 1_000_000):
        for n5 in (0, 250_000, 500_000, 750_000, 1_000_000):
            fee, im = n2 * .001 + n5 * .0015, n2 * .03 + n5 * .06
            stress = []
            for s in scenarios:
                asset = bond_pv(s['discount'], s['slope']) - base
                hedge = sum(swap_pv(t, n, fixed[t], s['discount'], s['projection'], s['slope']) for t, n in ((2, n2), (5, n5)))
                stress.append({'label': s['label'], 'asset_pnl': asset, 'hedge_pnl': hedge,
                               'combined_pnl_before_fee': asset + hedge, 'combined_pnl_after_fee': asset + hedge - fee})
            worst = max(abs(s['combined_pnl_after_fee']) for s in stress)
            candidates.append({'two_year_notional': n2, 'five_year_notional': n5,
                               'transaction_fee': fee, 'initial_margin_assumption': im,
                               'initial_cash_use': fee + im,
                               'feasible': fee <= 2_000 and fee + im <= 70_000,
                               'objective_worst_absolute_scenario_pnl_after_fee': worst,
                               'scenarios': stress})
    selected = min((c for c in candidates if c['feasible']), key=lambda c: c['objective_worst_absolute_scenario_pnl_after_fee'])
    def hedged(shift):
        return bond_pv(shift) + sum(swap_pv(t, selected[key], fixed[t], shift, shift) for t, key in ((2, 'two_year_notional'), (5, 'five_year_notional')))
    return {'selection_rule': 'Minimum worst absolute marked-value change after fees across four stated shocks; exhaustive 25-point notional grid',
            'fixed_swap_rates': fixed, 'asset_base_pv': base, 'selected': selected,
            'unhedged_risk': finite_difference_risk(bond_pv),
            'selected_risk': finite_difference_risk(hedged),
            'risk_at_half_bump': finite_difference_risk(hedged, 5e-5),
            'candidates': candidates}


def _next_weekday_morning(timestamp):
    due = (timestamp + timedelta(days=1)).replace(hour=9, minute=0)
    while due.weekday() >= 5:
        due += timedelta(days=1)
    return due


def collateral_case(mode='bilateral', threshold=5_000.0, mta=500.0, haircut=.02):
    """Dated funding ledger: receive-fixed 250k 2Y + pay-fixed 750k 5Y.

    Bilateral VM is restricted collateral, next-weekday settlement; cleared
    variation is same-event final cash settlement. IM is restricted in both.
    Positive bilateral threshold is an illustrative legacy CSA assumption,
    not a claim about covered-entity regulatory permission.
    """
    _finite(threshold, mta, haircut)
    if mode not in ('bilateral', 'cleared') or threshold < 0 or mta < 0 or not 0 <= haircut < 1:
        raise ValueError('Invalid collateral terms')
    events = [('2026-10-05T09:00', 0), ('2026-10-05T15:00', -.005),
              ('2026-10-06T09:00', -.005), ('2026-10-06T15:00', -.01),
              ('2026-10-07T09:00', -.01), ('2026-10-07T15:00', -.02),
              ('2026-10-08T09:00', -.02), ('2026-10-08T15:00', -.02)]
    initial_cash, base_asset = 40_000.0, bond_pv()
    posted, borrowing, funded_expense = 0.0, 0.0, 0.0
    pending, rows = [], []
    previous_time = datetime.fromisoformat(events[0][0])
    for stamp, shift in events:
        now = datetime.fromisoformat(stamp)
        funded_expense += borrowing * .12 * (now - previous_time).total_seconds() / (365 * 86400)
        settled_collateral = sum(amount for due, amount in pending if due <= now)
        posted += settled_collateral
        pending = [(due, amount) for due, amount in pending if due > now]
        marks = [-swap_pv(2, 250_000, par_swap_rate(2), shift, shift),
                 swap_pv(5, 750_000, par_swap_rate(5), shift, shift)]
        net_mark = sum(marks)
        # Synthetic stress IM policy; no production clearing model is claimed.
        im_requirement = 30_000 * (1 + abs(shift) / .02)
        im_market_value = im_requirement / (1 - haircut)
        required_vm = max(-net_mark - threshold, 0) if mode == 'bilateral' else 0.0
        collateral_call = 0.0
        if mode == 'bilateral':
            vm_target = required_vm / (1 - haircut)
            collateral_call = vm_target - posted - sum(amount for due, amount in pending)
            if abs(collateral_call) >= mta and abs(collateral_call) > 1e-10:
                pending.append((_next_weekday_morning(now), collateral_call))
            else:
                collateral_call = 0.0
            settlement_paid, derivative_on_balance = 0.0, net_mark
        else:
            settlement_paid, derivative_on_balance = -net_mark, 0.0
        restricted = im_market_value + posted
        uses = restricted + settlement_paid + funded_expense
        borrowing = max(uses - initial_cash, 0.0)
        available_cash = initial_cash + borrowing - uses
        asset_change = bond_pv(shift) - base_asset
        net_wealth = available_cash + restricted + asset_change + derivative_on_balance - borrowing
        expected_wealth = initial_cash + asset_change + net_mark - funded_expense
        rows.append({'timestamp': stamp, 'parallel_shift': shift, 'individual_swap_marks': marks,
                     'net_derivative_mark_before_settlement': net_mark,
                     'gross_out_of_money_marks_without_netting': sum(max(-m, 0) for m in marks),
                     'asset_value_change': asset_change, 'combined_economic_change': asset_change + net_mark,
                     'im_required': im_requirement, 'im_collateral_market_value': im_market_value,
                     'vm_required_before_haircut': required_vm,
                     'vm_collateral_posted_market_value': posted,
                     'vm_call_market_value': collateral_call,
                     'vm_pending_market_value': sum(amount for due, amount in pending),
                     'gap_after_posted_vm': max(-net_mark - posted * (1 - haircut), 0) if mode == 'bilateral' else 0,
                     'cumulative_final_variation_settlement_paid': settlement_paid,
                     'restricted_collateral_asset': restricted, 'funding_borrowing': borrowing,
                     'cumulative_funding_expense': funded_expense, 'available_cash': available_cash,
                     'funding_identity_residual': initial_cash + borrowing - restricted - settlement_paid - funded_expense - available_cash,
                     'net_wealth_identity_residual': net_wealth - expected_wealth})
        previous_time = now
    return {'mode': mode, 'terms': {'threshold': threshold if mode == 'bilateral' else 0,
                                   'minimum_transfer_amount': mta if mode == 'bilateral' else 0,
                                   'haircut': haircut, 'initial_cash': initial_cash,
                                   'funding_rate': .12, 'funding_day_basis': 'ACT/365 with intraday fractions',
                                   'settlement': 'Next weekday 09:00' if mode == 'bilateral' else 'Same-event settlement to market'},
            'events': rows, 'peak_borrowing': max(r['funding_borrowing'] for r in rows),
            'peak_pending_vm_market_value': max(r['vm_pending_market_value'] for r in rows)}


def merton_terminal_debt(asset_value, debt_face, asset_volatility, rate, maturity):
    """Single zero-coupon terminal debt; no dividends, bankruptcy cost or early default.

    PD is under Q. Asset value/volatility are explicit inputs, not accounting
    total assets or equity volatility. Deterministic and maturity limits defined.
    """
    _finite(asset_value, debt_face, asset_volatility, rate, maturity)
    if asset_value <= 0 or debt_face <= 0 or asset_volatility < 0 or maturity < 0:
        raise ValueError('Positive asset/debt, nonnegative volatility/maturity required')
    risk_free_debt = debt_face * math.exp(-rate * maturity)
    if maturity == 0 or asset_volatility == 0:
        equity = max(asset_value - risk_free_debt, 0)
        probability = float(asset_value < risk_free_debt)
        delta = float(asset_value > risk_free_debt)
    else:
        phi = lambda z: .5 * (1 + math.erf(z / math.sqrt(2)))
        root_t = math.sqrt(maturity)
        d1 = (math.log(asset_value / debt_face) + (rate + .5 * asset_volatility ** 2) * maturity) / (asset_volatility * root_t)
        d2 = d1 - asset_volatility * root_t
        equity = asset_value * phi(d1) - risk_free_debt * phi(d2)
        probability, delta = phi(-d2), phi(d1)
    debt = asset_value - equity
    return {'asset_value': asset_value, 'equity_value': equity, 'debt_value': debt,
            'risk_free_debt_pv': risk_free_debt, 'put_credit_discount': risk_free_debt - debt,
            'terminal_default_probability_Q': probability, 'equity_delta': delta,
            'equity_volatility': asset_value * delta * asset_volatility / equity if equity > 0 else None,
            'asset_debt_equity_residual': asset_value - debt - equity,
            'credit_spread_continuous': -math.log(debt / debt_face) / maturity - rate if maturity > 0 and debt > 0 else None}


def recover_merton_assets(equity, equity_volatility, debt_face, rate, maturity):
    """Nested bracketed solves for synthetic E and sigma_E; returns residuals."""
    _finite(equity, equity_volatility, debt_face, rate, maturity)
    if min(equity, equity_volatility, debt_face, maturity) <= 0:
        raise ValueError('Positive E, equity volatility, debt and maturity required')
    def fit_value(sigma):
        low, high = equity, equity + debt_face * math.exp(-rate * maturity)
        for _ in range(100):
            value = (low + high) / 2
            quote = merton_terminal_debt(value, debt_face, sigma, rate, maturity)
            if quote['equity_value'] > equity:
                high = value
            else:
                low = value
        return value, quote
    low, high = 1e-6, 3.0
    if not fit_value(low)[1]['equity_volatility'] <= equity_volatility <= fit_value(high)[1]['equity_volatility']:
        raise ValueError('Equity volatility outside asset-volatility calibration bracket')
    for iteration in range(1, 101):
        sigma = (low + high) / 2
        value, quote = fit_value(sigma)
        residual = quote['equity_volatility'] - equity_volatility
        if abs(residual) < 1e-12:
            return {'asset_value': value, 'asset_volatility': sigma,
                    'equity_value_residual': quote['equity_value'] - equity,
                    'equity_volatility_residual': residual, 'iterations': iteration}
        if residual > 0:
            high = sigma
        else:
            low = sigma
    raise ArithmeticError('Merton calibration did not converge')


def option_examples():
    months = 36
    discounts = tuple(math.exp(-(.085 + .003 * (i / 12)) * (i / 12)) for i in range(months + 1))
    tree = calibrate_rate_tree(discounts)
    known_spread = .0175
    pool = mortgage_pool(tree, spread=known_spread)
    no_prepay = mortgage_pool(tree, base_cpr=0, response=0, cpr_cap=0)
    optimal = optimal_mortgage_value(tree)
    merton = merton_terminal_debt(1_500_000, 1_000_000, .30, .085, 3)
    return {'scope': 'Synthetic reproducible R04/R05/R06 reference cases; institution, market and empirical validation remain separate',
            'rate_tree': {'model': 'Ho-Lee-style additive recombining lattice', 'dt_years': tree.dt,
                          'assumed_sigma': .015, 'discount_factors': discounts,
                          'short_rate_nodes': tree.rates,
                          'repricing_residuals': [sum(q) - d for q, d in zip(tree.state_prices, discounts)]},
            'mortgage': {'principal': 1_000_000, 'coupon': .14, 'months': months,
                         'cpr_policy': {'base': .04, 'response': 6, 'refinance_markup': .025, 'cap': .60},
                         'measure': 'Explicit assumed Q dynamics for rates and CPR; no empirical calibration',
                         'known_spread': known_spread, 'pool_at_known_spread': pool,
                         'recovered_oas': solve_oas(tree, pool['pv']),
                         'pv_spread_down_100bp': mortgage_pool(tree, spread=known_spread - .01)['pv'],
                         'pv_spread_up_100bp': mortgage_pool(tree, spread=known_spread + .01)['pv'],
                         'no_prepayment_pv_at_zero_spread': no_prepay['pv'],
                         'behavioural_prepayment_pv_at_zero_spread': mortgage_pool(tree)['pv'],
                         'optimal_exercise_pv_at_zero_spread': optimal['pv'],
                         'optimal_exercise_node_count': optimal['exercise_node_count']},
            'hedge_selection': hedge_selection_case(),
            'collateral': {'bilateral': collateral_case(), 'cleared': collateral_case('cleared')},
            'structural_credit': {'scope': 'R12 single terminal-debt baseline with synthetic inverse calibration; compound options and empirical validation remain open',
                                  'known_asset_volatility': .30, 'case': merton,
                                  'recovered_assets': recover_merton_assets(merton['equity_value'], merton['equity_volatility'], 1_000_000, .085, 3)}}


if __name__ == '__main__':
    import json
    print(json.dumps(option_examples(), indent=2, allow_nan=False))
