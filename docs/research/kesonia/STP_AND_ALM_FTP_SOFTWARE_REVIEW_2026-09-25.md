> **Historical review.** Current completion status and reproducible cases are tracked in [the 1 October implementation register](../../methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md).

# Straight-through processing and ALM/FTP software

**25 September 2026 · Targeted check of the treasury paste and KESONIA vendor discussions**

## 1. Direct answer

**The relevant passage has now been checked against primary vendor material.** The treasury paste discusses automated ALM analysis and hedge workflows around physical lines 20–23, then revisits behavioural adjustment and portfolio management around lines 27–36. It names **Abrigo**, **MORS Software**, **Bloomberg** and **Reuters** in this context. Oracle, SAP and Microsoft come from the KESONIA articles and the broader integration discussion; they are assessed below in their actual product roles.

The useful idea is to connect **analysis → decision → execution → financial records → refreshed analysis**. There is concrete vendor evidence for parts of this chain. The current review is documentation-based: no licensed installation, API connection, execution venue, Kenyan product coverage or live trade has been tested.

## 2. Four responsibilities to distinguish

| Responsibility | Business question | Output |
|---|---|---|
| Asset-liability management, ALM | How do rates, cash flows and customer behaviour affect the balance sheet? | Cash projections, earnings and value sensitivities, funding gaps and scenarios |
| Funds transfer pricing, FTP | How should internal funding cost and funding benefit be allocated? | Transfer rates, charges/credits and product/business profitability attribution |
| Treasury management and execution | What transaction is authorised, and what happened to it? | Proposal, limit check, order, execution, confirmation, collateral and settlement records |
| Accounting and reporting | How is the business event recognised and reconciled? | Subledger events, journals, positions, reports and acknowledgements |

STP is the **connected processing of those events**, reducing repeated entry and manual hand-offs. It can coexist with approvals and exceptions. ALM results do not require a trade in every case: management may change product terms, funding composition, limits or liquidity buffers instead.

## 3. What the vendor evidence supports

The entries below are a capability map, not a vendor ranking. “Documented” means described in the cited vendor source, not independently proven in an implementation.

| Product or service | Documented capability | Useful role in our material | What remains to establish |
|---|---|---|---|
| **Abrigo ALM** | Instrument cash-flow assumptions, static/dynamic forecasts, scenarios, liquidity and EVE reporting; connections to its other portfolio-risk tools | Example of ALCO analysis and controlled scenario reporting | The reviewed page does not establish a direct swap-execution or universal automatic recalibration workflow. [Abrigo ALM](https://www.abrigo.com/software/portfolio-risk-cecl/asset-liability/) |
| **MORS ALM** | Deal-level balance-sheet input, cash-flow drill-down, scenario/NII analysis and an optional treasury-management component | Example of linked bank balance-sheet analysis and treasury operations | Actual modules, data refresh, model settings and instruments in the selected deployment. [MORS ALM](https://morssoftware.com/mors-solution/asset-liability-management/) |
| **MORS FTP** | Configurable internal transfer-pricing rules, ex-ante/ex-post analysis and grouping by maturity, currency, product and contingent exposure | Develop the internal pricing and profitability section using explicit allocation rules | The bank's approved funding methodology and how allocations reconcile to external costs. [MORS FTP](https://morssoftware.com/modules/mors-funds-transfer-pricing/) |
| **MORS–Bloomberg workflow** | Pre-deal limit checks; an approved soft-deal identifier; dealer entry in Bloomberg; returned confirmation matched to that identifier | Concrete example of an approved deal moving across connected systems | No inference of autonomous hedge selection or blanket KESONIA swap support. [MORS integration description, January 2025](https://morssoftware.com/mors-enhances-tms-with-bloomberg-trade-workflow-automation/) |
| **Bloomberg SEF** | Execution facilities covering rates, credit and currency products | Explain where an eligible trade can be executed | Product/currency availability, participation, clearing and connectivity for the intended institution. [Bloomberg facilities](https://professional.bloomberg.com/products/trading/electronic-markets/venues/swap-execution-facility/) |
| **Tradeweb rates derivatives** | IRS execution protocols and post-trade links including STP to MarkitWire and clearing-house connections | A separately documented rates-execution example; it was added in this check, not named as a product in the paste | Its published list reviewed here does not establish KES/KESONIA support. [Tradeweb rates derivatives](https://www.tradeweb.com/our-markets/institutional/rates/rates-derivatives/) |
| **LSEG Workspace with FXall** | Integrated FX data, analytics and multidealer execution workflows | Replace the broad “Reuters” label with an identified service where discussing FX | FX execution capability does not itself establish an interest-rate-swap route. [LSEG Workspace/FXall](https://www.lseg.com/en/fx/updates/fxall-workspace-integration) |
| **Oracle ALM and FTP cash-flow engine** | Cash-flow/repricing logic, rate conversion, option-cost and Monte Carlo calculations, and detailed audit output | Strong technical reference for a common cash-flow engine serving different analytical purposes | Match the documentation to the selected product release and deployment. The reviewed guide is the 8.1.2 documentation set. [Oracle cash-flow guide](https://docs.oracle.com/en/industries/financial-services/ofs-analytical-applications/analytical-applications-infrastructure/812/cferg/overview6.html) |
| **SAP Treasury and Risk Management** | Deal capture, valuation, risk/return analysis and transfer to financial accounting; documented APIs | Treasury transaction and accounting integration, distinct from a general ERP label | Selected release, instrument coverage, configuration and banking ALM/FTP fit. The reviewed help page identifies version 2608. [SAP TRM](https://help.sap.com/docs/SAP_S4HANA_CLOUD/4574d8b965404a45a11e19a8d0fbe96f/cf31a5fa099043919c7076059964b24a.html) |
| **SAP Financial Products Subledger** | Accounting portfolio structures and import of external risk/hedge portfolio information | Subledger destination for appropriately defined risk and transaction information | It should not be described as the whole bank ALM/FTP or execution system. [SAP FPSL documentation](https://help.sap.com/doc/4234275c8b3b44a8b5503eec0c1c0ad8/2306.005/en-US/Finanzprodukt_Nebenbuch_EN.pdf) |
| **Dynamics 365 Finance** | Cash forecasting connected to ledger, receivables, payables and other transactions; import of external cash forecasts | Business operating-cash and accounting integration; useful for the MSME and workbench cases | The reviewed pages do not establish a native bank IRRBB/FTP or swap-execution engine. [Cash forecasting](https://learn.microsoft.com/en-us/dynamics365/finance/cash-bank-management/cash-flow-forecasting), [external forecast data](https://learn.microsoft.com/en-us/dynamics365/finance/finance-insights/external-data-in-cash-flow) |

Microsoft also documents OData and batch/data-management integration patterns. These are possible interfaces, not a ready-made treasury model. Choose the pattern according to the entities, transaction semantics, volume and recovery requirements. [Microsoft integration overview](https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/data-entities/integration-overview).

## 4. What to borrow from the STP passage

The paste's four-stage narrative is valuable: ingest positions, analyse exposure, evaluate a hedge, and connect the approved response to downstream processing. Develop it using a transaction whose identity survives each hand-off.

For the proposed series architecture:

1. **Position and data snapshot.** Lock contract, balance, fixing, curve and behavioural-model versions for the run.
2. **ALM scenario.** Produce NII, EVE and liquidity outputs with their separate horizons and assumptions.
3. **Candidate response.** Compare funding changes, product changes, buffers and eligible hedges. Record costs, residual risk and constraints.
4. **Pre-deal review.** Check authorised instruments, counterparty capacity, limits, collateral cash and accounting implications. Identify the approved proposal precisely.
5. **Execution.** Send or enter an authorised order through the selected service. Preserve order and proposal identifiers.
6. **Confirmation and booking.** Match actual terms to the proposal; record partial fills, cancellations and amendments explicitly.
7. **Clearing or bilateral processing.** Apply the actual transaction's arrangement; neither clearing nor a particular collateral agreement should be presumed.
8. **Settlement and accounting.** Record payments, positions, valuation and journals according to their distinct rules.
9. **Reconciliation and refreshed risk.** Confirm the resulting positions and cash, then rerun relevant exposures. A successful execution is not proof that every risk has disappeared.

This is our proposed target workflow. The vendor matrix establishes examples of supporting capabilities; it does not establish that one reviewed product supplies every step out of the box.

## 5. A reusable integration record

| Field group | Suggested fields |
|---|---|
| Identity | Entity ID, contract/portfolio ID, scenario run ID, proposal ID, approval ID, order ID, trade ID, external confirmation ID |
| Economic terms | Currency, instrument/index, direction, notional, start/end dates, reset/payment conventions, quoted/executed price |
| Evidence | Source versions, curve/model versions, calculation hash, approval timestamp, authorised user/role |
| Lifecycle | Proposed, approved, sent, acknowledged, executed/partially executed, confirmed, booked, settled, reconciled, exception |
| Financial link | Cash-flow IDs, collateral event IDs, subledger/journal IDs, reporting batch ID |
| Recovery | Idempotency key, correlation ID, retry status, original-event reference, cancellation/amendment link |

These are design fields, not a claim that all vendors expose this schema. Map them to the chosen interfaces. If a message is repeated, the workflow must recognise the same business event rather than create another trade or journal. If acknowledgement is missing, query/reconcile status before assuming that execution failed.

## 6. How this improves each project

- **KESONIA Part 1:** add the responsibility map and distinguish analytics, transactions and accounting in the architecture.
- **KESONIA Part 2:** present accrual-to-ledger STP as a replayable calculation and posting workflow, with independent verification and adjustments.
- **KESONIA Part 3:** turn risk outputs into documented response proposals, showing expected benefit, cost and residual exposure.
- **KESONIA Part 4:** add the vendor matrix, transaction identifiers, exception handling and end-to-end reconciliation case. Retain “RegTech sweep” as the reporting workflow, separate from order routing and settlement.
- **Mwendo:** reuse the event chain for collections, approved refunds, received cash, reserve changes and waterfall allocation. The SPV does not need a bank's complete ALM or trading stack to benefit from those controls.
- **SokoIntel:** develop a scenario and decision workbench with traceable calculations and explicit export/integration contracts. Live trading is a separate product capability and authority boundary.
- **Business Credit and Owner Earnings:** use operating-data integration to connect receipts, commitments, loan payments and cash forecasts. These projects gain more from reliable dates and reconciliations than from adding a derivatives platform description.

## 7. A focused proof of concept

Start with a read-only scenario case and a simulated transaction lifecycle. The demonstration should ingest a small contract panel, generate cash flows, calculate FTP and ALM outputs, record a proposed response, and process a simulated confirmation into a position and accounting-event record. Then reconcile the result and rerun the exposure.

Test rejected proposals, changed prices, duplicate confirmations, partial fills, missing acknowledgements, late fixing corrections and settlement failure. Measure processing completion, exception age, manual touches, amount/position mismatches and time to reconciliation. Those measures make STP operationally meaningful.

Only a later implementation stage selects licensed products and proves instrument eligibility, connectivity and controls in an approved environment. **No vendor contact, booking, subscription or external transaction was performed for this review.**


---
Project copy. [Master review pack](<../../../output/kesonia_treasury_deep_review_2026-09-25/00_READ_ME.md>).
