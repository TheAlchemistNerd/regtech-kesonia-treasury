"""Versioned fixings and explicit half-open accrual schedules for constant principal.

Business-day lookback is an EXAMPLE contract convention, not an interpretation
of the CBK document's unqualified five-day wording. Supply the approved calendar.
"""
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal as D, localcontext, ROUND_HALF_UP


def finite(value: D) -> D:
    if not isinstance(value, D) or not value.is_finite():
        raise ValueError('Use finite Decimal values and decimal annual rates')
    return value


@dataclass(frozen=True)
class Calendar:
    holidays: frozenset[date] = frozenset()

    def business(self, day: date) -> bool:
        return day.weekday() < 5 and day not in self.holidays

    def previous_or_same(self, day: date) -> date:
        while not self.business(day):
            day -= timedelta(days=1)
        return day

    def next(self, day: date) -> date:
        day += timedelta(days=1)
        while not self.business(day):
            day += timedelta(days=1)
        return day

    def lag(self, day: date, business_days: int) -> date:
        if business_days < 0:
            raise ValueError('Lookback must be nonnegative')
        day = self.previous_or_same(day)
        for _ in range(business_days):
            day = self.previous_or_same(day - timedelta(days=1))
        return day


@dataclass(frozen=True)
class Interval:
    start: date
    end: date
    observation: date
    weight_days: int


@dataclass(frozen=True)
class Fixing:
    observation: date
    available_at: datetime
    rate: D
    version: str
    source: str = 'KESONIA'
    fallback_authorization: str | None = None


def schedule(start: date, end: date, calendar: Calendar, lookback: int = 0,
             observation_shift: bool = False) -> list[Interval]:
    """No shift: retain accrual-day weights. Shift: use shifted observation spans.

    Observation-shift examples require business-day endpoints so that the
    mapping is unambiguous. Nonbusiness clipped endpoints are supported only
    for the explicitly unshifted schedule.
    """
    if end <= start:
        raise ValueError('Interest period must have positive length')
    if observation_shift and not (calendar.business(start) and calendar.business(end)):
        raise ValueError('Shifted demonstration requires business-day endpoints')
    rows = []
    cursor = start
    while cursor < end:
        effective = calendar.previous_or_same(cursor)
        stop = min(end, calendar.next(effective))
        observed = calendar.lag(effective, lookback)
        weight = ((calendar.lag(stop, lookback) - observed).days if observation_shift
                  else (stop - cursor).days)
        if weight <= 0:
            raise ValueError('Nonpositive observation weight')
        rows.append(Interval(cursor, stop, observed, weight))
        cursor = stop
    return rows


def select_fixing(observation: date, fixings: list[Fixing], cutoff: datetime) -> Fixing:
    if cutoff.utcoffset() is None:
        raise ValueError('Calculation cutoff must include a timezone')
    for fixing in fixings:
        finite(fixing.rate)
        if fixing.available_at.utcoffset() is None or not fixing.version:
            raise ValueError('Fixings require availability timezone and version')
    candidates = [f for f in fixings if f.observation == observation and f.available_at <= cutoff]
    if not candidates:
        raise LookupError(f'No published fixing available for {observation} at cutoff')
    official = [f for f in candidates if f.source == 'KESONIA']
    eligible = official or [f for f in candidates if f.source == 'CBR' and f.fallback_authorization]
    if not eligible:
        raise ValueError('Missing KESONIA requires explicitly approved fallback')
    latest = max(f.available_at for f in eligible)
    chosen = [f for f in eligible if f.available_at == latest]
    if len(chosen) != 1:
        raise ValueError('Ambiguous fixing revision at the same availability time')
    return chosen[0]


def compound(rows: list[Interval], fixings: list[Fixing], cutoff: datetime,
             principal: D, margin: D = D('0'), day_basis: int = 365) -> dict:
    """Compound benchmark only; add a simple margin on ACT period days.

    This profile is constant principal, no cap/floor, no in-period reset, no
    capitalisation of unpaid interest. Other contractual profiles must not be
    silently passed through it. All intermediate arithmetic uses 40 digits.
    """
    finite(principal)
    finite(margin)
    if principal < 0 or not rows or day_basis <= 0:
        raise ValueError('Invalid principal, schedule or basis')
    for i, row in enumerate(rows):
        if row.end <= row.start or row.weight_days <= 0:
            raise ValueError('Invalid interval')
        if i and rows[i - 1].end != row.start:
            raise ValueError('Accrual schedule has a gap, overlap or is unordered')
    days = (rows[-1].end - rows[0].start).days
    with localcontext() as ctx:
        ctx.prec = 40
        accumulated = D(1)
        ledger = []
        for row in rows:
            fixing = select_fixing(row.observation, fixings, cutoff)
            factor = D(1) + fixing.rate * row.weight_days / day_basis
            if factor <= 0:
                raise ValueError('Compounding factor must be positive')
            previous = accumulated
            accumulated *= factor
            ledger.append({'start': row.start.isoformat(), 'end': row.end.isoformat(),
                           'observation': row.observation.isoformat(), 'weight_days': row.weight_days,
                           'rate': str(fixing.rate), 'source': fixing.source, 'version': fixing.version,
                           'available_at': fixing.available_at.isoformat(),
                           'fallback_authorization': fixing.fallback_authorization,
                           'benchmark_increment': str(principal * (accumulated - previous))})
        factor = accumulated - 1
        benchmark_cash = principal * factor
        margin_cash = principal * margin * days / day_basis
        return {'period_days': days, 'weight_days': sum(r.weight_days for r in rows),
                'factor': str(factor), 'annualised_period_rate': str(factor * day_basis / days),
                'benchmark_cash': str(benchmark_cash), 'simple_margin_cash': str(margin_cash),
                'total_cash_unrounded': str(benchmark_cash + margin_cash),
                'total_cash_rounded': str((benchmark_cash + margin_cash).quantize(D('.01'), rounding=ROUND_HALF_UP)),
                'ledger': ledger}


def published_index_ratio(start: D, end: D) -> D:
    finite(start); finite(end)
    if start <= 0 or end <= 0:
        raise ValueError('Index values must be positive')
    with localcontext() as ctx:
        ctx.prec = 40
        return end / start - 1


def benchmark_examples() -> dict:
    c = Calendar()
    historical = Fixing(date(2025, 9, 5), datetime.fromisoformat('2025-09-08T09:00:00+03:00'),
                        D('.094618'), 'historical-published', 'KESONIA')
    cutoff = datetime.fromisoformat('2025-09-18T09:00:00+03:00')
    historical_result = compound(schedule(date(2025, 9, 5), date(2025, 9, 8), c),
                                 [historical], cutoff, D('1000000'), D('.03'))
    idx = published_index_ratio(D('100.10451025'), D('100.18235974'))
    historical_result['published_index_factor'] = str(idx)
    historical_result['index_minus_fixing_cash'] = str(idx * D('1000000') - D(historical_result['benchmark_cash']))
    # A synthetic holiday forces no-shift and observation-shift weights to differ.
    synthetic_calendar = Calendar(frozenset({date(2025, 9, 15)}))
    fixing_days = [date(2025, 9, d) for d in (3, 4, 5, 8)]
    synthetic_fixings = [Fixing(day, datetime.fromisoformat(c.next(day).isoformat() + 'T09:00:00+03:00'),
                                rate, 'synthetic-v1') for day, rate in zip(fixing_days, map(D, ['.09', '.095', '.10', '.105']))]
    output = {'historical_weekend': historical_result,
              'synthetic_calendar_note': '15 September is an invented holiday for this test, not an asserted Kenyan holiday.'}
    for shift in (False, True):
        rows = schedule(date(2025, 9, 10), date(2025, 9, 17), synthetic_calendar, 5, shift)
        output['five_business_day_' + ('shift' if shift else 'no_shift')] = compound(rows, synthetic_fixings, cutoff, D('1000000'), D('.03'))
    return output
