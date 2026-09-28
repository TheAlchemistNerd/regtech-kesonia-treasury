# Part 2: Computing KESONIA Interest, Curves and Contract Cash

**Series:** Operationalising KESONIA: benchmark calculations, credit economics, treasury and governed operations
**Author:** Nevil Maloba
**Revision:** 28 September 2026

> LinkedIn reading edition, synchronised with the 28 September technical revision. Formulas are retained for the downloadable HTML; launch-post copy is separate.

## Abstract

A benchmark formula is reproducible only when its dates, information cutoff, rate units, weights and balances are defined. This article derives the compounded factor and its annualised rate, specifies a complete observation map, and connects calculation results to controlled postings. It also develops the distinction between historical compounding and a future term structure through bootstrapping and instrument repricing. The Python research laboratory is the executable reference for the teaching fixtures. SQL is presented as a calculation contract to implement and independently test in a selected database, without claiming that one mixed-dialect snippet is ready for every institution.

## 1. A factor, a rate and a cash amount

Let $r_i$ be an annual decimal fixing, $n_i$ the calendar-day weight assigned to it, and $b=365$ the ACT/365 denominator. For an approved sequence of intervals,

$$A_0=1,\qquad A_j=\prod_{i=1}^{j}\left(1+r_i\frac{n_i}{b}\right),\qquad F=A_N-1.$$

$A_N$ is an accumulation factor and $F$ a dimensionless period return. When the weights cover an accrual period of $d=\sum_i n_i$ days, its annualised equivalent is

$$R_{KES}=F\frac{b}{d}.$$

For constant principal $P$ and a separately simple-accrued annual margin $k$,

$$I=P F+Pk\frac{d}{b}.$$

This derives the amount from the contract convention. Compounding $r_i+k$ inside every factor would define a different margin treatment. Neither formula, on its own, calculates customer APR including fees.

The term $r_i n_i/b$ applies one fixing over its specified calendar span. A three-day weight is not three successive one-day reinvestments: $1+3r/b$ differs from $(1+r/b)^3$. The required convention determines which expression is appropriate. Similarly, rearranging factors does not change their product; the compounding effect is not evidence that adjacent high-rate days have a unique extra effect independent of the rates and weights.

The CBK's August 2025 framework adopts compounded-in-arrears for its in-scope loans, specifies ACT/365 in the index construction and describes the lookback. It also distinguishes the index's internal and published precision. These source conventions anchor the engine; the product's remaining calculation details must be explicit. [CBK framework, Appendix I](https://www.centralbank.go.ke/wp-content/uploads/2025/08/Revised-Risk-based-Credit-Pricing-Model.pdf).

## 2. Build the interval ledger before calculating

Represent periods as half-open intervals $[s,e)$: include the start and exclude the end. If a Friday observation covers Friday through Sunday, the unlagged span is $[Friday,Monday)$ and has three days. If the interest period ends on Sunday, clip at Sunday; that partial span has two days. A Tuesday fixing followed by a Wednesday holiday and Thursday reopening spans two days, not three.

The ledger must contain enough history to find a valid predecessor observation for an accrual period beginning on a non-business day. It must contain an explicit end boundary to close the final span. Defaulting the final weight to one day loses weekend or holiday accruals.

| Field | Meaning |
|---|---|
| Contract/period/version | The exact interest period and terms being calculated |
| Accrual start/end | Boundaries of the interest-bearing span |
| Observation value date | Economic date of the selected fixing |
| Publication/receipt times | When the fixing became available and entered the system |
| Fixing version | Original or corrected observation actually used |
| Day weight and calendar version | Why that fixing receives that weight |
| Principal and balance-event version | Balance relevant to the selected product rule |
| Mapping convention | Lookback/shift/payment lag, floor and margin conventions |
| Calculation cutoff/status | Actual, provisional, scenario or historical replay |

Check that intervals neither overlap nor leave gaps. Under a non-shifted accrual-weight convention, their day weights must sum to the period length. A shifted observation convention needs its own separately reconciled observation and accrual lengths.

## 3. Lookback, observation shift and payment lag

The framework's five-day lookback provides operational time to determine the interest amount before payment. The cited wording should not be expanded silently into a universal five-business-day rule. Specify the approved interpretation and retain its supporting authority. The laboratory's expressly labelled business-day fixture teaches date mapping; it does not settle that implementation decision for a live contract.

Three transformations must remain distinct:

1. **Rate lookback without observation shift:** map each accrual interval to an earlier fixing while retaining the accrual interval's weight.
2. **Observation shift:** move the observation interval and use weights associated with that shifted interval, following its own annualisation/cash convention.
3. **Payment lag:** leave interest observation/accrual terms unchanged but move the payment date.

Applying a lookback means mapping every interval across the whole period. Selecting only the last five observations discards most of the interest period. Holiday patterns can also give the shifted observation and accrual calendars different weights. Their economic difference can be measured; it should not be declared negligible before the calculation.

Availability is a separate test. A fixing dated Monday but published Tuesday cannot enter a Monday calculation merely because its value date is Monday. Preserve the CBK publication convention, actual receipt and authorised cutoff. Forecasts may use assumed future observations, but must remain visibly separate from final contractual accrual.

## 4. Historical index verification

The saved September 25 casebook records the CBK fixing for 5 September 2025 as 9.4618%, with index values 100.10451025 on 5 September and 100.18235974 on 8 September. These are historical values, not a current-rate quote. The three-day observation-span return is

$$F_{fixing}=0.094618\frac{3}{365}=0.00077768219178.$$

The rounded published index gives

$$F_{index}=\frac{100.18235974}{100.10451025}-1
=0.00077768214245.$$

On a hypothetical KES 1 million, these produce KES 777.68219178 and KES 777.68214245. The difference is about KES 0.00004933; both round to KES 777.68. A hypothetical simple 3% margin over the same three days adds KES 246.57534247, giving total illustrative interest KES 1,024.26.

This is an observation-span check. A customer invoice still needs its lookback/accrual mapping. An index ratio is a valid independent comparison only when dates, weights and conventions correspond. Since the published index is rounded, exact bitwise equality with an unrounded direct product is not the acceptance rule. Use the disclosed precision to set an amount tolerance and report both the unrounded difference and final cash rounding. [CBK fixing series](https://www.centralbank.go.ke/kesonia/); [CBK index](https://www.centralbank.go.ke/kesonia-compounded-index/).

## 5. Balance events and the meaning of daily accrual

For constant principal, interval increments reconcile exactly:

$$\Delta I_j=P(A_j-A_{j-1})+Pk\frac{n_j}{365},\qquad
\sum_j\Delta I_j=I.$$

The final annualised period rate is not necessarily the rate known on each earlier day. Reapplying it to a changing daily principal does not generally reproduce the contractual interest.

A repayment, draw or reversal must split the balance timeline at its effective date. Then apply the product's documented balance rule. For example, a hypothetical capitalising cash account can evolve as

$$V_{j+1}=V_j\left(1+r_j\frac{n_j}{365}\right)+c_{j+1},$$

where $c$ is a signed cash addition at the interval end. Its benchmark interest is terminal value minus starting value and net contributions. This is a clearly defined teaching convention, not permission to capitalise overdue customer interest. A non-capitalising loan or a product using non-cumulative compounded rates requires its own event specification.

The dated FTP examples in Part 3 use stated balance/reset assumptions. A schedule must disclose these assumptions before its interest can be compared to an actual loan. The important control is a reproducible opening balance, each principal event, accrued interest, cash settlement and closing balance; the benchmark formula cannot resolve an unspecified contract.

## 6. An implementable calculation contract

Separate data preparation from aggregation. The interval service interprets the contract and constructs validated rows. The calculation service consumes those rows. The posting service receives an approved amount and event identity.

```text
load contract and period version
build complete accrual intervals and principal-event schedule
map each interval to its approved observation and calendar
select fixing versions available at the calculation cutoff
validate uniqueness, coverage, units and valid factors
compute period return and the product-specific cash schedule
compare with an independent reference calculation
record immutable run inputs and result version
approve the identified version, then post idempotently
reconcile amount, period, entity and ledger event
```

For a constant-principal period, one SQL implementation can aggregate **validated** rows by `(contract_id, period_id, calculation_version)`:

```sql
-- Algorithmic SQL shape; adapt and test numerical functions per dialect.
SELECT contract_id, period_id, calculation_version,
       EXP(SUM(LN(1.0 + annual_decimal_rate * day_weight / 365.0))) - 1.0
         AS period_return,
       SUM(day_weight) AS mapped_days
FROM validated_observation_intervals
GROUP BY contract_id, period_id, calculation_version;
```

This query does not discover calendars, infer missing rates, authorise changes or post journals. Validate every factor as positive before taking its logarithm. Negative rates are not intrinsically invalid; the factor and any contractual floor govern admissibility. A floor on each daily fixing differs from a floor on the period rate.

The [benchmark reference module](../../research_lab/benchmark.py) and [worked examples](../../docs/methods/WORKED_EXAMPLES.md) provide the executable teaching interface. A database implementation should reconcile to independent high-precision fixtures, including `log1p`/`expm1` or an appropriately precise product method. SQL decimal types, floating-point aggregates and available functions differ by engine, so numerical precision and performance must be measured for the selected dialect.

## 7. From historical compounding to future curves

A historical accumulation uses realised observations. A future curve is constructed at a valuation date from instrument quotations or explicit assumptions. Its inputs include settlement dates, cash-flow dates, day counts, coupon frequency, index, collateral/credit basis and quote conventions.

Consider synthetic instruments with annual payments, a one-year simple deposit rate $q_1=10\%$ and a two-year par coupon $c_2=12\%$. Under a single-curve teaching convention,

$$D_1=\frac{1}{1+q_1},\qquad
1=c_2D_1+(1+c_2)D_2,$$

so

$$D_2=\frac{1-c_2D_1}{1+c_2}.$$

These equations construct discounts from prices, rather than assuming a spot curve and naming it a bootstrap. With annual compounding, recover zero and one-year forward rates through

$$z_2=D_2^{-1/2}-1,\qquad f_{1,2}=D_1/D_2-1.$$

Reinsert the fitted discounts into both instrument prices. The residuals must meet the declared tolerance. A smooth plot is not a repricing check.

Between pillars, a transparent choice is linear interpolation of log discount factors:

$$\log D(t)=(1-w)\log D(t_a)+w\log D(t_b),\quad
w=\frac{t-t_a}{t_b-t_a}.$$

State the resulting forward behaviour and test sensitivity to another method. Positivity is necessary; declining discounts are not a universal requirement where negative rates are admissible. Extrapolation outside quoted maturities needs an explicit rule and a visible unsupported-tenor flag. The [curve module](../../research_lab/curves.py) supplies the laboratory implementation and repricing output.

## 8. Projection and discounting can differ

For a reset interval with accrual fraction $\alpha_j$, a simple forward implied by a projection curve is

$$L_j=\frac{D_p(t_{j-1})/D_p(t_j)-1}{\alpha_j}.$$

For floating cash on notional $N$, its discounted value is

$$PV_{float}=\sum_j N\alpha_j L_jD_d(t_j).$$

$D_p$ projects the indexed cash; $D_d$ discounts it under the chosen valuation purpose. They may coincide in a single-curve exercise but should remain separately named. Multi-curve bootstrapping solves the relevant instrument equations using both sets of assumptions. A government yield curve, historical KESONIA average and bank funding curve are not interchangeable substitutes.

A forward is an implied rate under the construction, not an assured future fixing. A liquid local swap market is also not established by the existence of the benchmark. Kenyan instrument coverage, executable quotations, bid/ask, tenors and collateral arrangements remain evidence requirements in the source register. Synthetic quotes teach the mechanism without implying market availability.

## 9. Verification, correction and scale

The minimum fixture set covers weekends, holidays, a non-business start, clipped final span, duplicate/missing observations, corrected fixing versions, lookback versus shift, margin treatment, principal changes and rounding. Check zero rates, one interval, positive/negative admissible rates and agreement between independent product and log-product calculations.

A correction creates a new run and a linked adjustment; it does not overwrite history. Duplicate delivery must not duplicate an accrual or journal. Compare original-cutoff replay with revised-information replay to establish what changed. Part 4 develops the event controls.

Performance evidence should state contracts, intervals, historical horizon, hardware, memory, database settings and correction workload. Measure throughput, latency and failure recovery as well as arithmetic accuracy. Partitioning, caching and parallel processing are engineering options to benchmark. They are not proof that millions of contracts can be processed within the institution's operating window.

The result of Part 2 is a traceable contractual calculation and an explicit curve-construction method. Part 3 uses them to ask whether the facility's expected cash covers funding, servicing, loss and capital while fitting the borrower's operating cycle.

## References and companion work

- [CBK August 2025 framework](https://www.centralbank.go.ke/wp-content/uploads/2025/08/Revised-Risk-based-Credit-Pricing-Model.pdf), Appendix I: compounding, index, lookback and publication conventions.
- [September 25 teaching casebook](../../output/kesonia_treasury_deep_review_2026-09-25/02_CALCULATION_AND_CASEBOOK.md): dated historical index example and earlier independent arithmetic.
- [Compounding, term structure and funding distinction](../../docs/research/kesonia/KESONIA_COMPOUNDING_TERM_STRUCTURE_AND_FUNDING_CURVE_NOTE.md).
- [Current worked examples](../../docs/methods/WORKED_EXAMPLES.md) and [source register](../../docs/methods/SCOPE_AND_SOURCE_REGISTER.md): executable fixtures, assumptions and validation boundaries.
