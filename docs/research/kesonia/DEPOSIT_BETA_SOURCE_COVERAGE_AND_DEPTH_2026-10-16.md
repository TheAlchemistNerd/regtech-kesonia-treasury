# Deposit beta: source coverage and research depth

**Review date:** 16 October 2026
**Natural owner:** RegTech-KESONIA Treasury
**New manuscript:** publications/linkedin/Deposit_Beta_KESONIA_and_Bank_Risk_2026-10-16.md
**Companion post:** publications/linkedin/Deposit_Beta_Companion_Post_2026-10-16.md

## Editorial result

The article body contains **3,500 words** under the declared reproducible count: remove standalone numbered citations and Markdown heading/emphasis/table markers; split on whitespace; count tokens containing at least one Unicode letter or number. The title, headings, questions, equations and worked examples are included. Editorial metadata and references are excluded. Word processors can count formula tokens differently.

The article is self-contained, with four research questions after the abstract and 12 IEEE-style references in first-appearance order. It develops a joint funding–credit framework and a fully stated hypothetical bank calculation. It does not require reading another project or a previous article to understand the argument. No original series manuscript was edited.

## Supplied text: complete reading coverage

Input: C:/Users/Nevo/.codex/attachments/6da43e01-52d6-4c0a-849a-6f52f84280bb/Pasted text.txt. All **639 physical lines**, including blank lines, duplicated conversation markers, source snippets and corrupted equation fragments, were read. The contiguous ranges below cover the complete file once; the ranges group decisions, not a selective keyword search.

| Lines | Material read | Editorial treatment |
|---|---|---|
| 1–3 | Definition and suggested resources | Retain definition; replace generic suggested guides with primary research. |
| 4–9 | Beta equation and deltas | Preserve visible ratio, define rates and matching interval. |
| 10–15 | Zero, 35% and 100% interpretations | Retain arithmetic; remove implication that zero beta means keeping a costless full spread. |
| 16–22 | Product beta ranges | Do not transplant unsourced US-style ranges into Kenyan calibration. Use segmentation and empirical research design. |
| 23–30 | NIM, retention, IRRBB and follow-up prompts | Explain asset-minus-deposit spread versus accounting NIM; retain retention/IRRBB connections; omit chat prompts. |
| 31–58 | Search snippets, videos and publication leads | Verify relevant primary papers and central-bank sources independently. |
| 59–72 | Credit-risk prompt, definition and lifecycle | Integrate credit decisions into Treasury/ALCO; avoid repeating an introductory lifecycle catalogue. |
| 73–84 | PD, LGD, EAD and EL | State consistent horizon; distinguish expected loss illustration from full IFRS 9 measurement. |
| 85–94 | Funding/credit interaction and capital claims | Replace deterministic risk-taking narrative with conditional strategy, cash-flow transmission and separate constraints. |
| 95–107 | NMD definition and core/volatile split | Develop cohort, account, relationship and product persistence; core funding remains an estimated classification. |
| 108–114 | Runoff, behavioural beta and maturity caps | Separate price and quantity; correct broad cap language to Basel category-specific standardised treatment and applicable mapping. |
| 115–124 | Outflow models, OAS and replication table | Develop replication objective and constraints. OAS is not treated as a validated universal withdrawal model. |
| 125–135 | 20% overnight / 30% two-year / 50% five-year ladder | Retain as a proposal; calculate 3.1-year weighted maturity; explain evidence and risk needed to justify it. |
| 136–147 | “Is beta how KESONIA enters credit risk?” and benchmark formula | Use the two-channel answer; verify official compounded benchmark and premium scope. |
| 148–159 | Low-beta aggressive lending / high-beta safe lending | Reject automatic mapping; compare capital, margins, competition and sustainable returns. |
| 160–174 | Borrower-distress loop, summary table and simulation offer | Retain interacting pressures; replace decision table with explicit bank scenario. |
| 175–202 | Kenyan source snippets and potentially dated assertions | Verify CBK directly; omit unverified current-market claims and social-media snippets. |
| 203–211 | Corrected high-level interpretation | Make this the article's central organizing argument. |
| 212–223 | Three transmission effects | Develop liability and asset branches meeting in bank income, liquidity, value and capital. |
| 224–417 | Pricing, weighted funding-cost equations and badly broken Unicode/formula fragments | Reconstruct economic identities; introduce FTP attribution and exact changing-funding-weight decomposition. |
| 418–451 | Kenyan RBCPM and beta as an internal ALM input | Verify final August 2025 framework and April 2026 report; separate customer pricing from internal economics. |
| 452–486 | Interactive shock numbers and spread caveat | Explicitly reconcile 30% beta → 140 bp gain and 35% beta → 130 bp gain; extend to actual NII, runoff replacement and expected loss. |
| 487–627 | Hierarchical credit proposal, splines and integrated model table | Preserve joint-model research aim; explain pooling and alternative credit horizons; require observed cash-flow/behavioural evidence. |
| 628–639 | Two corrections and final research proposition | Preserve strategic discretion and integrate into research questions and ALCO decisions. |

The pasted source has encoding damage; line fragments are treated as pieces of the surrounding formula, not additional mathematical claims. Its “contractual beta” language is not accepted as a universally defined metric.

## SVG reading

Input: C:/Users/Nevo/Downloads/download.svg. The complete SVG source was inspected. Its viewBox is 340 × 330. It shows policy/interbank conditions → KESONIA/market rates → liability channel (beta, runoff, funding costs) and asset channel (loan repricing, debt service) → bank profitability, liquidity, PD/LGD → pricing and risk appetite.

This is a useful conceptual map. The converging arrows do not establish statistical identification, causal direction among all outcomes, estimated parameters or validated bank integration. The article supplies the measurement and decision layers missing from the graphic. Its reference to bank EVE and capital broadens the map's bank-outcome box.

## How deep the existing corpus already goes

| Area | Evidence already present | Remaining research depth |
|---|---|---|
| RegTech deposit response | research_lab/operations.py:167–275 and tests/test_operations.py:76–107 implement segmented synthetic asymmetric immediate/one-month-lag OLS, frozen future holdout, parameter recovery and singular-design rejection. OPERATIONS_METHODOLOGY.md:61–87 explains design and uncertainty limits. | Actual longitudinal account data; lag selection; robust standard errors; rate-level and regime effects; forecasts with uncertainty. |
| Cohorts and retention | operations.py:276–358; tests/test_operations.py:109–140; OPERATIONS_METHODOLOGY.md:89–109 separate external withdrawals, same-bank migration and inflows, then enumerate a retention-constrained short maturity ladder. | Continued interest expense/withdrawal of migrated balances; customer selection; multiple cohorts; longer-horizon retention and rolling replication. |
| NII/EVE/liquidity | REGULATORY_WORKED_CASES.md:148–214 and regulatory_cases.py:206–262 implement a same-opening-book example with different NII/EVE balance assumptions. Independent tests are at test_regulatory_cases.py:86–122. | A joint dynamic path with calibrated behaviour, endogenous funding replacement and validated full supervisory scenarios. |
| Treasury/FTP | OPERATIONS_METHODOLOGY.md:1–59 provides dated funding contributions, explicit contingent costs and internal elimination. October 3 IFoA and October 4 screenshot reviews develop ALCO, uncertainty and decision governance. | Institutional curves, product conventions, incentives, reconciled reports and tested action policies. |
| Mwendo | mwendo_operating_case/model.py:195–200 and 424–469 compound synthetic note funding, trace recovery delay/coupon loss/capital time, and solve a clearing coupon; tests feed price back through affordability. | An SPV funding/reset problem remains distinct from a bank deposit franchise. It supplies cash mechanics, not estimated NMD beta or causal bank risk appetite. |
| Underwrite | research_lab/cases.py:104–180 and tests/test_cases.py:31–72 distinguish average-drawn interest, stressed EAD, margin budgets and dated lifetime losses. | Borrower-level behavioural estimates and intervention evidence must be linked to, rather than conflated with, bank Treasury models. |

The corpus is **already deeper than the introductory paste**. The new material's contribution is a coherent, externally sourced synthesis and a clear next empirical programme. It should not be described as the first appearance of beta, FTP, NMD modelling, bank NII/EVE or lifetime credit economics.

RegTech's current status matrix is docs/methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md:40–59. Earlier September gap registers are historical evidence; they should not be used to erase subsequent implemented examples.

No current file establishes empirical Kenyan beta estimates, an identified beta→PD causal effect, an institutionally validated deposit-duration model or a production bank ALCO engine.

## Authority and claim checks

Article reference numbers are used below.

- [1] CBK April 2026 MPC report: full March 2026 implementation, checked in report text and glossary.
- [2] CBK KESONIA page: administrator, unsecured overnight volume-weighted basis, unchanged predecessor methodology and historical data context.
- [3] Final August 2025 RBCPM: compounded reference, product/currency perimeter, K and separate charges. Consultation responses are not treated as the final policy.
- [4], [6] New York Fed: deposit-rate measurement and historical US timing. The near-0.4 claim is specifically cumulative interest-bearing beta in 2022 Q4.
- [5] Emin et al.: peer-reviewed Journal of Financial Intermediation article; two average estimators 0.30/0.46 and regime means 0.26/0.49 are identified separately. No foreign estimate is imported as a Kenyan calibration.
- [7] Dias/Scott: Federal Reserve working paper, identified as such rather than peer-reviewed evidence.
- [8] Osoro/Talam: KBA working paper; local market-feedback evidence, not a bank-account beta dataset.
- [9] Drechsler et al.: peer-reviewed Journal of Finance paper; economic argument for matching franchise income sensitivity and fixed-rate assets.
- [10] Basel SRP31: version identified explicitly; NMD caps are standardised-framework category constraints, not an unverified blanket Kenyan rule.
- [11] US FTP guidance: supervisory applicability is stated; used for economic comparison.
- [12] IFRS Foundation: standard owner and implementation resources; the article's one-period loss illustration is not presented as a booked ECL figure.

Only short paraphrases of external findings are used. The behavioural designs, decomposition, hypothetical bank and decision examples are the article's analytical development.

## Numerical verification

All amounts below are hypothetical KES, annualised with a constant full-year exposure unless the scenario states replacement.

- Simple spread: 13% − 4% = 9%; beta 0.30 gives 15% − 4.60% = 10.40%; beta 0.35 gives 15% − 4.70% = 10.30%.
- Bank balance sheet: 100m assets = 80m deposits + 10m wholesale + 10m equity.
- Baseline NII: 13m − 3.2m − 1m = 8.8m.
- Shock NII: 15m − 3.76m − 1.2m = 10.04m; change = 1.24m.
- Replacement funding: 8m × (12% − 4.70%) = 584,000; NII after replacement = 9.456m; improvement = 656,000.
- One-period expected-loss increase: (4% − 2%) × 45% × 100m = 900,000.
- Change in NII less that expected-loss charge: 656,000 − 900,000 = −244,000.
- Replication-ladder weighted maturity: 20% × 0 + 30% × 2 + 50% × 5 = 3.1 years.
- Cohort: 100m − 8m − 12m = 80m original-product retention; 92m bank-retained cohort; +15m new inflows gives 95m product closing.

The bank scenario does not model endogenous exposure, timing of default, foregone coupon, recovery delays, tax or capital changes. It is a defined NII-minus-simplified-EL attribution, not a complete economic-profit or IFRS 9 calculation. A full expected-cash-flow model must reconcile lost income, recovery and provisions to avoid double counting.

## Files and review boundary

Only the three new Markdown outputs named at the top were created. Existing series, laboratory code, historical reports and guest repositories were left unchanged. The repository had substantial pre-existing modifications and untracked work before this task. No commit, push or LinkedIn publication was performed.

The writing-style skill was read. Its dedicated retrieval tools were unavailable; the manuscript follows the user's explicit preferences rather than claiming a retrieved style match. Word/PDF production is a subsequent review step, after manuscript approval within the parent task.

## Fresh focused verification

On 16 October 2026, the parent review ran the operations and regulatory-case suites using the bundled Python runtime with bytecode writing disabled. All **49 tests passed**, exit code 0, in 86.217 seconds. The run did not regenerate outputs. This verifies the current focused synthetic examples; it does not extend their empirical scope.
