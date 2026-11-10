> **Historical review, 25 September 2026.** For current executable evidence and open requirements, use the [1 October implementation register](../../docs/methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md). The dated review below retains its original scope.

# KESONIA and treasury: derivations and checked teaching cases

**25 September 2026 · Companion to the detailed material review**

The cases below establish reusable calculations and teaching examples. Except for the explicitly sourced historical benchmark observations, numbers are **hypothetical**, not current market quotations, portfolio findings or regulatory thresholds. The [independent calculation script](<verify_examples.py>) produces [checked results](<checked_examples.json>). It does not execute code embedded in the pasted conversation or the draft articles.

## 1. One dictionary before any formula

| Symbol | Meaning | Unit or boundary |
|---|---|---|
| $r_i$ | Applicable overnight fixing | Annual decimal rate |
| $n_i$ | Days to which that fixing applies | Calendar days after the approved observation mapping |
| $A_j$ | Accumulation factor through interval $j$ | Dimensionless; begins at 1 |
| $R_{KES}$ | Annualised compounded benchmark for a specified period | Annual rate; not a full customer APR |
| $k$ | Customer margin in this example | Annual rate; separate from allocated capital |
| $B_t$ | Interest-bearing principal | Currency, on a specified date |
| $D(0,t)$ | Discount factor | Price of one future currency unit under a stated valuation basis |
| $EC_t$ | Allocated economic capital | Currency; distinct from a prudential requirement |
| $S(t)$ | Survival probability | Probability under a stated measure and event definition |
| $CCR_{cp}$ | Counterparty credit risk | Risk category; avoid using “CCR” for both this and a compounded rate |

The official “K” premium can be written $K_{RBCP}$ where needed, following the controlled Mwendo chapter. Use $K_{cap}$ for capital. All results need a date, horizon, entity, currency and calculation version.

## 2. From an overnight fixing to period interest

For a constant principal and an approved sequence of rate/day-weight pairs, on ACT/365:

$$A_j=\prod_{i=1}^{j}\left(1+r_i\frac{n_i}{365}\right),\qquad F=A_n-1.$$

For total interest-period length $d$, where the mapping makes these weights cover that period:

$$R_{KES}=F\frac{365}{d}.$$

If the contract adds its margin simply, rather than compounding the margin:

$$I=B_0F+B_0k\frac{d}{365}.$$

This follows directly from accumulating the benchmark return and adding the separately defined margin accrual. A contract that compounds the full rate needs a different calculation. For fixed $B_0$, interval accrual can be reconciled through:

$$\Delta I_j=B_0(A_j-A_{j-1})+B_0k\frac{n_j}{365}.$$

Summing these increments returns period interest. Multiplying the final annualised period rate by each day's principal is not a general substitute for this calculation. With changing principal, adopt the product's explicit balance/accrual rule and partition the ledger at every relevant balance event.

### Historical verification: 5–8 September 2025

CBK lists the 5 September fixing as **9.4618%**. Its published index is **100.10451025** on 5 September and **100.18235974** on 8 September. [CBK fixing series](https://www.centralbank.go.ke/kesonia/), [CBK compounded index](https://www.centralbank.go.ke/kesonia-compounded-index/).

The three-day observation-span factor from the fixing is:

$$F_{fixing}=0.094618\frac{3}{365}=0.00077768219178.$$

The index comparison is:

$$F_{index}=\frac{100.18235974}{100.10451025}-1=0.00077768214245.$$

On a hypothetical KES 1 million, the two methods give KES 777.68219178 and KES 777.68214245: a difference of about **KES 0.00004933**, consistent with using rounded published index values. Both round to KES 777.68. Adding a hypothetical simple 3% margin for the same three days gives KES 246.57534247, and total illustrative interest of **KES 1,024.26**.

This verifies the **historical benchmark observation span**. It is not a customer invoice and does not demonstrate a complete five-day-lookback contract. That requires a separate mapping from the customer's accrual dates to these or other observation dates. An index ratio is an independent check only when its boundaries, day weights and conventions match the calculation being verified.

### Implementation specification for Part 2

1. Read the contract and interest-period version, including date endpoints and margin rule.
2. Create accrual intervals on a half-open date basis: start included, end excluded.
3. Resolve observation dates using the approved lookback/calendar convention. Preserve both observation and accrual dates.
4. Join observations by value date and by the information available at the calculation cutoff. Keep republications as new versions.
5. Partition intervals for balance events; clip weekend/holiday spans at period endpoints.
6. Validate coverage, uniqueness, units, positive factors and approved fallback status.
7. Calculate factors and cash; retain sufficient internal precision and round at defined output points.
8. Compare with an independent calculation, approve the result, and post/reconcile the identified version.

For the fixed-principal benchmark calculation, an aggregate such as `expm1(sum(log1p(rate × days / 365)))` is numerically useful. SQL syntax and decimal precision depend on the database. The primary grouping key must include contract and interest period. This is an algorithmic specification, not a deployable replacement for Part 2's SQL.

## 3. From spot rates to discount factors, forwards and par coupons

Assume annual compounding, annual payments, one currency, and hypothetical spot rates of 3%, 3.5% and 4% at years 1, 2 and 3.

$$D(0,t)=(1+z_t)^{-t},\qquad f_{a,b}=\left(\frac{D(0,a)}{D(0,b)}\right)^{1/(b-a)}-1.$$

| Maturity | Spot rate | Discount factor |
|---|---:|---:|
| 1 year | 3.0000% | 0.9708737864 |
| 2 years | 3.5000% | 0.9335107004 |
| 3 years | 4.0000% | 0.8889963587 |

The implied one-year forward from year 1 to 2 is **4.002427%**; from year 2 to 3 it is **5.007258%**. A three-year instrument with annual coupons and unit redemption prices at par when:

$$1=c\sum_{t=1}^{3}D(0,t)+D(0,3),\qquad c=3.973810\%.$$

The forward rates and par coupon are different descriptions derived from these assumptions. They are not additional observed Kenyan rates. A production curve needs instrument-specific day counts, settlement, calendars, interpolation, instrument repricing checks and a documented extrapolation policy. A forecasting curve may also differ from the discounting curve.

**Business use:** compare a borrower's projected reset payments with the dates of receipts; compare the lender's expected asset cash with its financing schedule. Keep a frozen-base scenario and alternative rate paths so the reader sees sensitivity rather than mistaking one curve for a prediction.

## 4. From monetary economics to a customer margin

Define the exposure-time denominator over the pricing horizon:

$$H=\sum_t E[B_t^{interest}]\Delta t.$$

In an undiscounted teaching model with a simply accrued margin, let $I_b$ be expected benchmark interest, $F_f$ expected fee income, $C_f$ funding cost, $C_o$ operating cost, $L$ expected credit loss and $hEC$ the required capital return. Solve:

$$I_b+kH+F_f-C_f-C_o-L=hEC,$$

so that:

$$k=\frac{C_f+C_o+L+hEC-F_f-I_b}{H}.$$

The numerator is money and the denominator is money-years. Their ratio is an annual rate. Interest collectibility, loss definition and balance forecasting must be mutually consistent; do not count unpaid interest both as absent income and again as the same loss. A discounted lifetime version needs dated cash flows and a specified hurdle methodology. Avoid adding a capital hurdle charge again if the same required return is already fully embedded in the chosen valuation criterion.

### One-year illustration, KES thousands

Assume a constant 1,000 interest-bearing balance for a year; 90 benchmark interest; 100 funding cost; 20 operating cost; 15 principal credit loss; 5 fees; and 10 required return on 50 allocated capital. Interest is assumed fully collectible for this simplified illustration, and taxes are omitted.

| Item | Amount |
|---|---:|
| Benchmark interest | 90 |
| Required margin income | 50 |
| Total interest | 140 |
| Fees | 5 |
| Funding, operating cost and expected loss | 135 |
| Return before the capital hurdle | 10 |
| Economic surplus after the hurdle | 0 |

The required margin is **5%**, producing 14% interest plus the separately stated fee. The 10 return equals a hypothetical 20% pre-tax capital hurdle on 50. This is not an APR calculation or an accounting recognition schedule. It demonstrates why the benchmark-to-customer spread must be reconciled to the institution's costs before being described as profit.

An internal FTP charge can allocate the funding component across departments. In a consolidated lender model, eliminate internal transfers and retain external funding costs once. For an SPV, the actual note coupon and expenses enter the cash waterfall; an internal valuation hurdle does not become a cash payment.

## 5. Deposit replication: maturity and rate pass-through

Assume a hypothetical 1 billion deposit-funded replication portfolio. Allocate 20% to three-month instruments yielding 3%, 30% to two-year instruments yielding 3.75%, and 50% to five-year instruments yielding 4.5%. Each bucket is initially spread uniformly across its monthly maturity rungs.

The opening weighted yield is:

$$0.2(0.03)+0.3(0.0375)+0.5(0.045)=3.975\%.$$

After a parallel 2-percentage-point rise, only maturing rungs reinvest at the new rate. At the end of month one, the annualised yield increases by:

$$0.02\left(\frac{0.2}{3}+\frac{0.3}{24}+\frac{0.5}{60}\right)=0.175\%.$$

The resulting annualised yield is **4.15%**. If all three-month exposure had instead matured immediately, the result would differ; the schedule must state which structure it represents.

With immediate deposit-rate pass-through $\beta$, deposit cost increases by $\beta\times2\%$. Holding balances fixed, the month-one annualised NII change is:

| Assumed beta | Annualised deposit-cost increase | Annualised asset-income increase | NII change |
|---|---:|---:|---:|
| 25% | 5.00 million | 1.75 million | −3.25 million |
| 75% | 15.00 million | 1.75 million | −13.25 million |

These are **annualised run rates at month one**, not realised full-year earnings. Forecast subsequent rollovers and rate changes to obtain actual period income. Re-estimate balance retention separately: stable balances are not legally locked funding, and a low beta is not proof of a long behavioural maturity.

## 6. One opening balance sheet, three different risk views

This separate example uses KES millions. Opening assets are 800 fixed-rate loans and 200 liquid assets; deposits are 900 and equity is 100. Loan yield is 10%, liquid-asset yield 6%, and deposit cost 3.5%. Opening annualised NII is **60.5**. Ignore fees, losses, operating costs and taxes for this sensitivity exercise.

### Earnings view

Apply a hypothetical +2 percentage-point rate shock, with loans unchanged over the horizon, liquid-asset income fully repricing and deposits repricing by beta. Hold balances constant:

$$\Delta NII=200(0.02)-900\beta(0.02).$$

The annualised change is **−0.5** at beta 25% and **−9.5** at beta 75%. A 12-month forecast requires an explicit reset schedule; these calculations assume the stated repricing effects apply throughout that year.

### Economic-value view

Assume modified durations of 3 years for loans, 0.25 for liquid assets and 2 for deposits. For a parallel shock, a first-order approximation is:

$$\Delta EVE\approx-\left(\sum_a V_aD_a-\sum_l V_lD_l\right)\Delta y.$$

This gives **−13**. If an alternative behavioural assumption shortens deposit duration to 0.5 years, it gives **−40**. The weighted liability contribution matters; subtracting unweighted asset and liability durations would not reproduce these results.

These are alternative sensitivities at the opening snapshot. They do not automatically determine an accounting equity write-down, a share-price change or today's cash requirement. Full valuation should reprice cash flows, including options and curve shape; the linear approximation omits convexity.

### Cash view

Within the 200 liquid-asset balance, assume only 70 can actually be made available inside the stress window without further financing or sale. Add 10 receipts. Assume 90 deposit withdrawals, 20 committed loan draws and 5 hedge-collateral payments:

$$Cash_{end}=70+10-90-20-5=-35.$$

Additional funding of **35** is needed merely to reach zero, and more would be needed for a positive minimum buffer. Specify saleability, haircuts, encumbrance and facility conditions before counting additional sources.

The cash stress changes balances. Its withdrawals and replacement funding would therefore require a new NII forecast and valuation. **Do not add the three outputs together or describe them as one fully integrated simulation.** They demonstrate separate views of the same opening balance sheet; the proposed laboratory must reconcile their evolving paths.

## 7. Optionality, hedging and counterparty exposure

For an instrument with path-dependent prepayment, an option-adjusted spread $s$ can be defined implicitly by a valuation equation such as:

$$P_{market}=E^{\mathbb Q}\left[\sum_t D_{\omega}(0,t)e^{-st}CF_{\omega,t}\right].$$

Specify the interest-rate process, risk-neutral calibration, prepayment model and cash-flow conventions before solving. OAS is model-dependent. A historical refinancing response estimated under the real-world measure cannot be transferred to valuation without explaining how it is used. US mortgage prepayment conventions can be teaching benchmarks; Kenyan product behaviour needs its own evidence.

A receive-floating/pay-fixed swap may offset part of the rate-up exposure of a fixed-rate asset funded by repricing liabilities. Size it using the relevant cash-flow and sensitivity analysis. Then show basis risk, changing notionals, costs, collateral and counterparty exposure. An economic hedge and accounting hedge designation are distinct decisions.

### CVA teaching calculation

For this simplified independent-exposure/default example, use undiscounted expected positive exposure $EE_j$, deterministic discount factors $D_j$, constant LGD and **unconditional marginal** default probabilities $\Delta PD_j$:

$$CVA\approx LGD\sum_jD_jEE_j\Delta PD_j.$$

| Annual interval | $D_j$ | Base $EE_j$ | Base $\Delta PD_j$ | Stress $EE_j$ | Stress $\Delta PD_j$ |
|---|---:|---:|---:|---:|---:|
| 1 | 0.95 | 5,000,000 | 1.0% | 12,000,000 | 6.0% |
| 2 | 0.90 | 3,500,000 | 1.5% | 8,000,000 | 8.0% |
| 3 | 0.85 | 1,500,000 | 2.0% | 4,000,000 | 10.0% |

With LGD 60%, base CVA is **72,150**, stressed CVA **960,000**, and the increase **887,850**, in the same currency units as exposure. These are recalculated teaching values. Do not discount $EE$ again if it already includes discounting. If input probabilities are conditional hazards $q_j$, first obtain marginal probabilities $S(t_{j-1})q_j$. With wrong-way risk, exposure and default must be evaluated jointly rather than factored as above.

CVA valuation, counterparty exposure measures and prudential CVA capital are separate outputs. The advanced module should specify each independently; this example makes no capital-compliance calculation.

## 8. How these cases become empirical work

Use a longitudinal contract panel joined to rates and events by information-availability date. Estimate deposit pass-through and retention separately; estimate prepayment, default, cure and recovery timing using appropriate competing states. Reserve later periods and unseen vintages for validation. Fit transformations and select policies using training data only.

Compare a transparent baseline against richer models on cash-flow forecast error, calibration, timing, subgroup reliability, uncertainty and operating cost. Reconcile economic results with accounting records. An offline gain in discrimination is useful evidence, but it does not establish profitable deployment or the causal value of a proposed intervention.

The next artefact should be a small, fully reconciled scenario laboratory using these case definitions. A large model becomes meaningful only when its component schedules and business decisions can be inspected.
