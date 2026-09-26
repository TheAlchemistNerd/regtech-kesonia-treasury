# RegTech–KESONIA: useful material for a future series overhaul

**23 September 2026 · Review of the two latest pastes · Outline, not an implemented overhaul**

## Reuse the present foundation

The existing four parts contain regulatory context, compounding mathematics and SQL, pricing/accounting interfaces, and enterprise controls. The separate compounding/term-structure/funding-curve note already states the central distinction clearly. Underwrite Part 5 has the most developed current FTP and ALM exposition and should be reused as a conceptual source.

## Proposed four-part core

### Part 1 — From benchmark to contract

Retain the reform context. Build the explanation around observation date, publication time, applicability, contract reset, approved premium, fees, fallback and customer disclosure. Explain what each party can reproduce from a lending quote. Use sourced dated benchmark data for a worked case rather than a standing assumed current rate.

### Part 2 — From observations to a verified accrual

Retain the compounding engine and make its calculation contract explicit: decimal/percentage units, value dates, business/calendar days, holiday runs, missing publications, lookback versus observation shift, period boundaries, principal changes, floors, rounding and reversals. Distinguish the compounded factor from its annualised equivalent and from total cost of credit. Verify direct-product and eligible index-ratio calculations against identical conventions. A daily benchmark observation does not imply daily customer repricing.

### Part 3 — From contractual income to sustainable economics

Extend beyond a PD-driven premium to a full money-to-rate reconciliation: expected cash, EAD/drawdown, LGD/recovery timing, operating cost, matched funding, capital allocation and commercial terms. Use separate outputs for customer price, IFRS 9 ECL, lender contribution and internal capital. Add a term/revolver example and a delayed-protection example. Contract modifications and ordinary floating-rate resets should have distinct event types and accounting review.

### Part 4 — From financial events to governed decisions

Retain maker-checker controls, lineage and enterprise adapters. Add the common scenario bridge: curves and behavioural cash flows → NII/EVE/liquidity → management decision → approved execution → reconciliation. State what Oracle, SAP or Dynamics receives and which product or accounting engine owns the authoritative calculation. Product marketing, vendor capabilities and regulatory reporting interfaces require their own current evidence when drafting.

## Extensions beyond the core series

| Candidate module | Purpose | Prerequisite |
|---|---|---|
| Curve construction and FTP | Par/zero/forward/projection/discount/funding curves; interpolation and sparse-tenor handling | Instrument conventions and reliable dated data |
| Behavioural ALM | Deposit beta/decay, prepayment, extension and commitment drawings | Longitudinal institution data and an approved fallback |
| Collateral and hedging | Economic hedge, margin liquidity, counterparty exposure and accounting treatment | Executed terms or clearly labelled hypothetical contracts |
| Structured receivables funding | Borrowing base, waterfall, reserve, triggers and investor reporting | Defined transaction and asset tape |
| Advanced valuation/capital | OAS, CVA, SA-CCR/SA-CVA and structural-credit laboratory | Intended use, complete rule version, market calibration and independent validation |

These extensions keep the series open. They need not all become compulsory chapters in the initial overhaul.

## Proposed replacement framing for the pricing section

The risk model supplies one part of the lending decision. Its outputs must be converted into expected monetary loss over the product's horizon and combined with the institution's funding, servicing and capital economics. The contract service then applies approved terms and permissions. The benchmark repository supplies common evidence to those processes, while each output retains its own purpose, date convention and owner.

## Reusable exercise sequence

1. Reproduce an accrual from dated overnight observations.
2. Build a small discount-factor/forward-rate example with stated conventions.
3. Add an institution-specific funding spread and an amortising loan schedule.
4. Add a revolving commitment and funding option.
5. Compare NII, EVE and cash needs under coherent rate/behaviour scenarios.
6. Record a proposed management action and the contractual/accounting steps needed to execute it.

Use the [CBK KESONIA source](https://www.centralbank.go.ke/kesonia/) for benchmark definition and the [April 2026 MPC report](https://www.centralbank.go.ke/uploads/monetary_policy_reports/131378250_36th%20Monetary%20Policy%20Committee%20Report%2C%20April%202026.pdf) for the RBCPM premium formulation. Basel material is comparative until entity-specific local applicability is established. No current benchmark quote or universal lending margin is adopted in this note.

## Shared review and calculation basis

See the [two-paste review index](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/pricing_treasury_cross_project_review_2026-09-23/00_READ_ME.md>) and [working formulations and checked examples](<../../../output/pricing_treasury_cross_project_review_2026-09-23/02_WORKING_FORMULATIONS_AND_EXAMPLES.md>). Catalogue IDs and source-line references are in the central package.
