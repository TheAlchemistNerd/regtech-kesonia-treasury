> **Historical review.** Current completion status and reproducible cases are tracked in [the 1 October implementation register](../../methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md).

# KESONIA, treasury curves and the business decisions they support

**25 September 2026 · Detailed development review · Proposed additions, not an implemented treasury system**

## 1. What the new material contributes

The treasury paste can make the KESONIA series substantially more useful by connecting a correctly calculated lending rate to the decisions surrounding it: **how the loan is funded, when its cash arrives, how behaviour changes that cash, what the institution earns, and what it can safely distribute.**

The existing series already has considerable substance on benchmark ingestion, compounding, credit modelling, accounting and controlled reporting. Its short compounding/term-structure note already makes the essential distinction between a realised overnight accumulation and a curve across future maturities. The new work should develop that foundation into calculations and business cases.

There is also a stronger existing source than the older gap reports suggest: [the controlled Mwendo pricing and capital chapter](<C:/Users/Nevo/Downloads/insuretech & embedded finance/docs/controlled-specifications/Part_5_KESONIA_Pricing_and_Capital_Orchestration.md>) already separates customer prices, note coupons, FTP, valuation hurdles, regulatory capital and SPV protections. It specifies cohort cash flows, a waterfall, reserves, repricing mismatch and accounting event boundaries. Bring those definitions into the research series before expanding the theory.

This review read **all nine existing Markdown files in `docs/research/kesonia`, the entire 180-line treasury paste, and the controlled pricing chapter**. Some paste lines contain whole conversations. The review includes the later material on derivatives, capital, insurance and modelling; embedded prompts were treated as source content. The [reading map](<../../../output/kesonia_treasury_deep_review_2026-09-25/04_READING_MAP_AND_REFERENCES.md>) records coverage. Adjacent business-analysis work is carried forward from the [completed Owner Earnings follow-up](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/pricing_treasury_cross_project_review_2026-09-23/06_BUSINESS_CREDIT_AND_OWNER_EARNINGS_FOLLOWUP_2026-09-25.md>); its workbooks were not audited here.

## 2. What is already covered, and what deserves development

| Existing material | Developed foundation | Useful next contribution |
|---|---|---|
| Part 1: reform and enterprise architecture | Benchmark reform, ingestion, calculation, pricing, accounting and reporting layers | Organise the layers around decisions, legal entities and dated cash flows; introduce the curve atlas below |
| Part 2: daily compounding and SQL | Compound-factor mathematics, calendars, data tables, lookback, reconciliation and scale | A complete observation-to-accrual mapping, corrected period-based computational specification, historical verification and balance-event examples |
| Part 3: AI pricing and IFRS 9 | PD/LGD/EAD, explanatory tools, model governance, accounting, FTP and ALM | Derive the margin from monetary economics; develop deposit behaviour and matched funding; separate NII, EVE, liquidity and payout |
| Part 4: reporting and platforms | Validation, evidence retention, approvals, vendor integration and a roadmap | A calculation-to-decision workflow, scenario controls, replayable reporting and acceptance gates tied to demonstrable outputs |
| Compounding/term/funding note | Correct separation of historical accrual, future maturity structure and bank funding | Expand into a worked curve laboratory; use it as the conceptual entry point |
| September 23 additional review | Four-part revision direction and advanced extensions | This package supplies the detailed placements, draft paragraphs, equations, examples and evidence requirements |
| CBK/K framework fragment | Relationship between customer pricing and wholesale funding | Replace the informal spread story with an institution-specific net-return bridge and contractual repricing rules |
| Enhancement report | Candidate architecture, analytics and control requirements | Convert candidates into a dated delivery backlog with owners and acceptance evidence |
| Gap analysis | Earlier inventory of desired capabilities | Retain as historical rationale; reassess individual items against the newer controlled chapter rather than restating everything as absent |

“Covered” here means developed in writing. It does not mean a model has been fitted, SQL deployed, controls independently tested or a regulator's interface integrated.

## 3. The organizing framework: six questions

1. **What was agreed?** Identify borrower, lender, currency, balance, benchmark, margin, reset dates, fees, options and payment dates.
2. **What is now known?** Distinguish the benchmark's value date from publication and ingestion times, and distinguish available information from subsequently revised data.
3. **What cash is expected?** Build principal, interest, fee, prepayment, drawdown, default, cure and recovery schedules under named scenarios.
4. **What funds that cash?** Assign funding and liquidity costs, commitments, collateral needs and refinancing dates to the same exposure.
5. **What is the effect?** Report customer cost, lender economics, accounting results, earnings sensitivity, economic value, cash shortfall and capital capacity separately.
6. **What changes?** Record the responsible owner, decision, approval, contractual effective date and subsequently observed outcome.

These questions supply a coherent narrative from business analysis to treasury and RegTech. A dashboard becomes useful when a change in its measurements leads to an accountable decision.

## 4. A curve atlas for the series

| Object | What it measures | Appropriate use and required evidence |
|---|---|---|
| Overnight fixing history | Observed rates through calendar time | Accrual using source, value date, publication time and applicable day spans |
| Compounded index/period factor | Accumulation over a historical observation interval | Independent benchmark verification where boundaries and conventions match |
| Par curve | Coupons that price specified instruments at par across maturities | Describe coupon frequency, instrument type, settlement, credit and quotation conventions |
| Zero curve/discount factors | Value today of future units of currency | Discount cash flows with a curve appropriate to the claim and valuation purpose |
| Forward curve | Rates implied between future dates by a consistent curve construction | Project floating cash flows under stated conventions; an implied forward is not an assured future fixing |
| Swap curve | Market swap quotations across tenors | Build a curve only from evidenced instruments; an overnight benchmark does not establish a liquid local swap market |
| Basis curve | Differences between identified indices or funding currencies across tenors | Diagnose asset/liability mismatch and specify any hedge's actual index and collateral terms |
| Institutional funding/FTP curve | Costs and internal allocation of financing an exposure over its life | Combine evidenced funding inputs, liquidity and optionality policies without repeating costs elsewhere |
| Credit spread/survival structure | Market compensation or forecast default timing, according to the model's purpose | Label market valuation versus real-world prediction; a spread is not itself a physical default probability |
| Behavioural profiles | Expected deposit retention, repricing, prepayment and utilisation | Estimate from longitudinal data with segment, regime, horizon and uncertainty recorded |
| Liquidity ladder | Dated receipts, payments and available funding | Find the lowest-cash date and the amount of financing available then |
| Vintage/loss profile | Performance by origination cohort and loan age | Feed seasoning and recovery timing into cash forecasts; keep denominators and exit states explicit |

For every object, store **currency, valuation/as-of date, purpose, units, day count, compounding, tenor dates, source, version and status**. Historical observations, market-derived quantities, calibrated forecasts and illustrative assumptions should be visibly labelled. Government yields may provide market context; they should not silently become KESONIA projections or a bank's own funding cost.

## 5. The practical gains for each core part

### Part 1 — make the business purpose visible

Lead with a business whose customer pays after its loan instalment falls due. Then follow that loan into the lender's funding and risk systems. This gives the reader a reason to care about the distinction between contractual rate, expected collection, funding maturity and realised cash.

The CBK framework adopts compounded KESONIA for in-scope variable-rate lending, specifies a five-day lookback, and describes separate premium and fee disclosures. Its Appendix I is the anchor for the benchmark calculation. The series should distinguish this published requirement from the detailed date-mapping decisions needed to implement it. [CBK revised framework, August 2025](https://www.centralbank.go.ke/wp-content/uploads/2025/08/Revised-Risk-based-Credit-Pricing-Model.pdf).

The architecture should identify systems by responsibility: contract master, market-data store, calculation service, risk models, accounting subledger, general ledger and reporting. The selected ERP may own several responsibilities, but the article should not require one vendor to perform all of them. Reconciliation remains an explicit control between these records.

### Part 2 — make the calculation reproducible

Develop the calendar and observation mapping before SQL. Give each interest period its own identifier. Show how the applicable fixing, day weight and principal balance were selected. The SQL should consume validated interval rows, rather than attempting to discover all contract rules inside an aggregate query.

A five-day lookback is not implemented by retaining only the final five days of observations. The engine needs a mapping for the whole relevant period. Specify the applicable business-day convention and whether observation weights shift; support the approved interpretation with worked fixtures. A payment delay, an observation shift and a rate lookback are different transformations.

The [casebook](<../../../output/kesonia_treasury_deep_review_2026-09-25/02_CALCULATION_AND_CASEBOOK.md>) provides a historical index reconciliation and the constant-principal derivation. Extend it with amortisation, partial periods, publication corrections, fallback and a rounded-index tolerance. That produces a much stronger article than unbenchmarked claims about millions of loans.

### Part 3 — connect the rate to the business economics

First calculate expected monetary income and costs over a defined horizon. Then solve for the margin. Display funding, servicing, loss, capital hurdle and fees separately. An estimated PD is an input into that calculation; it is not the whole price.

Develop funds transfer pricing as an internal allocation whose maturity and behavioural assumptions can be inspected. The BIS liquidity-transfer-pricing paper supports matching marginal funding costs to the product and recognising contingent liquidity use. It is practice guidance, not a Kenyan regulatory tariff. [BIS/FSI liquidity transfer pricing paper](https://www.bis.org/publications/fsi-paper-10-liquidity-transfer-pricing-guide-better-practice).

The treasury paste's strongest practical addition is the distinction between **deposit beta**—how deposit rates respond—and **deposit retention**—how balances persist. Low rate sensitivity does not prove long-lasting balances. Use separate estimates and stress both. Replication ladders can allocate funding value, but their internal credits do not create additional consolidated income.

Maintain four outputs: earnings over a stated horizon; present-value sensitivity; dated cash availability; and capital/distribution capacity. Basel's current IRRBB chapter treats earnings and economic value as complementary perspectives and addresses behavioural assumptions. The bank framework is a reference for bank analysis; its application to a particular Kenyan institution needs a separate jurisdictional mapping. [Basel SRP31, effective January 2026](https://www.bis.org/committees/bcbs/basel-framework/standard/srp/31/inforce/2026-01-01/published/2024-07-16).

Finally, separate a risk-model refresh from a proposed price, an authorised contract change and an accounting event. Explain the change in business terms before supplying SHAP or another statistical explanation.

### Part 4 — make governance demonstrable

Use one workflow: prepare data, validate, calculate, review exceptions, approve the identified result, sign/package the approved version where required, submit through the verified channel, receive acknowledgement and reconcile. A corrected fixing creates a new calculation version with a traceable adjustment.

Expand the vendor discussions into interface requirements: what data arrive, which service calculates, what is posted, who approves, how an error is retried, and what evidence survives. An encrypted payload or model explanation alone does not establish compliance. Confirm actual reporting specifications and vendor capabilities when implementation choices are made.

Move tests into every delivery stage. A deterministic, reviewed pricing baseline should work before an advanced machine-learning model is introduced. Additional complexity should earn its place through measurable improvement, operational reliability and a useful decision.

The [targeted software review](<../../../output/kesonia_treasury_deep_review_2026-09-25/05_STP_AND_ALM_FTP_SOFTWARE_REVIEW.md>) now verifies the products and workflow examples named in the treasury paste against primary vendor material. The [remaining-work register](<../../../output/kesonia_treasury_deep_review_2026-09-25/06_WHAT_REMAINS_TO_BE_DEVELOPED.md>) distinguishes documented capabilities and completed teaching examples from the fuller methods and implementations still to develop.

## 6. How the business-analysis context improves the teaching

| Destination | Useful addition | Boundary that preserves meaning |
|---|---|---|
| Making Business Credit Work, Part 2 | Put customer receipts, loan repayment and facility expiry on one dated schedule | Commercial margin and cash available to repay are different quantities |
| Owner Earnings Project 1 | Link debt schedules to the owner's minimum cash, maintenance spending and withdrawals | Borrowing increases financing cash, not owner earnings; direct receipt/payment forecasts already contain working-capital timing |
| Owner Earnings Project 2, Parts 7–9 | Add commitment/refinancing calendars and a bank earnings-to-capital-to-distribution bridge | EVE is not share-market value; accounting earnings are not automatically distributable cash |
| Mwendo Pamoja | Implement the existing cohort/waterfall design with curve, reset, collection and refund timing scenarios | A refund receivable reaches available funds only when received under the transaction's rules; internal FTP is not an SPV payment |
| Underwrite to Collect and its whitepaper | Show how rate stress changes affordability, utilisation, collection timing, recovery value and lender action | Better prediction does not by itself establish the causal benefit of a collection intervention |
| SokoIntel financial analytics workbench | Reuse a quantity dictionary, dated cash-flow schema and reconciled calculation outputs | A shared interface can present different sector models without forcing one universal valuation formula |
| IFRS 17 material | Connect insurer claims, investment cash, reinsurance receipts and remittance restrictions to dates | Insurer accounting, lender receivables, SPV debt and parent distributions belong to different records |
| Bayesian relativities and credit research | Supply estimated frequency, severity, behaviour and uncertainty where supported by data | Reuse existing derivations; pricing, discounting and legal cash allocation remain separate calculations |

The research contribution can therefore be framed as a testable question: **Does adding behavioural and funding information improve cash-flow forecasts and decisions beyond a benchmark-plus-credit-score approach?** Suitable comparisons include payment-timing errors, margin adequacy, calibration by vintage and cash-shortfall prediction. Mortgage datasets can support loan age, prepayment, delinquency and recovery studies; they do not establish Kenyan deposit behaviour, MSME business cash flows or local hedge availability.

## 7. What belongs in the core, and what goes further

**Core revision:** benchmark and contract conventions; money-to-margin pricing; curve purposes; matched funding; deposit and loan behaviour; NII/EVE/liquidity separation; accounting events; approvals and reconciliation.

**Companion laboratories:** deposit replication, scenario cash flows, hedge economics and collateral; borrower order/debt calendar; SPV cash waterfall; bank and insurer distributions. These make the existing ideas usable without overloading the introductory narrative.

**Advanced research:** option-adjusted spreads, counterparty valuation, counterparty capital, modelled dependence and advanced neural architectures. Preserve these as separate modules with their own data, assumptions and validation requirements. FRTB, SA-CVA and SA-CCR should not be presented as one interchangeable capital calculation. A local derivative strategy requires evidence of instruments, prices, documentation and operational ability before any deployment claim.

## 8. Recommended next editorial step

Keep the four core articles, expand their worked cases, and add companion laboratories as needed. Use the [revision blueprint and proposed paragraphs](<../../../output/kesonia_treasury_deep_review_2026-09-25/03_REVISION_BLUEPRINT_AND_INSERTS.md>) to revise each part. Use the [checked casebook](<../../../output/kesonia_treasury_deep_review_2026-09-25/02_CALCULATION_AND_CASEBOOK.md>) for numerical teaching material.

This review is a development package. It does not silently rewrite the canonical articles, retire unique derivations, fit empirical models or claim that a treasury platform has been built. The immediate gain is a precise route from the useful material to publishable explanations and testable implementation work.


---
Project copy. [Master review pack](<../../../output/kesonia_treasury_deep_review_2026-09-25/00_READ_ME.md>).
