# Review integration, implemented examples and remaining work

**Reconciled 1 October 2026.** The audit parsed all **71 existing Markdown and HTML documents** outside caches/vendor folders: 47 Markdown and 24 HTML. The [baseline inventory](../governance/implementation-2026-10-01/review_inventory.json) records hashes and text coverage; the [baseline audit](../governance/implementation-2026-10-01/BASELINE_REVIEW_AUDIT.md) records what was missing before this update. Parsing a document establishes coverage of its text, not independent validation of each inherited assertion.

## 1. Main conclusion

KESONIA supplies the reference **within** CBK's revised Risk-Based Credit Pricing Model. Borrower risk, lending costs and shareholder return determine the institution's approved customer premium; FTP explains internal funding/liquidity economics. These are complementary layers. The earlier wording about a transition “from RBCPM to KESONIA” should not be used. Part 1 and the active bibliography now state this relationship explicitly. [CBK issued framework, §§4–5](https://www.centralbank.go.ke/wp-content/uploads/2025/08/Revised-Risk-based-Credit-Pricing-Model.pdf).

The September review correctly identified work beyond compounding, but its delivery status became stale as code was added in RegTech, Mwendo and Underwrite. This revision supplies missing reproducible **reference implementations** and retains a separate list of unfinished research, institutional and integration work. No broad R-item below is claimed to be a completed bank deployment.

## 2. Read and reproduce

| Reading route | Implementation / result key |
|---|---|
| [Original worked examples](WORKED_EXAMPLES.md) | `benchmark.py`, `curves.py`, `pricing.py`, `scenarios.py`; original result keys |
| [FTP, deposits and existing STP](OPERATIONS_METHODOLOGY.md) | `operations.py`; `operations` |
| [Dated accrual, correction and workflow extensions](LIFECYCLE_WORKED_CASES.md) | `lifecycle_cases.py`; `lifecycle` |
| [OAS, priced hedges, collateral and structural credit](OPTION_AND_COLLATERAL_CASES.md) | `option_cases.py`; `options` |
| [Liquidity, exposure, CVA and trading-book components](REGULATORY_WORKED_CASES.md) | `regulatory_cases.py`; `regulatory` |
| [Hedge accounting and connected financing](ACCOUNTING_AND_CONNECTED_CASES.md) | `accounting_cases.py`, `connected_cases.py`; `accounting`, `connected` |
| [Symbols and units](SYMBOLS_AND_UNITS.md) | Original glossary plus links to extension-specific definitions |
| [SokoIntel candidate map](SOKOINTEL_CANDIDATE_MAP.md) | Product candidates and acceptance fixtures; no guest implementation claimed |
| [Screenshot synthesis: ALM, credit loss and workbench boundaries](SCREENSHOT_ENRICHMENT_ALM_CREDIT_LOSS_AND_WORKBENCH_2026-10-04.md) | Proactive ALM/ALCO, IRRBB/NMD/FTP framing, Treasury control proposal, credit-loss tail illustration and project/export boundaries |

From the repository root, run:

```text
python -m unittest discover -s tests -v
python -m research_lab.run_examples
python publications/build_publications.py
python publications/build_worked_examples_pdf.py
```

The calculation code uses the Python standard library. HTML and PDF publication commands need the documented rendering dependencies. The deterministic result file is [checked_examples.json](../../research_lab/results/checked_examples.json). Source and data hashes connect that output to its implementation. Tests check independent identities, limiting cases, replay, accounting balance and cash conservation, alongside invalid-input failures.

## 3. Eighteen-item reconciliation

“Reference implemented” means the stated bounded fixture runs and has tests. “Partial research” identifies executable progress with substantive model work still open. “Owning project” prevents duplicate methods and records the current external evidence.

| ID | Delivery status and executable evidence | Work still required |
|---|---|---|
| R01 Curves | **Reference implemented:** annual deposit/par bootstrap, interpolation, separate projection/discount curves, repricing and sensitivity convergence; options tree additionally fits all monthly synthetic discounts | Dated executable Kenyan quotes, instrument calendars, stale-quote/version controls and multi-instrument market calibration |
| R02 FTP lifecycle | **Reference implemented:** fixed, amortising, floating and revolving dated funding, commitment costs, ex-ante/ex-post bridge and consolidated elimination in `operations.py` | Complete volume/rate/basis/loss attribution, actual servicing ledger, institutional optionality/liquidity policies |
| R03 Deposits | **Partial research:** segmented asymmetric lagged regression, temporal holdout, retention/migration and constrained ladder | Permissioned data, robust uncertainty, feedback into dynamic reinvestment/withdrawal decisions and empirical stress validation |
| R04 Prepayment/OAS | **Reference implemented:** monthly curve-fitted short-rate tree, amortising pool, CPR/SMM, assumed rate-responsive prepayment, optimal-exercise comparison and numerical OAS solve in `option_cases.py` | Hull–White/Black–Karasinski alternative calibration, market volatility data, real borrower behaviour and measure/identification validation |
| R05 Hedge choice | **Reference implemented:** priced two-tenor swaps, finite portfolio search, basis/twist stress, slope/curvature, fees and initial-cash limits; original PV01 illustration retained | Executable prices, liquidity/counterparty/product constraints and dynamic rebalancing |
| R06 Collateral | **Reference implemented:** dated/intraday bilateral versus cleared cash, netting, threshold/MTA, haircuts, IM/VM and funding reconciliation | Actual CSA/CCP terms, disputes/default closeout, full instrument calendar roll, operational margin feed |
| R07 SA-CCR/CVA | **Scoped components implemented:** single-currency interest-rate netting/margin exposure, CVA valuation/CS01 and wrong-way comparison, reduced BA-CVA illustration | Other asset classes, full hedged BA/SA-CVA, actual netting/eligibility, local rule mapping; valuation hedging is not automatic capital relief |
| R08 Bank path | **Reference implemented:** original three-period cash/equity roll; new common-balance liquidity, NII/EVE and reverse-stress scenario | One fully dynamic institution-calibrated accounting/ALM/capital/distribution simulation and actual returns |
| R09 STP | **Reference implemented:** original durable proposal-to-reconciliation flow; partial fill/settlement, unknown acknowledgement, cancellation/amendment, correction approval/replay extensions | Unify reference flows with real vendor schemas, authentication, acknowledgements, capacity/recovery, exception-service standards and operational approval |
| R10 Mwendo SPV | **Owning-project reference exists:** October 1 canonical case covers funded closing reserve, priority payments, triggers, arrears and delayed refund/recovery; RegTech freezes provenance and adds a small handoff fixture | Live pool/servicer evidence, enforceable transaction terms, distribution/credit/rate stress calibration; reuse Mwendo engine |
| R11 Insurance | **Cash interface implemented:** accepted refund, settlement and lender/SPV allocation have distinct dates, rights and conservation tests | Full IFRS 17 group measurement, incurred claims, insurer and lender/SPV journals and approved handoff from accounting owner |
| R12 Structural credit | **Partial research:** Merton terminal-debt/equity valuation and inverse synthetic calibration | Compound-option payoff/exercise model, coupon/barrier extensions, observable data and reduced-form comparison |
| R13 Bayesian/statistical | **Owning-project methods recognised:** credit timing/cure, hierarchy/shrinkage and insurance relativities retain their canonical owners | Permissioned empirical, temporal, subgroup, ablation and decision-value experiments; not duplicated as KESONIA functionality |
| R14 Borrower-to-owner | **Reference implemented:** common borrower/originator/SPV/investor cash ledger, tax/retention, distinct earning power and distribution cash, delayed parent remittance; typed quantity checks | Institution/group-specific capital, tax, approvals and cross-project production schemas; connected fixture remains deliberately small |
| R15 FRTB | **Component implemented:** scoped standardised GIRR delta calculation with tenor/currency aggregation and correlation scenarios | Full relevant risk classes, vega/curvature, DRC/RRAO; IMA liquidity-horizon/stress ES, RFET, P&L attribution/backtesting and supervisory approval |
| R16 LCR/NSFR | **Reference implemented:** explicit eligibility, encumbrance, HQLA caps, runoff/inflow cap, ASF/RSF and undrawn commitment; linked to available cash | Complete bank classifications/returns, actual collateral monetisation and regulatory reporting reconciliation |
| R17 Hedge accounting | **Reference implemented:** fair-value hedge journals, recalculated-EIR amortisation, cumulative cash-flow reserve, ineffectiveness, settlement/reclassification, discontinuation alternatives and prospective designation control | Instrument valuation after rebalancing, real designation/effectiveness/credit-risk assessment, accounting approval and GL integration |
| R18 Kenya scope | **Verified source map plus research profiles:** issued CBK framework, historical fixing/index check, local liquidity guidance; source/version and evidence gates in fixtures | Actual entity/product contracts, authoritative unresolved day mapping, local available instruments/quotes, approved rules and reporting endpoints |

## 4. Cross-project acceptance cases

The [boundary document](CROSS_PROJECT_BOUNDARIES.md), section 13, reconciles Cases A–F and actions XB01–XB10. Its source map preserves September 28 reading anchors. The new snapshot at [cross_project_reference_2026-10-01.json](../../research_lab/data/cross_project_reference_2026-10-01.json) records the current owning-project results and hashes.

Mwendo's existing 28-test verification and Underwrite's saved borrower/decision cases are recognised as **external reference evidence**. They were read, not independently recertified by RegTech's test run. Neither a snapshot nor this repository's candidate map proves that SokoIntel has implemented those contracts.

## 5. Historical material and remaining delivery priorities

The September 23 pricing formulations, September 25 treasury casebook/software/FRTB reviews, original gap/enhancement notes, and screenshot-driven cross-project material informed this work. Historical review landing pages now point here. The old bibliography is preserved before targeted corrections to active claims about RBCPM, SHAP, benchmark-reform accounting and mandated cryptography. Bibliographic metadata outside the checked source register remains inherited material.

Remaining work has three concrete groups:

1. **Further code and research:** quote/calibration governance, full FTP attribution and behavioural uncertainty; unified dynamic bank/operational adapters; fuller capital approaches; post-rebalancing valuation and compound options. These are genuine unfinished developments, not merely missing approvals.
2. **Owning-project work:** insurance accounting, Mwendo transaction evidence and empirical Bayesian/credit experiments. Existing methodology and simulations are reused.
3. **Institutional evidence and execution:** permissioned histories, market quotes, signed terms, local classifications, approved calendars, vendor environments and supervisory/accounting acceptance.

This completes the stated new reference examples while preserving those broader requirements. The series and future SokoIntel programme remain larger than this review pack.

## 6. Screenshot-derived scope and export additions

The 4 October screenshot synthesis adds a reading and modelling checklist to the existing bounded examples: NII and EVE must be reported as different IRRBB views; deposit beta/pass-through, repricing lag, runoff and migration require segment-specific evidence and stress; “free funds” is a conditional spread outcome; and ALCO risk appetite, model-risk challenge and Treasury execution authority must remain visible. These topics sharpen R03/R08/R16 but do not turn the current examples into a calibrated institution's balance-sheet model.

The screenshot's expected-versus-unexpected-loss bridge is now stated with an explicit two-loan dependence illustration. It distinguishes approximate one-period \(PD\times LGD\times EAD\), IFRS 9 discounted cash-shortfall ECL, internally defined economic capital, and rule-based regulatory capital. The illustration is a conceptual review fixture in the note, not new checked Python or a validated capital method.

SokoIntel now has two additional candidate exports: (a) a versioned ALCO scenario/decision packet with NII/EVE, liquidity/collateral, binding constraints, sensitivity and approval state; and (b) a portfolio expected-loss/tail-risk bridge that identifies its method and dependence assumptions and labels ECL, economic-capital and regulatory-capital outputs separately. Both remain candidate requirements for product-owner mapping. The workbench may explain or carry approval records but must not select risk appetite, approve a capital method, or execute a hedge or funding transaction.
