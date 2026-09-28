# Reproducible KESONIA, pricing and treasury examples

**28 September 2026 reference edition.** These examples implement useful parts of the introduced reviews. One case checks historical CBK observations. All portfolios, instrument quotes, holidays, behaviour and transactions in the remaining cases are synthetic. Read the [scope register](SCOPE_AND_SOURCE_REGISTER.md) before applying a formula to a product.

## Reproduce

From the repository root, with Python 3.10 or later:

```text
python -m unittest discover -s tests -v
python -m research_lab.run_examples
```

No third-party Python dependencies are required. The workflow case creates and removes a temporary SQLite database. The runner writes [checked_examples.json](../../research_lab/results/checked_examples.json), including hashes of the executing modules. It does not fetch quotes, connect to a bank or transmit instructions. Decimal is used for benchmark and monetary ledgers; curve/OLS/root-solving examples use floating point with stated residual checks.

## 1. Compounding is a dated observation contract

For constant principal P, decimal benchmark observations r_i, weights n_i and basis B, define:

$$G=\prod_i(1+r_i n_i/B),\qquad A=G-1,$$
$$I_{benchmark}=PA,\qquad I_{margin}=Pk\,d/B.$$

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

The synthetic September 10–17 fixture invents a September 15 holiday. Five-business-day lookback without observation shift retains seven accrual weights; shifting observation intervals produces six weights. This demonstrates why the schedule, weight convention and annualisation denominator must be recorded. The final CBK wording is five days; this synthetic fixture does not settle its operational interpretation.

Fixing selection is as-of a timezone-aware calculation cutoff. Later corrections cannot enter an earlier replay. Missing observations fail rather than carrying an old rate automatically. An explicitly authorised CBR fallback is possible; an available KESONIA observation takes priority. Duplicate latest versions, invalid factors, gaps and overlaps fail. Negative rates are allowed where their factors remain positive.

Implementation: [benchmark.py](../../research_lab/benchmark.py). A production profile still needs the official holiday source, approved mapping, fallback clause, balance events, spread convention, floors/caps, correction policy and customer-statement rounding.

## 2. Build a curve from instruments and reprice it

Use invented unit-price annual instruments: a one-year deposit at 10%, a two-year par coupon at 12%, and a three-year par coupon at 13%. With annual unit accruals:

$$D_1=(1+q_1)^{-1},\qquad D_n=\frac{1-c_n\sum_{j=1}^{n-1}D_j}{1+c_n}.$$

| Tenor | Discount factor | Instrument repricing error |
|---|---:|---:|
| 1 year | 0.909090909091 | 0 |
| 2 years | 0.795454545455 | about -2.22 × 10^-16 |
| 3 years | 0.688857602574 | 0 |

Between nodes, interpolate log discount factors. Thus D(1.5) = sqrt(D(1)D(2)) = 0.850376678812. This ensures positive factors. It does not require decreasing factors when rates are negative. Extrapolation fails without a separately supplied policy.

Projection and discounting remain separate inputs. For coupon dates t_j:

$$f_j=\frac{D_P(t_{j-1})/D_P(t_j)-1}{t_j-t_{j-1}},$$
$$PV=N\left[\sum_j f_j(t_j-t_{j-1})D_D(t_j)+D_D(T)\right].$$

Using the same curve for both purposes gives a par floating note of **1,000,000**, by telescoping. Using a separately bootstrapped projection curve with quotes 11%, 13%, 14% gives **1,024,330.90** under the selected discount curve. The difference is an imposed basis, not an estimated Kenyan basis.

For fixed cash flows of 100,000, 100,000 and 1,100,000, central finite-difference node sensitivities are approximately **9.090909, 15.909091 and 227.323012 currency per basis point**. Tests halve the bump and compare the aggregate with the independent analytic parallel-shift derivative. This is sensitivity to specified zero-rate nodes, not regulatory market-risk capital.

Implementation: [curves.py](../../research_lab/curves.py). Instrument calendars, market quotes, liquidity/basis calibration and option models remain future work.

## 3. Derive the margin from money

Let H be the interest-bearing exposure in currency-years. Solve the pricing bridge before presenting a rate:

$$k=\frac{C_{fund}+C_{op}+EL_{principal}+hEC-Fee-I_{benchmark}}{H}.$$

All numerator terms are money over the same horizon. Capital EC is a stock; hEC is the required return flow. Expected loss here is principal loss, with the income convention explicit. A model that already removes defaulted interest from expected income must not charge it again inside another loss term.

| Item | KES |
|---|---:|
| H | 1,000,000 currency-years |
| Benchmark income / fees | 90,000 / 5,000 |
| Funding / operating cost | 100,000 / 20,000 |
| Expected principal loss | 15,000 |
| Economic capital / annual hurdle | 50,000 / 20% |
| Required margin income | 50,000 |

The margin is **5%**. Total income including fees is 145,000; return before the capital hurdle is 10,000; one-year pre-tax RAROC is **20%**; surplus after the hurdle is **zero**. These outputs reconcile to one economic case, rather than adding a percentage capital stock to an interest rate.

A separate fee example advances net 990,000 and receives 1,140,000 exactly one year later. The annual cash-flow yield solves 990,000 = 1,140,000/(1+y), giving **15.151515%**. The numerical solver's PV residual is below 10^-8 currency. This is not labelled statutory APR: the legally required included costs and conventions must first be established.

Implementation: [pricing.py](../../research_lab/pricing.py). The IRR helper permits one initial negative cash flow followed by nonnegative receipts, ensuring monotonicity and avoiding ambiguous multiple-root cases. It rejects other sign patterns.

## 4. Dated FTP, deposit estimation and replication

The [operations methodology](OPERATIONS_METHODOLOGY.md) provides input calendars, equations, panels and complete tables.

For drawn exposure-time H_D and undrawn commitment-time H_U, customer income, internal transfer charges and external funding are separate records. The business unit's income less FTP plus Treasury's FTP less external cost equals consolidated income less external cost. Conditional-default EAD does not become the interest-bearing balance.

| Synthetic 2027 product | Consolidated contribution before credit/operating/capital costs |
|---|---:|
| Fixed bullet | 70,000.00 |
| Amortising | 43,582.19 |
| Floating | 60,000.00 |
| Revolver, realised example path | 41,379.45 |
| Same revolver, frozen plan | 37,000.00 |

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

Equity changes by realised profit less distributions. Posting collateral uses cash and creates a restricted asset; it is not treated as an expense. Charge-off reduces loans and profit; recoveries relate to already charged-off balances. Facility limits can cause a case to fail rather than creating unrestricted funding.

The Decimal residual tolerance is 10^-20 in the chosen unit. A regression rescales the same path from millions to KES and checks that continuation and economic results are preserved. The scenario excludes impairment allowances, tax, fair-value accounting, capital ratios and loss of interest before the chosen charge-off date. It therefore demonstrates a cash/equity bridge, not IFRS financial statements or an LCR/NSFR return.

### Default timing and discounted recovery are separate calculations

Conditional default hazards 10% then 20% produce marginal default probabilities **10% and 18%**, with 72% survival. Summing conditional hazards would be wrong.

A separate fixed-rate example contracts to collect 1,060 after one year at original EIR 6%. With 90% probability it collects as promised; with 10% probability it receives only 300 after two years. The expected discounted shortfall is:

$$0.1\left(1000-\frac{300}{1.06^2}\right)=73.3001068.$$

This illustrates recovery timing. It does not choose stage, define default or infer cure from cumulative-minus-current delinquency. Those credit states require the existing Underwrite/Mwendo definitions and event histories.

### A constrained hedge choice

The toy exposure is (800,1200) currency/bp on two axes. Candidate unit vectors are (100,10) and (10,200); positions are integers from zero to ten. Costs are 100/200 currency per unit and collateral needs 500/1,500. Exhaustive search over 62 feasible choices under a 10,000 cash budget selects five units of each, leaving sensitivity (250,150), cost 1,500 and collateral 10,000.

The objective is dimensionless: sum((residual PV01/1000)^2) + 0.001 × cost/1000. The scale and penalty are explicit policy assumptions. This is a transparent limited optimisation problem, not an optimal market hedge, margin model, option valuation or capital-relief calculation.

Implementation: [scenarios.py](../../research_lab/scenarios.py).

## 6. STP demonstrated locally

The SQLite case follows a synthetic 250,000 KES deposit placement through proposal, approval, order, confirmation, booking, failed settlement, retry and reconciliation. Eight accepted events produce four journal lines. Reopening the database and replaying settlement adds neither a second event nor another posting.

Role violations, changed confirmed economics, duplicate IDs with different payloads, wrong settlement amounts and wrong retry references fail. Journal reconstruction checks accounts and amounts against accepted events. A deliberately doubled but still balanced ledger fails that reconstruction: a zero trial balance alone is insufficient.

Actor labels are not authenticated identities. No vendor, broker, bank or supervisor is connected. Partial fills, cancellation, distributed recovery, accrued interest and production security remain outside the local demonstration. See [operations.py](../../research_lab/operations.py) and the [full operations limitations](OPERATIONS_METHODOLOGY.md#durable-local-stp-demonstration).

## 7. Verification boundary and next work

Tests check independent identities, historical index agreement, analytic curve sensitivities, unit scaling, probability mass, money conservation, known parameter recovery, future-data separation and durable workflow behaviour. They do not prove data quality, causal treatment effects, legal enforceability, accounting approval or production performance.

The [18-item reconciliation](REVIEW_INTEGRATION_AND_REMAINING_WORK.md) keeps OAS/prepayment calibration, full LCR/NSFR, SA-CCR/CVA capital, complete hedge accounting, live interfaces and the full borrower-to-owner connected case open. The [cross-project report](CROSS_PROJECT_BOUNDARIES.md) identifies what already exists and which project owns each extension.
