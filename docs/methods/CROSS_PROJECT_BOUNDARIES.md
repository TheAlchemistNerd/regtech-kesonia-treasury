# KESONIA, treasury and credit: boundaries across the project family

**Review date:** 28 September 2026; implementation status reconciled 1 October 2026
**Purpose:** Give the RegTech revision a reliable account of what other projects already own, what can be reused, and what requires a distinct rule, contract, model or operational implementation.
**Status:** Source-grounded editorial and interface review. This document does not approve a financial product, accounting treatment, regulatory interpretation or software integration.
**Audit write scope:** The cross-project audit read the other projects without editing them. Its results are integrated into RegTech only; guest repositories remain unchanged.

## 1. Findings that should govern the revision

1. **KESONIA, risk-based customer pricing, funding allocation and valuation are complementary layers with distinct financial quantities.** The common KESONIA reference, customer all-in rate, note coupon, FTP allocation, valuation discount rate and forecast curve connect through dated cash and approved policies. They may share observations or scenarios, but their purposes, parties, horizons and approval authorities differ. The existing Underwrite Part 5 already provides much of the required bridge.
2. **The final CBK bank pricing framework adopts compound-in-arrears for its covered variable-rate KES lending.** The published rule is not merely an optional compounding illustration. Conversely, that banking-sector rule does not by itself prescribe a non-bank digital lender's product or an SPV note coupon. Entity, product and contract scope must be established before applying the rule.
3. **Financing a business and financing an identified pool of receivables are already distinguished in Underwrite to Collect.** Mwendo's controlled documents further specify the SPV, eligible assets, accounts, reserves and waterfall. RegTech should consume these definitions instead of presenting the distinction as an undiscovered gap.
4. **SokoIntel's current specification already incorporates the credit, SPV and owner-earnings interfaces.** The earlier September 2026 addenda describe their introduction; they are no longer sufficient evidence that the canonical requirements are missing. Adoption in a specification is still different from implemented, tested software.
5. **Bayesian relativities owns the insurance frequency/severity, credibility and ratemaking work.** Credit default, lender ECL, insurer IFRS 17, regulatory capital and SPV enhancement must retain separate quantities and models. Shared scenario identifiers are useful; relabelling the same model as all five outputs is not.
6. **Several older RegTech reviews mix useful design ideas with unsupported assertions of legal necessity or readiness.** Preserve their history and harvest their useful controls, but mark the affected assertions as superseded by the current scoped specification. A proposed control, a vendor capability and a worked illustration each need their own status.

## 2. Reading scope and source precedence

This review inspected substantive passages in the sources listed in section 10: pricing and compounding, the SPV financing stack and waterfall, credit/insurance/accounting interfaces, business cash and owner claims, SokoIntel requirements and data contracts, and the existing RegTech review/casebook/register. It is a **targeted cross-project review**, not a claim that every line of every large manuscript or every referenced workbook was independently checked. No guest workbook was recalculated and no vendor integration was exercised in this audit.

Apply this precedence within each subject:

| Material | What it can establish | What it cannot establish alone |
|---|---|---|
| Applicable final rule and current supervisory communication | The rule's actual entity/product perimeter, effective dates and required treatment | Terms of an unrelated SPV, a non-bank product or an unexecuted agreement |
| Executed financing/product documents | Parties, recourse, benchmark convention, payment obligation, account control and waterfall | Compliance with a different entity's rules or an accounting conclusion |
| Approved accounting, model and treasury policies | Controlled implementation choices within the applicable rules and contracts | A contractual amendment or legal exemption |
| Current controlled specifications | Intended architecture, definitions, models and interfaces | Production operation, calibration, legal execution or accounting approval |
| Whitepapers and articles | Explanation and examples tied to the controlled definitions | New authoritative commercial terms |
| Review notes, screenshots, pasted material and vendor descriptions | Questions, useful methods, proposed extensions and evidence leads | Proof of a legal mandate, model adequacy or working integration |

Mwendo's term sheet explicitly says that executed documents prevail and that its current terms are illustrative and non-binding [M2]. The historical reviews must not reverse that hierarchy.

### Regulatory verification supplied by the parallel fact check

The main review verified the [CBK Revised Risk-based Credit Pricing Model, August 2025](https://www.centralbank.go.ke/wp-content/uploads/2025/08/Revised-Risk-based-Credit-Pricing-Model.pdf). Its section 4 establishes compound-in-arrears within the banking-sector variable-rate KES perimeter; fixed-rate and foreign-currency loans are excluded. The premium includes borrower risk, operating expenses and shareholder return. Section 5 addresses disclosure of weighted premiums, fees and APR. A submitted consultation request for an exemption is not the final exemption.

Appendix I describes a **five-day** lookback. The verified text does not explicitly settle business-versus-calendar-day wording or every observation/weight mapping needed by software. Do not silently promote the older review's “strict five business days” statement into a verified rule. Preserve the exact published wording, identify the unresolved convention, and require the authoritative implementation interpretation before production calculations depend on it. The parallel fact check also reports ACT/365 index calculation, 18-decimal underlying precision, eight-decimal publication, and publication at 9 a.m. on the next business day. Distinguish published index precision from internal accrual rounding and customer statement rounding.

The main fact check also verified section 1.3 of the [CBK April 2025 Basel III liquidity and leverage guidelines](https://www.centralbank.go.ke/wp-content/uploads/2025/04/GUIDELINES-ON-BASEL-III-LIQUIDITY-STANDARDS-AND-LEVERAGE-RATIO.pdf): the LCR, NSFR and leverage guidelines apply to institutions licensed under the Banking Act and took effect on 1 October 2025. Accordingly, do not describe Kenyan LCR/NSFR adoption as wholly unverified. Identify the covered bank and applicable calculation instead. This does not automatically subject the SPV or every non-bank lender to those bank requirements.

## 3. Keep the financial quantities separate

### 3.1 A shared dictionary

| Quantity | Definition and required dimensions | Primary owner/application |
|---|---|---|
| Daily KESONIA fixing | Dated overnight benchmark observation; publication date/time, effective date, percentage/decimal unit, correction version and source | Benchmark evidence and ingestion |
| Period compounded benchmark | Accumulation over a governed observation/accrual schedule; a factor and, where required, its annualised equivalent | Covered bank product calculation or separately specified contractual use |
| Customer rate and charges | Applicable benchmark plus customer premium, with fees and disclosure conventions identified separately | Originating lender; Product, Credit, Finance and Legal approvals |
| Investor note coupon | The issuer's contractual payment to a note class; benchmark convention, margin, balance, currency, floor/cap and payment date | SPV finance documents and calculation agent |
| FTP rate/charge | Internal allocation of funding, liquidity, basis and optionality economics to an institution's assets and liabilities | Treasury/ALCO and Finance policy |
| Expected loss | A money amount for a specified entity, exposure, horizon, probability model, recovery timing and discount convention | Credit model/Finance; converted into a pricing component only through a documented bridge |
| Economic capital and capital charge | Allocated risk capacity versus the money return required on that allocation; a stock and a flow are different | Risk appetite/Finance pricing policy |
| Regulatory capital | Entity-specific regulatory calculation and eligible capital under the applicable rule version | Regulated entity and regulatory reporting |
| Enhancement/reserve | Contractual subordination, overcollateralisation, funded reserve or other support, with amount, availability and exhaustion rules | SPV documents and stateful waterfall |
| Discount/forward/forecast curve | Dated term structure with instrument set, currency, horizon, interpolation, collateral assumptions, measure and intended use | Valuation, ALM or scenario engine; not produced by renaming realised overnight compounding |
| Owner-distributable cash | Cash that the relevant entity can prudently and lawfully distribute after dated claims, restrictions and buffers | Business owner, parent or shareholder analysis |

This largely reuses [M1, sections 2–5], [U1, customer-premium/FTP bridge and financial-measure table], [S1, FR099 and section 6.2.1], and [O3, financial-quantity dictionary]. It should be one cross-project contract, not a new inconsistent glossary in each article.

### 3.2 Resolve the existing factor notation before exchanging data

Mwendo Part 5 denotes the **excess accrual factor** by `F = product(1 + r_i d_i / D) - 1`. Underwrite Part 5 uses `F = product(1 + r_i d_i / D)` for the **gross accumulation factor**, then computes interest with `F - 1`. Both are coherent within their documents. Exchanging an unqualified field called `F` would create a one-principal error.

Use explicit names:

```text
gross_accumulation_factor = product(1 + fixing_decimal_i * weight_days_i / basis)
benchmark_accrual_factor = gross_accumulation_factor - 1
annualised_benchmark_rate = benchmark_accrual_factor * basis / total_accrual_days
interest_money = principal_money * benchmark_accrual_factor
```

For a contract with a **simple additive margin** over a constant principal:

```text
coupon_accrual_factor = benchmark_accrual_factor + margin_decimal * days / basis
coupon_interest_money = principal_money * coupon_accrual_factor
```

Do not apply that margin treatment where the contract specifies another convention. Changing principal requires effective-dated cash-flow handling; applying one opening balance to the whole period is not a general solution. A number quoted as an annual percentage must be converted to a decimal before multiplication. A period factor cannot be added directly to an annual percentage margin.

**Illustration, not a prescribed CBK schedule:** three equal one-day weights, an unchanged 10% annual fixing and ACT/365 produce an excess factor of `(1 + 0.10/365)^3 - 1`, approximately `0.000822143`. On KES 1,000,000 that is approximately KES 822.14 benchmark interest. A simple 4% margin for the same three days adds KES 328.77, giving approximately KES 1,150.91. The annualised compounded benchmark is approximately 10.00274%; the excess factor is approximately 0.0822143%. These are different representations of the same period accrual. Actual schedule, lookback and rounding must be supplied by the governed implementation.

### 3.3 A defensible customer-premium/FTP bridge

Underwrite already develops the bridge [U1, lines 64–135]. In a matched period, express the funding difference as:

```text
funding_difference = approved_FTP_rate - applicable_period_benchmark_rate
customer_premium_bridge = funding_difference + loss_component + operating_component
                          + servicing_component + capital_return_component
                          + profit_component + other_approved_components
```

This internal reconciliation supports the bank-approved pricing model within CBK's benchmark-plus-premium framework. It explains how funding, loss, operating costs and shareholder return contribute to the price. The final framework allows bank-defined components; it does not mandate this exact FTP decomposition. Components must be expressed on compatible balances, horizons and units. If the borrower-risk allowance already contains expected loss, do not add that same expected loss again. If capital return is already contained in a specified shareholder-return component, do not duplicate it under another label. Margin, lifetime expected loss, a regulatory capital stock and a one-year return hurdle cannot be added without transformation.

A daily data refresh does not itself authorize daily changes to a customer's instalment, margin or agreement. Separate scheduled accrual, contractual benchmark reset, correction of an input error, a new offer, a proposed modification and an approved amendment [U1, lines 35–62; M3, lines 426–436].

## 4. Entity and accounting boundaries

| Entity or analytical layer | Reuse from the existing work | Boundary the RegTech revision must retain |
|---|---|---|
| In-scope bank lender | Covered KESONIA bank pricing, IFRS 9 asset treatment, treasury funding, relevant capital/liquidity controls | Confirm actual entity and instrument perimeter. Bank rules do not automatically become SPV rules. Fixed-rate and FX products need their own basis. |
| Non-bank digital lender | Credit cash flows, collection evidence, pricing bridge, funding and applicable lender obligations | Do not infer that the bank benchmark rule, banking-book IRRBB, LCR/NSFR or a bank capital model applies merely because the lender is digital or uses KESONIA. |
| SPV issuer | Eligible receivable cash, account controls, reserves, tranches, triggers, coupon conventions and waterfall | A note margin is not automatically customer `K`. A waterfall is not an internal FTP allocation. Ring-fencing requires rights and controls; it does not eliminate servicer, sponsor or operational dependence. |
| Insurer | Claim frequency/severity, policy service, claims payments, reinsurance and applicable IFRS 17 inputs | Insurance premium/claim/refund accounting is not the lender's loan accounting. A posterior uncertainty interval is not automatically the IFRS 17 risk adjustment. |
| Lender/holder accounting | Contractual cash flows, EIR, ECL inputs and event classification | Separate ordinary floating-rate reset, modification, derecognition, correction, impairment and write-off. Do not apply a financial-liability 10% test as an automatic universal loan-asset rule. |
| Consolidated group/parent | Entity-level earnings, restrictions, capital, permitted remittances and dated owner cash | Local cash and local regulatory headroom are not automatically parent-distributable cash. Do not deduct the same local claims again after using net permitted remittances. |
| SokoIntel | Typed data, evidence, scenarios, comparisons, analytical adapters and stateful simulation | Current scope does not authorize executing loans, amending contracts, settling claims, operating vehicles, posting journals or supervising an institution. |

Mwendo has a KES operating/asset/account/waterfall design expressed at a USD-equivalent presentation scale. Its USD-equivalent 9 million financing stack is **not an all-senior USD 9 million obligation**: Class A is 6.75 million equivalent, Class B 1.35 million and Class C 0.9 million [M1, lines 203–230; M2, lines 26–61]. A USD reporting presentation does not by itself create FX debt or justify a cross-currency hedge. The optional HoldCo facility remains a separate claim unless binding documents connect it.

Credit enhancement, legal true sale, accounting derecognition, consolidation and regulatory capital relief are distinct assessments. None is established simply by using an SPV, assigning a receivable or describing the vehicle as bankruptcy remote. The term sheet already retains these boundaries [M2, lines 164–176].

## 5. Financing a business, a facility and a ring-fenced cash stream

The useful unit of analysis is the **claim being financed**, with its payer, evidence, timing, recourse and control.

| Question | Business/facility finance | Receivable or SPV finance | Owner/equity endpoint |
|---|---|---|---|
| What supports repayment? | The business's operating cash and other agreed recourse, constrained by all its obligations | Identified eligible assets and their transferred/pledged rights, plus precisely defined support | Residual cash after the relevant entity's senior claims, restrictions and reinvestment needs |
| What evidence is central? | Economic entity, purpose, trading cycle, obligations, sustainable cash generation | Asset identity, obligor, enforceability, eligibility, collection account, servicer, dilution/refund rights and timing | Owner labour, maintenance investment, working capital, capital restrictions, debt and distribution dates |
| What can go wrong? | Purpose/schedule mismatch, hidden related exposures, weak margins or working-capital shortage | Invalid/incomplete transfer, commingling, ineligible assets, delayed collections, exhausted reserves or servicer interruption | Attractive earnings with little transferable cash, a premature distribution or a required replacement cost omitted |
| What metric belongs here? | Dated debt-service headroom, borrower liquidity and approved facility economics | Contract-defined borrowing base, coverage, tranche cash and reserve state | Claim-consistent owner earnings, FCFE/dividends or parent cash availability |

Underwrite Part 1 already ties the loan to the economic unit, business clock and use of proceeds [U2]. Underwrite Part 5 explicitly provides the optional SPV branch, including account architecture, transfer/servicing, borrowing base, coverage, reserves and liquidity-versus-loss protection [U1, lines 816–923]. It does not claim every loan should be moved to a vehicle.

For Mwendo, distinguish:

- Class A's **75% share of the financing stack**;
- a contractual **advance rate** applied to an eligible balance;
- **overcollateralisation**, whose numerator and note denominator must be specified; and
- a **reserve**, with a location, permitted use and replenishment rule.

The controlled illustration uses total capital 9 million equivalent and a 75% advance assumption to imply 12 million eligible assets, then compares those assets with 8.1 million debt notes to obtain approximately 148.15% coverage [M1, lines 232–261]. Reuse the arithmetic only alongside its explicit definitions. The coincidence of a 75% Class A share and a 75% advance assumption does not make them the same ratio.

The business-credit article supplies a complementary borrower-side analysis: compare offers on usable proceeds, maturity and downside cash, then reconcile bank credits to actual operating sales and connected counterparties [B1, lines 19–108]. It does not replace the SPV claim analysis. An automatic cash sweep that helps a lender this week can reduce the borrower's inventory funding and later repayment capacity; this must remain an explicit scenario, not an assumed welfare improvement.

## 6. Project ownership: what to reuse and where the extensions belong

| Project | Existing substantial content | Appropriate next contribution | Avoid recreating or transferring incorrectly |
|---|---|---|---|
| RegTech–KESONIA | Benchmark evidence, calculation controls, treasury cases, remaining-work register, STP design | Governed rate/curve engine; reproducible cash-flow and funding cases; rule/contract/policy provenance; integration acceptance tests | A second master credit loss model, a replacement SPV term sheet, a claim that every institution needs every advanced capital module |
| Underwrite to Collect | Business/facility cash, interventions, ECL/capital/FTP bridge, liquidity boundaries, optional receivable vehicle and roles | Explanatory articles and connected case material grounded in the existing Part 5 | Calling already-written distinctions new discoveries or inferring causal treatment effects from a scenario comparison |
| Mwendo Pamoja | Product-cohort loss and refund interfaces, financing stack, borrowing base, accounts/reserves and waterfall | Demonstrate asset cash → SPV receipts → class cash → dated residual under common scenarios | Making bank FTP a contractual waterfall payment; applying insurance IFRS 17 to the whole financing vehicle |
| Bayesian telematics relativities | Insurance frequency/severity, exposure, credibility, rating layers, development/payment timing, reinsurance and accounting handoff | Supply insurer cash distributions and approved calibration/scenario metadata | Repeating gamma/negative-binomial derivations in RegTech or treating claim frequency as credit default probability |
| African business credit Part 2 | Purpose and trading-cycle fit, offer comparison, connected entities and bank-cash reconciliation | A consistent borrower case connecting usable proceeds, operations, debt service and owner effects | Borrower suitability inferred from lender RAROC; related payment automatically labelled fraud |
| Owner Earnings Project 1 | Owner labour, maintenance, working capital, dated liquidity, debt and buying/selling | Connect lending terms to retained operating capacity and prudent distributions | SDE/owner-operator benefit, transferable earnings, CFADS and immediate distribution treated as synonyms |
| Owner Earnings Project 2 | Public-filings bridges, equity claim, banks/insurers, capital and remittances | Connect institution-level profitability to capital-constrained distribution and parent liquidity | Industrial-company cash-flow adjustments copied unchanged into banks/insurers; local profit treated as parent cash |
| SokoIntel workbench | FR099–FR132 and shared entity/evidence/cash/facility/protection/pool/waterfall/owner contracts | Implement and test the adopted interfaces in bounded modules; map reviewed cases to acceptance fixtures | Writing the same requirements as though newly proposed; implying the workbench is a lender, insurer, TMS, GL or regulatory approval system |

### Owner earnings: two concrete constraints on the common case

Project 1's normalisation bridge explicitly estimates economic earning power after market replacement labour, maintenance and required working capital. That does not equal today's permitted owner withdrawal [O1]. Project 1 Part 4 separately calculates dated obligations and reserves; do not subtract an anticipated late receipt again if it was never in the opening cash [O2].

Project 2 requires a claim-specific valuation bridge: FCFF with the appropriate operating discount/enterprise-to-equity bridge; FCFE with an equity discount; permitted parent remittances with entity/date constraints [O3]. Its bank/insurer article also separates regulatory headroom, declared dividends and sustainable distribution. An economic capital return charged in pricing is not a second cash payment automatically deducted after the same earnings have already absorbed the underlying costs [O4].

**Small guest follow-up to retain, without editing the guest:** Project 1 Part 1's example calculates KES 990,000 after the KES 300,000 replacement-pay adjustment, but a subsequent sentence still refers to KES 1.29 million normalised earning power. That sentence appears to retain the pre-adjustment subtotal. The correct shared fixture should expose the adjustment ledger and use one declared endpoint; resolve the article text with its owner before copying it.

### Insurance handoff

The relativities paper already separates expected claim cost, expenses, risk transfer, capital provision and commercial layers [A1, section 2.4]. Its section 12 supplies the IFRS 17 boundary: the actuarial process hands over cash flows, timing, uncertainty, cohort and reconciliation metadata; accounting owns grouping, measurement choices and presentation. Daily usage observations do not establish a new short-duration insurance contract or automatic PAA eligibility. An accepted refund receivable is not received cash. The lender, insurer and SPV must record distinct rights and settlements [A1; A2].

## 7. Minimum shared data contracts

These consolidate interfaces already present in the controlled documents and SokoIntel. They are proposed cross-repository contract names, not a claim that identical executable schemas have been deployed.

| Contract | Minimum fields | Owner and acceptance condition |
|---|---|---|
| `BenchmarkObservation` | benchmark, currency, effective date, publication time, source, decimal rate/index value, precision, correction/supersession version, retrieval timestamp | Benchmark steward; reproduce the as-known observation for any prior decision cutoff |
| `AccrualConvention` | governing rule/contract/policy ID and version; scope; accrual period; observation mapping; day count; non-business-day weights; lookback; margin treatment; rounding; fallback; floor/cap | Product/Legal/calculation owner; unresolved values explicit, no silent production default |
| `CurveSnapshot` | currency, valuation date, intended use, measure, instrument quotes, quote status, collateral/funding assumptions, interpolation/extrapolation, calibrated parameters, repricing residuals | Treasury/valuation owner; reproduce each calibration instrument and distinguish market evidence from assumption |
| `EconomicQuantity` | value, unit/scale, currency, legal entity, claim, balance basis, period/date, sign, measure, evidence status, source/version | Shared analytical contract; unknown is not zero; incompatible quantities cannot be silently aggregated |
| `FacilityContract` / `FacilityEpisode` | parties, purpose, commitment/draw history, maturity, schedule, security/recourse, price/reset terms, amendments, decision and availability timestamps | Lender/product owner; replay the terms actually known and in force at each date |
| `ProtectionAndClaim` | policy/guarantee/refund right, covered event, trigger, exclusions, deductible/limit, counterparty, claim date, acceptance, expected/actual settlement, costs and expiry | Relevant protection owner; do not count both the recovery right and its cash receipt as two recoveries |
| `PoolAndWaterfallState` | asset identity/eligibility, transfer status, borrowing base, note balances, arrears, reserve balances/restrictions, collections, triggers, priority rules and distribution state | SPV/servicer/calculation agent; cash conservation and state roll-forward hold under normal and stressed cases |
| `LossAndAccountingHandoff` | default/cure/redefault definition, exposure, cash recoveries/costs/dates, scenarios/probabilities, discount basis, horizon, model version, accounting classification and approval/reconciliation key | Model owner plus Finance; output supports review and reconciliation, not automatic journal authority |
| `OwnerOrParentCashBridge` | source entity/claim, earnings adjustments, obligations, maintenance/WC, local restrictions, permitted remittance date, parent obligations and distribution policy | Owner/Finance analyst; preserve entity and date boundaries and deduct each claim once |
| `DecisionAndExecutionEvent` | analytical run, candidate, owner, approval/override, instruction, execution/confirmation, settlement/reconciliation status, idempotency key and exception | Operational system owners; analysis, authorization, execution and reconciliation remain separate states |

The existing SokoIntel `EvidenceRecord`, `CashEvent`, `FacilityContract`, `FacilityEpisode`, pool/waterfall and owner/bank/insurer contracts are the strongest implementation destination [S1, section 6.2.1]. RegTech should provide governed input/output schemas and reference cases; it should not become an undocumented second source of truth for the same financial objects.

## 8. How to revise the older reviews constructively

| Existing passage | Useful material to retain | Current formulation or treatment |
|---|---|---|
| Gap report, lines 37–44; enhancement report, lines 42–51 | Explainable premiums, review evidence, model monitoring | PD/LGD/EAD can inform a pricing loss component. They are not the exhaustive legal definition of the customer premium. SHAP/LIME may be chosen techniques; a Gini statistic is not a fairness assessment. |
| Gap report, lines 54–63 | Explicit accounting event classification and review | Separate asset and liability analysis, ordinary resets and actual modification/derecognition questions. Remove an automatic universal 10% loan-asset test or an assertion that every premium update forces a journal. |
| Gap report, lines 73–99 | Funding mismatch, security, audit evidence and institution perimeter | Identify which controls are legal obligations, policy choices or proposed engineering controls. Do not present specific encryption/PKI choices or bank IRRBB as automatic SPV mandates. Correct the all-senior USD stack description. |
| Enhancement report, lines 7, 29, 49 and 64 | Calculation discipline, audit trail and interoperable reporting | Replace “fully compliant/ready” implications with scoped evidence and open requirements. Preserve the official five-day wording pending authoritative mapping. A CBK-facing reporting API needs a verified interface; it is not established by proposing signed messages. |
| `cbk_kesonia_k_framework.md`, lines 11–18 | Link analytical inputs to pricing and distinguish investor margins | A governed system proposes/supports a premium decision. SPV note margins are contractual investor margins, not automatically institutional customer `K`. Structural profitability requires dated cash, costs, losses and priorities. |
| Compounding/curve note and additional pricing/treasury review | Distinction between realised compounding, term structure and institution funding | Retain and expand with numerical repricing. Add the actual covered-bank compounding requirement while preserving separate contractual use outside that perimeter. |
| STP/software review | System roles, identifiers, approval states, exceptions and reconciliation | Keep the explicit “documentation-based, not tested integration” boundary. Convert workflows into controlled mock interfaces and failure cases before claiming STP delivery. |
| Remaining-work register and casebook | Transparent completion requirements and illustrative calculations | Keep unfinished model calibration, applicable-rule checks, live integration and integrated cases open until their completion evidence exists. |

Suggested historical note for affected review files:

> This is a dated review record. Its useful design questions informed the current specification. Assertions about mandatory methodologies, institution scope, exact operating conventions or implementation readiness must be read against the current verified rule register, governed contracts and tested implementation. A topic's appearance in this report does not establish a legal obligation or a completed capability.

Suggested replacement paragraph for “where the contract elects compounded KESONIA” in Mwendo's explanatory Part 5:

> For banking-sector variable-rate KES lending covered by the final CBK framework, apply its compound-in-arrears common reference and the applicable implementation conventions. For SPV notes and other uses outside that product perimeter, establish the benchmark and accrual terms in the governing documents. A daily fixing, a period accrual factor and an annualised compounded rate are separate quantities; customer and investor margins retain their own contractual definitions.

This is proposed replacement text for the parent editor. No manuscript was altered by this review.

## 9. Connected case: acceptance requirements rather than another broad outline

One scenario family should connect the projects without forcing them into one measure or balance sheet.

### Case A — Borrower, benchmark and lender economics

Start from an actual-defined business purpose and usable proceeds, with a dated operating cash forecast and obligations. Add a precisely specified illustrative facility, benchmark schedule, premium/fees and repayment terms. Reconcile borrower cash received and paid with lender cash invested and received. Report borrower downside headroom separately from lender expected economics. Verify simple-period, annualised and effective-return displays on the same cash flows.

**Pass conditions:** cash dates and net proceeds match; every fee has a payer/recipient/date; matched-period FTP and loss components reconcile; no lifetime PD is treated as an annual spread; a refreshed signal cannot amend the contract automatically. Reuse [B1] and [U1].

### Case B — Asset cash to SPV and tranche cash

Feed eligible receivable events into the actual controlled Mwendo structure. Show a missed payment, later recovery, claim/refund acceptance and actual settlement as separate events; activate one reserve draw and one trigger. Compare scheduled collections, settled cash and available cash. Distribute to the 75/15/10 classes according to the defined priorities, not simply in proportion to ownership.

**Pass conditions:** every monetary unit is conserved through the accounts; reserve balances roll forward; unpaid interest/principal persist; no residual is distributed when a blocking condition applies; default and later recovery are not double-counted. Test a servicer interruption even when ultimate obligor receipts are unchanged. Reuse [M1, M2, U1].

### Case C — Treasury curve and funding path

Construct a small curve from explicitly labelled quotations or synthetic fixtures, state interpolation and reprice the instruments. Use dated amortising and revolving exposures. Show interest income, internal funding attribution, economic value and cash availability as different outputs under common scenario IDs.

**Pass conditions:** calibration residuals are shown; all outputs have matched entities, dates and units; a realised KESONIA index is not advertised as a forward curve; assumptions about available Kenyan instruments/tenors are visible. Existing casebook NII, EVE and cash sensitivities are separate illustrations, not already one reconciled dynamic balance-sheet simulation [R6].

### Case D — Insurer, financed policy and refund timing

Connect usage/claim evidence to the insurer cash-flow model; separately model the lender's financed premium, customer obligations, cancellation/refund rights and collection of the refund. Record insurer IFRS 17 and lender IFRS 9 handoffs separately.

**Pass conditions:** insurance service, financing cash, accepted claim/refund and cash settlement retain distinct dates; no automatic PAA inference from daily data; common scenarios do not erase different marginals, contract rights or accounting owners. Reuse [A1, A2, M1].

### Case E — Business and parent distribution endpoints

After the relevant claims above, calculate business owner earnings and an immediate distribution limit as separate outputs. For a bank/insurer or group, include local capital/liquidity restrictions, permitted remittance and parent receipt dates. Retain a case where positive year-end headroom coexists with an earlier cash shortfall.

**Pass conditions:** replacement labour, maintenance and working capital are applied once; cash already net of local claims is not charged again at the parent; a late remittance cannot pay an earlier obligation without an explicit bridge; FCFF, FCFE and owner-distributable cash labels follow their actual claim. Reuse [O1–O4].

### Case F — Demonstrated software workflow

Route the case through a mock benchmark feed, calculation run, approval, booking instruction, confirmation, settlement and reconciliation adapters. Include duplicate inputs, corrected benchmark values, missing quotes, rejected approval, partial execution and failed settlement.

**Pass conditions:** idempotency, versioning, evidence replay, exception ownership and reconciliation are demonstrated. A mock proves the interface behavior only; it does not prove access to a vendor, a market, a supervisor endpoint or an institution's live workflow. Reuse [R5] and [S1].

## 10. Source map and exact entry points

Line anchors refer to the working files inspected on 28 September 2026. Later edits can move the lines; the section names above identify the intended passages.

### Mwendo Pamoja

- **M1:** [Controlled Part 5 — purpose/boundary and quantity taxonomy](<C:/Users/Nevo/Downloads/insuretech & embedded finance/docs/controlled-specifications/Part_5_KESONIA_Pricing_and_Capital_Orchestration.md:8>); customer and compounding sections at lines 62–165; stack at 203–261; accounting/insurance/capital/FTP boundaries at 406–451.
- **M2:** [SPV financial term sheet](<C:/Users/Nevo/Downloads/insuretech & embedded finance/docs/controlled-specifications/Mwendo_Pamoja_SPV_Financial_Term_Sheet.md:3>); parties/currency/stack at 10–61; eligibility/accounts/waterfall at 62–147; accounting and capital boundaries at 164–176.
- **M3:** [Whitepaper Part 5](<C:/Users/Nevo/Downloads/insuretech & embedded finance/whitepapers/mwendo-pamoja/parts/Part_5_KESONIA_Pricing_and_Capital_Orchestration.md:59>); optional-compounding wording at 151–153; insurance at 408–422; reset/modification distinction at 426–436; treasury/SPV and vendor boundaries at 460–512.
- [Controlled Part 2b — customer premium](<C:/Users/Nevo/Downloads/insuretech & embedded finance/docs/controlled-specifications/Part_2b_Bayesian_Underwriting_and_Asymmetric_Copulas.md:321>). Targeted search/read found a KESONIA-plus-premium explanation, not an explicit prohibition on the governed compound-in-arrears period reference.
- [Controlled loss architecture](<C:/Users/Nevo/Downloads/insuretech & embedded finance/docs/controlled-specifications/CREDIT_RISK_MODEL_AND_LOSS_ARCHITECTURE_SPECIFICATION.md>): canonical loss/timing/refund/dependence owner identified by M1. This audit did not reread its full manuscript.

### Underwrite to Collect

- **U1:** [Part 5 — KESONIA, ECL, capital and funding](<C:/Users/Nevo/Downloads/behavioural credit scoring - underwrite to collect rct/series/parts/Part_5_KESONIA_Pricing_Expected_Credit_Loss_Capital_and_Funding.md:14>); premium/FTP bridge at 64–135; financial quantities at 173–229; cash/liquidity distinctions at 382–411; treasury and deposit FTP at 423–574; SPV branch at 816–923; roles and adoption at 994–1026.
- **U2:** [Part 1 — business unit, cash and purpose](<C:/Users/Nevo/Downloads/behavioural credit scoring - underwrite to collect rct/series/parts/Part_1_MSME_Credit_Lifecycle_and_Collection_Cascades.md:30>); business/credit clocks at 95; use of proceeds and sweep effects at 137–141.

### Bayesian relativities

- **A1:** [Telematics relativities paper](<C:/Users/Nevo/Downloads/bayesian-telematics-relativities/whitepapers/telematics-relativities/paper.md:159>); pricing layers in section 2.4; capital distinctions at 740–749; IFRS 17 handoff in section 12, lines 940–967; pilot gates at 1014–1020.
- **A2:** [Additional pricing/treasury review](<C:/Users/Nevo/Downloads/bayesian-telematics-relativities/whitepapers/telematics-relativities/ADDITIONAL_REVIEW_PRICING_AND_TREASURY_2026-09-23.md:7>); insurance/IPF connected case and accounting boundaries at 11–39.

### Guest financial material — read only

- **B1:** [Making Business Credit Work — actual Part 2 file](<C:/Users/Nevo/Downloads/financial material/African Markets and Business Credit/LinkedIn Articles/Part 2 - Business Credit and Fintech.md:19>); offer/margin/downside examples at 42–52; cash/entity reconciliation at 67–108; borrower/provider outcomes at 145–149. The historical `Part_2/*.md` path is not the current file location.
- **O1:** [Owner Earnings Project 1, Part 1](<C:/Users/Nevo/Downloads/financial material/Owner's Earning/Project 1 - MSMEs and Small Businesses/Part 01 - The Cash an Owner Can Actually Claim.md:11>); bridges at 22–50; adjusted example and immediate cash at 90–106.
- **O2:** [Owner Earnings Project 1, Part 4](<C:/Users/Nevo/Downloads/financial material/Owner's Earning/Project 1 - MSMEs and Small Businesses/Part 04 - Owner Pay Reserves Growth and Debt.md:25>); debt terms at 52–60; dated cash/reserve/purpose treatment at 100–114.
- [Owner Earnings Project 1, Part 5](<C:/Users/Nevo/Downloads/financial material/Owner's Earning/Project 1 - MSMEs and Small Businesses/Part 05 - Buying Selling and Succession.md:11>); replacement roles and buyer-specific claim at 32–68.
- **O3:** [Owner Earnings Project 2, Part 6](<C:/Users/Nevo/Downloads/financial material/Owner's Earning/Project 2 - Listed Companies and Valuation/Part 06 - Reconstructing Owner Earnings from Public Filings.md:9>); evidence/unknowns at 26–53; quantity and valuation-claim dictionary at 160–172.
- **O4:** [Owner Earnings Project 2, Part 9](<C:/Users/Nevo/Downloads/financial material/Owner's Earning/Project 2 - Listed Companies and Valuation/Part 09 - Banks and Insurers Distributable Capital.md:5>); bank/insurer distinctions at 5–31; illustrative capital headroom at 54–58; extended pricing/capital and parent cash cases at 160–175. The referenced workbook implementation was not independently inspected or run for this audit.

### Guest SokoIntel — read only

- **S1:** [Canonical workbench specification](<C:/Users/Nevo/Downloads/business and technical website blog/product_architecture/SokoIntel Financial Analytics Workbench_ Comprehensive Software Requirements and Design Specification.md:98>); scope boundary at 114; adopted FR099–FR132 at 427–473; shared domain contracts at 772–804; current adoption notes at 1364–1368.
- [Dated credit pricing/SPV addendum](<C:/Users/Nevo/Downloads/business and technical website blog/product_architecture/ADDITIONAL_CREDIT_PRICING_AND_SPV_REQUIREMENTS_2026-09-25.md:43>). Read with the later canonical adoption, not as a continuing absence of requirements.

### Canonical RegTech reviews and examples

- **R1:** [Historical gap analysis](<C:/Users/Nevo/Downloads/regtech-kesonia-treasury/source_library/review-history/2026-09-28/RegTech_Gap_Analysis_Report.md:37>); accounting 54–63, bank/SPV/security claims 73–99, supervisory interface assertions 117–120.
- **R2:** [Historical enhancement report](<C:/Users/Nevo/Downloads/regtech-kesonia-treasury/source_library/review-history/2026-09-28/RegTech_KESONIA_Enhancement_Report.md:7>).
- **R3:** [Early K framework note](<C:/Users/Nevo/Downloads/regtech-kesonia-treasury/source_library/review-history/2026-09-28/cbk_kesonia_k_framework.md:11>).
- **R4:** [Compounding, term structure and funding note](<C:/Users/Nevo/Downloads/regtech-kesonia-treasury/docs/research/kesonia/KESONIA_COMPOUNDING_TERM_STRUCTURE_AND_FUNDING_CURVE_NOTE.md:1>) and [additional pricing/treasury review](<C:/Users/Nevo/Downloads/regtech-kesonia-treasury/docs/research/kesonia/ADDITIONAL_REVIEW_PRICING_AND_TREASURY_2026-09-23.md:7>).
- **R5:** [STP and ALM/FTP software review](<C:/Users/Nevo/Downloads/regtech-kesonia-treasury/docs/research/kesonia/STP_AND_ALM_FTP_SOFTWARE_REVIEW_2026-09-25.md:9>); proposed workflow at 46–71; proof-of-concept requirements at 85–89. Vendor statements were reviewed as existing documentation claims, not freshly tested capabilities.
- **R6:** [Calculation and casebook](<C:/Users/Nevo/Downloads/regtech-kesonia-treasury/output/kesonia_treasury_deep_review_2026-09-25/02_CALCULATION_AND_CASEBOOK.md:73>); pricing 93–125; deposit assumptions 127–148; independent sensitivities 150–180; OAS/CVA boundaries 182–214.
- **R7:** [Remaining-work register](<C:/Users/Nevo/Downloads/regtech-kesonia-treasury/docs/research/kesonia/TREASURY_REMAINING_WORK_REGISTER_2026-09-25.md:1>); existing substantial coverage at 48–54, priorities at 58–62.
- [Cross-project working formulations](<C:/Users/Nevo/Downloads/regtech-kesonia-treasury/output/pricing_treasury_cross_project_review_2026-09-23/02_WORKING_FORMULATIONS_AND_EXAMPLES.md:5>); quantity dictionary, money pricing, borrower/vehicle cash, accounting and capital boundaries.

## 11. Later review packs and the screenshot lineage

The following four later files were read in full for this audit. Their proposals must be reconciled against the newer canonical source state, rather than repeatedly catalogued as newly missing foundations.

| Review and passage | Useful material and current disposition | Specific action |
|---|---|---|
| [September 25 development notes](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/pricing_mwendo_underwrite_sokointel_review_2026-09-25/02_MWENDO_AND_UNDERWRITE_DEVELOPMENT_NOTES.md:19>), 133 lines | Existing coverage matrix, proposed insertions A–F, public-article alignment and three article briefs. Separate Underwrite, Mwendo and the older practitioner/LinkedIn drafts. | Reuse the proposed money-before-rates, unused commitment, recovery-ready claim ledger and payment-date waterfall exhibits. Keep causal evidence requirements at lines 67–71. Treat Geske, syndication, CVA/IRB and FRTB as separately gated advanced applications. The three articles are candidates, not the limit of the editorial programme. |
| [September 25 SokoIntel addendum](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/pricing_mwendo_underwrite_sokointel_review_2026-09-25/03_SOKOINTEL_CREDIT_AND_SPV_SPECIFICATION_ADDENDUM.md:41>), 143 lines | CR-FR-001–020, domain records, ten invariants and staged module releases. Its opening describes the then-current 1,245-line specification. The present canonical specification has adopted the extension as FR099–118 and expanded it further. | Preserve the historical addendum, use the current FR identifiers in new delivery plans, and trace each fixture to its requirement. Do not claim a repeated proposal is new specification work. Cash conservation and capital-unit failures cannot be waived by an aggregate test pass-rate. |
| [September 25 checked casebook](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/pricing_mwendo_underwrite_sokointel_review_2026-09-25/04_WORKED_PRICING_AND_CASHFLOW_CASES.md:7>), 127 lines | Nine existing arithmetic cases: term pricing, revolver, hazard conversion, reserve, OC, capital units, CVA, migration and syndication. Their original review reports independent calculation. | Reuse these as reference fixtures with the accompanying script/JSON versions. A reserve unit test is not the complete Mwendo waterfall; a fixed migration mass is not projected EAD; a one-period CVA approximation is not regulatory CVA capital. This audit read the casebook but did not rerun that historical script. |
| [Business credit and Owner Earnings follow-up](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/pricing_treasury_cross_project_review_2026-09-23/06_BUSINESS_CREDIT_AND_OWNER_EARNINGS_FOLLOWUP_2026-09-25.md:5>), 108 lines | Corrects the former planning-only description, explicitly brings in Project 2 and maps OE01–OE06. Describes already existing articles/workbooks and a dated borrower example. | Adopt the borrower → lender → bank-shareholder bridge without treating a fee or margin as a dividend. Keep construction/commitment calendars, insurer remittance and sector cases as separate endpoints. Reconcile these September 25 proposals against subsequent article/specification additions before calling them outstanding. Workbook existence is not an independent cell audit. |

### Re-verification and recovery severity: refinement of existing work

The [first screenshot coverage matrix](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/coverage_retirement_audit_2026-09-22/01_POST_COVERAGE_MATRIX.md:9>) already identifies the difference between historical point-in-time correctness and current freshness. Its [protocol F](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/coverage_retirement_audit_2026-09-22/03_RESEARCH_PROTOCOL_ADDENDUM.md:62>) records economic date, lawful availability, verification, assessment, approval and disbursement times. Age limits are governed parameters, not invented legal deadlines.

The [additional screenshot review](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/coverage_retirement_audit_2026-09-22/06_ADDITIONAL_MATERIAL_REVIEW_2026-09-23.md:39>) goes further with RR (recovery readiness), AR (trade exposure), ACT (execution), PM (scoped provision matrix), PV (purpose verification) and MC (complexity acceptance). Its RR case holds PD at 2% and exposure at KES 1 million while severity rises from 20% to 50%: illustrative expected loss rises from KES 4,000 to KES 10,000. That is a useful separate loss-severity signal, not evidence of a PD increase or an automatic accounting-stage change.

The [collectability feedback note](<C:/Users/Nevo/Downloads/behavioural credit scoring - underwrite to collect rct/series/research/COLLECTABILITY_FEEDBACK_AND_CONTINUOUS_REVERIFICATION_2026-09-25.md:29>) explicitly connects Chen Avnery's observation to F/RR and identifies the remaining work as a bridge paragraph, ownership table and worked case. Its three snapshots—previously verified, new evidence received, review completed—should be reused. It supplies `verified_at`, result, coverage, next review, trigger, reviewer, effective/known times, dispute status, affected assumptions, action state and closure evidence. Source failure must not refresh an old valuation or establish an adverse borrower fact. The current SokoIntel evidence contract already includes this direction [S1, line 778].

For RegTech, the incremental task is to demonstrate how a verified change reaches the relevant recovery, eligibility, funding or valuation assumption, with an owner and approval trail. Preserve unchanged borrower PD where the case changes only recoverability. A registry failure is a separate evidence-availability case. Public mortgage experiments do not supply unobserved Kenyan lien, litigation, invoice-allocation or staff-action histories.

### A compact action catalogue

| ID | Owner/destination | Reuse | Completion artifact |
|---|---|---|---|
| XB01 | RegTech benchmark and rule steward | Final CBK perimeter plus controlled compounding | Scoped rule/convention register; unresolved five-day mapping visible; dated benchmark replay and accrual fixtures |
| XB02 | RegTech + Underwrite financial-method owner | U5 bridge and September 25 cases A/B | Same-facility money, rate, RAROC and economic-profit reconciliation; borrower capacity retained |
| XB03 | Mwendo transaction/calculation owner | Controlled term sheet and development note D | Stateful eligible-asset/account/note/reserve/waterfall case including trigger persistence and funded closing reserve |
| XB04 | Underwrite source owners + RegTech adapters | F/RR/ACT and reader-feedback workflow | Verified/no-change, changed-right and unavailable-source cases with downstream assumption/review histories |
| XB05 | SokoIntel product owner | Adopted FR099–132; historical CR-FR mapping | Requirement-to-case-to-function traceability; typed contracts and intended-use gates; no operational authority implied |
| XB06 | Business credit and Owner Earnings owners | OE01–OE06; current articles | Claim/date-consistent borrower, business owner, bank and insurer-parent views; guest follow-up only until an authorized edit |
| XB07 | Insurance/actuarial and accounting owners | Relativities section 12 and IPF interface | Insurer/lender/SPV claim and settlement handoff with refund timing and no duplicated recovery |
| XB08 | RegTech documentation owner | Historical gap/enhancement notes and remaining-work register | Supersession/status annotations, useful controls retained, unsupported mandatory/readiness assertions removed from current normative text |
| XB09 | Treasury/ALM owner | Existing curve, FTP and independent sensitivity fixtures | Repriced curve and coherent dated balance-sheet case; institution-specific LCR/NSFR treatment separated from internal cash availability |
| XB10 | Integration owner | STP design and SokoIntel event/result contracts | Mock approvals/booking/settlement/reconciliation adapters and failure tests, explicitly distinguished from live vendor integration |

## 12. Editorial completion criteria

The RegTech revision can claim the cross-project review is incorporated when it:

- identifies every rate, loss, capital and cash number by entity, claim, unit, date/horizon, measure and governing source;
- applies the actual bank compound-in-arrears perimeter and explicitly preserves unresolved operational conventions;
- references the existing Underwrite, Mwendo, Bayesian and owner-earnings content rather than duplicating their methodology;
- distinguishes current SokoIntel requirements from implemented modules and future operational adapters;
- replaces or annotates obsolete overstatements in the older review trail;
- supplies reproducible examples with visible assumptions and matched ledgers; and
- keeps legal execution, empirical calibration, accounting sign-off, live integrations and local market applicability open where their evidence is still missing.

These criteria close the editorial and interface work. They do not claim that every item in the treasury remaining-work register has been implemented.

The companion `SOURCE_READING_MANIFEST.json` records the cited file paths, SHA-256 hashes, byte/line counts and entry-point anchors. It also records the independently recalculated three-day accrual illustration. It is a source-state record, not a claim of a full line-by-line reread of every referenced manuscript.

## 13. Current implementation status — 1 October 2026

The September 28 source map above records that review's evidence. Later executable work changes its implementation status. The [current reconciliation](REVIEW_INTEGRATION_AND_REMAINING_WORK.md) and [SokoIntel candidate map](SOKOINTEL_CANDIDATE_MAP.md) supply the present delivery view.

| Case / action | Now demonstrated | Still required |
|---|---|---|
| A / XB02 | Original money-to-rate bridge; current Underwrite borrower case; new connected borrower/originator/SPV cash ledger | One permissioned institution/customer dataset and approved product terms |
| B / XB03 | Mwendo October 1 canonical stateful waterfall has funded reserve, trigger persistence, arrears and refund/recovery timing; frozen evidence referenced by RegTech | Transaction-specific legal terms, calibrated portfolio and live servicing |
| C / XB09 | Curve and dated FTP laboratory; same-balance-sheet liquidity/NII/EVE/stress illustration in regulatory cases | Dynamic calibrated behaviour, ledger/return mapping and market quotes |
| D / XB07 | Dated accepted-refund/right/settlement/loan-allocation fixture | Full insurer contract-group IFRS 17 measurement and entity-specific journals |
| E / XB06 | Typed owner/cash distinction, bank retention and late parent remittance fixture | Real bank/insurer distribution rules, approval and evidence |
| F / XB10 | Durable SQLite workflow plus isolated partial execution, missing acknowledgement and accrual-correction reference cases | Single vendor-connected workflow, authentication, recovery and performance acceptance |
| XB01 | Original fixing/index check plus specified changing-balance convention and correction replay | Authoritative institution-specific five-day mapping |
| XB04 | Existing Underwrite permission/evidence/no-action engine recognised; dated RegTech freshness gate | Connected source-refresh adapters and operational exception ownership |
| XB05 | Typed quantities, reproducible exported cases and product candidate map | SokoIntel product selection and implementation; guest repository unchanged |
| XB08 | Current wording clarified; active bibliography corrected and historical notes point to current status | Full independent verification of inherited bibliography metadata remains open |
