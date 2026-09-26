"""Independent arithmetic checks for the teaching cases, not a production model."""
from decimal import Decimal as D, getcontext
from pathlib import Path
import json

getcontext().prec = 32
out = Path(__file__).resolve().parent

fixing = D('0.094618')
factor = fixing * 3 / 365
index_factor = D('100.18235974') / D('100.10451025') - 1
benchmark_interest = D(1000000) * factor
index_interest = D(1000000) * index_factor
spread_interest = D(1000000) * D('.03') * 3 / 365
assert abs(benchmark_interest-index_interest) < D('.0001')

spots = [D('.03'), D('.035'), D('.04')]
discounts = [(1+r) ** (-t) for t,r in enumerate(spots,1)]
forward_12 = discounts[0]/discounts[1]-1
forward_23 = discounts[1]/discounts[2]-1
par_coupon = (1-discounts[-1])/sum(discounts)
assert abs(par_coupon*sum(discounts)+discounts[-1]-1) < D('1e-28')

weights=[D('.2'),D('.3'),D('.5')]
yields=[D('.03'),D('.0375'),D('.045')]
roll_months=[3,24,60]
initial=sum(w*r for w,r in zip(weights,yields))
increment=sum(w*D('.02')/m for w,m in zip(weights,roll_months))
month1=initial+increment
assert initial==D('.03975') and month1==D('.0415')
ladder_nii={str(beta): D(1000000000)*(increment-beta*D('.02')) for beta in [D('.25'),D('.75')]}
assert ladder_nii['0.25']==D('-3250000')

# Single-currency, non-reinvested one-year pricing bridge, KES thousands.
funding,operating,loss,capital_hurdle,fees,benchmark,H=map(D,['100','20','15','10','5','90','1000'])
margin=(funding+operating+loss+capital_hurdle-fees-benchmark)/H
customer_interest=benchmark+margin*H
pretax_return=customer_interest+fees-funding-operating-loss
assert margin==D('.05') and pretax_return==capital_hurdle

# One starting bank balance sheet; independent sensitivity experiments, KES millions.
assets,liabilities,equity=map(D,['1000','900','100'])
assert assets==liabilities+equity
nii_base=D(800)*D('.1')+D(200)*D('.06')-D(900)*D('.035')
nii_changes={str(beta): D(200)*D('.02')-D(900)*beta*D('.02') for beta in [D('.25'),D('.75')]}
eve_changes={str(duration): -(D(800)*3+D(200)*D('.25')-D(900)*duration)*D('.02') for duration in [D(2),D('.5')]}
cash_after=D(70)+D(10)-D(90)-D(20)-D(5)
assert nii_base==D('60.5') and nii_changes['0.25']==D('-.5') and nii_changes['0.75']==D('-9.5')
assert eve_changes['2']==D('-13') and eve_changes['0.5']==D('-40') and cash_after==D('-35')

df=list(map(D,['.95','.90','.85']))
ee=list(map(D,['5000000','3500000','1500000']))
pd=list(map(D,['.01','.015','.02']))
stress_ee=list(map(D,['12000000','8000000','4000000']))
stress_pd=list(map(D,['.06','.08','.10']))
cva=D('.6')*sum(d*e*p for d,e,p in zip(df,ee,pd))
cva_stress=D('.6')*sum(d*e*p for d,e,p in zip(df,stress_ee,stress_pd))
assert cva==D(72150) and cva_stress==D(960000)

result={
 'status':'All assertions passed; illustrative arithmetic only',
 'historical_benchmark':{'factor':factor,'index_factor':index_factor,'benchmark_interest':benchmark_interest,'index_interest':index_interest,'difference_KES':index_interest-benchmark_interest,'hypothetical_spread_interest':spread_interest,'hypothetical_total_interest':benchmark_interest+spread_interest},
 'curve':{'discount_factors':discounts,'forward_1_to_2':forward_12,'forward_2_to_3':forward_23,'par_coupon_3y':par_coupon},
 'deposit_ladder':{'initial_yield':initial,'month_one_yield':month1,'annualised_nii_change_by_beta':ladder_nii},
 'pricing_KES_thousands':{'margin_decimal':margin,'interest':customer_interest,'income_with_fees':customer_interest+fees,'return_before_capital_hurdle':pretax_return,'economic_surplus_after_hurdle':pretax_return-capital_hurdle},
 'bank_KES_millions':{'initial_nii':nii_base,'nii_change_by_beta':nii_changes,'eve_change_by_deposit_duration':eve_changes,'cash_after_stress':cash_after,'additional_funding_to_zero':-cash_after},
 'cva_currency_units':{'base':cva,'stress':cva_stress,'change':cva_stress-cva},
}
(out/'checked_examples.json').write_text(json.dumps(result,indent=2,default=str),encoding='utf-8')
print(json.dumps(result,indent=2,default=str))
