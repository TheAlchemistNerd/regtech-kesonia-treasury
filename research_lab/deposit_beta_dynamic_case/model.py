"""Reconciled synthetic monthly bank case. Money is KES; rates are annual decimals.

This is a deterministic expected-cohort cash simulation, not sampled realised defaults.
All transitions, accounting entries and decision rules are explicit in the case note.
"""
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import calendar
import json
import math
from pathlib import Path
from research_lab.benchmark import Calendar, Fixing, schedule, compound
from research_lab.operations import synthetic_deposit_panel, fit_deposit_passthrough, evaluate_deposit_model

HERE = Path(__file__).resolve().parent


def assumptions():
    return json.loads((HERE / 'assumptions.json').read_text(encoding='utf-8'))


def month_start(start, index):
    year, month = start.year + (start.month - 1 + index) // 12, (start.month - 1 + index) % 12 + 1
    return date(year, month, 1)


def logistic(z):
    return 1 / (1 + math.exp(-max(-40, min(40, z))))


def pd_for_capacity(base_pd, coverage, reference_coverage, slope, macro_logodds):
    return min(.95, logistic(math.log(base_pd / (1-base_pd)) + slope * (reference_coverage-coverage) + macro_logodds))


def reserve(principal, remaining, annual_pd, lgd):
    """Undiscounted 12-month expected principal loss on scheduled amortisation.

    Annual PD converts to a constant monthly hazard; declining exposure and survival
    are retained. A simplified management allowance, with no IFRS 9 staging claim.
    """
    if remaining <= 0 or principal <= 0:
        return 0.0
    h = 1-(1-annual_pd)**(1/12)
    return lgd * sum(principal*(1-k/remaining)*(1-h)**k*h for k in range(min(12, remaining)))


def static_bridge():
    initial = 100e6*.13-80e6*.04-10e6*.10
    repricing = 100e6*.02-80e6*.02*.35-10e6*.02
    replacement = 8e6*(.12-.047)
    extra_el = 100e6*(.04-.02)*.45
    return dict(initial_nii=initial, repricing_gain=repricing, replacement_cost=replacement,
                extra_expected_loss=extra_el, net_change=repricing-replacement-extra_el)


def source_models():
    panel = synthetic_deposit_panel()
    train = [x for x in panel if x['date'] < '2025-01-01']
    future = [x for x in panel if x['date'] >= '2025-01-01']
    fitted = fit_deposit_passthrough(train)
    return {'fit': fitted, 'future_holdout': evaluate_deposit_model(fitted, future),
            'source': 'research_lab.operations; frozen synthetic training through 2024-12-01',
            'application': 'Up/down and lag coefficients reused. Intercept set to zero to avoid deterministic rate drift.'}


def benchmark_schedule(cfg, shocks):
    start = date.fromisoformat(cfg['start_date'])
    cal = Calendar()  # Weekends only: a synthetic contract calendar.
    end = month_start(start, cfg['months'])
    fixings = []
    cursor = start-timedelta(days=20)
    while cursor <= end+timedelta(days=3):
        idx = (cursor.year-start.year)*12+cursor.month-start.month
        market = cfg['market_rate'] + (shocks['rate_shock'] if idx+1 >= cfg['shock_month'] else 0)
        if cal.business(cursor):
            available = datetime.combine(cal.next(cursor), datetime.min.time(), timezone.utc)
            fixings.append(Fixing(cursor, available, Decimal(str(market)), 'synthetic-monthly-path-v1'))
        cursor += timedelta(days=1)
    result = []
    for i in range(cfg['months']):
        a,b = month_start(start,i),month_start(start,i+1)
        rows = schedule(a,b,cal,lookback=5,observation_shift=False)
        cutoff = datetime.combine(b+timedelta(days=5),datetime.min.time(),timezone.utc)
        x = compound(rows,fixings,cutoff,Decimal('1'))
        result.append({'month':i+1,'start':a.isoformat(),'end':b.isoformat(),'days':(b-a).days,
                       'annualised_reference':float(x['annualised_period_rate']),
                       'market_rate':cfg['market_rate']+(shocks['rate_shock'] if i+1>=cfg['shock_month'] else 0)})
    return result


def validate(cfg):
    if not 1 <= cfg['months'] <= 120:
        raise ValueError('Use one to 120 monthly periods')
    if not 0 < cfg['lgd'] < 1 or cfg['recovery_lag_months'] < 1:
        raise ValueError('LGD must be in (0,1) and recoveries must follow default')
    if cfg['interest_settlement_lag_months'] not in (0,1):
        raise ValueError('Interest settlement lag must be zero or one month')
    if cfg['cash_floor'] < 0 or cfg['wholesale_limit'] < 0:
        raise ValueError('Cash and funding limits must be nonnegative')
    if sum(x['balance'] for x in cfg['deposits']) <= 0:
        raise ValueError('Opening deposits are required')
    for x in cfg['loans']:
        if x['balance'] <= 0 or not 0 < x['annual_pd'] < 1 or x['tenor_months'] < 1:
            raise ValueError('Invalid opening loan cohort')
    def visit(obj):
        if isinstance(obj,dict):
            for v in obj.values(): visit(v)
        elif isinstance(obj,list):
            for v in obj: visit(v)
        elif isinstance(obj,float) and not math.isfinite(obj): raise ValueError('Finite inputs required')
    visit(cfg)


def run_case(scenario='baseline', policy='standard', cfg=None, fitted=None):
    cfg = deepcopy(cfg or assumptions()); validate(cfg)
    if scenario not in cfg['scenarios'] or policy not in cfg['policies']:
        raise ValueError('Unknown scenario or policy')
    shock = cfg['scenarios'][scenario]; pol = cfg['policies'][policy]
    rates = benchmark_schedule(cfg,shock)
    fitted = fitted or source_models()['fit']
    coefs = {p:fitted[s]['coefficients'] for p,s in [('operating','operating'),('savings','rate_sensitive')]}
    rates_paid = {x['product']:x['rate'] for x in cfg['deposits']}
    base_paid = dict(rates_paid)
    deposits = [dict(x,id='original_'+x['product'],original=True,maturity=6 if x['product']=='term' else 0) for x in cfg['deposits']]
    loans = []
    def new_loan(template,balance,m):
        ref = cfg['market_rate'] if m == 0 else rates[m-1]['annualised_reference']
        return dict(id=f"{template['name']}_{m}",name=template['name'],balance=balance,
                    original_balance=balance,remaining=template['tenor_months'],tenor=template['tenor_months'],
                    annual_pd=template['annual_pd'],last_pd=template['annual_pd'],spread=template['spread'],
                    rate=ref+template['spread'],reset_months=template['reset_months'],originated=m,
                    cash_per_original=template['reference_coverage']*(1/template['tenor_months']+(cfg['market_rate']+template['spread'])/12),
                    reference_coverage=template['reference_coverage'])
    for x in cfg['loans']: loans.append(new_loan(x,x['balance'],0))
    wholesale = [dict(id='opening',balance=cfg['opening_wholesale'],rate=cfg['market_rate']+cfg['wholesale_spread'],maturity=3)]
    workout=[]; interest_due=0.0; cash=cfg['opening_cash']
    allowance = sum(reserve(x['balance'],x['remaining'],x['last_pd'],cfg['lgd']) for x in loans)
    equity = cash+sum(x['balance'] for x in loans)-allowance-sum(x['balance'] for x in deposits)-sum(x['balance'] for x in wholesale)
    opening_equity=equity; opening_allowance=allowance; monthly=[]; loan_rows=[]; deposit_rows=[]; events=[]
    previous_market=cfg['market_rate']; lag_delta=0.0
    for meta in rates:
        m=meta['month']; dt=meta['days']/365; market=meta['market_rate']
        stressed=m>=cfg['shock_month']
        ocash,oeq,oallow,oirec=cash,equity,allowance,interest_due
        oloans=sum(x['balance'] for x in loans); owork=sum(x['balance'] for x in workout)
        odeps=sum(x['balance'] for x in deposits); owhole=sum(x['balance'] for x in wholesale)
        delta=market-previous_market
        # Rate offers: coefficients use annual decimals consistently with the bp regression.
        for product in ('operating','savings'):
            c=coefs[product]
            change=c['beta_up']*max(delta,0)+c['beta_down']*min(delta,0)+c['lag_beta_up']*max(lag_delta,0)+c['lag_beta_down']*min(lag_delta,0)
            rates_paid[product]=max(cfg['deposit_rate_floor'],rates_paid[product]+change)
        rates_paid['term']=max(cfg['deposit_rate_floor'],base_paid['term']+(market-cfg['market_rate']))
        premium=pol['savings_premium'] if m>=cfg['shock_month'] else 0.0
        offer={**rates_paid,'savings':rates_paid['savings']+premium}
        depinterest=0.0; withdrawals=0.0; migration=0.0; orig_withdrawals=0.0; dep_residual=0.0
        # Flows occur at period end. All opening money earns the applicable full-period rate.
        for d in list(deposits):
            opening=d['balance']; p=d['product']; due=p!='term' or m>=d['maturity']
            if p!='term': d['rate']=offer[p]
            elif m>d['maturity']: raise AssertionError('Term deposit missed renewal')
            paid_rate=d['rate']
            depinterest+=opening*paid_rate*dt
            gap=max(0,(market-offer[p])-(cfg['market_rate']-base_paid[p]))
            base=cfg['deposit_flows'][p]
            leave=min(.9,base['runoff']+base['gap_sensitivity']*gap+(shock['extra_runoff'] if stressed else 0)) if due else 0.0
            external=opening*leave
            move=0.0
            if p=='savings':
                yieldgap=max(0,(offer['term']-offer['savings'])-(base_paid['term']-base_paid['savings']))
                frac=min(.5,base['migration']+cfg['migration_gap_sensitivity']*yieldgap)
                move=(opening-external)*frac
            d['balance']-=external+move
            withdrawals+=external; migration+=move; orig_withdrawals+=external if d['original'] else 0
            if move:
                deposits.append(dict(id=f"migration_{m}_{d['id']}",product='term',balance=move,rate=offer['term'],maturity=m+cfg['deposit_term_months'],original=d['original']))
            if p=='term' and due:
                d['rate']=offer['term']; d['maturity']=m+cfg['deposit_term_months']
            dep_residual+=opening-external-move-d['balance']
            deposit_rows.append(dict(month=m,cohort_id=d['id'],product=p,original=d['original'],opening=opening,paid_rate=paid_rate,
                                     external_withdrawal=external,internal_migration=move,closing=d['balance'],maturity_month=d['maturity']))
        inflow=0.0
        for p,base in cfg['deposit_flows'].items():
            amount=base['new_inflow']*(shock['inflow_multiplier'] if stressed else 1)
            inflow+=amount
            deposits.append(dict(id=f'new_{p}_{m}',product=p,balance=amount,rate=offer[p],maturity=m+cfg['deposit_term_months'] if p=='term' else 0,original=False))
        # Existing wholesale funding pays interest, then matures. New funding begins earning next month.
        wholeinterest=sum(x['balance']*x['rate']*dt for x in wholesale)
        maturity=sum(x['balance'] for x in wholesale if x['maturity']==m)
        wholesale=[x for x in wholesale if x['maturity']>m]
        loaninterest=0.0; principalpaid=0.0; defaults=0.0; dscr_sum=0.0; pd_sum=0.0
        for x in loans:
            opening=x['balance']
            if opening<1e-8 or x['remaining']<=0: continue
            age=m-x['originated']
            reset=(age-1)%x['reset_months']==0
            if reset: x['rate']=meta['annualised_reference']+x['spread']
            scheduled=opening/x['remaining']
            cash_available=x['original_balance']*x['cash_per_original']*(shock['cash_multiplier'] if stressed else 1)
            coverage=cash_available/(scheduled+opening*x['rate']*dt)
            pd=pd_for_capacity(x['annual_pd'],coverage,x['reference_coverage'],cfg['pd_coverage_slope'],shock['macro_logodds'] if stressed else 0)
            hazard=1-(1-pd)**dt
            default=opening*hazard
            surviving=opening-default
            paid=surviving/x['remaining']
            interest=surviving*x['rate']*dt
            x['balance']=surviving-paid; x['remaining']-=1; x['last_pd']=pd
            # Original cash capacity and loan size scale with surviving mass; no survivor windfall.
            x['original_balance']*=1-hazard
            loaninterest+=interest; principalpaid+=paid; defaults+=default
            dscr_sum+=opening*coverage; pd_sum+=opening*pd
            workout.append(dict(balance=default,due=m+cfg['recovery_lag_months'],cohort=x['id']))
            loan_rows.append(dict(month=m,cohort_id=x['id'],opening=opening,loan_rate=x['rate'],reset=reset,
                                  cfads=cash_available,scheduled_service=scheduled+opening*x['rate']*dt,dscr=coverage,
                                  annual_pd=pd,period_hazard=hazard,default_transfer=default,principal_received=paid,
                                  interest_accrued=interest,closing=x['balance'],remaining=x['remaining']))
        recovery_principal=sum(x['balance'] for x in workout if x['due']==m)
        recoveries=recovery_principal*(1-cfg['lgd']); writeoffs=recovery_principal*cfg['lgd']
        workout=[x for x in workout if x['due']>m]
        interest_cash=interest_due if cfg['interest_settlement_lag_months']==1 else loaninterest
        interest_due=loaninterest if cfg['interest_settlement_lag_months']==1 else 0.0
        cashinterest=max(0,ocash)*cfg['cash_yield']*dt
        cash+=interest_cash+cashinterest+principalpaid+recoveries+inflow-withdrawals-depinterest-wholeinterest-maturity-cfg['monthly_operating_cost']
        issuance=0.0
        # A specified committee plan executed at month 2, paired across scenarios.
        if m==pol['prefund_month'] and pol['term_prefund']>0:
            amount=min(pol['term_prefund'],max(0,cfg['wholesale_limit']-sum(x['balance'] for x in wholesale)))
            wholesale.append(dict(id=f'term_policy_{m}',balance=amount,rate=market+cfg['term_spread'],maturity=m+pol['term_months']))
            issuance+=amount; cash+=amount
            events.append(dict(month=m,event='PREAPPROVED_TERM_FUNDING',amount=amount,actor='Treasury',approval='ALCO synthetic policy fixture'))
        available_headroom=max(0,cfg['wholesale_limit']-sum(x['balance'] for x in wholesale))
        if cash<cfg['cash_floor']:
            draw=min(cfg['cash_floor']-cash,available_headroom)
            wholesale.append(dict(id=f'replacement_{m}',balance=draw,rate=market+cfg['wholesale_spread'],maturity=m+cfg['wholesale_tenor_months']))
            issuance+=draw; cash+=draw
        provisional_allowance=sum(reserve(x['balance'],x['remaining'],x['last_pd'],cfg['lgd']) for x in loans)+sum(x['balance']*cfg['lgd'] for x in workout)
        nii=loaninterest+cashinterest-depinterest-wholeinterest
        provisional_equity=oeq+nii-cfg['monthly_operating_cost']-(provisional_allowance-oallow+writeoffs)
        # End-month origination uses current observed snapshot. No current-month interest.
        target=cfg['new_lending_per_month']*pol['origination_multiplier']
        template=cfg['new_loan']
        initial_coverage=template['reference_coverage']*(1/template['tenor_months']+(cfg['market_rate']+template['spread'])/12)/(1/template['tenor_months']+(meta['annualised_reference']+template['spread'])/12)
        newpd=pd_for_capacity(template['annual_pd'],initial_coverage*(shock['cash_multiplier'] if stressed else 1),template['reference_coverage'],cfg['pd_coverage_slope'],shock['macro_logodds'] if stressed else 0)
        loss_per_unit=reserve(1,template['tenor_months'],newpd,cfg['lgd'])
        existing_rwa=sum(x['balance'] for x in loans)+sum(x['balance'] for x in workout)
        capital_capacity=max(0,(provisional_equity-cfg['capital_floor']*existing_rwa)/(cfg['capital_floor']+loss_per_unit))
        available_headroom=max(0,cfg['wholesale_limit']-sum(x['balance'] for x in wholesale))
        liquidity_capacity=max(0,cash-cfg['cash_floor']+available_headroom)
        originations=min(target,capital_capacity,liquidity_capacity)
        draw=max(0,cfg['cash_floor']+originations-cash)
        if draw:
            wholesale.append(dict(id=f'origination_funding_{m}',balance=draw,rate=market+cfg['wholesale_spread'],maturity=m+cfg['wholesale_tenor_months']))
            issuance+=draw; cash+=draw
        cash-=originations
        if originations>0:
            x=new_loan(template,originations,m); x['last_pd']=newpd; loans.append(x)
        allowance=provisional_allowance+originations*loss_per_unit
        expense=allowance-oallow+writeoffs
        profit=nii-cfg['monthly_operating_cost']-expense; equity=oeq+profit
        gross=sum(x['balance'] for x in loans); work=sum(x['balance'] for x in workout)
        deps=sum(x['balance'] for x in deposits); whole=sum(x['balance'] for x in wholesale)
        assets=cash+gross+work+interest_due-allowance
        cf=interest_cash+cashinterest+principalpaid+recoveries+inflow+issuance-withdrawals-depinterest-wholeinterest-maturity-cfg['monthly_operating_cost']-originations
        row=dict(scenario=scenario,policy=policy,**meta,opening_cash=ocash,cash=cash,gross_loans=gross,workout_gross=work,
                 allowance=allowance,interest_receivable=interest_due,total_assets=assets,deposits=deps,wholesale=whole,equity=equity,
                 earning_exposure_years=(oloans+max(0,ocash))*dt,loan_interest_accrued=loaninterest,loan_interest_received=interest_cash,cash_interest=cashinterest,deposit_interest=depinterest,
                 wholesale_interest=wholeinterest,nii=nii,cash_nii=interest_cash+cashinterest-depinterest-wholeinterest,
                 operating_cost=cfg['monthly_operating_cost'],impairment_expense=expense,profit=profit,originations=originations,
                 lending_requested=target,lending_deferred=target-originations,principal_received=principalpaid,
                 default_transfer=defaults,recoveries=recoveries,writeoffs=writeoffs,external_withdrawals=withdrawals,
                 original_cohort_withdrawals=orig_withdrawals,new_deposits=inflow,internal_migration=migration,
                 wholesale_maturity=maturity,wholesale_issued=issuance,operating_rate=offer['operating'],savings_rate=offer['savings'],term_offer=offer['term'],
                 average_dscr=dscr_sum/oloans if oloans else 0,average_pd=pd_sum/oloans if oloans else 0,
                 original_deposits_remaining=sum(x['balance'] for x in deposits if x['original']),
                 term_deposits=sum(x['balance'] for x in deposits if x['product']=='term'),
                 cash_floor_gap=max(0,cfg['cash_floor']-cash),capital_proxy=equity/(gross+work) if gross+work else 0,
                 balance_sheet_residual=assets-deps-whole-equity,cash_residual=cash-ocash-cf,
                 loan_residual=gross-oloans+defaults+principalpaid-originations,
                 workout_residual=work-owork-defaults+recovery_principal,
                 deposit_residual=deps-odeps-inflow+withdrawals,
                 allowance_residual=allowance-oallow-expense+writeoffs,
                 interest_residual=interest_due-oirec-loaninterest+interest_cash,
                 wholesale_residual=whole-owhole-issuance+maturity,
                 equity_residual=equity-oeq-profit)
        monthly.append(row)
        previous_market=market; lag_delta=delta
    summary={k:sum(r[k] for r in monthly) for k in ('nii','cash_nii','profit','impairment_expense','originations','lending_deferred','default_transfer','recoveries','writeoffs','external_withdrawals','internal_migration','deposit_interest','wholesale_interest')}
    summary['annualised_nim']=summary['nii']/sum(x['earning_exposure_years'] for x in monthly)
    summary.update(scenario=scenario,policy=policy,months=cfg['months'],opening_equity=opening_equity,opening_allowance=opening_allowance,
                   closing_equity=equity,closing_cash=cash,closing_deposits=deps,closing_wholesale=whole,closing_gross_loans=gross,
                   closing_workout=work,closing_allowance=allowance,closing_interest_receivable=interest_due,
                   peak_wholesale=max(r['wholesale'] for r in monthly),minimum_cash=min(r['cash'] for r in monthly),
                   minimum_capital_proxy=min(r['capital_proxy'] for r in monthly),cash_floor_breaches=sum(r['cash_floor_gap']>1e-6 for r in monthly),
                   maximum_reconciliation_error=max(abs(r[k]) for r in monthly for k in r if k.endswith('_residual')),
                   feasible=all(r['cash_floor_gap']<1e-6 and r['capital_proxy']>=cfg['capital_floor']-1e-8 for r in monthly))
    return {'summary':summary,'monthly':monthly,'loans':loan_rows,'deposits':deposit_rows,'events':events}
