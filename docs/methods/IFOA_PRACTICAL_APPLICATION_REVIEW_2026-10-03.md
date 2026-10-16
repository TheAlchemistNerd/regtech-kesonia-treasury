# RegTech–KESONIA: practical depth and the next decision cases

**3 October 2026. Status: development requirements derived from the current implementation and official curriculum.**

## Assessment and existing evidence

The [worked examples](WORKED_EXAMPLES.md), [18-item register](REVIEW_INTEGRATION_AND_REMAINING_WORK.md) and [cross-project boundaries](CROSS_PROJECT_BOUNDARIES.md) already provide substantial selected banking/Treasury depth. [Verification dated 1 October](../governance/implementation-2026-10-01/verification.json) reports 139 passing tests and identical repeated numerical output. This documentation review does not rerun that suite.

Important strengths include dated benchmark corrections, FTP cash, deposit estimation, curve construction, a prepayment/OAS tree, hedge alternatives, collateral timing, liquidity and capital components, accounting journals and reconciliation workflows. These support a focused professional portfolio. Completion of the entire banking or derivatives syllabus would require materially broader evidence.

The key official benchmarks are [SP10/B100/F107, objectives 5–10](https://actuaries.org.uk/media/vsgfrfdr/subject-f107_b100-banking-principles-_2026_clean.pdf), [SA10/B200/F207, objectives 1–9](https://actuaries.org.uk/media/zt0nlydf/subject-f207_b200-banking-applciations-2026_clean.pdf), [SP6, objectives 3–4](https://actuaries.org.uk/media/rnaebhef/sp6_syllabus-2026-_final-proof.pdf) and [CP2](https://actuaries.org.uk/media/ujbbaef3/cp2_syllabus-2026-_final-proof.pdf). The proposed packages below turn that comparison into practical acceptance conditions. They supplement the R01–R18 register; they do not close it.

## K1 — A connected ALCO decision

**Maps to:** R02, R08, R14, R16. **Owner roles:** Treasury, Finance and Risk.

Use one dated bank opening balance sheet and a monthly plan. Compare feasible combinations of lending growth, deposit repricing, term funding, hedging and distributions. Carry credit losses, margin cash, operational expense, tax assumptions and capital resources through the same periods. Import borrower and SPV outputs using their defined entity and cash-right boundaries.

**Deliverables:** base/adverse/reverse-stress paths, financial statements, funding plan, capital/liquidity constraints and an ALCO recommendation. Include a rejected feasible alternative and the assumption that would change the choice.

**Completion evidence:** each period reconciles cash, income and equity; internal FTP cancels in consolidation; economic, regulatory and accounting quantities remain identifiable; actions cannot use unavailable funding. Explain differences between a ratio passing and cash being available at the required time. Attribute subsequent earnings to volume, rates, basis, credit experience and costs without counting the same loss twice.

## K2 — Estimation and calibration that support the decision

**Maps to:** R01, R03, R04, R18. **Owner roles:** quantitative Treasury and model validation.

Use dated, licensed/permissioned instrument quotes and longitudinal deposit/prepayment observations. Specify instrument conventions and information cut-offs. Fit deposit pass-through, withdrawal and migration with uncertainty; compare a simpler challenger. For options, separate the physical behaviour model from the valuation-measure assumptions and justify their connection.

The current `calibrate_rate_tree` fits synthetic discounts with assumed volatility. Recovering the input OAS checks the solver. To validate a valuation model, also use independently supplied target prices, quote tolerances, a volatility calibration/challenger and stressed residuals.

**Deliverables:** data/quote register, calibration report, time-based validation, parameter sensitivity, numerical convergence and fallback policy.

**Completion evidence:** holdout observations are excluded from fitting; missing/stale data trigger a defined response; repricing meets stated tolerances; intervals and parameter changes are propagated to the actual K1 decision. A model can be rejected despite better fitting statistics if its maintenance or input requirements make it impractical.

## K3 — A hedge through its full life

**Maps to:** R05, R06, R07, R17. **Owner roles:** Treasury dealing, collateral operations and accounting.

Extend the current alternatives through execution, market movement, a margin call, a dispute/delay, rebalancing and termination. Recalculate instrument values after rebalancing. Include transaction costs, available collateral, basis mismatch and counterparty limits.

**Deliverables:** dated trade and collateral ledgers, valuation comparison, journal reconciliation and a decision on whether and when to rebalance. Define PV01 (value sensitivity to a one-basis-point rate move), option exposure, margin cash and accounting result separately.

**Completion evidence:** cash and journals reconcile; the economic benefit survives executable costs and constraints; the hedge's value-risk reduction and liquidity burden are both visible. Actual designation, netting and capital eligibility require the applicable contractual/accounting/regulatory evidence. Scoped SA-CCR and CVA functions retain their stated product coverage.

## K4 — An operational integration exercise

**Maps to:** R09. **Owner roles:** operations, engineering and independent control.

Reuse the durable workflow and correction/replay cases in one connected harness. Map an actual sandbox or agreed vendor message schema, permissions and acknowledgements. Exercise duplicate messages, unknown execution status, partial fills, partial settlement, stale approvals, outages and reconciliation breaks.

**Deliverables:** interface contract, exception queue, ownership/deadlines, recovery log and independently reconciled transaction record.

**Completion evidence:** retries do not create duplicate trades or payments; unknown outcomes are investigated before re-execution; recovery respects approved intent; the reported state agrees with external acknowledgements. Label a mock endpoint as simulated until a real counterpart is exercised. Measured service limits and operator recovery are required for an operational demonstration.

## K5 — Institutional risk and investment interpretation

**Maps to:** R07, R08, R15, R16, R18. **Owner roles:** risk, compliance, Finance and investment decision maker.

Build an entity-specific rule and product profile and explain why each selected capital/liquidity method applies. Extend GIRR delta, reduced BA-CVA and single-currency SA-CCR only where the intended portfolio requires the additional scope. Add a mandate and benchmark for the Treasury investment sleeve, then attribute its performance and liquidity use.

**Completion evidence:** reporting classifications reconcile to source positions; remaining exclusions are explicit; management limits translate into actions and accountable owners. A full FRTB implementation remains a distinct undertaking with the relevant risk classes, approaches and validation. Syllabus coverage does not decide Kenyan regulatory applicability.

## Publication and product boundary

Each package needs an executive decision memo, an operating instruction and a technical handover, with reader testing appropriate to [CP3](https://actuaries.org.uk/media/vsnpg4zm/cp3_syllabus-2026-_final-proof.pdf). KESONIA remains the reference within the revised RBCPM; internal FTP and risk-adjusted pricing have complementary roles.

The [SokoIntel candidate map](SOKOINTEL_CANDIDATE_MAP.md) can consume scenario, valuation, constraint and decision records after their evidence level is declared. It should preserve canonical method ownership and expose data quality, conventions, validity dates and open exceptions. This review edits no guest repository. K1–K5 are **proposed extensions**, with current reference cases retained as their starting evidence.
