# Cross-repository implementation traceability audit

**Audit date:** 16 October 2026. **Scope:** RegTech KESONIA, Bayesian Telematics Relativities, Shared Value, Underwrite for Collection, Mwendo Pamoja, and SokoIntel ownership/product boundaries. This is a read-only source and evidence review; the only new output is this audit note. Existing manuscripts, calculations, generated results and the guest website were not changed.

## 1. Findings

RegTech contains a substantial tested synthetic reference library. Its September remaining-work lists are historical inputs, not the current completion register. Bayesian contains a developed paper and a reproducible synthetic comparison, with unresolved calibration, reserve, tail-risk and release-integrity work. Shared Value has complete source coverage and a detailed twelve-article plan; its new articles, computational cases and empirical pilot remain to be produced. SokoIntel already implements public scenario calculators in Django, while its C#/Excel/Azure enterprise workbench and most cross-project contracts remain requirements.

No reviewed financial model meets **EMPIRICALLY_VALIDATED** on the evidence inspected. Published external studies, checked arithmetic, source hashes, synthetic holdouts, software tests and a recorded website deployment each provide different evidence; none alone establishes population-specific financial-model validation.

### Status definitions

- **OPEN:** a proposal or required deliverable exists, but the corresponding executable model, integration or validation evidence was not found in the inspected scope.
- **PARTIAL:** meaningful work exists, with a substantive portion of the stated capability still open. A completed specification or manuscript does not close implementation.
- **IMPLEMENTED_SYNTHETIC:** executable bounded calculation or scenario, with synthetic/assumed inputs and supporting checks. The status applies to the named scope only.
- **EMPIRICALLY_VALIDATED:** evidence would need an identified real population, lawful/source-controlled data, suitable temporal/group validation, uncertainty and decision-performance evaluation. No row is assigned this status.

For operational website features, these four financial-model labels are insufficient: the audit records the dated deployment evidence separately and does not relabel a security release as empirical financial validation.

## 2. Ownership and paths

All path-and-line anchors below are relative to these exact roots.

| Key | Canonical local root | Ownership |
|---|---|---|
| R | C:/Users/Nevo/Downloads/regtech-kesonia-treasury | Treasury benchmark, ALM/FTP, bounded regulatory/accounting and operational research cases |
| B | C:/Users/Nevo/Downloads/bayesian-telematics-relativities | Canonical actuarial paper, derivations and Brian Hey synthetic experiment |
| V | C:/Users/Nevo/Downloads/Shared Value for Both Shareholders and Customers | Customer/shareholder programme, source record, articles and new reward/product cases |
| S | C:/Users/Nevo/Downloads/business and technical website blog | SokoIntel platform and controlled Workbench requirements; guest repository, read only |

The S root's Git remote is **https://github.com/TheAlchemistNerd/sokointel-platform.git**, verified locally during this audit. Its folder name does not indicate a separate publication-only repository. C:/Users/Nevo/SokoIntel Backend is a different news/backend project and is not the owner of this financial Workbench specification.

## 3. Scope and verification performed

The inventory read every Markdown/HTML file as text for counts and duplicate analysis. Close reading and implementation tracing concentrated on current registers, later reviews, manuscript scope/validation sections, relevant functions/tests and saved results. This is not a claim that every line of every legacy manuscript or every scientific source was independently revalidated.

| Scope inventoried | Files | Physical text lines | Treatment |
|---|---:|---:|---|
| R, excluding tmp and ordinary caches/vendor directories | 89: 60 Markdown, 29 HTML | 33,030 | Main four-part series, methods, historical review packs, rendered reading editions and source history included |
| B | 17 Markdown | 4,784 | Canonical paper/derivations/plan/correction ledger, later reviews and submission material included |
| V | 8 Markdown | 2,286 | Source extract, full article plan, coverage, standard, reference register and draft reply included |
| S/product_architecture | 83: 51 Markdown, 32 HTML | 17,748 | Controlled specification and 75 imported review-package files included; selected platform docs/code/tests traced separately |

Counts are a pre-save snapshot and include different publication representations. They are not counts of distinct models or new work items. An earlier broader R scan included 25 tmp-backup Markdown files and therefore counted 114 documents; those backup copies are excluded from the table. The full S tree scan found 282 Markdown/HTML documents, but most publication/vendor copies were irrelevant to this focused implementation audit.

### Fresh checks on 16 October

1. **RegTech provenance:** all 12 calculation-source hashes, all nine test-source hashes and the saved numerical-result hash match R/docs/governance/implementation-2026-10-01/verification.json. This preserves the link to its recorded 139-test run; it does not represent a fresh rerun of all 139 tests.
2. **RegTech focused rerun:** the parent task independently ran test_operations and test_regulatory_cases with bundled Python, -B; all 49 tests passed, exit 0, 86.217 seconds. No numerical-output regeneration was performed.
3. **Bayesian canonical validator:** fresh pass: 10,133 body words, 51 references, 43 equations and seven Mermaid figures. This is structural validation.
4. **Bayesian submission validator:** fresh run passed preceding structure/saved-result checks, then failed at validation/validate_submission.py:109 on the pinned canonical-paper hash. Current EF155755DA4B1907C34C8A127D4C394CD84A551BDBDB7A014B3C2191947A16A4 differs from expected 283AE8C7A96C362BC6B5E8224F91770C295CB2D4B3357D4AF3E758A58309FFFD. The expected hash was not changed.
5. **Bayesian experiment provenance:** current run_synthetic_comparison.py SHA-256 equals its saved manifest: 0EC2A1507FF9E09B1D9EA5DBCF5507AFC164672D8E201F86B30051CBE7846707. The experiment itself was not rerun.
6. **Shared Value:** current source hash matches the 10 October record: 5e718f11beaec08cc7fccc00aa75663118a05bd00761896b48a13ad4b6fc46c0. Independently checked 1,589 lines and 46 adjacent coverage ranges spanning 1–1,589 without gaps/overlaps. The saved plan validation records twelve articles, 36 questions and twelve 3,500-word budgets.
7. **SokoIntel:** source/test inspection and dated release records only. No website mutation, production check or new platform test run was performed.

## 4. RegTech evidence and remaining work

Use R/docs/methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md:36–59 as the current R01–R18 register. The source labels “reference implemented” and “component implemented” describe bounded fixtures, not whole institutional systems.

| Item and assessed status | Existing evidence, with exact relative path:line | Substantive remaining work |
|---|---|---|
| R01 curves — IMPLEMENTED_SYNTHETIC | research_lab/curves.py:39 bootstrap, :57 quote repricing, :67 separate projection/discount and :80 key-rate sensitivity; tests/test_benchmark_curves_scenarios.py; current register:42 | Dated executable Kenyan quotes, calendars, stale-quote/version controls and multi-instrument market calibration |
| R02 FTP lifecycle — IMPLEMENTED_SYNTHETIC | docs/methods/OPERATIONS_METHODOLOGY.md:1; research_lab/operations.py; current register:43 | Full volume/rate/basis/loss attribution, actual servicing cash and institutional optionality/liquidity policy |
| R03 deposits — PARTIAL; existing estimator and ladder IMPLEMENTED_SYNTHETIC | docs/methods/OPERATIONS_METHODOLOGY.md:61–109; research_lab/operations.py:167–358; tests/test_operations.py:76–140; current register:44 | Permissioned cohort history, uncertainty, regime/segment stability and joint dynamic retention/reinvestment validation |
| R04 prepayment/OAS — IMPLEMENTED_SYNTHETIC | research_lab/option_cases.py:24 curve-fitting, :69 pool, :114 OAS, :138 optimal exercise; tests/test_option_cases.py:19–116; current register:45 | Market-volatility calibration, alternative rate models, real borrower behaviour and physical/risk-neutral identification |
| R05 hedge selection — IMPLEMENTED_SYNTHETIC | research_lab/option_cases.py:172–243; tests/test_option_cases.py:122–150; current register:46 | Executable prices, liquidity/counterparty/product constraints, dynamic rebalancing and subsequent valuation |
| R06 collateral — IMPLEMENTED_SYNTHETIC | research_lab/option_cases.py:251; tests/test_option_cases.py:154–188; current register:47 | Actual CSA/CCP terms, dispute/default closeout, complete calendars and operational margin feed |
| R07 SA-CCR/CVA — PARTIAL; named components IMPLEMENTED_SYNTHETIC | research_lab/regulatory_cases.py:319 SA-CCR, :353 CVA, :386 wrong-way, :407 reduced BA-CVA; current register:48 | Other risk classes, full hedged BA/SA-CVA, valid netting/eligibility and applicable local rules |
| R08 bank path — PARTIAL; bounded common-book case IMPLEMENTED_SYNTHETIC | research_lab/regulatory_cases.py:181 reverse stress and :206–262 NII/EVE; tests/test_regulatory_cases.py:86–122; docs/methods/REGULATORY_WORKED_CASES.md:148–214; current register:49 | One dynamic, institution-calibrated accounting/ALM/capital/distribution path, with comparable scenario identity and explicit horizons |
| R09 STP — IMPLEMENTED_SYNTHETIC for local reference workflows | research_lab/operations.py:367; research_lab/lifecycle_cases.py:269 posting book and :335 partial settlements; tests/test_lifecycle_cases.py:154–249; current register:50 | Real vendor schemas/authentication/acknowledgements, unified recovery, capacity/exception service and authorized operational acceptance |
| R10 Mwendo handoff — PARTIAL, externally owned | research_lab/connected_cases.py:153 snapshot; current register:51 and :65 | Reuse Mwendo's canonical engine; live pool/servicer evidence and transaction/calibration work belong there. Parent task audits that owner separately |
| R11 insurance — PARTIAL; cash handoff IMPLEMENTED_SYNTHETIC | research_lab/connected_cases.py:114 refund case; tests/test_connected_cases.py:17; current register:52 | Insurer group measurement, incurred claims, IFRS 17 journals and approved accounting handoff remain distinct from refund cash allocation |
| R12 structural credit — PARTIAL | research_lab/option_cases.py:326 terminal Merton and :356 inverse calibration; tests/test_option_cases.py:200–229; current register:53 | Compound-option payoff/exercise, coupons/barriers, observable calibration and reduced-form comparison |
| R13 statistical/Bayesian — PARTIAL, externally owned | current register:54; Bayesian evidence in section 5 below | Permissioned empirical/temporal/subgroup/ablation and decision-value work; do not duplicate actuarial ownership in Treasury |
| R14 borrower-to-owner — IMPLEMENTED_SYNTHETIC | research_lab/connected_cases.py:15 typed quantities, :38 ledger, :74 finance, :133 owner case; tests/test_connected_cases.py:7–39; current register:55 | Institution/group-specific capital, taxes, approvals and production schemas |
| R15 FRTB — PARTIAL; GIRR delta component IMPLEMENTED_SYNTHETIC | research_lab/regulatory_cases.py:442–501; current register:56 | Other relevant classes, vega/curvature, DRC/RRAO and IMA data/validation/approval; a GIRR component is not complete FRTB |
| R16 liquidity ratios — IMPLEMENTED_SYNTHETIC | research_lab/regulatory_cases.py:41 LCR, :101 NSFR, :126 fixture; current register:57 | Actual position classifications, collateral monetisation and bank-return reconciliation |
| R17 hedge accounting — IMPLEMENTED_SYNTHETIC | research_lab/accounting_cases.py:21, :39, :54, :63 and :88; tests/test_accounting_cases.py:8–31; current register:58 | Valuation after rebalancing, real designation/effectiveness assessment, accounting approval and general-ledger integration |
| R18 Kenya scope — PARTIAL: source map and research profiles | current register:59; docs/methods/SCOPE_AND_SOURCE_REGISTER.md | Approved entity/product contracts, available instruments, unresolved authoritative day mapping and reporting endpoints |
| K1–K5 practical extensions — OPEN beyond reused fixtures | docs/methods/IFOA_PRACTICAL_APPLICATION_REVIEW_2026-10-03.md:13, :23, :35, :45, :55; explicit proposal status at :67 | Connected ALCO decision, estimation, full hedge life, real integration and institutional risk interpretation with the review's completion evidence |
| October 4 synthesis and October 16 beta article — PARTIAL as explanatory integration | docs/methods/SCREENSHOT_ENRICHMENT_ALM_CREDIT_LOSS_AND_WORKBENCH_2026-10-04.md:3, :40–57, :66; current register:79–85; publications/linkedin/Deposit_Beta_KESONIA_and_Bank_Risk_2026-10-16.md | These explain decision links. The two-loan tail example and new beta scenarios do not create a calibrated credit, ALCO or autonomous Treasury controller |

The deposit module is already beyond a one-parameter beta screen: it has asymmetric immediate/lagged OLS by synthetic segment, an explicit future holdout, distinct external withdrawals/internal migrations/new inflows, and a constrained ladder. Its deliberately changed holdout regime raises RMSE from approximately 0.121 to 4.209 basis points. That is evidence of a designed model-risk demonstration, not Kenyan calibration. The NII/EVE case also already uses the same opening book with separately specified horizons and balance conventions; its next gap is a joint dynamic path, not another introductory NII-minus-EVE explanation.

## 5. Bayesian Relativities

Paths in this table are relative to B. The correction ledger's completed items are primarily manuscript corrections and delivery checks. They should not be counted as sixteen deployed modelling capabilities.

| Item and assessed status | Existing evidence | Substantive remaining work |
|---|---|---|
| Canonical theory and manuscript — PARTIAL as a research-to-product programme; editorial structure complete | whitepapers/telematics-relativities/paper.md; Mathematical_Derivations.md; IMPLEMENTATION_CORRECTION_LEDGER.md:24–38; fresh structural validator pass | Product implementation, real-data evidence and later review deliverables are separate from paper completeness |
| Five-model comparison — IMPLEMENTED_SYNTHETIC | publications/submissions/brian-hey-2026/experiment/run_synthetic_comparison.py:152 simulation, :245–306 train/future split and grouped residualisation, :309–329 shrinkage approximation, :332 credibility; experiment/results/run_manifest.json | Permissioned populations, repeated temporal/group holdouts, cold start, calibration/ablation and business decision value |
| B1 calibration and complexity — PARTIAL | whitepapers/telematics-relativities/IFOA_PRACTICAL_APPLICATION_REVIEW_2026-10-03.md:13–21; experiment/results/model_comparison.csv | M4 pure-premium error 14.5136% versus M3 14.2989%; M4 severity deviance improves, but 90% aggregate predictive interval coverage is 9/12. Complexity is not uniformly superior. Repeat validation and quantify uncertainty |
| B2 reserves — PARTIAL; reserve illustration IMPLEMENTED_SYNTHETIC | experiment/run_synthetic_comparison.py:364–375; later review:23–31; experiment/results/reserve_comparison.csv | Reporting/payment geometric parameters match the generator. Independently estimate development, use paid/incurred triangles and multiple valuation/runoff dates |
| B3 capital/treaty — PARTIAL; bounded simulation IMPLEMENTED_SYNTHETIC | experiment/run_synthetic_comparison.py:378–397; later review:33–41; experiment/results/capital_and_risk_transfer.csv | 8,000 draws give about 40 observations in a 99.5% tail. Need seed/convergence uncertainty, dependence challenge, treaty price/reinstatement/recoverability timing and gross/net cash economics |
| B4 offered premium — OPEN beyond theory and loss-cost inputs | later review:43–51; canonical paper premium layers | Reconcile indicated loss, expenses, commission, reinsurance, capital, taxes and approved offered price; test renewal/selection/retention and customer effects |
| B5 insurer planning/IFRS 17 — OPEN beyond a specified interface | later review:53–61; whitepapers/telematics-relativities/ADDITIONAL_REVIEW_PRICING_AND_TREASURY_2026-09-23.md:11–45 | Joined policy/IPF/refund/incurred-claim event case, insurer measurement and cash/reserve/asset/capital/distribution reconciliation |
| Submission release integrity — OPEN | README.md:20; later review:63–67; publications/submissions/brian-hey-2026/validation/validate_submission.py:14 and :107–109 | Explain and reconcile working-paper version against pinned submission baseline; then rebuild/revalidate affected derived artifacts. Do not silently reset the expected hash |

In the table, experiment/ is shorthand for publications/submissions/brian-hey-2026/experiment/. “Later review” is the full October 3 path in the B1 row. The manifest accurately labels M4 a regularised-horseshoe **penalised conditional-mode approximation**. It is not a demonstrated full posterior sampler. The synthetic representation is not evidence of a trained production neural sensor pipeline.

## 6. Shared Value

Paths are relative to V. Current October 10 records supersede the earlier six-article sketch.

| Item and assessed status | Existing evidence | Substantive remaining work |
|---|---|---|
| Source extraction and planning — PARTIAL overall; preparation complete | README.md:5–11; 00_READ_ME.md:7, :18 and :35; SOURCE_TO_SERIES_COVERAGE.md:11 and :97–101; fresh hash/range checks above | Twelve finished articles and new numerical implementations remain open; named figures are plans |
| Risk and price cases — OPEN | SHARED_VALUE_SERIES_PLAN.md:63–109; PROJECT_RESEARCH_STANDARD.md:42–52 | Exposure/claims hierarchy, uncertainty, posterior-to-approved-price bridge and case validation using reused Bayesian theory with explicit provenance |
| Behavioural effects and customer outcomes — OPEN | SHARED_VALUE_SERIES_PLAN.md:113–159 | Executable intervention/eligibility specification, pilot design, safe delivery, causal outcome analysis and customer understanding/remedy evidence |
| Cohort economics and shareholder profit — OPEN | SHARED_VALUE_SERIES_PLAN.md:163–209 | Monthly renewals/migration and claims/reward cash over three renewals, revised LTV and setup allocation, dated capital/distribution ledger, NPV uncertainty and peak funding |
| Governance, engineering and operation — OPEN | SHARED_VALUE_SERIES_PLAN.md:213–335; PROJECT_RESEARCH_STANDARD.md:78–109 | Activity-specific legal checks, correction/deletion case, complete schemas, replay/latency/recovery tests, merchant settlement and operating controls |

The only Python file found here is build/source_extraction/extract_source.py. It supports document extraction, not insurance/behavioural economics. The 10,000-policy case, KES 35 million setup cost, reward shares, retention and timing targets are source/scenario assumptions awaiting calculation and evidence (SHARED_VALUE_SERIES_PLAN.md:33). A source register containing external studies does not empirically validate this proposed programme.

## 7. SokoIntel owner and implementation boundary

Paths are relative to S. The guest repository was inspected read only.

| Item and assessed status | Existing evidence | Substantive remaining work |
|---|---|---|
| Public listed-company scenarios — IMPLEMENTED_SYNTHETIC for seven bounded tools | apps/calculators/valuation_engines.py:1 and :10–171; valuation_views.py:53; apps/calculators/test_valuation_tools.py:47–443; docs/Calculator Architecture and Product Boundary.md:22–28 | Full issuer reconstruction, maintained source ingestion, professional review and institutional workflows. The documented 38 focused tests are dated evidence, not a fresh audit rerun |
| Public business cash/credit tools — IMPLEMENTED_SYNTHETIC for scoped defaults/relationships | apps/calculators/business_engines.py:13 owner cash, :75 weekly cash, :119 facility; docs/Business Calculators Release 2026-09-25.md:3–28 | Full maintained borrower/issuer models and enterprise lifecycle semantics remain outside free-tool scope |
| Enterprise Workbench — PARTIAL: controlled specification; enterprise implementation OPEN | product_architecture/SokoIntel Financial Analytics Workbench_ Comprehensive Software Requirements and Design Specification.md:23 and :185 | Shared C# core, professional Excel clients and Azure enterprise services are not established by this specification or the Django calculators |
| FR-099–132 cross-project contracts — PARTIAL: adopted requirements and reference cases | same specification:427–473, :772–804, :1066–1084 and :1364–1368 | Requirement → versioned model/function → independent vector → adapter → product acceptance trace. The specification explicitly says a reviewed document is not an executable suite |
| ALCO and tail-risk candidate packets — OPEN as product integrations | R/docs/methods/SOKOINTEL_CANDIDATE_MAP.md; R/docs/methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md:85; S specification:1368 | Product-owner mapping, typed schema and failure tests. Do not infer live hedge execution, automatic capital approval or autonomous risk appetite |
| Platform security/operations — PARTIAL operational scope, separate from model validation | docs/SokoIntel Security Milestone and Production Checks 2026-10-03.md:9–17, :19–33 and :39–44 | Dated record reports 211 passing tests and observed production protections at b11c3ab. It explicitly leaves private-bucket activation and CSP compatibility work open. This audit did not check current deployment |

Public scenario code is real implementation: for example, valuation_engines.py:10–39 reconciles earnings and CFO routes and preserves an unavailable CFO as None; tests/test_valuation_tools.py:48–94 check double counting, missing information and sensitivity. These controls should be reused where appropriate. They do not satisfy all FR-099–132 contracts or establish complete empirical issuer valuation.

## 8. Duplicates, historical records and true increments

1. **RegTech historical reviews:** docs/research/kesonia/TREASURY_REMAINING_WORK_REGISTER_2026-09-25.md:1 directs readers to the current October 1 register. docs/research/kesonia/RegTech_Gap_Analysis_Report.md:3 explicitly says it is superseded. The September HTML/Markdown pairings, source_library/review-history/ and tmp backups are provenance/reading copies, not additional unfinished programmes.
2. **Imported SokoIntel reviews:** product_architecture/SOKOINTEL_CROSS_PROJECT_REVIEW_INDEX.md:11 warns that a copied review does not make every proposal a current gap. Its :13 records seven subsequently implemented public tools. The imported 75-file package should feed one owner-specific register.
3. **Exact duplicate review groups found in S:** the business-credit follow-up equals its cross_project/project_notes copy; listed-company Owner Earnings and MSME follow-ups each equal their project-note copy; one pricing plan appears under linkedin, mwendo and underwrite_research; the entity-resolved cash-flow article appears under linkedin and underwrite_linkedin. These five byte-identical review groups represent eleven files, not eleven distinct deliverables. Markdown/HTML mirrors add further representational duplication.
4. **Bayesian plan versus correction ledger:** DETAILED_IMPLEMENTATION_PLAN.md and the correction ledger track much editorial development. Later B1–B5 are genuinely additional model/decision evidence requirements. Reopening already corrected notation is different from completing those requirements.
5. **Shared Value:** six themes became twelve planned articles on October 10. This is a justified editorial split, not twelve implemented model modules. Its novelty is a joined product/reward/customer/shareholder case and operating evidence; importing Bayesian or Mwendo introductory chapters would add repetition.
6. **Ownership prevents duplicate engines:** reuse Bayesian insurance likelihood/credibility, Mwendo receivables economics, Underwrite credit/causal methods and RegTech Treasury cases under versioned handoffs. A copied formula or SokoIntel requirement is not a second implementation.
7. **New beta article:** the October 16 article is synthesis and a research agenda built on already existing RegTech depth. It adds a self-contained explanation and hand arithmetic; it does not close R03, R08, K1 or empirical validation.

## 9. Practical completion sequence

1. Resolve Bayesian submission-version integrity as a bounded release task.
2. Keep one maintained status register per owner, linking historical proposals to current functions, tests, outputs and explicit open items.
3. Build RegTech's joined dynamic ALCO case and Bayesian's independent reserve/tail/price cases using current modules; attach uncertainty and scenario identity to each decision.
4. Develop Shared Value's first self-contained article/case, then its causal pilot and dated economics, using the canonical methods without duplicating ownership.
5. Promote a small SokoIntel vertical slice only after a requirement maps to an independently checked model, typed inputs/outputs, failure diagnostics and product acceptance. Retain its actual public calculators as useful starting evidence.
6. Empirical work requires its own population/data/temporal/group/outcome evidence. It cannot be closed by another narrative review or synthetic test count.

This audit changed no research result, expected hash, model, test, manuscript or guest-repository file. The prior combined-PDF visual QA is a separate task and does not establish financial-model validation.


## 10. Underwrite for Collection and Mwendo completion audit

Roots: **U** = `C:/Users/Nevo/Downloads/behavioural credit scoring - underwrite to collect rct`; **M** = `C:/Users/Nevo/Downloads/insuretech & embedded finance`. This additional read-only review inventories 167 Markdown files / 39,491 physical lines across selected canonical, research, case and publication directories, plus 82 MD/HTML files / 15,527 lines across five named historical output packs. Close reading covers current registers, laboratory READMEs, source-integration passages, selected code and saved evidence. Inventory coverage is separate from factual review of every assertion.

| Topic | Located implementation or manuscript evidence | Remaining development |
| --- | --- | --- |
| Underwrite statistical architecture | U `series/parts/Part_2b_Hierarchical_Bayesian_Underwriting_Causal_Identification_and_Lifecycle_Dependence.md`, lines 146, 406, 514, 592, 681, 772 and 799: hierarchy, augmentation, causal estimands, survival, cash targets and validation | Population-specific fitting, temporal/group validation, calibration and decision-performance evidence |
| Operating/finance case | U `research_lab/cases.py`, lines 71-183 and 252: borrower cash, pricing, shortfall, cash earnings, protection and static pool; IMPLEMENTED_SYNTHETIC | Calibrated PD/LGD/CCF, broader calendars, actual costs and authorised accounting/capital treatment |
| GOV-001 evidence-to-intervention case | U `research_lab/decision_case.py`, lines 101-147; integrated exhibit in `series/parts/Part_3_Regulatory_Orchestration_Fair_Intervention_and_Collection_Governance.md`, lines 344-354; IMPLEMENTED_SYNTHETIC | Broader entity/transaction matching, multihop transfers, actual approvals and follow-up |
| U1-U4 IFoA extensions | U `series/research/IFOA_PRACTICAL_APPLICATION_REVIEW_2026-10-03.md`, lines 13-57; PARTIAL | Fuller workout alternatives, identified intervention evaluation, longitudinal protection history and actual-versus-expected economics |
| Treasury and ring-fenced receivables | U `series/parts/Part_5_KESONIA_Pricing_Expected_Credit_Loss_Capital_and_Funding.md`, lines 339-648, 836-973 and 1014-1091: settlement, liquidity, curves, FTP, IRRBB, ALCO, funding ownership and reconciliation | Institution-specific calibration and live interfaces; older proposed-destination descriptions should use current Part 5 as evidence |
| Five AI follow-up articles | U `series/publications/linkedin/2026-10-08_causal_credit_series/`; developed articles and appendices, numerical identities in `build/mathematical_audit_checks.py` | Learned sequential policies, prospective outcomes and production orchestration remain implementation work |
| Mwendo static finance engine | M `research_lab/mwendo_operating_case/model.py`, lines 94, 111, 203, 242, 424; Part 5 Appendix B at lines 665-704; IMPLEMENTED_SYNTHETIC and integrated in manuscript source | Replenishment, new vintages, servicing failure, actual terms and calibrated behaviour |
| Mwendo M1/M2/M4 | M `docs/research/IFOA_MWENDO_APPLICATION_REVIEW_2026-10-03.md`, lines 11-29, 41-55; PARTIAL | Dated management decisions, revolving pools, separate HoldCo ledger, investor mandate/comparator and empirical outcomes |
| 156-week mobility follow-up | M `research_lab/mobility_fleet_case/README.md`, lines 3, 18-44; Part 5 lines 548-567; IMPLEMENTED_SYNTHETIC | Contract calibration, sponsor caps, lender-default path, early termination, tax and claims; supplied repair effects require causal evidence |
| Insurance profit-testing follow-up | M `research_lab/mobility_insurance_profit_case/model.py`, lines 77-112, 227, 516-552; `docs/research/MOOVE_BAYESIAN_INSURANCE_PROFIT_TESTING_CASE_2026-10-14.md`, lines 105-176; IMPLEMENTED_SYNTHETIC, partially advances M3 | Exposure/claim matching, independent development/tail validation, treaty/expense terms, identified intervention effects and IFRS 17 extension |
| Earlier workbook | M `docs/research/MWENDO_LEGACY_WORKBOOK_RECONCILIATION_2026-10-01.md`, lines 7-36 and 54-65 | Reuse corrected recurrences for any needed workbook extension; the historical workbook is an additional input |

### Navigation and status housekeeping

- U `README.md` and `series/parts/README.md` describe six parts/seven manuscripts with a pending Part 6. Their navigation should distinguish the released five-part edition and the subsequent programme.
- U `series/research/WORKED_CASE_REVIEW_COVERAGE_2026-10-01.md` already records GOV-001's later integration; interpret its earlier missing-work paragraph with that update.
- U's five-article `RELEASE_VALIDATION.md` and `build/pdf_final_visual_qa.json` held older counts. The publication handover now identifies those records as historical and supplies `build/publication_release_checks_2026-10-16.json` for the current editions.
- M `research_lab/mwendo_operating_case/README.md:68` still calls the case an appendix candidate; Part 5 now contains Appendix B. Update this navigation wording in a subsequent source housekeeping change.
- M `docs/controlled-specifications/README.md` distinguishes implementation specifications from public narratives. Similarly named Part 1 and Part 5 files differ in content and should retain their separate roles.
- M `research_lab/mobility_insurance_profit_case/model.py:526` uses an internal scenario name `validated_intervention`; the research note correctly describes the effect as assumed. Align the label with the documented evidence status in a subsequent code housekeeping change.

Fresh read-only hash checks match all six U operating-case sources, all three Mwendo static-case code files, and both mobility-case sources against their saved manifests. Saved records report 54 Underwrite tests, 28 Mwendo static-case tests and eight insurance-case tests; these counts are historical runs, not fresh tests in this audit. The parent publication task separately reran 37 mathematical checks for the five-article edition.
