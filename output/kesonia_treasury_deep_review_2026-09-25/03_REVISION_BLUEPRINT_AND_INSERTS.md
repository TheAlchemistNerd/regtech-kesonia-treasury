> **Historical review, 25 September 2026.** For current executable evidence and open requirements, use the [1 October implementation register](../../docs/methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md). The dated review below retains its original scope.

# Revision blueprint and proposed article additions

**25 September 2026 · Editorial specification for the four KESONIA articles**

The following is a practical incorporation plan. It preserves the four-part structure and reuses the stronger definitions already in the controlled pricing chapter. Proposed paragraphs are supplied for later integration; the canonical articles have not been rewritten in this review.

## 1. Part 1: from benchmark reform to a financial decision architecture

**Suggested title:** *KESONIA, cash flows and the architecture of credit decisions.*

| Existing placement | Revision or addition | Exhibit |
|---|---|---|
| Introduction and Section I | Open with a borrower whose cash receipts and debt payments occur on different dates; explain the pricing reform in that context | One-page borrower/lender/treasury decision map |
| Section II, benchmark plus premium | Introduce the quantity dictionary and separate benchmark history, projected resets, customer margin and lender funding | Curve atlas from the material review |
| Sections III–IV, data flow and layers | Map responsibilities across contract, market data, calculation, risk, accounting and reporting; align section and diagram labels | Versioned information flow with as-of timestamps |
| Section V, vendor landscape | Classify products by actual responsibility and evidenced interfaces | Capability matrix in the software review |
| Section VI, engineering principles | Explain replay, calendar handling, independent verification and exception ownership | “A fixing was corrected after posting” walkthrough |
| Section VII, series roadmap | Make each article answer a business question and identify its demonstrable output | Four-part reader journey |

### Proposed insertion after the benchmark/premium explanation

> A lending benchmark is one input into a dated financial agreement. The borrower needs to understand the amount and timing of payments. The lender needs to understand the income likely to be collected and the costs of funding, servicing and bearing risk. Treasury needs to understand how those receipts line up with deposits, wholesale funding and other obligations. The same contract therefore produces several useful measures, each with its own purpose. Our architecture carries their common source data forward while keeping their meanings distinct.

### Proposed insertion at the start of the architecture section

> Every calculation should be recoverable from a specific contract version, information cutoff, rate source, calendar, balance history and approved set of assumptions. This allows us to explain a change in a result: the contract changed, a new fixing arrived, a balance moved, behaviour was re-estimated, or an earlier record was corrected. Assigning these responsibilities to systems is an implementation choice. The requirement is that the resulting cash, risk and accounting records reconcile.

**Acceptance evidence:** the reader can trace one loan from observed benchmark to contract payment and distinguish that payment from a forecast, an internal transfer price and an accounting entry.

## 2. Part 2: from compounding mathematics to verified contract cash

**Suggested title:** *Computing KESONIA interest: calendars, observations, balances and reconciliation.*

| Existing placement | Revision or addition | Exhibit |
|---|---|---|
| Sections I–II | State the accumulation-factor derivation, annualisation and simple-margin assumption | Casebook §2 |
| Sections III–IV | Specify the entire observation/accrual mapping and endpoint clipping | Date table showing accrual start/end, observation date, publication time, weight and source version |
| Section V, schema | Add interest-period, balance-event and calculation-version records | Proposed data contract below |
| Sections VI–VIII, SQL | Rebuild around validated interval rows and contract-period grouping; make rate joins, calculated outputs and posting scope explicit | Pseudocode plus independently calculated fixtures before dialect-specific SQL |
| Section IX, scale | Replace a generic scale assertion with measured workloads and accuracy/latency targets | Benchmark plan covering normal runs and corrections |
| Conclusion | Explain how verified actual accrual becomes the starting point for projected cash flows | Actual-versus-forecast bridge |

### Proposed insertion before the SQL

> The calculation begins with a complete interval ledger. Each row identifies an accrual span, its applicable observation, the number of days, the relevant principal and the governing convention. The aggregate query then combines rows whose meaning has already been established. This makes the result inspectable: a reviewer can check which fixing was used, why it was used, and how a balance change affected the amount. The database implementation should preserve that explanation rather than hiding contract interpretation inside a formula.

### Proposed data contract

| Record | Essential fields | Business reason |
|---|---|---|
| Contract version | Legal entities, currency, rate/index, margin rule, reset and payment schedules, fees, conventions, effective dates | Determines what may be charged and when |
| Fixing version | Source, value date, publication/receipt times, decimal rate, correction status, hash | Establishes information availability and provenance |
| Balance event | Contract, effective date, recorded time, amount, type, source transaction | Supports draws, repayments, reversals and delayed reporting |
| Observation map | Period, accrual interval, observation date, day weight, calendar version, fallback decision | Makes the lookback and calendar calculation testable |
| Calculation run | Purpose, cutoff, input versions, formula version, scenario, reviewer, status | Separates actual accrual from forecast and historical replay |
| Result/event | Factor, interest, fees, due date, approval, posting ID, settlement status | Connects calculated amounts to accounting and cash |

**Fixtures:** ordinary business days; weekend; holiday; partial final span; period boundaries; missing fixing; corrected fixing; simple versus compounded margin; principal change; duplicate input; rerun after posting. Define numerical tolerances from precision and rounding rules. These are meaningful requirements for future engine testing, not claims that the current SQL passes them.

## 3. Part 3: from risk estimates to pricing, funding and outcomes

**Suggested title:** *Pricing credit through the cycle: expected loss, funding, behaviour and accounting.*

| Existing placement | Revision or addition | Exhibit |
|---|---|---|
| Section I, margin formulation | Derive the rate from money, exposure-time and a stated return criterion | Casebook §4 |
| Sections II–IV, credit models | Align PD horizon, EAD, loss/recovery timing and expected interest; use uncertainty in decisions | Model-input-to-cash-flow table |
| Sections V–VII, explanations and governance | Explain the monetary price bridge alongside predictive drivers; compare simple and complex models on deployment-relevant evidence | Reasons for change, calibration, feature availability and monitoring record |
| Sections VIII–IX, IFRS 9 | Introduce an accounting event decision table before journals | Market reset / correction / modification / derecognition / forbearance / write-off |
| Section X, FTP | Develop matched funding, contingent drawdowns and deposit replication | Casebook §§3–5 |
| Section XI, ALM | Show NII, EVE and cash sensitivity from the same opening position; specify how an integrated path will reconcile | Casebook §6 |
| Section XII, audit | Preserve the route from prediction to proposed action, approval, contract change and subsequent outcome | Decision record |

### Proposed replacement for a stand-alone margin formula

> We begin by forecasting monetary amounts over the chosen pricing horizon: interest and fees, funding and servicing costs, expected credit losses and the return required on allocated capital. The proposed margin is the rate that reconciles those amounts against the balance expected to earn it. This exposes the source of the price. A higher margin may reflect a funding change, slower recovery, higher utilisation or a different return requirement; it cannot be explained adequately by a default score alone.

### Proposed addition to the FTP discussion

> A floating-rate loan can reset frequently while still tying up funding for several years. Its interest-rate reset horizon and its liquidity horizon are therefore different inputs. A revolving commitment also creates exposure before it is drawn: the institution may need cash precisely when market funding becomes more expensive. Our transfer-pricing policy should make those funding and optionality components visible, then reconcile internal allocations to the institution's external costs.

### Proposed addition to the behavioural discussion

> Deposit pricing and deposit retention should be estimated separately. One model asks how much and how quickly the institution changes the rate paid to a customer. Another asks how much of the balance remains under different conditions. Loan customers have options too: they may prepay, extend their effective borrowing period, or increase utilisation. These behaviours alter future cash flows, so their assumptions should be visible in both the base forecast and stress scenarios.

### Accounting decision table

| Trigger | Required distinction | Output |
|---|---|---|
| Scheduled benchmark reset | Existing contract operation versus negotiated change | Revised contractual cash-flow schedule and applicable interest treatment |
| Corrected fixing or balance record | Correction versus new economic agreement | Linked adjustment and reconciliation |
| Proposed customer-margin change | Model recommendation versus legal authority/effective terms | Approved or declined proposal; contract version if changed |
| Borrower modification | Asset analysis versus lender's own liability analysis | Assessment, carrying-value effect and accounting decision |
| Financial difficulty | Commercial change versus forbearance/credit deterioration | Credit and accounting assessment linked to the event |
| Hedge transaction | Economic risk reduction versus accounting designation | Separate trade, valuation and hedge-accounting records |

For assets modified without derecognition, IFRS 9 §5.4.3 provides the carrying-amount and modification-result basis, including the applicable original effective-rate rule. The ten-percent test in B3.3.6 concerns liabilities; it should not be copied into the loan-asset workflow as a universal test. [IFRS 9 §5.4.3](https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2022/issued/part-a/ifrs-9-financial-instruments.pdf?bypass=on), [IFRS 9 B3.3.6](https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2021/issued/part-a/ifrs-9-financial-instruments.pdf?bypass=on). These paragraph references support the editorial distinction; implementation requires the applicable current edition and approved accounting policy.

**Acceptance evidence:** one example reconciles customer cost, lender economics and funding allocation, while an event table explains why a risk refresh does not automatically produce a new invoice or journal.

## 4. Part 4: from controlled calculations to controlled action

**Suggested title:** *RegTech and treasury operations: approvals, straight-through processing and reconciliation.*

| Existing placement | Revision or addition | Exhibit |
|---|---|---|
| Sections I–II, sweep and validation | Define separate calculation, submission and trade workflows; introduce explicit exception states | State transitions and ownership |
| Sections III–V, evidence/security/approval | Tie approval to the exact result version and authorised action; preserve receipts, corrections and retries | End-to-end event chain |
| Sections VI–VIII, vendor discussions | Add MORS and Abrigo in the roles documented by their vendors; retain Oracle, SAP and D365 with module-specific boundaries | [Software and STP review](<05_STP_AND_ALM_FTP_SOFTWARE_REVIEW.md>) |
| Section IX, roadmap | Deliver through acceptance gates; include tests from the first stage | Prioritised delivery table below |
| Sections X–XI, future reporting | Treat protocol and market connectivity as verified integration requirements | Interface contract and external acknowledgement |

### Proposed insertion: what straight-through processing contributes

> Straight-through processing carries an authorised transaction through connected systems with little repeated manual entry. In treasury, that may connect a reviewed hedge proposal to an order, execution confirmation, booking, settlement and reconciliation. In lending, it may connect a verified accrual to an approved accounting event and statement. The shared requirement is continuity of identity and evidence: we can follow the same business event across systems and identify exceptions without losing its meaning.

### Proposed insertion: decision support and execution

> An ALM model estimates exposures and evaluates possible responses. An FTP model assigns internal funding costs and credits. A treasury management system and execution service manage trades and their lifecycle. Some products combine these capabilities, but the responsibilities still need to be distinguished. A model result becomes an executed position only through the institution's authorised workflow, and residual exposure must be measured again after execution.

## 5. Deliver the next work in six gates

| Gate | Deliverable | Evidence required before the next stage |
|---|---|---|
| 1: definitions and contracts | Financial quantity dictionary, applicable convention sheet and event taxonomy | Owners agree dates, units, scope and accounting boundaries |
| 2: deterministic cash | Small KESONIA calculator plus borrower and SPV schedules | Independent amounts agree; cash and balances reconcile; corrections replay |
| 3: curves and funding | Versioned projection/discount/funding curves and FTP calculation | Input instruments or assumptions identified; curve instruments reprice; internal transfers reconcile |
| 4: behaviour and scenarios | Deposit, prepayment, utilisation, default and recovery estimates where data allow | Longitudinal data, out-of-time validation and uncertainty analysis |
| 5: workflows | Calculation, approval, exception, submission and simulated trade workflows | Duplicate, delayed, rejected and partially completed events handled correctly |
| 6: platform integration | Selected system interfaces and operational monitoring | Sandbox acceptance, supported products/currencies, access controls, operational ownership and reconciliation |

The advanced derivative and capital laboratories follow only where the business case and data support them. This order is a proposed implementation sequence, not a committed delivery schedule or a purchase recommendation.

## 6. What to do with the shorter existing notes

Keep the compounding/term-structure note as the concise conceptual introduction. Keep the CBK/K fragment as historical source material, with the money-to-margin case as its developed successor. Treat the enhancement and gap reports as dated planning evidence. Their useful requirements should migrate into the acceptance backlog, with a destination and status for each. No unique text needs to be discarded to make this transition.

The older September 23 review remains the cross-project entry point. This package develops its KESONIA branch. The cumulative screenshot catalogue and wholesale revision of neighbouring manuscripts remain separate work.

## 7. Explicit additions following the remaining-work review

The treasury paste's regulatory and accounting subjects need visible destinations beyond a general advanced-work label:

| Addition | Placement | Completion evidence |
|---|---|---|
| FRTB and regulatory book boundaries | Part 1 scope map; Part 3 risk-method interfaces; Part 4 desk/data controls; specialist appendix | Scoped standardised example and a separate internal-model/data-validation specification; see the [FRTB note](<07_FRTB_SCOPE_AND_DEVELOPMENT_NOTE.md>) |
| LCR/NSFR and operational liquidity | Part 3 integrated bank scenario; Part 4 source-to-report controls | Classified balance sheet and commitments, applicable weights/haircuts, ratio reconciliation and a separate cash-survival schedule |
| IFRS 9 hedge accounting | Part 3 immediately after the accounting decision table | Fair-value and cash-flow hedge examples with designation, valuation, journals, ineffectiveness and reconciliation |
| Kenyan market and rule applicability | Part 1 institutional scope; Parts 2–4 input and interface requirements | Dated rule map and evidence of instruments, quotations, terms and system support; identify proxies and synthetic examples |

The [eighteen-item register](<06_WHAT_REMAINS_TO_BE_DEVELOPED.md>) specifies the remaining methods and evidence. These additions make the future work explicit; they do not imply that the numerical modules have already been delivered.
