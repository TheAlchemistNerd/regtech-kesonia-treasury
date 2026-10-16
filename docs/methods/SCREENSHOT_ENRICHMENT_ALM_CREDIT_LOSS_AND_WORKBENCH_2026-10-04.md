# Screenshot enrichment: ALM, credit loss and analytics-workbench boundaries

**4 October 2026.** This note distils the supplied professional-learning and credit-risk screenshots into additions for the maintained project reviews. The screenshots are prompts for useful questions, not evidence of a Kenyan institution's policy, a model's validation, or a completed implementation.

## 1. Proactive balance-sheet management and governance

Asset-liability management (ALM) is a continuing balance-sheet discipline: forecast contractual and behavioural cash flows, test rate and liquidity scenarios, compare earnings and value effects, and prepare feasible responses. It can support profitability, but profitability is not its sole objective. Resilience, customer commitments, capital, risk appetite, operational capacity and regulatory limits constrain the choice.

ALCO sets or recommends strategy within the institution's delegated governance; Treasury manages positions and executes approved funding/hedging; independent risk challenges assumptions, measures and limits; Finance owns accounting treatment and reconciliations; model-risk and validation functions challenge material models. Exact delegations vary by institution and must be evidenced. A course advert or generic role description does not establish an actual bank's mandate.

The distinction between banking book and trading book matters for the exposure, valuation, accounting and prudential treatment being analysed. Banking-book interest-rate risk (IRRBB) includes both earnings and economic-value views. Credit spread risk in the banking book (CSRBB) is a related but separately defined risk channel; it must not be folded into IRRBB without identifying the applicable measurement and policy perimeter. Do not import trading-book FRTB measures or trading-book limits as if they were a universal banking-book requirement.

## 2. IRRBB, deposits and performance measures

- **NII / earnings view:** compare projected net interest income over a specified horizon and scenario. State the horizon, balance-sheet assumptions, basis, and whether the calculation is static or dynamic.
- **EVE / value view:** compare the present value of relevant asset, liability and off-balance-sheet cash flows under defined rate shocks. Specify discount curves and options/behaviour assumptions. A small earnings impact does not establish a small EVE impact, or vice versa.
- **Non-maturing deposits (NMDs):** distinguish observed customer rates from reference rates. Estimate pass-through/beta, repricing lag, decay, runoff, migration and stability by justified segment and date. Present uncertainty and stress alternatives; “core deposit” is a behavioural estimate, not a contractual maturity.
- **Free funds in rising-rate conditions:** the benefit depends on the observed repricing and retention of deposits, asset reinvestment rates, volume migration, floors/caps, expenses and the chosen comparison. Do not describe low-cost balances as unconditionally free profit.
- **NIM and ROE:** define numerator, denominator, consolidation perimeter, capital allocation and time basis. A movement in a management ratio is not automatically economic profit, distributable cash, or shareholder return.
- **Model risk and risk appetite:** identify owners, assumptions, validation evidence, limits, triggers and fallback actions. Risk appetite constrains an action set; it should not be encoded only as a penalty that a high expected reward could offset.

The existing RegTech reference cases include dated curve construction and repricing, FTP lifecycle, NMD regression/ladder, an NII/EVE and reverse-stress balance-sheet case, and liquidity ratios. They are bounded synthetic/reference calculations. The outstanding evidence remains institution-specific curves and classifications, permissioned behavioural histories, dynamic ALM calibration, model validation and reconciled bank returns; see [review integration and remaining work](REVIEW_INTEGRATION_AND_REMAINING_WORK.md), especially R01–R03, R08 and R16.

## 3. FTP is a strategic internal price, not the customer rate

FTP assigns internal funding, term and liquidity economics to products and business units and transfers specified balance-sheet risks to Treasury/ALM. It can shape origination, deposit gathering and product mix, so curve design, behavioural assumptions, incentives and overlays require governance. A defensible view should show the benchmark or risk-free basis, projection/discount conventions where relevant, term/liquidity adjustments, optionality assumptions, asset charge, liability credit and Treasury residual. Internal transfers should eliminate on consolidation.

Customer pricing remains a separate decision. A customer rate or premium must reconcile its applicable benchmark, credit and operating costs, risk/protection costs, capital-return hurdle and contractual features without duplicating an FTP charge or a separately explicit funding cost. Report product/business-unit profitability with a defined NIM/ROE or contribution denominator and show how the result changes with curve, deposit behaviour and customer volumes. LCR/NSFR are prudential ratios with their own eligibility, runoff, inflow, stable-funding and reporting rules; they are not interchangeable with internal FTP charges or unrestricted cash forecasts.

## 4. Treasury control/RL research framing

The proposed Treasury case can be formalised as a partially observed, constrained sequential-control problem. A candidate state/observation at decision time may contain dated balance-sheet cash flows and repricing gaps; market/projection curves; NMD repricing and runoff estimates with uncertainty; prepayment assumptions; NII/EVE sensitivities; liquidity and capital headroom; collateral and contingent calls; executed positions; model and limit versions; and unresolved data-quality flags. Use the smallest aggregated sufficient state that supports the decision. Account-level personal data should not be pulled into a bank-wide policy when approved aggregates suffice.

Candidate actions can include a choice among approved funding tenors, a bounded hedge size or instrument set, liquidity-buffer allocation, and a request for human review. The feasible-action gate must enforce legal authority, risk appetite, limits, concentration, eligible instruments, settlement capacity and ALCO delegation before optimisation. A proposal may not execute, reclassify a book, change a customer contract, override a limit or amend accounting treatment.

The reward can report risk-adjusted earnings/contribution net of explicitly defined execution, funding, carry, collateral and operating costs, while hard constraints separately cap liquidity-shortfall probability, NII/EVE sensitivity, leverage/capital measures, counterparty and concentration exposures. If risk measures enter the objective (for example an expected-shortfall penalty), name their horizon, confidence level, scenario distribution and calibration. Do not award a generic “compliance reward” that lets a violation trade off against income. Compare first against fixed rules, static constrained optimisation and model-predictive control using the same forecast and stress scenarios. RL/POMDP is a research candidate only if partial observability, action-dependent transitions and repeated decisions are material and testable. Simulation results are conditional on the simulator, not proof of real-bank improvement.

An ALCO-facing export should include the recommended next action and approval state, feasible alternatives, binding constraints, state timestamp, curve/model/policy versions, NII/EVE and liquidity/collateral projections, uncertainty and stress ranges, costs, exceptions, validation status, reason codes, responsible owner and review date. SokoIntel can present/reconcile this evidence; it is not the risk owner, optimiser authority, execution venue or regulatory approval.

## 5. Credit expected loss, portfolio tail risk and capital

For a simplified one-period loan with exposure \(EAD_i\), default probability \(PD_i\) and loss fraction \(LGD_i\), \(PD_i\times LGD_i\times EAD_i\) is a useful expected-loss approximation. It relies on an identified horizon and consistent definitions and does not by itself describe accounting ECL, realised cash, or tail capital. A portfolio loss variable can be written

\[
L=\sum_i EAD_i\,LGD_i\,\mathbf{1}(D_i),
\]

where \(D_i\) denotes default in the defined horizon. Portfolio expected loss is \(E[L]\); common economic drivers and residual dependence affect the distribution and upper tail even when marginal PD, LGD and EAD are unchanged.

**Illustration (hypothetical, one period):** two loans each have EAD KES 100,000, marginal PD 5%, and LGD 50%. Each default costs KES 50,000, and portfolio expected loss is KES 5,000. If defaults are independent, the loss distribution is KES 0 with probability 90.25%, KES 50,000 with probability 9.5%, and KES 100,000 with probability 0.25%; the 99% VaR is KES 50,000. If a common shock makes both loans default together with probability 5% and neither default otherwise, expected loss remains KES 5,000 but the 99% VaR is KES 100,000. At this discrete distribution, the simple \(VaR_{99\%}(L)-E[L]\) illustration is respectively KES 45,000 and KES 95,000. This shows why dependence can move tail exposure without changing the expected loss. It is **not** a bank capital formula or a calibrated portfolio model.

Use these terms carefully:

- **IFRS 9 ECL** is a probability-weighted, discounted cash-shortfall measurement using relevant forward-looking information and the applicable 12-month/lifetime horizon. \(PD\times LGD\times EAD\) can be a component or simplifying approximation, not a universal identity for the booked amount.
- **Economic capital** is an institution-defined internal measure of loss capacity under a stated horizon, confidence/risk measure, diversification, and governance. It may compare a portfolio loss quantile or expected shortfall with expected loss, but there is no universal capital identity.
- **Regulatory capital** is calculated under the applicable prudential approach, exposure class, inputs, floors, buffers and supervisory rules. A generic “stressed loss minus expected loss” expression is not a substitute for that calculation.
- **Pricing and P&L** must avoid charging or deducting the same expected loss, funding cost or capital charge twice. Provision recognition, capital allocation, economic pricing and realised recovery answer different questions.

Underwrite for Collection owns borrower/loan-level cash definitions, PD/LGD/workout evidence and intervention experiments. RegTech owns bank-level capital, liquidity, ALM/FTP and ALCO presentation. Mwendo owns its platform/SPV contractual waterfall and investor distribution. Bayesian Relativities owns GI claim-frequency/severity and insurance capital/reserving methods. SokoIntel may consume versioned outputs through explicit interfaces without claiming these methods.

## 6. Project and curriculum implications

- **IFoA crosswalk:** strengthens selected evidence links for CP1/CP2/CP3, SP5/SP6, SP9, SP10/B100 and SA10/B200, especially ALM control, derivatives/collateral, risk aggregation and decision governance. It does not close full-subject evidence gaps or establish examination equivalence. The [portfolio crosswalk](<../../../insuretech & embedded finance/docs/research/IFOA_OBJECTIVE_TO_PROJECT_EVIDENCE_CROSSWALK_2026-10-04.md>) carries the objective-level status.
- **Underwrite for Collection:** add the tail-risk bridge alongside—not inside—the borrower ECL/pricing identity, and pass only dated, validated collection cash and behavioural estimates to Treasury.
- **Mwendo Pamoja:** use transaction funding, reserve, arrears and distribution schedules. Bank NII/EVE, bank FTP and ALCO governance are not substitutes for SPV cash waterfall, legal transfer, platform viability or investor distribution conditions.
- **RegTech KESONIA:** reuse the existing bounded ALM/FTP/liquidity/collateral/capital examples; identify their scenario assumptions and empirical calibration work. This note proposes no unvalidated controller implementation.
- **SokoIntel:** see the added candidate rows in [SokoIntel candidate map](SOKOINTEL_CANDIDATE_MAP.md). Export is for traceable analysis and governed review, not autonomous execution.

## Sources and interpretation

The supplied screenshots cover ALM/ALCO strategy, IRRBB, deposit behaviour, FTP, model risk, the proposed RL state/action/reward framing, and an EL–UL–capital explainer. Their formulations have been treated as prompts and reconciled to the repository's worked examples and stated boundaries. Accounting and regulatory capital conclusions require the entity's adopted accounting policies and applicable prudential methodology; this note is a research/design aid, not legal, accounting or supervisory advice.
