> **Historical review.** Current completion status and reproducible cases are tracked in [the 1 October implementation register](../../methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md).

# FRTB: scope, useful contribution and development requirements

**25 September 2026 · Companion to the KESONIA and treasury review**

## 1. What our earlier treatment had not completed

The treasury paste explicitly discusses the Fundamental Review of the Trading Book (FRTB), especially around physical lines 78–79. Our earlier review routed it to advanced market-risk work. That was a placement decision, not a developed treatment. This note supplies the missing conceptual structure and a concrete development specification. A numerical FRTB capital engine, desk validation exercise and Kenyan implementation assessment remain outstanding.

FRTB matters to the wider programme because a bank can originate credit, fund it, hedge interest-rate exposure, trade securities and hold positions issued by an SPV. These activities need connected information, while their regulatory treatments depend on the activity, instrument, book, entity and applicable rules. The useful question is: **what happens to risk, cash, accounting and capital when a proposed treasury action becomes an actual position?**

## 2. Start with the regulatory perimeter

The Basel banking-book/trading-book boundary has explicit assignment and transfer rules. An internal transfer of general interest-rate risk from the banking book has conditions, including documentation and a dedicated approved desk; the banking-book leg remains in IRRBB measurement. We therefore need a book-assignment and internal-risk-transfer record, rather than inferring prudential classification solely from an accounting label or the fact that Treasury owns the position. [Basel RBC25, especially §§25.25–25.27](https://www.bis.org/committees/bcbs/basel-framework/standard/rbc/25/inforce/2023-01-01/published/2020-03-27).

For our research design, record legal entity, instrument, purpose, regulatory book, accounting category, desk, internal transfer and external hedge identifiers separately. A Mwendo investor position also needs its own holder-specific assessment. The SPV waterfall alone cannot determine a bank investor's capital treatment.

## 3. Two approaches need separate explanations

### Standardised approach

The standardised capital requirement combines the sensitivities-based method, default-risk charge and residual-risk add-on:

$$K_{SA}=K_{SbM}+K_{DRC}+K_{RRAO}.$$

The sensitivities-based calculation uses delta, vega and curvature with prescribed aggregation rules. This is a separate calculation from an internal expected-shortfall model. [Basel MAR20, §§20.1–20.4](https://www.bis.org/committees/bcbs/basel-framework/standard/mar/20/inforce/2023-01-01/published/2020-03-27).

**Proposed laboratory:** begin with a small synthetic portfolio, retain instrument valuations and sensitivities, map each applicable risk factor, and reconcile the components to the total. Explain each change in capital after a hedge. Do not assume every component is nonzero for every portfolio. Publish the framework version, input classifications and independent check alongside the result.

### Internal models approach

Basel's internal-model approach uses one-sided 97.5% expected shortfall, with stressed calibration and risk-factor liquidity horizons of 10, 20, 40, 60 and 120 days. Non-modellable risk factors require separate treatment. A simple historical expected-shortfall statistic therefore does not reproduce the complete capital requirement. [Basel MAR33, especially §§33.3–33.5, 33.12 and 33.16](https://www.bis.org/committees/bcbs/basel-framework/standard/mar/33/inforce/2023-01-01/published/2020-06-05).

For teaching, a general definition for an integrable loss variable is:

$$ES_\alpha=\frac{1}{1-\alpha}\int_\alpha^1 VaR_u\,du.$$

This identifies the tail-average idea without treating it as the full regulatory algorithm. Our proposed extension should distinguish the illustrative distribution calculation, the market-risk model and the regulatory aggregation. Each needs its own validation evidence.

## 4. Data and desk validation are substantive work

**Risk-factor modellability.** Market observations need to satisfy the framework's evidence requirements. The presence of a long spreadsheet or a smooth fitted curve is insufficient evidence by itself. [Basel MAR31, risk-factor eligibility and modelling requirements](https://www.bis.org/committees/bcbs/basel-framework/standard/mar/31/inforce/2023-01-01/published/2020-03-27).

**P&L attribution and backtesting.** P&L attribution compares risk-theoretical P&L with hypothetical P&L. Backtesting is a distinct exercise using VaR and the specified P&L series. VaR therefore still has a validation role; the use of expected shortfall does not make it disappear from the framework. [Basel MAR32, §§32.18–32.26](https://www.bis.org/committees/bcbs/basel-framework/standard/mar/32/inforce/2023-01-01/published/2020-03-27).

**Our proposed evidence set:** daily positions, market-data snapshots, curve versions, valuation/model versions, risk-factor observations, independently constructed P&L series, missing-data explanations, test dates and resulting decisions. Before coding eligibility decisions, extract the applicable assessment windows, thresholds and transition rules into a versioned specification. A single unusual trading day should not be translated into an improvised approval rule.

For KESONIA, the research question becomes concrete: which proposed KES risk factors have usable observations, how are proxies justified, and what changes when quotations are sparse? This review has not established that an executable KES swap market or a sufficient modellability history exists for the intended portfolio.

## 5. Keep the connected outputs distinguishable

The following is our proposed workbench organisation, not a claim that all modules are implemented:

| Module | Question to answer | Required connection |
|---|---|---|
| Banking-book ALM/IRRBB | How do rate and behavioural changes affect earnings and economic value? | Loan/deposit cash flows and internal risk transfers |
| FRTB market risk | What market-risk capital treatment applies to the scoped positions? | Book/desk assignment, valuations, risk factors and validation |
| Counterparty exposure/SA-CCR | What derivative counterparty exposure is recognised under the selected method? | Netting set, collateral terms and position details |
| CVA valuation and CVA capital | How does counterparty credit affect value, and what separate capital calculation applies? | Exposure paths, spreads, hedges and rule version |
| Liquidity and funding | Can the institution fund settlements, margin and customer withdrawals? | Dated cash, collateral and funding sources |
| Accounting | What is recognised, where, and when? | Trade events, measurement policy and hedge designation |

A common trade identifier should join these outputs. A common number should not replace them. For example, a hedge proposal should produce separate changes in earnings sensitivity, economic-value sensitivity, cash needs, accounting results and applicable capital.

## 6. Where this belongs across the documents

- **KESONIA Part 1:** add a compact map of banking-book, trading-book, accounting and legal-entity scope.
- **Part 3:** connect instrument sensitivities and behavioural cash flows to the appropriate risk calculation; point to the specialist laboratory for regulatory detail.
- **Part 4:** include market-data lineage, desk/model status and exception handling in the operating model. Verify vendor support at module and version level.
- **SokoIntel workbench:** propose separate valuation, scenario, exposure, capital and reporting services linked by position and run identifiers. This is an interface proposal, not a fresh audit of its entire architecture.
- **Mwendo/Underwrite to Collect:** explain investor and hedge-counterparty interfaces where relevant. Keep borrower underwriting and collection research centred on its own observable outcomes.

## 7. Completion criteria for the future FRTB module

1. A jurisdiction- and entity-specific applicability map with dated primary authority.
2. A documented position/book/desk inventory, including any internal transfers.
3. A reproducible standardised example with component reconciliation.
4. An expected-shortfall teaching case clearly separated from a full internal-model implementation.
5. A market-observation inventory and explicit treatment of weak or absent evidence.
6. Independently constructed P&L series and the applicable validation procedure.
7. A hedge comparison linking risk reduction, collateral cash, transaction cost and capital.
8. An auditable report explaining changes, approvals, exceptions and residual exposure.

These criteria define the outstanding work. The Basel chapters above provide the global framework consulted on 25 September 2026; this note does not establish their adoption, scope or effective date for a particular Kenyan institution. That local mapping belongs in R18 of the [remaining-work register](<../../../output/kesonia_treasury_deep_review_2026-09-25/06_WHAT_REMAINS_TO_BE_DEVELOPED.md>).


---
Project copy. [Master review pack](<../../../output/kesonia_treasury_deep_review_2026-09-25/00_READ_ME.md>).
