# Symbols, units and reading conventions

**1 October 2026.** Reference for the worked examples and the accompanying operations methodology. A symbol's definition applies within its named section. Calculations retain full precision and round at the stated reporting step.

## 1. Common conventions

| Notation | Meaning and units |
|---|---|
| KES | Kenya shillings. A table explicitly marked KES millions uses one unit for KES 1,000,000. |
| Annual decimal rate | A quoted 10% enters arithmetic as 0.10. Interest conventions determine how that annual quote accrues. |
| bp / bps | Basis point(s): 1 bp = 0.01 percentage point = 0.0001 in decimal-rate units. |
| ACT/365 | Actual elapsed calendar days divided by a fixed denominator of 365. Leap-year intervals still use 365 in this particular convention. |
| `[start, end)` | A half-open interval includes the start date and excludes the end date. |
| Currency-years | Money multiplied by elapsed years. KES 1,000,000 outstanding for half a year contributes KES 500,000-years. |
| `i`, `j`, `n` | Integer indices. Their exact roles are defined below; they are not interest rates by themselves. |
| Sum / `sum` | Add the indexed terms. The large sigma in a displayed formula denotes this operation. |
| Product | Multiply the indexed terms. The large pi in the compounding formula denotes this operation. |
| `sqrt(x)` | Nonnegative square root of x. |
| `ln(x)` / `log(x)` | Natural logarithm; the inverse of the exponential function. |
| `exp(x)` | Exponential function with base e. |
| `max(x, 0)` / `min(x, 0)` | Positive part of x / nonpositive part of x. The latter retains the negative sign. |
| `x^2`, `x^-1` | Square / reciprocal of a scalar; for a matrix the exponent -1 means its matrix inverse. |
| `10^-8`, `10^-20` | Powers of ten: numerical tolerances, not percentages. The accompanying text supplies the unit. |
| `m`, `k` in amount labels | Million and thousand, for example 1m = 1,000,000 and 400k = 400,000. These suffixes are distinct from the pricing variable k. |

## 2. Benchmark compounding

| Symbol | Meaning | Unit / convention |
|---|---|---|
| P | Principal held constant during the illustrated coupon period | KES |
| i | Index of a mapped benchmark observation interval | Integer |
| r_i | Annual decimal benchmark fixing assigned to interval i | Annual rate |
| n_i | Number of calendar days for which that observation contributes to the compounded factor | Days |
| B | Day-count denominator | 365 days per convention-year in the examples |
| d | Actual number of days in the contractual interest period | Days |
| G | Gross accumulation factor, product of all terms 1 + r_i n_i/B | Dimensionless; includes principal factor 1 |
| A | Benchmark accrual factor G - 1 | Dimensionless; interest factor only |
| I_benchmark | Benchmark interest P times A | KES |
| k | Annual simple contractual margin above the benchmark | Annual decimal rate |
| I_margin | Simple margin interest P k d/B | KES |
| F | A symbol used inconsistently in other manuscripts; deliberately not used as a calculation variable here | Use the explicit fields gross_accumulation_factor and benchmark_accrual_factor |

The observation weights n_i need not sum to contractual d when a profile shifts observation intervals. The benchmark uses its mapped weights; simple margin uses contractual d. The lookback example must therefore retain both calendars. For the historical weekend, n_1 = d = 3 and B = 365.

The annualised period benchmark rate is A times B/d. The saved JSON field `factor` contains A, the accrual factor, rather than G. It should therefore be read with the field definition instead of inferred from its short name.

The published index is a dimensionless accumulated index level. The benchmark factor inferred from two levels is end index / start index - 1. On principal P, multiply that factor by P. Index publication rounding can create a small difference from fixing-based arithmetic.

In the historical example, the multiplication is P = 1,000,000; r_1 = 0.094618; n_1 = 3; B = 365; k = 0.03; d = 3. Benchmark and margin interest sum to KES 1,024.26 after rounding once to two decimals.

## 3. Curves, forward rates and value sensitivity

| Symbol | Meaning | Unit / convention |
|---|---|---|
| D_n / D_j | Present value of one currency unit payable at annual node n / j | Dimensionless discount factor |
| D(t) | Discount factor at time t, including between nodes | Dimensionless; D(0) = 1 |
| q_1 | One-year simple deposit quote used to obtain D_1 | Annual decimal rate; a one-year accrual |
| c_n | Annual par coupon quote for the unit-price instrument maturing at year n | Annual decimal rate; annual coupon intervals |
| n | Final annual coupon number / maturity year in the bootstrap | Integer |
| j | Coupon or payment index in the applicable sum | Integer |
| t_j | Time of payment j measured from valuation time | Years; t_0 = 0 |
| T | Final payment time of the floating note | Years; equals its last t_j |
| D_P(t) | Factor from the projection curve used to infer forward coupons | Dimensionless; subscript P means projection, not principal |
| D_D(t) | Factor from the discount curve used to value payments | Dimensionless; subscript D means discounting |
| f_j | Simple forward rate for interval from t_(j-1) to t_j | Annual decimal rate |
| N | Floating-note principal or notional repaid at T | Currency |
| PV | Present value of the stated cash flows | Currency |
| DV01 / PV01 | Change in present value associated with a one-basis-point movement in the specified rate or curve node | Currency per bp |

The bootstrap assumes a price of one, annual coupons and unit year fractions. Thus c_n times the sum of earlier discount factors is the present value of earlier coupons, and the final payment is 1 + c_n. A different coupon calendar needs its own accrual fractions.

The curve table's repricing error is calculated price minus one, a dimensionless unit-price residual. It differs from the fee-yield solver's present-value residual, which is measured in currency.

The reported key-rate DV01 is positive when raising that node's continuously compounded zero rate reduces value. It uses central finite differences: value after a downward bump less value after an upward bump, divided by twice the decimal bump size, then multiplied by 0.0001. The bump is initially 0.0001. The hedge example uses sensitivities to two specified axes; it does not assume those axes identify traded instruments.

## 4. Pricing, capital and yield

| Symbol | Meaning | Unit / convention |
|---|---|---|
| H | Expected collectible interest-bearing balance integrated over the pricing horizon | Currency-years |
| k | Annual simple margin solved from the pricing identity | Annual decimal rate |
| C_fund | External funding expense over that same horizon | Currency |
| C_op | Allocated operating cost over that horizon | Currency |
| EL_principal | Expected loss of principal over that horizon | Currency; excludes missing coupon already removed from income |
| C_cap | Required return on allocated economic capital over that horizon | Currency; supplied directly to the calculation |
| Fee | Fee income included in the pricing identity | Currency |
| I_benchmark | Expected collectible benchmark income used by the pricing identity | Currency; calculate from the actual eligible balance path |
| EC | Allocated economic capital | Currency stock |
| h | Annual required return on economic capital | Annual decimal rate |
| tau | Length of the pricing horizon | Years |
| h EC | Capital return in the original one-year example | Currency for that one-year horizon |
| h EC tau | Simple capital return when EC and h are constant over a general horizon | Currency; dated capital changes need a dated sum |
| y | Annual effective cash-flow yield in the separate fee example | Annual decimal yield; distinct from regression vector y below |

For a one-year constant-capital example, C_cap = h EC = 0.20 times 50,000 = KES 10,000. For other horizons the program still expects C_cap in money. It does not infer a time horizon from an annual hurdle. With changing capital, accrue the required return on each dated capital balance under the elected convention.

RAROC is risk-adjusted return on capital. Here it is the one-year pre-tax return after funding, operating cost and expected principal loss, divided by EC. The numerator is KES 10,000 and EC is KES 50,000, giving 20%. Economic surplus subtracts C_cap from that numerator and is zero.

The fee-yield equation discounts KES 1,140,000 received after exactly one year to KES 990,000 net advanced: 990,000 = 1,140,000/(1+y). The one-year exponent is 1. The resulting yield is 15.151515%; statutory APR requires its own defined costs and legal convention.

## 5. Dated funding transfer pricing

| Symbol / field | Meaning | Unit / convention |
|---|---|---|
| H_D | Drawn balance times the interval's actual days / 365 | Currency-years; D denotes drawn |
| H_U | Undrawn commitment, limit less drawn balance, times actual days / 365 | Currency-years; U denotes undrawn |
| drawn | Funded principal outstanding in an interval | Currency |
| limit | Approved total facility ceiling in an interval | Currency |
| days | Calendar days in the half-open interval | Days |
| customer rate | Interest rate earned on drawn principal | Annual decimal rate |
| customer commitment fee | Fee rate earned on undrawn commitment | Annual decimal rate |
| drawn FTP rate | Internal funding rate charged on drawn principal | Annual decimal rate |
| internal liquidity rate | Internal charge on undrawn commitment | Annual decimal rate |
| external drawn rate | External cost of funding drawn principal | Annual decimal rate |
| external commitment cost rate | External cost assigned to maintaining undrawn funding capacity | Annual decimal rate |
| reset_date | Most recent rate-reset date known by the interval start | Calendar date |
| liquidity_horizon | Date through which the funding commitment must be supported | Calendar date |

Multiply each rate by its matching H_D or H_U to obtain interval income or expense in money. Sum intervals before rounding. A reset date and a liquidity horizon have separate roles. The business-unit margin plus Treasury margin equals consolidated contribution because the internal transfers cancel.

EAD means exposure at default, a currency amount conditional on default. A CCF, or credit conversion factor, maps an undrawn amount to an assumed default-time draw. Neither quantity replaces the actually drawn principal on which this example earns interest.

## 6. Deposit regression and retention

The paid-rate equation uses changes measured in basis points. It is estimated separately for each synthetic segment.

| Symbol / field | Meaning | Unit / convention |
|---|---|---|
| change_in_paid_rate | Current month's change in the rate paid on deposits | bp |
| market_change | Current month's change in the selected market rate | bp |
| previous_market_change | Previous month's market-rate change | bp; zero for the first change record in this fixture |
| intercept | Fitted change when all four market-change regressors equal zero | bp |
| b_up / b_down | Immediate response to positive / negative market changes | Dimensionless bp per bp |
| lag_up / lag_down | One-month delayed response to positive / negative market changes | Dimensionless bp per bp |
| error | Observed paid-rate change less the fitted change | bp |
| beta | A rate-response coefficient; also shorthand for the vector of fitted coefficients | Components have the units specified above |
| X | Design matrix: a ones column, current positive and negative market changes, and lagged positive and negative changes | 23 rows by 5 columns for each training segment |
| X' | Transpose of X, exchanging rows and columns | 5 rows by 23 columns |
| y in OLS | Column vector of observed paid-rate changes | 23 rows by 1 column; bp |
| (X'X)^-1 X'y | Ordinary least-squares coefficient estimate | Five coefficients; assumes X has full column rank |
| RMSE | Root mean squared error: square root of the average squared observed-minus-predicted change | bp; averaged across the evaluated rows |

Combined up response is b_up + lag_up; combined down response is b_down + lag_down. A downward market change is negative, so a positive b_down implies a negative contribution to the paid-rate change. The combined responses describe this chosen two-term lag structure. They do not measure balance retention or deposit duration.

The coefficient covariance diagnostic uses the residual sum of squares divided by 23 - 5 = 18 training degrees of freedom, multiplied by (X'X)^-1. Reported standard errors are square roots of its diagonal entries. This diagnostic assumes independent, constant-variance residuals. RMSE uses the number of evaluated rows in its averaging denominator, not those degrees of freedom.

The retention bounds pool the two initially equal 1,000,000 cohorts. At each horizon, add the surviving original-product cohort balances and divide by their total initial 2,000,000. This retains the original tags and excludes new inflows.

| Retention / ladder term | Meaning and units |
|---|---|
| original cohort | Deposits tagged at the starting date; opening and closing balances are currency amounts. New inflows do not replenish this tag. |
| original product | The initial deposit product, including subsequently added inflows; its balances are currency amounts. |
| withdrawals | Money leaving the bank, in currency. |
| migration | Money leaving the original product for another product at the same bank, in currency. |
| retention fraction | Original tagged amount still in the original product divided by its initial amount; dimensionless. |
| retention haircut | Policy reduction of the available retention bound; 10% means multiply the bound by 0.90. |
| ladder weight | Fraction of the total allocation assigned to one maturity; nonnegative and summing to one. |
| 3m / 6m / 12m | Three-, six- and twelve-month terminal maturities. The suffix m here denotes months, not millions. |
| overnight rung | Allocation available without a term lock; represented as zero months in the ladder's maturity constraint. |
| weighted average maturity | Sum of weight times maturity in months; capped at six months here. |
| weighted yield | Sum of weight times the annual quoted yield; a simple annualised comparison. |
| locked fraction | Total weight whose maturity is strictly beyond the horizon being tested. |

## 7. Bank balances, default and recovery

| Symbol / quantity | Meaning | Unit / convention |
|---|---|---|
| Cash | Unrestricted bank cash at the stated balance-sheet date | KES millions in the table |
| Loans | Outstanding loan principal recognised in this simplified ledger | KES millions |
| Collateral | Posted collateral recorded as a restricted asset | KES millions; separate from available Cash |
| Deposits | Customer deposit liability | KES millions |
| Wholesale | Drawn wholesale funding liability | KES millions |
| Equity | Residual accounting equity in this simplified scenario | KES millions |
| NII | Net interest income: loan/cash interest less deposit/wholesale interest | KES millions over the period |
| hazard | Probability of default in a period conditional on survival to its start | Probability between 0 and 1 |
| marginal default probability | Probability, from the starting date, of default in one particular period | Prior survival probability times that period's hazard |
| survival | Probability of reaching the next period without default | Dimensionless probability |
| EIR | Original effective interest rate for the separate fixed-rate shortfall example | 6% annual effective rate |

Cash + Loans + Collateral equals Deposits + Wholesale + Equity at every shown date. Cash interest and funding interest accrue on opening balances; end-period movements affect interest in the next period. This is the elected ordering of the synthetic case.

For hazards of 0.10 and 0.20, second-period marginal default is (1 - 0.10) times 0.20 = 0.18, and final survival is 0.90 times 0.80 = 0.72.

In the shortfall formula, 0.10 is the probability of the default path; 1,000 is the original carrying amount; 300 is the default-path recovery at year two; 1.06 is one plus EIR; and exponent 2 is two years. The other path pays the contractual 1,060 at year one and therefore contributes zero discounted shortfall. Amounts in this separate example are currency units, not the bank table's millions.

## 8. Hedge objective and transaction units

| Term | Meaning | Unit / convention |
|---|---|---|
| (800, 1200) | Unhedged sensitivities along the two specified axes | Currency per bp |
| (100, 10), (10, 200) | Sensitivity reductions from one unit of each candidate hedge | Currency per bp per instrument unit |
| position | Integer number of units of a hedge; each ranges from 0 to 10 | Instrument units |
| residual PV01 | Original sensitivity less both selected hedge contributions, separately by axis | Currency per bp |
| cost | Total transaction cost of selected units: 100 per first hedge plus 200 per second hedge | Currency |
| collateral_cash | 500 per first hedge unit plus 1,500 per second hedge unit | Currency |
| 10,000 budget | Maximum permitted collateral_cash | Currency; transaction cost is outside this constraint |
| first 1,000 in objective | Sensitivity scale used to normalise residual PV01 | Currency per bp |
| second 1,000 in objective | Money scale used to normalise transaction cost | Currency |
| 0.001 | Relative penalty weight on normalised transaction cost | Dimensionless policy choice |
| objective | Sum of squared normalised sensitivities plus weighted normalised cost | Dimensionless |

Five units of each hedge use collateral of 10,000 and incur cost of 1,500. Residual sensitivities are (250, 150). The objective equals 0.25 squared + 0.15 squared + 0.001 times 1.5 = 0.0865. If collateral and costs are both paid initially, total cash needed is 11,500. The enumerated collateral constraint alone does not certify that total cash is available.

| Processing notation | Meaning |
|---|---|
| STPWorkflow(db_path) | Class implementing the local straight-through-processing workflow; db_path names its SQLite database file. |
| event ID | Persistent unique event identifier. Replaying the same content with the same ID must not duplicate effects. |
| minor units / cents | One hundredth of KES in this fixture: 25,000,000 minor units = KES 250,000. |
| placement_asset +25,000,000 | Increase in the placement asset, recorded using a debit-positive signed ledger. |
| settlement_payable 0 | Booking credit and settlement debit have offset after successful payment. |
| cash -25,000,000 | Credit to cash for this transaction; an incremental movement, not total bank cash. |
| bank_cash_cents | Signed external statement movement for this transaction in minor units. |
| rate in processing payload | Integer basis points, unlike the annual decimal inputs to the pricing formulas. |
| notional_cents / cash_cents / position_cents | Placement principal, settlement cash amount and reconciled position, respectively, in integer minor units. |
| rate_bps | Annual rate stored as integer basis points: 500 denotes 5%. |
| PROPOSE / APPROVE / ORDER / CONFIRM | Propose the placement, authorise it, issue an order and verify confirmed economics. |
| BOOK / SETTLE / RECONCILE | Recognise the placement/payable, record payment and match the accepted events to journals and external totals. |
| SETTLEMENT_FAILED / REJECTED | A failed payment attempt / a proposal refused by the approval step. |

## 9. Abbreviation key

| Abbreviation | Expansion |
|---|---|
| KESONIA | Kenya Shilling Overnight Interbank Average |
| CBK / CBR | Central Bank of Kenya / Central Bank Rate |
| RegTech | Regulatory technology |
| FTP / ALM | Funds transfer pricing / asset-liability management |
| EL / ECL | Expected loss / expected credit loss |
| EAD / CCF | Exposure at default / credit conversion factor |
| EC / RAROC | Economic capital / risk-adjusted return on capital |
| EIR / IRR / APR | Effective interest rate / internal rate of return / annual percentage rate |
| OLS / RMSE | Ordinary least squares / root mean squared error |
| PV / NPV | Present value / net present value |
| NII / EVE | Net interest income / economic value of equity |
| DV01 / PV01 | Dollar value / present-value sensitivity for a one-basis-point rate movement; expressed in the model's currency |
| STP / SQL / SQLite | Straight-through processing / Structured Query Language / the embedded database used here |
| API / ID | Application programming interface / identifier |
| IFRS | International Financial Reporting Standards |
| LCR / NSFR | Liquidity Coverage Ratio / Net Stable Funding Ratio |
| OAS | Option-adjusted spread |
| SA-CCR | Standardised approach for counterparty credit risk |
| CVA | Credit valuation adjustment; its valuation and capital measures remain distinct |
| FRTB / IRRBB | Fundamental Review of the Trading Book / interest rate risk in the banking book |
| SPV | Special-purpose vehicle |
| R02 / R03 / R09 | Existing work-register identifiers for lifecycle FTP, deposit behaviour and STP respectively |

## 10. Sources and software

The numerical baseline is the repository's 28 September 2026 checked-example output. The 1 October edition adds notation, unit definitions and explanatory clarifications. Calculation modules and baseline inputs are unchanged.

- [RegTech-KESONIA Treasury repository](https://github.com/TheAlchemistNerd/regtech-kesonia-treasury): calculation source, tests and publication builders.
- [CBK revised risk-based credit pricing model, August 2025](https://www.centralbank.go.ke/wp-content/uploads/2025/08/Revised-Risk-based-Credit-Pricing-Model.pdf): section 4 and Appendix I provide benchmark-pricing context. A contract still needs its applicable conventions.
- [CBK KESONIA observations](https://www.centralbank.go.ke/kesonia/) and [compounded index](https://www.centralbank.go.ke/kesonia-compounded-index/): primary-source series for the historical cross-check. Printed historical inputs are retained in the worked example; live tables can change their displayed window.

The public-source links were checked on 1 October 2026. The saved historical fixture remains dated evidence. Other portfolios, quotes, deposit panels, assumptions and transactions in this publication are synthetic.

## 11. Symbols in the expanded cases

This reference defines the original three-part laboratory. Each October 1 extension includes its own complete definitions beside equations and in a symbol/unit table:

- [Lifecycle](LIFECYCLE_WORKED_CASES.md): dated balances, accrual profiles, correction amounts and execution states.
- [Options and collateral](OPTION_AND_COLLATERAL_CASES.md): lattice state prices, CPR/SMM, OAS, swap risks, collateral and structural credit.
- [Liquidity and capital](REGULATORY_WORKED_CASES.md): HQLA, ASF/RSF, RC/PFE/EAD, CVA and GIRR terms.
- [Accounting and connected finance](ACCOUNTING_AND_CONNECTED_CASES.md): designation, cumulative reserve, journal and cash-handoff fields.

Symbols are local to their declared case; typed result fields preserve the economic meaning when exchanging outputs.
