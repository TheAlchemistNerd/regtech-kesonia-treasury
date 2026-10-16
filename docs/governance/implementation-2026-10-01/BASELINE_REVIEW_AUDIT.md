# RegTech review-to-implementation audit

Read-only audit on 1 October 2026. Repo: `C:/Users/Nevo/Downloads/regtech-kesonia-treasury`.

## Scope and evidence standard

Parsed every Markdown and HTML file throughout the repository outside `.git`, `tmp`, `__pycache__`, `node_modules` and `.venv`: 71 files, comprising 47 Markdown and 24 HTML documents. HTML script/style contents are excluded from visible-text extracts in `parsed_all/`, mapped by `review_inventory.json`. That inventory records paths, bytes, lines and SHA-256 hashes. The initial eight-directory focused pass covered 52 files; the expansion additionally parses inherited drafts, LinkedIn editions and repository navigation material. Current four core manuscripts, current method registers, September 23/25 review requirements, the casebook/blueprint/software/FRTB notes and historical gap/enhancement/K fragments were reviewed substantively. Rendered copies are presentations of those sources, not independent implementation evidence. The reference bibliography also remains in the parse scope; bibliographic correctness was not independently verified here. Additional inherited drafts were parsed and inventoried, not represented as an independent fresh legal or financial fact check of every sentence.

All seven `research_lab/*.py` hashes match the saved September 28 `research_lab/results/checked_examples.json` source hashes. This confirms source/result association. This agent did not rerun the full test suite, independently calibrate a financial model or exercise a vendor interface. Existing test names and assertions were inspected. No RegTech or guest source was edited.

A narrative, a numerical identity, an executable fixture, an empirical model and an institutional implementation require separate status labels. No entire R01–R18 requirement is closed by the existing seven modules.

## Register reconciliation at the existing baseline

Line references below are pre-change audit anchors. `REG` means `docs/methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md`; `BOUND` means `docs/methods/CROSS_PROJECT_BOUNDARIES.md`.

| ID | Existing demonstrated component | Executable work still missing in this repo | External completion dependency |
|---|---|---|---|
| R01, REG26 | `curves.py:39` annual-par bootstrap, log-discount interpolation, quote repricing, dual projection/discount values and finite-difference DV01. Tests `test_benchmark_curves_scenarios.py:74–97`. | Quote-quality/staleness input contract, curve-version comparisons, instrument cash calendars, coherent NII/EVE/cash scenario linkage. Extrapolation is explicitly rejected rather than implemented. | Kenya instrument universe, actual quotes, conventions, validation. |
| R02, REG27 | `operations.py:51,115` fixed/amortising/floating/revolver accrued FTP, commitment costs, ex-ante/ex-post total bridge, internal transfer elimination. | Attribution of actual-minus-plan to volume/rate/basis/loss/policy separately; servicing-event-to-ledger bridge. | Approved institution policy and actual servicing ledger. |
| R03, REG28 | `operations.py:172,218,256,276,295,309` two synthetic segments, asymmetric lagged OLS, later regime holdout, tagged retention/migration and constrained finite-grid ladder. | Dynamic reinvestment/withdrawal stress coupled to the bank path; estimation uncertainty propagated to decisions. Current SEs are explicitly iid diagnostics. | Longitudinal permissioned data and robust empirical validation. |
| R04, REG29 | OAS equation and scope only in historical casebook §7. | Interest-rate path calibration fixture; assumed/estimated exercise law; generated cash-flow paths; bracketed OAS root solve; limiting/residual/convergence tests. | Real market calibration and local behaviour. |
| R05, REG30 | `scenarios.py:128` finite two-PV01 hedge choice subject to assumed collateral budget. | Instrument-priced hedge comparison; nonlinear/basis/tenor stress; explicit funding/product-change alternative. | Approved instruments, executable prices and limits. |
| R06, REG31 | `scenarios.py:42` posted collateral is a restricted asset and reduces cash. | CSA/cleared collateral timeline, thresholds, VM/IM, haircut, netting, settlement lag and funding; connect value benefit to margin cash. | Actual legal terms and margin model. |
| R07, REG32 | Historical `verify_examples.py` checks independent-exposure CVA arithmetic. | SA-CCR replacement cost/PFE example, standalone CVA-capital method, spread-risk/hedge calculation and joint wrong-way-risk case. | Method/jurisdiction/eligibility and legal netting evidence. |
| R08, REG33 | `scenarios.py:42,158` three periods reconcile cash, gross loans, deposits, wholesale funds, equity, losses and recovery. | Curve-valued EVE, full base/shock/reverse-stress comparison, prudential ratios and accounting connected to same path. | Bank data and policy. |
| R09, REG34 | `operations.py:366–573` durable SQLite proposal/approval/order/confirmation/booking/settlement/reconciliation; restart, idempotence, rejection, changed terms, tampering, settlement failure and retry. | Accrual-to-ledger correction workflow; partial fills; unknown acknowledgement; cancellation/amendment; event-time/exception-age metrics; calculation/position/risk refresh linkage. | Vendor sandboxes, authentication, external acknowledgements, capacity/recovery sign-off. |
| R10, REG35 | RegTech owns interfaces, not canonical waterfall. | Import a versioned, bounded Mwendo scenario output and reconcile rate/funding handoffs. | Mwendo transaction legal terms and empirical assumptions. **Oct1 Mwendo case now exists; refresh the Sep28 status instead of recreating it.** |
| R11, REG36 | Boundaries and planned numeric insurance handoff only. | Insurer/lender/SPV accepted-claim/refund and settlement event bridge; no duplicated recovery. | Insurer measurements/journals and approved IFRS17 methodology belong to owning project. |
| R12, REG37 | Structural/compound-option concept only. | Payoff/exercise specification, calibration/valuation and sensitivity checks. | Advanced research; not a compulsory CBK benchmark implementation. |
| R13, REG38 | Cross-project statistical ownership recognised. | Temporal/subgroup/decision-value ablations remain in owning credit/actuarial projects. | Data and experimental design. Do not rederive Gamma/NB here. |
| R14, REG39 | Quantity dictionary, margin bridge and interface map. | Same scenario’s borrower, lender, SPV, business-owner and parent distribution reconciliation including restrictions and dates. | Owner/accounting policy; guest repos remain read-only. Oct1 Underwrite/Mwendo components should be reused. |
| R15, REG40 | Book/method boundary and FRTB plan. | Scoped standardised example with component reconciliation, separate illustrative ES, rule-based risk-factor/desk evidence specification. | Local applicability, chosen method, actual inventory/data/approval. A simple ES statistic is not full IMA. |
| R16, REG41 | Kenya issued guidelines identified; no ratio engine. | Classified HQLA/haircuts/encumbrance/outflows/inflow-cap and ASF/RSF calculation linked to same cash case. | Entity-specific local classifications and return mapping. |
| R17, REG42 | Part3:163–169 has simple 8/8 versus 8/7 fair-value journal description and cash-flow OCI explanation. | Full fair-value and cash-flow journals, cumulative lower-of constraint, ineffectiveness, settlement/reclassification, rebalancing and discontinuation. | Designation eligibility and accounting sign-off. |
| R18, REG43 | Scoped final framework, historical fixing/index check, local liquidity guideline source map. | Machine-readable purpose/entity/rule/convention eligibility gate and dated input inventory. | Actual contracts/calendar, supervisory interpretation, quotes, platform interfaces. |

## Additional core requirements that the 18 rows hide

1. **Balance changes and margin treatment.** `benchmark.py:110–119` expressly supports only constant principal, simple margin, no caps/floors or in-period reset. Part2:80–95 describes a capitalising account recurrence but does not implement it. Part2:172 and September25 blueprint fixtures request principal changes, simple versus compounded margin, corrected fixing and rerun after posting. A specified synthetic profile can be implemented now without claiming it resolves every CBK contract convention.
2. **Corrections cross the calculation/ledger boundary.** Benchmark tests select a corrected fixing by information cutoff, but no calculation result is connected to an approved posted accrual and linked delta/reversal. Part4:43–61 gives KES1,024.26 as the example and asks for the full replay report. Existing STP is a fixed deposit placement, not this accrual workflow.
3. **Partial and unknown execution states.** `operations.py:448–505` supports PROPOSE/APPROVE/REJECT/ORDER/CONFIRM/BOOK/SETTLEMENT_FAILED/SETTLE/RECONCILE. It requires exact full confirmation. The September25 STP review:85–87 explicitly asks changed prices, partial fills, missing acknowledgements and late corrections, and Part4:97–103 retains these requirements. These are implementable mock cases, distinct from live API dependencies.
4. **Shared typed data contracts.** BOUND:168–184 defines ten cross-project schema names, but these are proposed names, not existing deployable schemas. Current dataclasses cover only calendar/fixing/interval/FTP/balance/period subsets. A minimal typed quantity/event/export fixture with entity/date/unit/source/version checks would close more of XB05 than another prose table.

## Cross-project case and action status

| Boundary request | Existing status and required update |
|---|---|
| CaseA, BOUND212; XB02 | Money/rate/RAROC arithmetic exists. Same-facility borrower cash and effective-return comparisons should cite current Underwrite executable case; RegTech currently presents separate fixtures. |
| CaseB, BOUND218; XB03 | No RegTech SPV engine, appropriately. **Mwendo `research_lab/mwendo_operating_case/README.md` now documents funded closing reserve, stateful waterfall, delayed refund/recovery, persistent triggers, retained arrears and current tests.** Update status using this evidence; do not call Sep28 interface-only state current. |
| CaseC, BOUND224; XB09 | Curve, FTP and bank cash components exist. They are not yet one common scenario producing recomputed EVE/NII/operational cash/ratios. |
| CaseD, BOUND230; XB07 | Insurance accounting contract-group computation remains elsewhere; accepted right versus actual cash principles can be enforced by an executable inter-entity event fixture. |
| CaseE, BOUND236; XB06 | No complete bank/insurer-parent remittance restriction engine in RegTech. The applicable quantity dictionary exists. Owner Earnings repositories remain guest sources. |
| CaseF, BOUND242; XB10 | Local SQLite trade path supplies significant subset. Benchmark feed/calculation to position and partial execution/missing data paths remain. |
| XB01, BOUND320 | Historical direct/index computation and versioned fixing selection done; institutional lookback mapping open. |
| XB04, BOUND323 | No RegTech recovery-readiness state adapter. Current Underwrite `decision_case.py` should be inspected for reusable evidence/permission states before adding another implementation. |
| XB05, BOUND324 | SokoIntel specification adoption is already recognised; no SokoIntel implementation proof from these documents. Provide typed exports and traceability here, keep guest unchanged. |
| XB08, BOUND327 | Three obsolete reports have current landing pages and preserved originals. Historical Sep25 output packs and legacy reference bibliography need visible current-status routing. |

## Documentation issue affecting claims of completed integration

`docs/research/kesonia/KESONIA_ERP_Reference_List.md:134` still says regulatory acceptance requires SHAP-level interpretability; line224 claims BCBS operational-resilience principles mandate immutable media/WORM/AES-256. The current core/articles and source register correctly limit these assertions, but the active bibliography and `publications/build/references/KESONIA_ERP_Reference_List.html` still publish the older language. The bibliography also mixes author/year/title metadata and contains citations without identifiers. It needs a clear legacy status and verified replacement citations, with targeted claim corrections rather than representing all references as checked. This finding does not ask that speculative security controls be implemented as legal requirements.

## Finite development order

1. **Core contract and event case:** explicit changing-principal profile, margin/floor specification, original-versus-corrected result, approved delta posting, deduplication and reconciliation.
2. **Connected treasury case:** price/source-versioned curve, dated FTP, balance-sheet NII/EVE/cash and LCR/NSFR reconciliation; preserve synthetic labels.
3. **Execution extension:** partial execution, unknown acknowledgement, cancellation/amendment, restart and reconciliation with residual exposure; no live external messages.
4. **Optionality and margin laboratory:** assumed/calibrated synthetic paths, prepayment cash, OAS solve, full instrument sensitivities and dated collateral cash.
5. **Specialist examples:** separate rule-versioned SA-CCR/CVA-capital, FRTB standardised subset and hedge-accounting cases with explicit domain limits. No all-purpose capital shortcut.
6. **Cross-project reuse and export:** read current Oct1 Underwrite/Mwendo outputs, define typed scenario exports and evidence/refund/owner endpoints, update XB status. Retain IFRS17/actuarial and guest ownership.
7. **Publication reconciliation:** update current MD registers with requirement→function→test→result links, preserve historical originals with current-status banners, rebuild HTML/PDF and symbols.

Live vendor connectivity, institution-specific scope, market data, empirical validation and legal/accounting approvals cannot be claimed from synthetic code. They are bounded external dependencies, not reasons to leave feasible research examples unimplemented.

## October 1 adjacent implementations: exact facts

The additional read-only checks support the following status improvements without claiming a new whole-repository audit:

- **Mwendo** `research_lab/mwendo_operating_case/model.py`: `product_schedule`94, `driver_case`111, `note_factor`195, `opening`203, `workout_per_default_driver`226, `pool_case`242, `management_pricing`424, `evidence_case`472. `baseline_verification.json` records 28 tests, zero failures/errors and deterministic repetition. Its common case has three products, driver operating constraints, a six-period KES financing stack, funded closing reserve, scheduled note coupons, constrained priority payments, trigger persistence, arrears, refund receipt delay and evidence clocks. `docs/research/MWENDO_WORKED_OPERATING_AND_FINANCING_CASE_2026-10-01.md:209–219` maps review requirements to actual scope and keeps durable events, live interfaces, concentration/new-purchase tape, empirical outcomes and parent distributions open. Thus XB03 and R10 have **an owning-project executable reference**, rather than only a design.
- **Underwrite** `research_lab/cases.py`: borrower71, pricing104, cash_shortfall135, scenario_profit156, protection183, evidence_state199, replay211, vintage235, stateful pool252. `series/appendices/WORKED_OPERATING_AND_FINANCE_CASE.md:A2–A9` publicly describes borrower cash, monetary pricing, recovery/protection timing, evidence, cure states and an optional vehicle with funded reserves and payment priority. This contributes reusable reference components to Cases A/B, XB02/XB03 and R10/R14, but it is not the complete bank/insurer-parent bridge.
- **Underwrite governance** `research_lab/decision_case.py`: visible19, transaction_view23, evidence_route101, amendment_gate132, append_event147, action_snapshot182, protection_snapshot200. It has point-in-time account ownership/classification, incomplete-evidence routes, permission and borrower-agreement gates, reviewed-version-before-approval checks, and approved no-borrower-action alongside a changed recovery assumption. This is substantive existing XB04 evidence. The retained contract and separate updated recovery assumption should be consumed through a RegTech adapter, not described as an unbuilt distinction.
- None of these checks establishes an actual IFRS17 contract-group measurement, insurer-parent remittance engine, SokoIntel running application or permission to edit a guest repository.
