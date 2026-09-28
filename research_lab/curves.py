"""Synthetic curve construction with explicit interpolation and repricing checks."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Curve:
    nodes: tuple[tuple[float, float], ...]
    label: str

    def __post_init__(self):
        if not self.label or not self.nodes or self.nodes[0] != (0.0, 1.0):
            raise ValueError('Curve requires identity, valuation origin and D(0)=1')
        if any(not math.isfinite(t) or not math.isfinite(df) or df <= 0 for t, df in self.nodes):
            raise ValueError('Finite times and positive discount factors required')
        if any(a[0] >= b[0] for a, b in zip(self.nodes, self.nodes[1:])):
            raise ValueError('Curve times must be strictly increasing')

    def df(self, time: float) -> float:
        if not math.isfinite(time) or time < 0 or time > self.nodes[-1][0]:
            raise ValueError('Extrapolation requires a separate approved policy')
        for (t0, d0), (t1, d1) in zip(self.nodes, self.nodes[1:]):
            if t0 <= time <= t1:
                w = (time - t0) / (t1 - t0)
                return math.exp((1 - w) * math.log(d0) + w * math.log(d1))
        return 1.0

    def simple_forward(self, start: float, end: float) -> float:
        if end <= start:
            raise ValueError('Forward interval must be positive')
        return (self.df(start) / self.df(end) - 1) / (end - start)

    def parallel_zero_shift(self, shift: float) -> 'Curve':
        if not math.isfinite(shift):
            raise ValueError('Finite shift required')
        return Curve(tuple((t, df * math.exp(-shift * t)) for t, df in self.nodes), self.label + '/shifted')


def bootstrap_annual_par(deposit_one_year: float, par_coupons: list[float], label: str = 'synthetic') -> Curve:
    """Unit-price annual fixed-coupon instruments at years 2,...,n; no calendar assumptions hidden.

    D_n=(1-c_n sum_{j<n} D_j)/(1+c_n). Rates and accruals here are
    annual decimals and unit years, NOT a KESONIA observation history.
    """
    rates = [deposit_one_year] + par_coupons
    if any(not math.isfinite(r) or r <= -1 for r in rates):
        raise ValueError('Invalid annual quote')
    discounts = [1 / (1 + deposit_one_year)]
    for rate in par_coupons:
        value = (1 - rate * sum(discounts)) / (1 + rate)
        if value <= 0:
            raise ValueError('Quotes imply a nonpositive discount factor')
        discounts.append(value)
    return Curve(((0.0, 1.0),) + tuple((float(i), df) for i, df in enumerate(discounts, 1)), label)


def quote_repricing(curve: Curve, deposit: float, coupons: list[float]) -> list[dict]:
    records = [{'tenor_years': 1, 'price': (1 + deposit) * curve.df(1)}]
    for n, coupon in enumerate(coupons, 2):
        price = coupon * sum(curve.df(t) for t in range(1, n + 1)) + curve.df(n)
        records.append({'tenor_years': n, 'price': price})
    for row in records:
        row['residual_to_unit_price'] = row['price'] - 1
    return records


def floating_note_pv(projection: Curve, discount: Curve, times: list[float], notional: float = 1.0) -> float:
    if not times or times[0] <= 0 or any(a >= b for a, b in zip(times, times[1:])):
        raise ValueError('Strictly increasing positive payment times required')
    if not math.isfinite(notional) or notional <= 0:
        raise ValueError('Positive notional required')
    start = 0.0
    coupons = 0.0
    for end in times:
        coupons += projection.simple_forward(start, end) * (end - start) * discount.df(end)
        start = end
    return notional * (coupons + discount.df(times[-1]))


def key_rate_dv01(curve: Curve, cashflows: list[tuple[float, float]], shift: float = 1e-4) -> list[dict]:
    """Central finite differences of PV to each continuous zero-rate node.

    Positive output means PV falls when that node's zero rate rises. Values
    are money per one basis point, not duration in years.
    """
    if shift <= 0 or not math.isfinite(shift):
        raise ValueError('Positive finite bump required')
    if any(not math.isfinite(t) or not math.isfinite(cash) for t, cash in cashflows):
        raise ValueError('Cash-flow dates and amounts must be finite')
    output = []
    for i in range(1, len(curve.nodes)):
        up, down = list(curve.nodes), list(curve.nodes)
        t, df = curve.nodes[i]
        up[i] = (t, df * math.exp(-shift * t))
        down[i] = (t, df * math.exp(shift * t))
        cu, cd = Curve(tuple(up), curve.label), Curve(tuple(down), curve.label)
        pv_up = sum(cash * cu.df(time) for time, cash in cashflows)
        pv_down = sum(cash * cd.df(time) for time, cash in cashflows)
        output.append({'tenor_years': t, 'dv01': (pv_down - pv_up) / (2 * shift) * 1e-4})
    return output


def curve_examples() -> dict:
    discount = bootstrap_annual_par(.10, [.12, .13], 'synthetic-discount-v1')
    projection = bootstrap_annual_par(.11, [.13, .14], 'synthetic-projection-v1')
    return {'market_status': 'Synthetic unit-price annual coupon quotes; not Kenyan market observations',
            'quotes': {'one_year_deposit': .10, 'two_year_par': .12, 'three_year_par': .13},
            'nodes': discount.nodes, 'repricing': quote_repricing(discount, .10, [.12, .13]),
            'df_1_5_log_interpolated': discount.df(1.5),
            'forwards': [discount.simple_forward(t - 1, t) for t in (1, 2, 3)],
            'same_curve_floating_note_pv': floating_note_pv(discount, discount, [1, 2, 3], 1000000),
            'separate_projection_floating_note_pv': floating_note_pv(projection, discount, [1, 2, 3], 1000000),
            'bullet_key_rate_dv01': key_rate_dv01(discount, [(1, 100000), (2, 100000), (3, 1100000)])}
