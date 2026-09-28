# Dated funding, deposit behaviour and controlled processing

**28 September 2026 | Synthetic reference implementation for R02, R03 and R09**

This laboratory turns three useful ideas from the supplied material into inspectable computations: internal funding attribution over a product's life, estimation of deposit repricing and runoff from a longitudinal panel, and a replay-safe transaction workflow. It supplies local examples and tests. It does not establish empirical Kenyan behaviour, executable market terms, regulatory compliance, accounting-policy approval or vendor connectivity.

## Source anchors and reading scope

Repository-relative paths below refer to the preserved originals; physical line numbers are retained because a single pasted line sometimes contains several paragraphs and search-result fragments.

| Source | Material read and used |
|---|---|
| `docs/research/kesonia/TREASURY_REMAINING_WORK_REGISTER_2026-09-25.md` | Read in full. R02 at line 16; R03 at line 17; R09 at line 23; the explicit restart/reconciliation requirement at line 40 |
| `output/kesonia_treasury_deep_review_2026-09-25/02_CALCULATION_AND_CASEBOOK.md` | Read in full. Sections 4-5 establish exposure-time, internal-transfer elimination and the distinction between beta and retention; sections 6 and 8 distinguish risk views and require future validation |
| `docs/research/kesonia/STP_AND_ALM_FTP_SOFTWARE_REVIEW_2026-09-25.md` | Read in full. Sections 2, 4, 5 and 7 distinguish responsibilities, identify durable transaction fields and specify a local proof of concept |
| `output/pricing_treasury_cross_project_review_2026-09-23/source_01_original.txt` | Relevant passages read sequentially: line 18; lines 66-101; lines 135-214. The revolver's drawn interest, undrawn fee and conditional-default EAD are explicit at lines 135-175; the later multi-period exposure example begins at line 175 |
| `output/pricing_treasury_cross_project_review_2026-09-23/source_02_original.txt` | Lines 1-74 read sequentially. FTP and future funding at lines 1-19; deposit observations and the STP chain at lines 20-23; deposit assumptions and EVE examples at lines 24-35; the replication illustration at lines 36-74 |

This reading record identifies the passages used for the operations module. It does not claim that this module reread every later option, capital, insurance and modelling passage in both full pastes. Those broader modules have their own work packages.

## 1. Dated product-level FTP

### Definitions

For each half-open interval `[start, end)`, use actual calendar days divided by 365. Partition at every balance or reset event. Inputs carry both the last rate-reset date and the liquidity/commitment horizon. A reset changes the rate; it does not necessarily release the bank from its remaining funding commitment.

Let `H_D = drawn × days / 365` and `H_U = (limit - drawn) × days / 365`.

| Quantity | Calculation |
|---|---|
| Customer income | `H_D × customer rate + H_U × customer commitment fee` |
| Drawn internal FTP | `H_D × drawn FTP rate` |
| Internal contingent-liquidity allocation | `H_U × internal liquidity rate` |
| External funding expense | `H_D × external drawn rate + H_U × external commitment cost rate` |
| Business-unit margin | Customer income less both internal charges |
| Treasury margin | Both internal charges less both external expenses |
| Consolidated margin | Customer income less external funding expense |

Adding business-unit and Treasury margins eliminates the internal transfers exactly before presentation rounding. Changing an internal FTP rate alone changes departmental attribution without changing consolidated margin. A conditional-default credit conversion factor is not used as the interest-bearing balance or as a universal liquidity-cost weight. Undrawn exposure-time and external contingent-funding cost are stated directly.

The calculation uses `Decimal` for monetary accumulation and rounds only the reported amounts to two decimal places. Displayed interval subtotals can differ by a cent from an independently rounded total. No discounting, credit losses, capital hurdle, tax or operating expense is included. The result is a funding contribution, not full economic profit or an APR. Principal repayments/draws change interval balances; principal is not counted as income.

### Worked year

The examples cover 1 January 2027 to 1 January 2028, with quarter lengths 90, 91, 92 and 92 days. All values are synthetic currency units, interpretable as KES for teaching.

| Product | Customer income | Internal FTP including commitment | Business margin | Treasury margin | Consolidated margin |
|---|---:|---:|---:|---:|---:|
| Fixed 1,000,000 bullet | 150,000.00 | 90,000.00 | 60,000.00 | 10,000.00 | 70,000.00 |
| Amortising 1m / 750k / 500k / 250k | 93,390.41 | 56,034.25 | 37,356.16 | 6,226.03 | 43,582.19 |
| Quarterly floating 1,000,000 | 148,794.52 | 93,794.52 | 55,000.00 | 5,000.00 | 60,000.00 |
| Revolver, actual synthetic path | 104,054.79 | 70,104.11 | 33,950.68 | 7,428.77 | 41,379.45 |
| Revolver, frozen ex-ante path | 88,000.00 | 59,000.00 | 29,000.00 | 8,000.00 | 37,000.00 |

The revolver has a 1m limit and quarter-opening drawings of 400k, 800k, 600k and 900k. Its ex-ante case holds drawings at 600k and initial rates constant. It earns a 1% annual fee on undrawn commitment, allocates 2% internally for contingent liquidity, and incurs a separately assumed 0.75% external commitment cost. The actual-path contribution exceeds plan by 4,379.45, while Treasury's allocated margin falls by 571.23. Those are changes in the explicitly stated paths, not proof of a better pricing policy.

**R02 advancement:** dated fixed/amortising/floating/revolving cases, separate reset and liquidity horizons, contingent funding costs, internal elimination and actual-versus-plan attribution now execute. Remaining: optional draw/prepayment valuation, calibrated funding curves, discounted lifetime economics, transaction accounting and evidenced product conventions.

## 2. Deposit repricing and balance evidence

### Synthetic panel and timing

`synthetic_deposit_panel()` provides two segment-level monthly panels, with opening observations in January 2023 and monthly changes through January 2026. The two names are labels of invented data-generating processes. They are not observed segment statistics or estimates from Kenyan accounts.

Training uses February 2023 through December 2024: 23 monthly changes per segment. Future holdout uses January 2025 through January 2026: 13 changes per segment. The January 2023 opening row is excluded from estimation. A known change in the synthetic immediate upward response begins in January 2025. The model is frozen at the training cutoff and is not refitted on this future segment.

The prespecified one-month distributed-lag equation, in basis points, is:

`change_in_paid_rate = intercept + b_up × max(market_change,0) + b_down × min(market_change,0) + lag_up × max(previous_market_change,0) + lag_down × min(previous_market_change,0) + error`.

Closed-form OLS uses `(X'X)^-1 X'y`, with pivoted elimination and singular-design rejection. A one-month lag is a modelling assumption here; the exercise estimates its coefficient, not the optimal lag length. Fit and validation are segment-specific. The reported standard errors use the simple independent, constant-variance residual formula. They are diagnostic only: real panels require autocorrelation/heteroskedasticity treatment, account/segment dependence, uncertainty assessment and a justified time-series specification.

| Segment | Immediate up beta | One-month up lag | Combined up response | Combined down response |
|---|---:|---:|---:|---:|
| Operating, synthetic | 0.15027 | 0.10202 | 0.25229 | 0.14948 |
| Rate-sensitive, synthetic | 0.50027 | 0.20202 | 0.70229 | 0.54948 |

Training RMSE is approximately 0.121 basis points for each segment. It rises to 4.209 basis points in the deliberately changed holdout regime. This is useful evidence that a good in-sample fit need not survive a change in the repricing process. It does not establish a forecasting result on bank data.

Holdout predictions condition on the market-rate changes observed in those future months. They test the frozen repricing relationship out of time; they are not an ex-ante forecast of the market-rate path itself.

### Balance decay and migration

Each original tagged cohort starts with 1m. Every monthly record separately stores withdrawals leaving the bank, migration to another product at the same bank, new inflows and closing balances.

`original-cohort closing = original-cohort opening - bank withdrawals - same-bank product migration`.

`original-product closing = original-product opening + new inflow - cohort withdrawals - cohort migration`.

The original cohort cannot be replenished by new sales or inflows. Same-bank migration reduces the original product's available funding but is separately visible in the bank-retained cohort. This simple generator keeps migrated funds at the same bank and does not model their subsequent withdrawal or interest expense. It is therefore not a complete bank deposit model.

### A constrained ladder using the observed retention path

The panel's original-product retention fractions at 1, 3, 6 and 12 months are 0.9810, 0.94415, 0.89162 and 0.79573. The ladder uses these *observed synthetic fractions*, not the estimated rate beta, as capacity bounds.

The solver enumerates 5% weight increments at overnight, 3m, 6m and 12m maturity. It maximises the weighted illustrative yield subject to:

- Weights are nonnegative and sum to one.
- At least 20% is available overnight.
- Weighted average maturity is at most six months.
- At each observed horizon, the fraction still locked beyond that horizon does not exceed observed retention multiplied by a stated policy haircut.

With synthetic yields of 4%, 5%, 5.5% and 6%, a 10% retention haircut gives 20% overnight, 60% at six months and 20% at twelve months: 5.3% annualised yield. A tighter 25% haircut requires at least 26.425% overnight from the one-month retention bound; the 5% grid makes that 30%. The resulting optimum is 30% overnight, 40% at six months and 30% at twelve months, yielding 5.2%. The policy assumption and the retention estimate are both visible and separately changeable.

These are terminal maturity rungs, not rolling multi-year bond buckets. The example does not extrapolate a five-year maturity from three years of synthetic data or infer duration from beta. It is an illustrative constrained cash ladder rather than a calibrated replicating portfolio minimising bank-wide NII/EVE error. Regulatory caps, collateral, credit risk, liquidity eligibility, transaction costs, reinvestment and actual execution remain separate work.

**R03 advancement:** segmented asymmetric lag estimation, explicit cohort flows, future validation and a data-constrained ladder now execute on synthetic data. Remaining: empirical longitudinal data, selection/attrition handling, robust uncertainty, competing products, multi-cohort validation, lag/regime selection and validated longer-horizon retention forecasts.

## 3. Durable local STP demonstration

`STPWorkflow(db_path)` models one fixed-deposit placement. It does not represent a swap execution facility or a vendor API. Amounts are integer minor units, and rate is an integer number of basis points. The demonstration's 25m minor units represent a 250,000 KES placement.

The accepted sequence is:

`PROPOSE → APPROVE → ORDER → CONFIRM → BOOK → SETTLE → RECONCILE`.

Approval may instead end at `REJECTED`. A booked placement may record `SETTLEMENT_FAILED`, with no cash journal; a subsequent settlement requires a new event ID and a reference to that failure. The worked case includes this failed-and-retried route.

| Control | Executable behaviour |
|---|---|
| Durable identity | SQLite event IDs; proposal/order/trade/confirmation/settlement IDs persist between process restarts |
| Frozen economics | Confirmation must equal approved currency, amount, dates, rate, instrument, counterparty and evidence versions, and match the order ID |
| Role separation | Proposer, approver, dealer, backoffice and reconciler are distinct mapped roles; a proposer cannot approve their own proposal even if their configured role later changes |
| Idempotency | Replaying the same event, actor, kind and payload returns the stored result; reusing its ID with changed content fails |
| Transaction boundary | Event, state projection and journal commit in one SQLite transaction; failed validation rolls back |
| Settlement | Cash amount must equal the approved full placement; a failed attempt produces no cash posting |
| Reconciliation | External cash and position totals must match the placement; the journal must match independent reconstruction from accepted events |

The booking entries are debit placement asset and credit settlement payable. Settlement debits settlement payable and credits cash. For the 250,000 KES example, the incremental minor-unit ledger records `placement_asset +25,000,000`, `settlement_payable 0`, and `cash -25,000,000`. These are changes attributable to this placement, not the bank's opening or closing cash balance. The external `bank_cash_cents` field is its signed statement movement for this transaction. The four journal lines sum to zero, and their accounts and amounts must also match the accepted event history. A test deliberately doubles every journal amount: the trial balance remains zero but the event reconstruction correctly rejects it.

Eight accepted events, including the failed settlement, produce four journal lines. Reopening the SQLite file and replaying the successful settlement leaves these counts unchanged. Invalid role, self-approval, rejected proposal, changed terms, wrong amount and wrong retry-reference cases are tested.

Actor names are supplied by the local application and are **not authenticated identities**. Database access is not tamper-proof. Rejected API attempts are rolled back rather than retained in a separate security audit log. The simulation has no external acknowledgement polling, partial fills, cancellation/amendment lifecycle, real settlement bridge, collateral engine or accrued-interest postings. Those features require their own interface, authority and accounting specifications.

**R09 advancement:** a durable, tested local reference chain now demonstrates identifiers, approval, confirmation, booking, failed settlement, restart, duplicate protection and reconciliation. Live interfaces, actual product eligibility and institutional acceptance remain unverified.

## 4. Verification and integration

Install `operations.py` in `research_lab/` and `test_operations.py` in `tests/`. The module depends only on the Python standard library. `operations_examples()` returns JSON-ready results for a shared build; it uses a temporary SQLite database for its demonstration. Direct use of `STPWorkflow` accepts an explicit durable database path.

From the repository root, run:

```text
python -m unittest discover -s tests -p test_operations.py -v
```

Tests independently check a full-year funding identity, amortising exposure-days, changing-rate expenses, leap-year days, pure transfer-price invariance, known OLS coefficient recovery, future-data separation, balance identities, constrained ladder bounds, restart safety and independently reconstructed accounting entries. These checks establish the stated calculations and control behaviours; they do not make the source financial material fully validated or complete every item in the remaining-work register.
