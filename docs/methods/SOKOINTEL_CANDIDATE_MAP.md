# SokoIntel Financial Analytics Workbench: candidates from RegTech

**1 October 2026.** All introduced material can inform the workbench. Product scope should distinguish a calculation users can inspect, a specialist analytical module, an acceptance fixture and an integration contract. This is a candidate map saved in RegTech. SokoIntel's guest repository remains unchanged; adopted requirements are not presented as implemented software.

## 1. Candidate modules and release order

| Priority | Candidate capability | Reusable reference and acceptance condition |
|---|---|---|
| Core | Borrower/owner cash and purpose analysis | Underwrite/Mwendo owning cases; `connected_cases.py`: every cash transfer has payer, recipient and date; earning power and permitted distributions remain distinct |
| Core | Customer pricing and lending contribution | `pricing.py`, `operations.py`: benchmark plus margin reconciles to funding, cost, expected principal loss, fees and capital-return money without double counting |
| Core | Typed quantities, point-in-time evidence and scenarios | `connected_cases.py`, `lifecycle_cases.py`: incompatible entity/unit/claim/date quantities fail; unavailable evidence preserves its freshness state |
| Specialist treasury | Curves, FTP, deposits and liquidity | `curves.py`, `operations.py`, `regulatory_cases.py`: instruments reprice, internal transfers eliminate, cash and prudential ratios are separately reconciled |
| Specialist treasury | ALCO scenario and constrained-policy evidence export | `regulatory_cases.py` and the screenshot synthesis: dated NII/EVE, liquidity/collateral, behavioural-deposit assumptions, binding limits, uncertainty, stress results, version lineage and approval state in one review packet; actions remain proposals until authorized |
| Specialist risk | Credit expected-loss to portfolio-tail bridge | Underwrite owns borrower PD/LGD/EAD and event outcomes; candidate adapter presents the portfolio loss distribution and dependence assumptions, with IFRS 9 ECL, economic capital and applicable regulatory capital in separately labelled views; no generic formula is presented as booked ECL or required capital |
| Specialist finance | SPV and protection/refund adapters | Mwendo canonical waterfall plus RegTech cash fixtures: funded reserves, persistent arrears and distinct acceptance/settlement dates |
| Specialist accounting | Hedge-accounting explanation and journal preview | `accounting_cases.py`: journal balance, cumulative reserve, discontinuation and cash/P&L reconciliation; posting authority stays with Finance/GL |
| Advanced analytics | OAS, optionality and constrained hedge comparisons | `option_cases.py`: curve fit, valuation-measure assumptions, numerical residuals and funding demands visible |
| Advanced regulatory | SA-CCR, CVA and FRTB components | `regulatory_cases.py`: explicit method/version/asset-class perimeter; component output cannot be labelled total capital |
| Research | Bayesian uncertainty, structural/compound credit and behavioural estimation | Canonical credit/relativities owners; experiments promoted only after temporal validation and material decision value |
| Integration | Approval, order, confirmation, booking and settlement contracts | `operations.py`, `lifecycle_cases.py`: replay, partial execution and exceptions as adapter acceptance tests; live execution belongs to connected operational systems |

## 2. Existing specification and new evidence

The September cross-project review already identified adopted SokoIntel requirements FR099–FR132. This update supplies executable evidence that can be mapped to those requirements during a product-owner review. It does not issue new FR numbers or claim exact requirement closure without inspecting the current controlled specification and implementation together.

Each candidate should carry: intended user and decision; source and model version; legal entity and claim; currency, units and horizon; input evidence status; result uncertainty; calculation/reconciliation tests; supported limitations; and approval owner where the output affects a contract, journal or instruction. Treasury exports should additionally identify NII horizon and EVE discount assumptions, NMD behaviour vintage, the exact binding risk appetite/limit and whether an action is approved, proposed or rejected. Risk exports should show dependence, confidence/risk measure, expected loss, quantile/shortfall measure, accounting basis and prudential method as distinct fields.

The workbench can explain how KESONIA, the approved customer premium, FTP, expected loss and capital-return amounts fit together. It should allow separate views of the same dated financing chain without merging borrower, lender, SPV, insurer and shareholder balances.

## 3. Practical promotion gates

1. Reproduce the case and its failure scenarios in the workbench's own test environment.
2. Bind inputs to versioned, typed evidence with explicit missing-data handling.
3. Provide plain-language result explanations and units beside each output.
4. Validate the module for the intended population, instrument and decision.
5. Integrate through documented, authorised APIs when execution or accounting is required.

An illustration is useful as an acceptance fixture before it becomes a product feature. Specialist capital and trading-book modules should be selected for users who need those methods; they are not prerequisites for an MSME cash-flow analysis screen.

See the [implementation register](REVIEW_INTEGRATION_AND_REMAINING_WORK.md) for current status and the [cross-project boundaries](CROSS_PROJECT_BOUNDARIES.md) for ownership.
The new [screenshot synthesis](SCREENSHOT_ENRICHMENT_ALM_CREDIT_LOSS_AND_WORKBENCH_2026-10-04.md) records these candidates and their limits. They are review/export requirements only: the maintained RegTech repository does not implement a sequential RL controller or an autonomous treasury execution service, and no guest SokoIntel files were changed.
