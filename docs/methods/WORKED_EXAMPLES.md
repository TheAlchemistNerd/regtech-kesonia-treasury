# Reproducible KESONIA, pricing and treasury examples

**28 September 2026 numerical baseline; 1 October 2026 notation and PDF edition.** These examples implement useful parts of the introduced reviews. One case checks historical CBK observations. All portfolios, instrument quotes, holidays, behaviour and transactions in the remaining cases are synthetic. Read the [scope register](SCOPE_AND_SOURCE_REGISTER.md) before applying a formula to a product.

The [symbol and unit reference](SYMBOLS_AND_UNITS.md) defines all mathematical notation, rate conventions, money scales and abbreviations. The standalone PDF includes this reference, the detailed operations methodology and the October 1 extensions listed below.

## Reproduce

From the repository root, with Python 3.10 or later:

```text
python -m unittest discover -s tests -v
python -m research_lab.run_examples
```

No third-party Python dependencies are required. The workflow case creates and removes a temporary SQLite database. The runner writes [checked_examples.json](../../research_lab/results/checked_examples.json), including hashes of the executing modules. It does not fetch quotes, connect to a bank or transmit instructions. Decimal is used for benchmark and monetary ledgers; curve/OLS/root-solving examples use floating point with stated residual checks.

## 1. Compounding is a dated observation contract

For constant principal P (KES), observation-interval index i, annual decimal benchmark fixing r_i, calendar-day weight n_i and day-count denominator B (365), define:

$$G=\prod_i(1+r_i n_i/B),\qquad A=G-1,$$
$$I_{benchmark}=PA,\qquad I_{margin}=Pk\,d/B.$$

**Symbols:** G is the dimensionless gross accumulation factor; A = G - 1 is the interest-only accrual factor. I_benchmark and I_margin are interest amounts in KES. The product operator multiplies all observation-interval factors. The annual simple margin is k; d is the actual contractual accrual-day count. Observation weights n_i and contractual days d are separately retained when observation intervals shift.

The implemented profile compounds the benchmark and adds a **simple margin** over actual accrual days d. It has constant principal, no caps/floors, no in-period margin changes and no capitalisation of unpaid interest. Those limits are deliberate. The profile cannot silently substitute for another executed contract. Use `gross_accumulation_factor` and `benchmark_accrual_factor` in shared schemas: the symbol F has different meanings in the existing project manuscripts.

### Historical weekend cross-check

The [CBK fixing and index sources](SCOPE_AND_SOURCE_REGISTER.md#historical-inputs-and-synthetic-inputs) supply the following inputs:

| Input/output | Value |
|---|---:|
| Accrual interval | 5–8 September 2025, half-open |
| Friday fixing, annual | 9.4618% |
| Principal | KES 1,000,000 |
| Benchmark weight | 3 calendar days |
| Simple illustrative margin | 3% |
| Benchmark interest | KES 777.68219178 |
| Margin interest | KES 246.57534247 |
| Total, rounded once half-up | **KES 1,024.26** |
| Start/end published index | 100.10451025 / 100.18235974 |
| Index-based less fixing-based interest | Approximately KES -0.00004933 |

The Friday observation carries one three-day **linear factor**. Replacing it with three independently compounded one-day factors changes the result. Published-index rounding explains why exact equality is not required: the test permits less than KES 0.0001 on this principal. This is an independent historical cross-check, not a full replication of CBK's unpublished precision pipeline.

### Mapping, availability and corrections

The synthetic September 10–17 fixture invents a September 15 holiday. Five-business-day lookback without observation shift has weights totalling seven calendar days; shifted observation intervals have weights totalling six calendar days. Both schedules contain four observation intervals: their day weights are [1, 1, 4, 1] and [1, 1, 3, 1], respectively. This demonstrates why the schedule, weight convention and annualisation denominator must be recorded. The final CBK wording is five days; this synthetic fixture does not settle its operational interpretation.

Fixing selection is as-of a timezone-aware calculation cutoff. Later corrections cannot enter an earlier replay. Missing observations fail rather than carrying an old rate automatically. An explicitly authorised CBR fallback is possible; an available KESONIA observation takes priority. Duplicate latest versions, invalid factors, gaps and overlaps fail. Negative rates are allowed where their factors remain positive.

Implementation: [benchmark.py](../../research_lab/benchmark.py). A production profile still needs the official holiday source, approved mapping, fallback clause, balance events, spread convention, floors/caps, correction policy and customer-statement rounding.

## 2. Build a curve from instruments and reprice it

Use invented unit-price annual instruments: a one-year deposit at 10%, a two-year par coupon at 12%, and a three-year par coupon at 13%. With annual unit accruals:

$$D_1=(1+q_1)^{-1},\qquad D_n=\frac{1-c_n\sum_{j=1}^{n-1}D_j}{1+c_n}.$$

**Symbols:** D_j is the dimensionless value today of one unit paid at year j; D_n is the factor at the final annual node n. q_1 is the one-year annual decimal deposit quote; c_n is the annual par coupon quote of the instrument maturing at year n. The sum adds earlier annual discount factors. The price residual below is dimensionless price minus one.

| Tenor | Discount factor | Instrument repricing error |
|---|---:|---:|
| 1 year | 0.909090909091 | 0 |
| 2 years | 0.795454545455 | about -2.22 × 10^-16 |
| 3 years | 0.688857602574 | 0 |

Between nodes, interpolate log discount factors. Thus D(1.5) = sqrt(D(1)D(2)) = 0.850376678812. This ensures positive factors. It does not require decreasing factors when rates are negative. Extrapolation fails without a separately supplied policy.

Projection and discounting remain separate inputs. For coupon dates t_j:

$$f_j=\frac{D_P(t_{j-1})/D_P(t_j)-1}{t_j-t_{j-1}},$$
$$PV=N\left[\sum_j f_j(t_j-t_{j-1})D_D(t_j)+D_D(T)\right].$$

**Symbols:** j indexes coupons; t_j is payment time in years from valuation, with t_0 = 0; T is the last payment time. D_P is the projection-curve factor representation and D_D is the discounting-curve factor. Their subscripts mean projection and discounting. f_j is the annual simple forward rate for that coupon interval; N is principal in currency; PV is present value in currency. The interval t_j - t_(j-1) is in years.

Using the same curve for both purposes gives a par floating note of **1,000,000**, by telescoping. Using a separately bootstrapped projection curve with quotes 11%, 13%, 14% gives **1,024,330.90** under the selected discount curve. The difference is an imposed basis, not an estimated Kenyan basis.

For fixed cash flows of 100,000, 100,000 and 1,100,000, central finite-difference node sensitivities are approximately **9.090909, 15.909091 and 227.323012 currency per basis point**. Tests halve the bump and compare the aggregate with the independent analytic parallel-shift derivative. This is sensitivity to specified zero-rate nodes, not regulatory market-risk capital.

Implementation: [curves.py](../../research_lab/curves.py). Instrument calendars, market quotes, liquidity/basis calibration and option models remain future work.

## 3. Derive the margin from money

Let H be the expected collectible interest-bearing balance integrated over year fractions, in currency-years. Solve the pricing bridge before presenting a rate:

$$k=\frac{C_{fund}+C_{op}+EL_{principal}+C_{cap}-Fee-I_{benchmark}}{H}.$$

**Symbols:** C_fund is external funding expense; C_op is operating cost; EL_principal is expected principal loss; C_cap is the required capital-return amount; Fee is included fee income; and I_benchmark is collectible benchmark income. All are money for the same entity and horizon. The solved k is an annual decimal margin.

Capital EC is a currency stock. With annual hurdle h and constant capital over tau years, C_cap = h times EC times tau. This example spans one year, so C_cap = 0.20 times 50,000 = 10,000. The implementation accepts C_cap in money directly. Dated capital changes require a dated capital-return calculation. Expected loss here is principal loss, with the income convention explicit. A model that already removes defaulted interest from expected income must not charge it again inside another loss term.

| Item | Value and unit |
|---|---:|
| H | 1,000,000 KES-years |
| Benchmark income / fees | 90,000 / 5,000 |
| Funding / operating cost | 100,000 / 20,000 |
| Expected principal loss | 15,000 |
| Economic capital / annual hurdle | 50,000 / 20% |
| Required margin income | 50,000 |

The margin is **5%**. Total income including fees is 145,000; return before the capital hurdle is 10,000; one-year pre-tax RAROC is **20%**; surplus after the hurdle is **zero**. These outputs reconcile to one economic case, rather than adding a percentage capital stock to an interest rate.

Here RAROC means risk-adjusted return on capital: the one-year pre-tax return before the capital hurdle divided by EC. In the following separate equation, y denotes annual effective cash-flow yield.

A separate fee example advances net 990,000 and receives 1,140,000 exactly one year later. The annual cash-flow yield solves 990,000 = 1,140,000/(1+y), giving **15.151515%**. The numerical solver's PV residual is below 10^-8 currency. This is not labelled statutory APR: the legally required included costs and conventions must first be established.

Implementation: [pricing.py](../../research_lab/pricing.py). The IRR helper permits one initial negative cash flow followed by nonnegative receipts, ensuring monotonicity and avoiding ambiguous multiple-root cases. It rejects other sign patterns.

## 4. Dated FTP, deposit estimation and replication

The [operations methodology](OPERATIONS_METHODOLOGY.md) provides input calendars, equations, panels and complete tables.

H_D is drawn balance times actual interval days / 365; H_U is the unused limit times that same year fraction. Both are currency-years. Across multiple intervals, sum those interval exposures. FTP means funds transfer pricing and EAD means exposure at default, in currency. FTP margins below are money contributions over the year; pricing k above is an annual rate.

For drawn exposure-time H_D and undrawn commitment-time H_U, customer income, internal transfer charges and external funding are separate records. The business unit's income less FTP plus Treasury's FTP less external cost equals consolidated income less external cost. Conditional-default EAD does not become the interest-bearing balance.

| Synthetic 2027 product | Consolidated contribution before credit/operating/capital costs |
|---|---:|
| Fixed bullet | 70,000.00 |
| Amortising | 43,582.19 |
| Floating | 60,000.00 |
| Revolver, realised example path | 41,379.45 |
| Same revolver, frozen plan | 37,000.00 |

RMSE means root mean squared error, measured here in basis points. One basis point (bp) is 0.01 percentage point or 0.0001 in decimal-rate units. A deposit beta is a dimensionless paid-rate response per unit market-rate change.

The deposit experiment estimates immediate and lagged upward/downward responses from 23 training changes per segment, then tests a frozen fit on 13 later changes. Synthetic regime change raises RMSE from approximately **0.121 to 4.209 basis points**. The experiment illustrates temporal instability; it is not an empirical performance claim.

Withdrawal, same-bank migration, new inflows and original-cohort retention are separate. A discrete ladder uses observed synthetic retention bounds, a minimum overnight allocation and a maturity limit. At the stated quotes/policy, the solution is 20% overnight, 60% six-month and 20% twelve-month, with **5.3% annualised yield**. Tightening the retention policy changes the solution and reduces yield to **5.2%**. A repricing beta is never converted directly into deposit duration.

## 5. Carry cash and equity across three dates

The synthetic opening bank has KES millions: cash 200, loans 800, deposits 900 and equity 100. All rates apply to opening balances with ACT/365; repayments, drawings, charge-offs, recoveries, distributions and collateral posting occur at period end. Required cash is 60; an explicitly assumed replacement facility has a total capacity of 150. Newly drawn funding incurs interest in the next period.

| Period end | NII | Closing cash | Closing loans | Deposits | Wholesale debt | Equity |
|---|---:|---:|---:|---:|---:|---:|
| 1 February 2026 | 5.138356 | 172.138356 | 710 | 810 | 0 | 77.138356 |
| 1 March 2026 | 3.706822 | 60 | 660 | 630 | 31.154822 | 71.845178 |
| 1 April 2026 | 3.314280 | 60 | 625 | 550 | 85.840543 | 62.159457 |

Collateral receivable grows from zero to 5, then 13. For each date:

$$Cash+Loans+Collateral=Deposits+Wholesale+Equity.$$

**Balance-sheet symbols:** Cash is unrestricted cash; Loans is recognised loan principal; Collateral is the restricted asset from posted collateral; Deposits and Wholesale are customer-deposit and drawn wholesale-funding liabilities; Equity is the residual equity stock. All refer to the same date and are in KES millions in this table. NII means net interest income over the period.

Equity changes by realised profit less distributions. Posting collateral uses cash and creates a restricted asset; it is not treated as an expense. Charge-off reduces loans and profit; recoveries relate to already charged-off balances. Facility limits can cause a case to fail rather than creating unrestricted funding.

The Decimal residual tolerance is 10^-20 in the chosen unit. A regression rescales the same path from millions to KES and checks that continuation and economic results are preserved. The scenario excludes impairment allowances, tax, fair-value accounting, capital ratios and loss of interest before the chosen charge-off date. It therefore demonstrates a cash/equity bridge, not IFRS financial statements or an LCR/NSFR return.

### Default timing and discounted recovery are separate calculations

Conditional default hazards 10% then 20% produce marginal default probabilities **10% and 18%**, with 72% survival. Summing conditional hazards would be wrong.

A separate fixed-rate example contracts to collect 1,060 after one year at original EIR 6%. With 90% probability it collects as promised; with 10% probability it receives only 300 after two years. The expected discounted shortfall is:

$$0.1\left(1000-\frac{300}{1.06^2}\right)=73.3001068.$$

In this formula, 0.1 is the probability of the default path, 1,000 is initial carrying value, 300 is the recovery at year two, 1.06 is one plus the original annual effective interest rate (EIR), and exponent 2 is the elapsed two years. Amounts are separate currency units, not the millions in the bank table.

This illustrates recovery timing. It does not choose stage, define default or infer cure from cumulative-minus-current delinquency. Those credit states require the existing Underwrite/Mwendo definitions and event histories.

### A constrained hedge choice

The toy exposure is (800,1200) currency/bp on two axes. Candidate per-unit sensitivity vectors are (100,10) and (10,200); positions are integers from zero to ten. Costs are 100/200 currency per unit and collateral needs 500/1,500. Exhaustive search over 62 feasible choices under a 10,000 collateral-cash budget selects five units of each, leaving sensitivity (250,150), cost 1,500 and collateral 10,000.

PV01 denotes value sensitivity to a one-basis-point movement on the selected axis, in currency per bp. The first normalising 1,000 below is in currency per bp; the cost normaliser is 1,000 currency; the penalty weight 0.001 is dimensionless. The sum is over both sensitivity axes.

The objective is dimensionless: sum((residual PV01/1000)^2) + 0.001 × cost/1000. The scale and penalty are explicit policy assumptions. This is a transparent limited optimisation problem, not an optimal market hedge, margin model, option valuation or capital-relief calculation.

The collateral constraint excludes transaction costs. For the selected hedge, collateral plus transaction cost requires 11,500 currency if both are paid at inception; the solved objective is 0.0865.

Implementation: [scenarios.py](../../research_lab/scenarios.py).

## 6. STP demonstrated locally

STP means straight-through processing. SQLite is the local database; ID means identifier, and API means application programming interface. Processing amounts use integer minor units: 100 minor units = KES 1; rates in the processing payload use integer basis points.

The SQLite case follows a synthetic 250,000 KES deposit placement through proposal, approval, order, confirmation, booking, failed settlement, retry and reconciliation. Eight accepted events produce four journal lines. Reopening the database and replaying settlement adds neither a second event nor another posting.

Role violations, changed confirmed economics, duplicate IDs with different payloads, wrong settlement amounts and wrong retry references fail. Journal reconstruction checks accounts and amounts against accepted events. A deliberately doubled but still balanced ledger fails that reconstruction: a zero trial balance alone is insufficient.

Actor labels are not authenticated identities. No vendor, broker, bank or supervisor is connected. The original demonstration's scope is in [operations.py](../../research_lab/operations.py) and the [operations methodology](OPERATIONS_METHODOLOGY.md#durable-local-stp-demonstration). The [lifecycle extension](LIFECYCLE_WORKED_CASES.md) adds partial fills/settlement, cancellation/amendment and approved accrual corrections. Distributed recovery and production security still require operational implementation.

## 7. Verification boundary and next work

Tests check independent identities, historical index agreement, analytic curve sensitivities, unit scaling, probability mass, money conservation, known parameter recovery, future-data separation and durable workflow behaviour. They do not prove data quality, causal treatment effects, legal enforceability, accounting approval or production performance.

The [18-item reconciliation](REVIEW_INTEGRATION_AND_REMAINING_WORK.md) now distinguishes the implemented OAS, liquidity, derivative-exposure/capital components, hedge-accounting and connected-cash fixtures from broader unfinished research and institutional work. Live interfaces and empirical calibration remain open. The [cross-project report](CROSS_PROJECT_BOUNDARIES.md) identifies current owning-project implementations and their remaining requirements.

## 8. Expanded reference cases — 1 October 2026

The original cases above retain their numerical baseline. These additions turn further review requirements into executable examples:

| Additional worked case | What to read |
|---|---|
| Dated balances, caps/floors, fixing-correction approval and partial settlement | [Lifecycle cases](LIFECYCLE_WORKED_CASES.md) |
| Curve-fitted rate paths, prepayment/OAS, priced hedges, collateral funding and Merton calibration | [Options and collateral](OPTION_AND_COLLATERAL_CASES.md) |
| Classified LCR/NSFR, SA-CCR, CVA/CS01, reduced BA-CVA and FRTB GIRR delta | [Regulatory cases](REGULATORY_WORKED_CASES.md) |
| Fair-value/cash-flow hedge journals and borrower-to-owner cash interfaces | [Accounting and connected finance](ACCOUNTING_AND_CONNECTED_CASES.md) |
| What is implemented and what still needs development or external evidence | [Updated implementation register](REVIEW_INTEGRATION_AND_REMAINING_WORK.md) |
| Product candidates and reusable acceptance fixtures | [SokoIntel map](SOKOINTEL_CANDIDATE_MAP.md) |

These methods complement CBK's benchmark-plus-premium pricing framework. Each module declares its own financial quantity, instrument and intended use; a capital component or cash illustration is labelled with that scope.
