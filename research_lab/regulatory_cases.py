"""Scoped, synthetic regulatory treasury cases; standard library only.

Rules are pinned in REGULATORY_WORKED_CASES.md. Monetary inputs within each
calculation must share one unit. These functions do not classify real instruments
or establish Kenyan adoption of the Basel market/counterparty capital chapters.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, expm1, isfinite, sqrt
from typing import Iterable


def _number(value: float, name: str, *, nonnegative: bool = False) -> float:
    value = float(value)
    if not isfinite(value) or (nonnegative and value < 0):
        raise ValueError(f"{name} must be finite" + (" and nonnegative" if nonnegative else ""))
    return value


def _fraction(value: float, name: str) -> float:
    value = _number(value, name, nonnegative=True)
    if value > 1:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


@dataclass(frozen=True)
class LiquidAsset:
    name: str
    market_value: float
    level: str
    encumbered: bool = False
    operationally_available: bool = True
    eligible: bool = True


HQLA_HAIRCUT = {"L1": 0.0, "L2A": 0.15, "L2B_CORPORATE": 0.50, "L2B_RMBS": 0.25}


def liquidity_coverage(assets: Iterable[LiquidAsset], outflows: Iterable[tuple[str, float, float]],
                       inflows: Iterable[tuple[str, float, float]], *,
                       short_sft_unwind_required: bool = False) -> dict:
    """CBK LCR subset with no short SFTs; factors are explicit classified inputs.

    No asset counted in HQLA may also supply an inflow. Both level caps are
    enforced simultaneously after haircuts. No cash inflow exemption is used.
    """
    if short_sft_unwind_required:
        raise ValueError("Unwind short SFTs before using this no-SFT profile")
    amounts = {"L1": 0.0, "L2A": 0.0, "L2B": 0.0}
    details, seen, included = [], set(), set()
    for asset in assets:
        if not asset.name or asset.name in seen:
            raise ValueError("Asset identifiers must be unique and nonempty")
        seen.add(asset.name)
        mv = _number(asset.market_value, "market_value", nonnegative=True)
        if asset.level not in HQLA_HAIRCUT:
            raise ValueError("Unsupported HQLA class")
        haircut = HQLA_HAIRCUT[asset.level]
        allowed = asset.eligible and asset.operationally_available and not asset.encumbered
        value = mv * (1 - haircut) if allowed else 0.0
        key = "L2B" if asset.level.startswith("L2B") else asset.level
        amounts[key] += value
        if allowed:
            included.add(asset.name)
        details.append({**asdict(asset), "haircut": haircut, "after_haircut_eligible": value})
    l1, l2a, l2b = (amounts[k] for k in ("L1", "L2A", "L2B"))
    # Maximise L1 + accepted L2A + accepted L2B subject to availability and caps.
    # This is the exact no-SFT solution, not two independent cap deductions.
    hqla = min(l1 + l2a + l2b, (l1 + l2a) / 0.85, l1 / 0.60)
    accepted_b = min(l2b, 0.15 * hqla)
    accepted_a = max(0.0, hqla - l1 - accepted_b)

    def weighted(rows: Iterable[tuple[str, float, float]], inflow: bool = False) -> list[dict]:
        result, names = [], set()
        for name, amount, factor in rows:
            if not name or name in names:
                raise ValueError("Flow identifiers must be unique and nonempty within their side")
            if inflow and name in included:
                raise ValueError("An HQLA asset cannot also be an inflow")
            names.add(name)
            a, f = _number(amount, "flow amount", nonnegative=True), _fraction(factor, "flow factor")
            result.append({"name": name, "amount": a, "factor": f, "weighted": a * f})
        return result

    outs, ins = weighted(outflows), weighted(inflows, True)
    out = sum(x["weighted"] for x in outs)
    gross_in = sum(x["weighted"] for x in ins)
    recognised_in = min(gross_in, 0.75 * out)
    net = out - recognised_in
    return {"assets": details, "post_haircut_levels": amounts, "hqla": hqla,
            "accepted_level2a": accepted_a, "accepted_level2b": accepted_b,
            "cap_excluded": l1 + l2a + l2b - hqla,
            "outflow_rows": outs, "inflow_rows": ins, "outflows": out,
            "inflows_before_cap": gross_in, "inflows_recognised": recognised_in,
            "inflow_cap_excluded": gross_in - recognised_in, "net_outflows": net,
            "lcr": hqla / net if net else None, "ratio_status": "defined" if net else "no_net_outflow"}


def stable_funding(funding: Iterable[tuple[str, float, float]],
                   assets: Iterable[tuple[str, float, float]],
                   commitments: Iterable[tuple[str, float, float]]) -> dict:
    """NSFR arithmetic on explicitly classified rows; amounts are carrying values."""
    def rows(items: Iterable[tuple[str, float, float]]) -> list[dict]:
        answer, names = [], set()
        for name, amount, factor in items:
            if not name or name in names:
                raise ValueError("Stable-funding row identifiers must be unique and nonempty")
            names.add(name)
            a = _number(amount, "carrying value", nonnegative=True)
            f = _fraction(factor, "stable funding factor")
            answer.append({"name": name, "amount": a, "factor": f, "weighted": a * f})
        return answer
    fs, ass, obs = rows(funding), rows(assets), rows(commitments)
    asf = sum(x["weighted"] for x in fs)
    rsf_assets = sum(x["weighted"] for x in ass)
    rsf_obs = sum(x["weighted"] for x in obs)
    rsf = rsf_assets + rsf_obs
    return {"funding": fs, "assets": ass, "commitments": obs, "asf": asf,
            "rsf_assets": rsf_assets, "rsf_commitments": rsf_obs, "rsf": rsf,
            "nsfr": asf / rsf if rsf else None,
            "balance_sheet_residual": sum(x["amount"] for x in ass) - sum(x["amount"] for x in fs)}


def liquidity_example() -> dict:
    """One KES-million opening balance feeds LCR, NSFR and dated cash."""
    liquid = [LiquidAsset("cash", 20, "L1"), LiquidAsset("government", 80, "L1"),
              LiquidAsset("qualifying_A", 100, "L2A"), LiquidAsset("qualifying_B", 80, "L2B_CORPORATE"),
              LiquidAsset("pledged_government", 20, "L1", encumbered=True)]
    outflows = [("stable_KES_retail", 400, .05), ("less_stable_KES_retail", 200, .10),
                ("nonfinancial_corporate", 200, .40), ("financial_wholesale", 50, 1),
                ("nonfinancial_credit_commitment", 100, .10), ("contractual_collateral_call", 10, 1)]
    lcr = liquidity_coverage(liquid, outflows, [("performing_retail_due", 350, .50)])
    funding = [("capital", 100, 1), ("debt_over_one_year", 50, 1),
               ("stable_KES_retail", 400, .95), ("less_stable_KES_retail", 200, .90),
               ("nonfinancial_below_one_year", 200, .50), ("financial_below_six_months", 50, 0)]
    assets = [("cash", 20, 0), ("government", 80, .05), ("qualifying_A", 100, .15),
              ("qualifying_B", 80, .50), ("government_encumbered_two_years", 20, 1),
              ("performing_retail_due_within_30d", 350, .50),
              ("performing_loans_over_one_year_RW_above_50pct", 350, .85)]
    nsfr = stable_funding(funding, assets, [("irrevocable_undrawn_credit", 100, .05)])
    # Scenario timing, chosen for illustration, is not prescribed by the LCR.
    closing_assets = {"cash": 20., "government": 80., "qualifying_A": 100., "qualifying_B": 80.,
                      "pledged_government": 20., "short_loans": 350., "long_loans": 350.,
                      "new_draw": 0., "posted_collateral": 0.}
    liabilities, equity, timeline = 900., 100., []
    for day, kind, item, carrying, receipt in [
        ("2026-10-02", "sale", "government", 80., 80.),
        ("2026-10-02", "sale", "qualifying_A", 100., 85.),
        ("2026-10-02", "sale", "qualifying_B", 10., 5.),
        ("2026-10-03", "deposit_withdrawal", "cash", 170., 0.),
        ("2026-10-03", "draw", "new_draw", 10., 0.),
        ("2026-10-03", "collateral", "posted_collateral", 10., 0.),
        ("2026-10-20", "repayment", "short_loans", 175., 175.)]:
        if kind == "sale":
            closing_assets[item] -= carrying
            closing_assets["cash"] += receipt
            equity -= carrying - receipt
        elif kind == "deposit_withdrawal":
            closing_assets["cash"] -= carrying
            liabilities -= carrying
        elif kind in ("draw", "collateral"):
            closing_assets["cash"] -= carrying
            closing_assets[item] += carrying
        else:
            closing_assets[item] -= carrying
            closing_assets["cash"] += receipt
        timeline.append({"date": day, "event": kind, "item": item, "carrying_movement": carrying,
                         "sale_or_collection_cash": receipt, "cash": closing_assets["cash"],
                         "assets": sum(closing_assets.values()), "liabilities": liabilities, "equity": equity,
                         "balance_residual": sum(closing_assets.values()) - liabilities - equity})
    return {"unit": "KES million", "opening_assets": 1000., "opening_liabilities": 900., "opening_equity": 100.,
            "lcr": lcr, "nsfr": nsfr, "timeline": timeline, "closing_asset_ledger": closing_assets,
            "cash_without_monetisation_on_3_oct": 20 - lcr["outflows"],
            "sale_proceeds": 170., "realised_sale_loss": 20., "closing_cash": closing_assets["cash"],
            "closing_equity": equity, "cash_bridge_residual": closing_assets["cash"] - (20 + 170 + 175 - 190),
            "interest_rate_case": balance_sheet_interest_case(), "reverse_cash_stress": reverse_cash_stress()}


def reverse_cash_stress() -> dict:
    """Solve the early cash constraint; the dated inflow arrives after this date.

    w multiplies the baseline aggregate withdrawal 170. Non-withdrawal calls
    remain 20. Zero cash is the boundary; any greater w produces a shortfall.
    Quoted sale prices are synthetic stressed scenario prices, not an automatic
    consequence of regulatory haircuts. All quantities are KES million.
    """
    result = []
    for name, sale_proceeds, sale_loss in [("no_sale", 0., 0.), ("dated_targeted_sales", 170., 20.),
                                          ("sell_all_unencumbered_securities", 205., 55.)]:
        available = 20. + sale_proceeds
        withdrawal_limit = available - 20.
        baseline_remaining = available - 170. - 20.
        result.append({"response": name, "opening_cash_plus_sales": available, "sale_proceeds": sale_proceeds,
                       "realised_sale_loss": sale_loss, "equity_after_sale": 100.-sale_loss,
                       "fixed_draw_and_collateral": 20., "withdrawals_exhausting_cash": withdrawal_limit,
                       "withdrawal_multiplier_exhausting_cash": withdrawal_limit/170.,
                       "cash_at_baseline_withdrawals": baseline_remaining,
                       "additional_collateral_call_capacity_at_baseline": max(baseline_remaining, 0.),
                       "baseline_funding_shortfall": max(-baseline_remaining, 0.)})
    return {"unit": "KES million", "constraint": "20 + sale_proceeds - 170*w - 20 >= 0",
            "deadline": "2026-10-03", "baseline_withdrawals": 170., "responses": result}


def balance_sheet_interest_case(parallel_shock: float = .02) -> dict:
    """Synthetic EVE and one-year NII on the same opening balance as the LCR.

    Coupon rates and discount rates are effective annual decimals. Coupons are
    paid annually with a prorated final stub; principal is repaid at maturity.
    EVE uses the existing book, with no replacement lending. NII holds opening
    balances constant for one year and rolls maturities at the shocked coupon.
    Behavioural deposit lives/betas are assumed inputs, not fitted estimates.
    """
    shock = _number(parallel_shock, "parallel_shock")
    # side, balance, life, coupon, reset time, pass-through beta
    specs = [("cash", "asset", 20., 0., 0., 0., 0.),
             ("government", "asset", 80., 3., .09, 3., 1.),
             ("qualifying_A", "asset", 100., 2., .10, 2., 1.),
             ("qualifying_B", "asset", 80., 4., .12, 4., 1.),
             ("pledged_government", "asset", 20., 3., .09, 3., 1.),
             ("performing_retail_due", "asset", 350., 19/365, .15, 19/365, 1.),
             ("performing_long_loans", "asset", 350., 3., .18, 3., 1.),
             ("debt_over_one_year", "liability", 50., 2., .11, 2., 1.),
             ("stable_KES_retail", "liability", 400., 2., .05, 0., .5),
             ("less_stable_KES_retail", "liability", 200., .5, .06, 0., .8),
             ("nonfinancial_corporate", "liability", 200., .25, .07, 0., 1.),
             ("financial_wholesale", "liability", 50., .10, .08, 0., 1.)]
    rows = []
    for name, side, balance, life, rate, reset, beta in specs:
        if rate+shock <= -1:
            raise ValueError("Discount rates must exceed -100%")
        dates = ([float(i) for i in range(1, int(life)+1)] + ([] if life == int(life) else [life])) if life else []
        cashflows, previous, base_pv, shocked_pv = [], 0., balance if not life else 0., balance if not life else 0.
        for t in dates:
            coupon = balance*rate*(t-previous)
            repriced_interval = max(0., t-max(previous, reset))
            shocked_coupon = coupon + balance*beta*shock*repriced_interval
            redemption = balance if abs(t-life) < 1e-12 else 0.
            base_cf, shocked_cf = coupon+redemption, shocked_coupon+redemption
            base_pv += base_cf/(1+rate)**t
            shocked_pv += shocked_cf/(1+rate+shock)**t
            cashflows.append({"time": t, "base_coupon": coupon, "shocked_coupon": shocked_coupon,
                              "redemption": redemption, "base_cashflow": base_cf, "shocked_cashflow": shocked_cf})
            previous = t
        base_interest = balance*rate
        shocked_interest = base_interest + balance*beta*shock*max(0., 1-reset)
        rows.append({"name": name, "side": side, "opening_carrying_value": balance, "maturity_years": life,
                     "coupon_and_base_discount_rate": rate, "reset_time_years": reset, "beta": beta,
                     "cashflows": cashflows, "base_pv": base_pv, "shocked_pv": shocked_pv,
                     "base_one_year_interest": base_interest, "shocked_one_year_interest": shocked_interest})
    sign = lambda row: 1 if row["side"] == "asset" else -1
    base_eve = sum(sign(row)*row["base_pv"] for row in rows)
    shocked_eve = sum(sign(row)*row["shocked_pv"] for row in rows)
    base_nii = sum(sign(row)*row["base_one_year_interest"] for row in rows)
    shocked_nii = sum(sign(row)*row["shocked_one_year_interest"] for row in rows)
    return {"unit": "KES million", "parallel_shock": shock, "rows": rows, "base_eve": base_eve,
            "shocked_eve": shocked_eve, "delta_eve": shocked_eve-base_eve, "base_nii": base_nii,
            "shocked_nii": shocked_nii, "delta_nii": shocked_nii-base_nii,
            "opening_asset_balance": sum(r["opening_carrying_value"] for r in rows if r["side"] == "asset"),
            "opening_liability_balance": sum(r["opening_carrying_value"] for r in rows if r["side"] == "liability"),
            "opening_book_equity": 100., "base_eve_to_book_equity_difference": base_eve-100.}


@dataclass(frozen=True)
class IRTrade:
    name: str
    notional: float
    start_years: float
    end_years: float
    maturity_years: float
    delta: int
    market_value: float


def supervisory_duration(start_years: float, end_years: float) -> float:
    s = _number(start_years, "start", nonnegative=True)
    e = _number(end_years, "end", nonnegative=True)
    if e <= s:
        raise ValueError("end must exceed start")
    # CRE52.34 floors calculated duration as well as the separate M floor.
    return max(10/250, exp(-.05 * s) * -expm1(-.05 * (e - s)) / .05)


def _ir_addon(trades: list[IRTrade], mpor_days: float | None) -> dict:
    buckets, rows = [0., 0., 0.], []
    if mpor_days is not None:
        mpor_days = _number(mpor_days, "MPOR", nonnegative=True)
        if mpor_days < 10:
            raise ValueError("This daily bilateral margin profile has a 10-business-day MPOR floor")
    for trade in trades:
        n = _number(trade.notional, "notional", nonnegative=True)
        _number(trade.market_value, "market_value")
        m = _number(trade.maturity_years, "maturity", nonnegative=True)
        if trade.delta not in (-1, 1) or m <= 0 or abs(m - trade.end_years) > 1e-12:
            raise ValueError("Only live linear IR trades ending at their final maturity, delta +/-1, are supported")
        duration = supervisory_duration(trade.start_years, trade.end_years)
        mf = sqrt(min(max(m, 10 / 250), 1)) if mpor_days is None else 1.5 * sqrt(mpor_days / 250)
        adjusted = n * duration
        effective = adjusted * mf * trade.delta
        bucket = 0 if trade.end_years < 1 else (1 if trade.end_years <= 5 else 2)
        buckets[bucket] += effective
        rows.append({**asdict(trade), "supervisory_duration": duration, "adjusted_notional": adjusted,
                     "maturity_factor": mf, "effective_notional": effective, "bucket": bucket + 1})
    a, b, c = buckets
    # CRE52.57: adjacent bucket cross coefficient 1.4; outer coefficient .6.
    variance = a*a + b*b + c*c + 1.4*a*b + 1.4*b*c + .6*a*c
    effective_hs = sqrt(max(variance, 0.))
    return {"trades": rows, "bucket_effective_notionals": buckets,
            "hedging_set_effective_notional": effective_hs, "addon": .005 * effective_hs}


def _multiplier(v_minus_c: float, addon: float) -> float:
    if addon == 0 or v_minus_c >= 0:
        return 1.
    return .05 + .95 * exp(v_minus_c / (1.90 * addon))


def sa_ccr_ir(trades: Iterable[IRTrade], *, collateral: float = 0., mpor_days: float | None = None,
              threshold: float = 0., minimum_transfer: float = 0., nica: float = 0.) -> dict:
    """One enforceable single-currency IR netting set, linear trades only.

    C is signed same-currency cash collateral already available to this set.
    Margined counterparty posts daily VM; same C is used for the unmargined cap.
    Threshold/MTA/NICA are not inferred from C. Other asset classes and CSA shapes
    need distinct models. Monetary outputs are currency, never capital percentages.
    """
    ts = list(trades)
    if len({t.name for t in ts}) != len(ts) or any(not t.name for t in ts):
        raise ValueError("Trade names must be unique and nonempty")
    c, n = _number(collateral, "collateral"), _number(nica, "NICA")
    th = _number(threshold, "threshold", nonnegative=True)
    mta = _number(minimum_transfer, "MTA", nonnegative=True)
    if mpor_days is None and (th != 0 or mta != 0 or n != 0):
        raise ValueError("Margin agreement fields require the margined profile")
    v = sum(_number(t.market_value, "market_value") for t in ts)
    unm = _ir_addon(ts, None)
    un_rc = max(v - c, 0.)
    un_mult = _multiplier(v - c, unm["addon"])
    un_ead = 1.4 * (un_rc + un_mult * unm["addon"])
    add = unm if mpor_days is None else _ir_addon(ts, mpor_days)
    rc = un_rc if mpor_days is None else max(v - c, th + mta - n, 0.)
    mult = _multiplier(v - c, add["addon"])
    pfe = mult * add["addon"]
    raw = 1.4 * (rc + pfe)
    ead = raw if mpor_days is None else min(raw, un_ead)
    return {**add, "V": v, "C": c, "NICA": n, "threshold": th, "minimum_transfer": mta,
            "mpor_days": mpor_days, "replacement_cost": rc, "multiplier": mult, "pfe": pfe,
            "uncapped_ead": raw, "unmargined_ead_same_collateral": un_ead, "ead": ead,
            "margin_cap_applied": mpor_days is not None and raw > un_ead}


def unilateral_cva(times: Iterable[float], exposures: Iterable[float], spread: float,
                   recovery: float, discount_rate: float) -> dict:
    """Synthetic flat-hazard unilateral CVA; positive loss and its spread sensitivity.

    Exposures are conditional on a default in each interval; they are held fixed
    for the CS01 derivative. Constant intensity = spread/LGD is a model assumption.
    """
    tt, ee = list(times), list(exposures)
    if len(tt) != len(ee) or not tt:
        raise ValueError("Need aligned nonempty time/exposure vectors")
    rec = _fraction(recovery, "recovery")
    if rec == 1:
        raise ValueError("Positive LGD is required by the spread/intensity model")
    s = _number(spread, "spread", nonnegative=True)
    r = _number(discount_rate, "discount_rate")
    lgd, hazard, previous, total, derivative = 1-rec, s/(1-rec), 0., 0., 0.
    rows = []
    for t, e in zip(tt, ee):
        t, e = _number(t, "time", nonnegative=True), _number(e, "exposure", nonnegative=True)
        if t <= previous:
            raise ValueError("Times must increase strictly above zero")
        q = exp(-hazard * previous) - exp(-hazard * t)
        df = exp(-r * t)
        loss = lgd * e * df * q
        total += loss
        derivative += e * df * (t * exp(-hazard*t) - previous * exp(-hazard*previous))
        rows.append({"time": t, "default_conditional_exposure": e, "marginal_default_probability": q,
                     "discount_factor": df, "loss": loss})
        previous = t
    return {"spread": s, "recovery": rec, "hazard": hazard, "discount_rate": r,
            "cva": total, "cs01": derivative * .0001, "rows": rows}


def wrong_way_example() -> dict:
    # One persistent market state per path. Independence comparator preserves the
    # exact marginal default probabilities, not merely the mean hazard.
    times, shape, weights = [1., 2., 3.], [1., .8, .4], [.5, .5]
    state_specs = [("calm", .004, 500_000.), ("stress", .036, 1_500_000.)]
    states = [{"name": name, "weight": weight,
               **unilateral_cva(times, [scale*x for x in shape], spread, .4, .09)}
              for weight, (name, spread, scale) in zip(weights, state_specs)]
    joint = sum(st["weight"]*st["cva"] for st in states)
    independent, rows = 0., []
    for j, t in enumerate(times):
        marginal_q = sum(st["weight"]*st["rows"][j]["marginal_default_probability"] for st in states)
        mean_e = sum(st["weight"]*st["rows"][j]["default_conditional_exposure"] for st in states)
        part = .6 * exp(-.09*t) * marginal_q * mean_e
        independent += part
        rows.append({"time": t, "marginal_default_probability": marginal_q, "mean_exposure": mean_e,
                     "independent_loss": part})
    return {"states": states, "independent_marginals": rows, "joint_cva": joint,
            "independent_cva_same_marginals": independent, "wrong_way_increment": joint-independent}


def reduced_ba_cva(counterparties: Iterable[dict]) -> dict:
    """MAR50 reduced BA-CVA, supplied approved RW and non-IMM effective maturity.

    Each row owns one counterparty with one or more (EAD, effective_maturity)
    netting sets. EAD already contains alpha=1.4; divide by it exactly once.
    Only the reduced approach is implemented; no hedge benefit is attributed.
    """
    rows, names = [], set()
    for cp in counterparties:
        name = cp["name"]
        if not name or name in names:
            raise ValueError("Counterparty names must be unique and nonempty")
        names.add(name)
        rw = _fraction(cp["risk_weight"], "counterparty risk weight")
        terms = []
        for ead, maturity in cp["netting_sets"]:
            ead, m = _number(ead, "EAD", nonnegative=True), _number(maturity, "effective maturity", nonnegative=True)
            if m < 1:
                raise ValueError("This BA-CVA profile uses effective maturities at least one year")
            df = -expm1(-.05*m) / (.05*m)
            terms.append({"ead": ead, "effective_maturity": m, "supervisory_discount": df,
                          "maturity_adjusted_exposure": m * ead * df})
        scva = rw / 1.4 * sum(t["maturity_adjusted_exposure"] for t in terms)
        rows.append({"name": name, "risk_weight": rw, "netting_sets": terms, "scva": scva})
    scvas = [x["scva"] for x in rows]
    reduced = sqrt((.5*sum(scvas))**2 + .75*sum(v*v for v in scvas))
    capital = .65 * reduced
    return {"counterparties": rows, "reduced_before_scalar": reduced,
            "discount_scalar": .65, "capital": capital, "rwa": 12.5*capital}


GIRR_WEIGHTS = {.25: .017, .5: .017, 1.: .016, 2.: .013, 3.: .012,
                5.: .011, 10.: .011, 15.: .011, 20.: .011, 30.: .011}


def girr_correlation(tenor_a: float, tenor_b: float, scenario: str = "medium") -> float:
    if tenor_a not in GIRR_WEIGHTS or tenor_b not in GIRR_WEIGHTS:
        raise ValueError("Unsupported regulatory tenor")
    rho = max(exp(-.03*abs(tenor_a-tenor_b)/min(tenor_a, tenor_b)), .4)
    return _correlation_scenario(rho, scenario)


def _correlation_scenario(rho: float, scenario: str) -> float:
    if scenario == "medium":
        return rho
    if scenario == "high":
        return min(1.25*rho, 1.)
    if scenario == "low":
        return max(2*rho-1, .75*rho)
    raise ValueError("scenario must be medium, high or low")


def girr_delta(sensitivities: Iterable[tuple[str, float, float]]) -> dict:
    """MAR21 GIRR yield-curve delta, one curve/currency, full unreduced weights.

    Sensitivity unit is reporting currency per unit DECIMAL rate, not per bp.
    Risk factors are netted before weighting. Inflation/basis not supported here.
    """
    net = {}
    for currency, tenor, sensitivity in sensitivities:
        if not currency or tenor not in GIRR_WEIGHTS:
            raise ValueError("Need a currency and prescribed GIRR tenor")
        key = (currency, float(tenor))
        net[key] = net.get(key, 0.) + _number(sensitivity, "sensitivity")
    factors = [{"currency": c, "tenor": t, "sensitivity": s, "risk_weight": GIRR_WEIGHTS[t],
                "weighted_sensitivity": s*GIRR_WEIGHTS[t]} for (c, t), s in sorted(net.items())]
    by_currency = {c: [x for x in factors if x["currency"] == c] for c, _ in net}
    scenarios = {}
    for scenario in ("medium", "high", "low"):
        buckets = []
        for currency in sorted(by_currency):
            f = by_currency[currency]
            variance = sum(x["weighted_sensitivity"]**2 for x in f)
            for i, x in enumerate(f):
                for y in f[i+1:]:
                    variance += 2*girr_correlation(x["tenor"], y["tenor"], scenario)*x["weighted_sensitivity"]*y["weighted_sensitivity"]
            k = sqrt(max(variance, 0.))
            buckets.append({"currency": currency, "K": k, "S": sum(x["weighted_sensitivity"] for x in f),
                            "within_variance": variance})
        gamma = _correlation_scenario(.5, scenario)
        total = sum(b["K"]**2 for b in buckets)
        total += sum(2*gamma*b["S"]*c["S"] for i, b in enumerate(buckets) for c in buckets[i+1:])
        alternative = total < 0
        if alternative:
            bounded = [min(b["K"], max(-b["K"], b["S"])) for b in buckets]
            total = sum(b["K"]**2 for b in buckets)
            total += sum(2*gamma*s*t for i, s in enumerate(bounded) for t in bounded[i+1:])
        scenarios[scenario] = {"buckets": buckets, "across_correlation": gamma,
                               "alternative_S_used": alternative, "capital_component": sqrt(max(total, 0.))}
    worst = max(scenarios, key=lambda s: scenarios[s]["capital_component"])
    return {"factors": factors, "scenarios": scenarios, "worst_scenario": worst,
            "girr_delta_component": scenarios[worst]["capital_component"],
            "scope": "GIRR yield-curve delta component only; full weights; one curve per currency"}


def regulatory_examples() -> dict:
    trades = [IRTrade("short_receive", 5_000_000., 0., .5, .5, 1, 150_000.),
              IRTrade("medium_pay", 8_000_000., 0., 3., 3., -1, -250_000.),
              IRTrade("long_receive", 10_000_000., 0., 7., 7., 1, 500_000.)]
    unm = sa_ccr_ir(trades)
    marg = sa_ccr_ir(trades, collateral=450_000., mpor_days=10, threshold=0,
                     minimum_transfer=10_000., nica=50_000.)
    separate = sum(sa_ccr_ir([t])["ead"] for t in trades)
    times, exposures, spread = [1., 2., 3.], [600_000., 900_000., 400_000.], .02
    cva = unilateral_cva(times, exposures, spread, .4, .09)
    up = unilateral_cva(times, exposures, spread+.0001, .4, .09)["cva"]
    down = unilateral_cva(times, exposures, spread-.0001, .4, .09)["cva"]
    cva["central_bump_cs01"] = (up-down)/2
    cva["one_bp_loss"] = up-cva["cva"]
    cva["illustrative_hedge_cs01"] = .6*cva["cs01"]
    cva["residual_cs01"] = .4*cva["cs01"]
    single = sa_ccr_ir([IRTrade("single_payment_three_year", 3_000_000., 0., 3., 3., 1, 100_000.)])
    capital = reduced_ba_cva([{"name": "synthetic_IG_industrial", "risk_weight": .03,
                              "netting_sets": [(single["ead"], 3.)]}])
    capital["source_sa_ccr"] = single
    # Hypothetical signed zero-coupon positions; FX-converted PV sensitivity
    # already expressed in the common KES reporting unit, holding FX fixed.
    positions = [("KES", 1., 1_000_000., .09), ("KES", 5., -700_000., .10),
                 ("USD", 2., 900_000., .04), ("USD", 10., -400_000., .05)]
    # MAR21.19 uses the +1bp repricing divided by .0001; keep its finite shift
    # rather than silently substituting an analytic derivative.
    sensitivities = [(c, t, n*exp(-r*t)*expm1(-.0001*t)/.0001) for c, t, n, r in positions]
    frtb = girr_delta(sensitivities)
    frtb["synthetic_positions"] = [{"currency": c, "tenor": t, "signed_reporting_notional": n,
                                    "continuous_zero_rate": r, "pv": n*exp(-r*t),
                                    "analytic_sensitivity_per_decimal": -t*n*exp(-r*t),
                                    "regulatory_one_bp_sensitivity_per_decimal": n*exp(-r*t)*expm1(-.0001*t)/.0001}
                                   for c, t, n, r in positions]
    return {"rule_review_date": "2026-10-01", "liquidity": liquidity_example(),
            "sa_ccr": {"unit": "KES", "unmargined": unm, "margined": marg,
                       "without_netting_ead": separate, "netting_benefit": separate-unm["ead"]},
            "cva_valuation": cva, "wrong_way_risk": wrong_way_example(),
            "reduced_ba_cva": capital, "frtb_girr_delta": frtb}
