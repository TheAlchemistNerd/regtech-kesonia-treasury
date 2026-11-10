# Part 3: Pricing Credit through Cash, Funding, Behaviour and Accounting

**Series:** Operationalising KESONIA: benchmark calculations, credit economics, treasury and governed operations
**Author:** Nevil Maloba
**Revision:** 28 September 2026

## Abstract

A default estimate becomes useful for pricing when it changes a defined monetary cash-flow case. This article derives the customer margin from expected income, funding, servicing, credit loss and an explicit capital hurdle. It then develops matched funding for term and revolving credit, distinguishes deposit pass-through from retention, and carries assumptions into separate earnings, economic-value and liquidity views. Machine learning remains a challenger within this framework. Accounting follows the business event and applicable policy, so a model refresh, ordinary rate reset, renegotiation and hedge designation cannot share an automatic posting rule.

KESONIA, customer risk-based pricing and internal funds-transfer pricing support the same economic reconciliation. The benchmark supplies the common reference; lending costs, borrower risk and shareholder return inform the bank-approved premium. Internal FTP attributes funding and liquidity cost to products. The monetary bridge below connects these layers without charging the same loss or capital return twice. The final CBK framework permits bank-defined premium components; the bridge is an explicit institutional policy example, rather than a quoted regulatory formula.

## 1. Begin with money rather than a score-to-rate shortcut

The CBK framework's benchmark-plus-premium formulation does not mean that the premium is only PD, LGD and EAD. Costs, risk and return must be reconciled under the institution's approved methodology. A coherent teaching model makes the rate denominator visible.

Let $B_t^{int}$ be the balance expected to earn margin and $\Delta t$ its year fraction. Define exposure-time

$$H=\sum_t E[B_t^{int}]\Delta t.$$

Let $I_b$ be expected benchmark interest, $F$ expected fee income, $C_f$ funding cost, $C_o$ operating cost, $L$ pricing credit loss, $EC$ allocated economic capital and $h$ a compatible annual capital hurdle. Under a one-year undiscounted teaching convention with a simply accrued margin $k$,

$$I_b+kH+F-C_f-C_o-L=hEC,$$

and therefore

$$k=\frac{C_f+C_o+L+hEC-F-I_b}{H}.$$

The numerator is currency; the denominator is currency-years. A money loss cannot be subtracted from the number one in a rate denominator. The cash amounts must also use compatible definitions: if uncollected interest is already removed from expected income, do not include the same shortfall again in $L$.

In a discounted lifetime model, solve using dated cash, survival, drawdown and recovery. State whether the hurdle enters a capital-charge schedule or a valuation criterion; including the same return twice overstates the required price. Taxes, fee recognition and capital release also need their own dates. A simple annual margin remains a useful explanatory benchmark, not a replacement for that fuller model.

## 2. A complete one-year margin bridge

Use KES thousands and the existing casebook's hypothetical assumptions: constant interest-bearing balance 1,000; benchmark interest 90; funding cost 100; operating cost 20; principal loss 15; fees 5; economic capital 50; pre-tax hurdle 20%. Interest is assumed collectible for this deliberately simplified case.

| Component | Amount |
|---|---:|
| Required return, $hEC$ | 10 |
| Funding, operations and principal loss | 135 |
| Less fee income and benchmark interest | −95 |
| Required margin income | 50 |
| Required annual margin | 5% |
| Total interest income | 140 |
| Interest plus fees less funding, operations and loss | 10 |
| Economic surplus after the capital hurdle | 0 |

Define the pre-capital risk-adjusted contribution and its associated measures consistently:

$$\Pi_{RA}=I+F-C_f-C_o-L,\qquad RAROC=\frac{\Pi_{RA}}{EC},\qquad EP=\Pi_{RA}-hEC.$$

Here RAROC is 20% and economic profit is zero. This is the chosen teaching convention; institutions must state their own horizon, tax, denominator and capital definitions. The contractual interest rate is 14% before the separately stated fee. Customer APR is a further calculation using the applicable disclosure convention and full cash dates.

Affordability remains a separate constraint. A price that clears the lender's hurdle may exceed the business's sustainable cash capacity. Compare the payment calendar with operating receipts after operating needs, tax, maintenance requirements and other obligations. Evaluate a smaller facility, different amortisation, suitable protection or a different funding structure rather than treating a higher quote as the only response.

## 3. Expected loss needs timing, exposure and recovery

For a performing asset at valuation date zero, one research decomposition is

$$EL=\sum_s w_s\sum_j q_{j,s}\,
E[D_j EAD_j LGD_j\mid T_D\in j,s].$$

$q_{j,s}$ is an unconditional marginal first-default probability for interval $j$, including survival to that interval and the chosen competing-event definition. Conditional hazards must first be converted: $q_j=S_{j-1}h_j$. Summing cumulative default probabilities across months would count defaults repeatedly.

Exposure and recovery may be dependent on the conditions causing default. Keep the conditional expectation of their product unless factorisation is justified. If LGD already discounts net recoveries to default, $D_j$ discounts default to valuation date; do not discount the same recovery period twice.

For a revolving line, a common descriptive conversion is

$$EAD=D_0+CCF\,(L_0-D_0),$$

with drawn amount $D_0$ and limit $L_0$ defined at a specific observation date. Estimating CCF requires limit histories, default dates, draws, cancellations, interest treatment and a sampling rule. A near-fully drawn line has a small denominator; a changed limit can invalidate a naive ratio. A pricing forecast of ordinary utilisation is not the same as exposure conditional on default.

Recovery readiness can change before PD does. Title evidence, guarantee eligibility, claim expiry, counterparty condition and enforcement delay can alter conditional severity or cash timing. Carry approved claims through notification, acceptance, payment and allocation. Insurance cover is not an immediate receipt. A reserve draw uses an existing asset; it does not create income or reduce the borrower's debt by itself.

Durable cure also needs an endpoint. Cumulative ever-90+ delinquency minus current 90+ can include lesser arrears, prepaid loans and terminal exits. Use longitudinal states, original/active denominators and confirmed cure/recurrence rules from the existing credit research. The treasury model consumes those outcomes as dated cash assumptions.

## 4. Fit risk models to the target and information available

A transparent pooled model, conventional scorecard and explicit hierarchical model provide useful baselines. Hierarchical pooling can help sparse groups when sharing assumptions are defensible. Tree and neural challengers can add nonlinear or sequence information; their value must be measured under matched data, tuning and decision conditions.

Each output carries outcome definition, horizon, product, population, prediction date, lawful availability cutoff, model version and uncertainty. Longitudinal validation must account for repeated loans, delayed entry, censoring, competing exits and label maturity. Fit transformations and select hyperparameters inside development data. Freeze later periods and cohorts for evaluation.

Compare calibration, proper scores, discrimination, timing and monetary cash error, as well as data cost, runtime, review burden and fallback performance. AUC/Gini do not measure calibration. PSI depends on its bins and reference sample and is not a universal retraining decision. A fixed Gini floor or PSI threshold must not be presented as an automatic Kenyan rule.

SHAP or another explanatory method can support review, but explain the scale and baseline. Feature contributions in log-odds do not add directly as percentage-point PD contributions. A decomposition of PD does not decompose the whole customer price, whose funding, cost and hurdle terms also need explanation. Attribution does not establish causality or fairness.

The operating sequence is **refresh evidence → estimate risk → evaluate allowed actions → authorise terms → execute → observe outcome**. Updating PD can support a review without changing $K$. A risk alert is not a permission to reprice, restrict credit or contact a third party. Collection interventions require their own assignment and outcome design before causal benefit is claimed.

## 5. FTP over a product's actual life

Funds transfer pricing allocates financing cost and benefit among business units. Its purpose is to show which part of performance belongs to lending, deposit gathering or central Treasury. A floating loan may reset monthly while requiring funding for years: the reset horizon and liquidity horizon are different.

For a dated balance schedule and assigned transfer rates $f_j$, a simple internal funding charge is

$$C_{FTP}=\sum_j B_j f_j\Delta t_j.$$

The policy must define whether $f_j$ is locked at origination, reset with a benchmark, decomposed into benchmark and term-liquidity components, or revised after specified events. For an amortising loan, match cash-flow amounts and dates rather than applying the final maturity to the opening balance throughout its life. For a revolver, distinguish drawn-balance funding, expected draws and the cost of maintaining undrawn availability.

For example, a KES 10 million line with KES 4 million drawn earns ordinary interest on the funded balance but exposes the institution to additional stress draws. A commitment fee, contingent-liquidity cost and stressed EAD answer different questions. Show each explicitly, and do not charge the same undrawn option once in FTP and again in operating cost without a reconciliation.

Ex-ante product contribution uses the information and curve available at origination. Ex-post profitability uses realised utilisation, resets, fees, losses and external funding. Attribute the difference to volume, benchmark, basis, timing, credit and policy changes. An internal debit to lending and corresponding credit to Treasury cancel in the consolidated institution; external interest expense remains once. [BIS/FSI, liquidity transfer pricing](https://www.bis.org/publications/fsi-paper-10-liquidity-transfer-pricing-guide-better-practice).

## 6. Deposits: rate pass-through is not retention

Deposit beta describes how paid rates respond to a reference-rate movement. Balance retention describes how funds persist, withdraw or migrate. They need separate longitudinal estimates by product, customer segment and regime.

A possible rate specification is a distributed-lag model,

$$r^d_t=\alpha+\sum_{\ell=0}^{p}\beta_\ell r^b_{t-\ell}+x_t'\gamma+\epsilon_t,$$

with attention to floors, asymmetric upward/downward responses and changes in product pricing. Retention can be modelled from customer/cohort balance histories with deposits, withdrawals, closures and transfers reconciled. Neither a low fitted beta nor an unchanged aggregate balance proves that the same funding will remain available under stress.

The earlier casebook gives a transparent replication example: KES 1 billion is allocated 20% to three-month, 30% to two-year and 50% to five-year ladders, initially yielding 3%, 3.75% and 4.5%. The weighted yield is 3.975%. With each bucket uniformly staggered across monthly maturities, a 2-percentage-point rise increases the month-one annualised yield by

$$0.02\left(\frac{0.2}{3}+\frac{0.3}{24}+\frac{0.5}{60}\right)=0.175\%.$$

Asset income's annualised run rate increases KES 1.75 million. Deposit beta 25% adds KES 5 million to annualised deposit cost; beta 75% adds KES 15 million. The resulting annualised NII changes are −3.25 and −13.25 million. These are month-one run rates, not realised annual totals. Full-year earnings require the remaining rollover path and changing balances.

Replication weights must eventually follow estimated retention, liquidity requirements and hedging policy. The teaching ladder establishes mechanics, not empirically supported behavioural maturity. Retain simple fallbacks and quantify what happens when funding leaves sooner than assumed.

## 7. One scenario, several financial outputs

The scenario engine should preserve one opening position and an evolving event path. Each period reconciles principal, interest, losses, recoveries, deposits, funding, collateral and cash. Four outputs remain separate:

| Output | Definition and interpretation |
|---|---|
| NII | Interest income less interest expense over a specified horizon and reset path |
| Earnings at risk | $EaR=NII_{base}-NII_{shock}$; positive means an earnings reduction |
| Economic value | Present value of scoped asset cash less liability cash under stated curves and behaviour |
| Cash survival | Opening usable cash plus dated available receipts/funding less payments and required buffers |

For a small parallel shock, a first-order value check is

$$\Delta EVE\approx-\left(\sum_a V_aD_a-\sum_l V_lD_l\right)\Delta y.$$

This uses value-weighted modified durations. Full repricing is preferable where options, curve twists or large shocks matter. EVE is neither today's accounting equity nor the market value of the institution's shares.

A cash view might have 70 immediately usable funds, 10 receipts, 90 withdrawals, 20 loan draws and 5 margin payments, all in KES millions. Closing cash before new funding is $70+10-90-20-5=-35$. A funding draw of 35 restores zero cash but changes future interest expense and liabilities. The next NII and value forecast must reflect that financing; it cannot simply reuse the old balance sheet.

A hedge can improve value sensitivity while creating variation-margin cash needs. Compare funding/product changes and permitted derivatives on cost, key-rate exposure, basis, convexity, counterparty exposure and collateral cash. A hedge proposal should report residual risks after execution, not just the sensitivity it reduces.

LCR and NSFR add distinct prudential views. LCR relates eligible HQLA to prescribed stressed net outflows over thirty days; NSFR relates available to required stable funding under its classification framework. They cannot be inferred from the cash-survival number. Eligibility, encumbrance, haircuts, inflow caps and entity-specific rules need an explicit balance-sheet mapping. The [remaining-work register](../../methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md) retains the full ratio modules and institution-specific mapping work; the current source register confirms Kenya's issued liquidity guidelines.

## 8. Accounting follows the event

The interest-rate calculation, accounting effective interest rate and expected-loss measurement are distinct. Maintain an approved event taxonomy:

| Event | Accounting question |
|---|---|
| Scheduled benchmark reset | How do the existing floating terms affect estimated contractual cash and applicable EIR treatment? |
| Corrected fixing/balance | Which prior amount requires correction, and how is the adjustment linked and recognised? |
| Risk estimate changes | Does this affect the allowance or a proposed action? No contract change is presumed |
| Negotiated borrower concession | Is the asset derecognised; if not, what modification adjustment applies? |
| Credit impairment | Which measurement basis, interest-recognition basis and disclosures apply? |
| Hedge execution | Is there a separately documented qualifying hedge designation? |

IFRS 9 B5.4.5 addresses floating-rate re-estimation reflecting market-rate movements. Benchmark-reform amendments have conditions and a defined purpose; they are not the general origin of all floating-rate reset accounting. A change in customer margin needs assessment of the contract and event; it is not automatically a renegotiation merely because the risk estimate changed.

For an asset modified without derecognition, IFRS 9 §5.4.3 requires recalculation of the gross carrying amount using modified contractual cash flows discounted at the applicable original effective interest rate, with the modification gain/loss recognised. The ten-percent test in B3.3.6 concerns financial liabilities and must not be copied into a universal loan-asset derecognition rule. [IFRS 9 text and paragraph references](https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2022/issued/part-a/ifrs-9-financial-instruments.pdf?bypass=on).

As a hypothetical modification example, gross carrying amount 1,000 and modified cash present value 960 imply a 40 modification loss under the stated non-derecognition assessment: debit modification loss 40; credit gross loan carrying amount 40. The allowance is assessed separately; do not count the same concession twice without reconciling the measurement bases. This is a teaching journal, not a complete accounting policy.

Under the general impairment approach, Stage 1's twelve-month ECL concerns lifetime shortfalls associated with possible defaults in the next twelve months. Stage 2 and credit-impaired Stage 3 use lifetime ECL; they are not identical measurement situations. PD, exposure and recoveries must match the applicable asset state. An LGD rise alone is not an automatic significant-increase-in-credit-risk trigger, and a wider posterior interval is not a staging rule.

## 9. Economic hedging and hedge accounting

Economic risk reduction does not establish hedge-accounting eligibility. Designation, documentation, the economic relationship, credit-risk effects and an appropriate hedge ratio are assessed separately.

For a simplified qualifying fair-value hedge, suppose an interest-rate move produces an 8 gain on the derivative and an 8 loss in the hedged item's fair value attributable to the designated risk. The example records the derivative asset/gain and corresponding hedged-item adjustment/loss in profit or loss. If the amounts were 8 and 7, the difference would need to be explained as measured ineffectiveness under the applicable rules, not forced to zero.

For a qualifying cash-flow hedge, the effective portion initially enters the cash-flow hedge reserve in OCI, subject to the applicable measurement limits and subsequent treatment; ineffectiveness enters profit or loss. Reclassification when hedged cash affects earnings is distinct from derivative settlement. Cash, fair value, OCI and earnings can therefore move at different times. Full journals, tax, rebalancing and discontinuation belong in the dedicated R17 accounting case, not in a generic “hedged” flag.

## 10. Evidence carried into operations

Preserve curve, model and contract versions; monetary price components; exposure-time; uncertainty; approved action; effective terms; accounting assessment; and settled cash. A useful explanation of a higher price might identify a longer funding horizon, delayed recovery and lower expected utilisation even when PD is unchanged.

The [worked examples](../../methods/WORKED_EXAMPLES.md) connect benchmark, curves, dated funding and scenarios. The [operations](../../../research_lab/operations.py) and [scenario](../../../research_lab/scenarios.py) modules provide teaching interfaces. Their synthetic cases establish arithmetic and event reconciliation; they do not estimate Kenyan deposit behaviour, validate a production risk model or complete a prudential capital engine.

Part 4 follows these outputs into approved execution and reporting. That final step is where a financially meaningful calculation becomes an accountable operational result.

## References and development lineage

- [CBK revised framework](https://www.centralbank.go.ke/wp-content/uploads/2025/08/Revised-Risk-based-Credit-Pricing-Model.pdf): applicable benchmark/premium and governance context.
- [BIS/FSI liquidity transfer pricing](https://www.bis.org/publications/fsi-paper-10-liquidity-transfer-pricing-guide-better-practice): matched funding and contingent liquidity principles.
- [Basel SRP31, effective January 2026](https://www.bis.org/committees/bcbs/basel-framework/standard/srp/31/inforce/2026-01-01/published/2024-07-16): earnings/economic-value and behavioural perspectives, subject to separate local applicability.
- [IFRS 9](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/) and [benchmark reform Phase 2](https://www.ifrs.org/projects/completed-projects/2020/ibor-reform-phase-2/): accounting authority rather than vendor automation claims.
- [September 25 casebook](../../../output/kesonia_treasury_deep_review_2026-09-25/02_CALCULATION_AND_CASEBOOK.md), [revision blueprint](../../../output/kesonia_treasury_deep_review_2026-09-25/03_REVISION_BLUEPRINT_AND_INSERTS.md) and [remaining work](../../methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md).
