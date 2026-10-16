# Lifecycle cases: balances, corrections, evidence and partial settlement

**Edition:** 1 October 2026. **Case:** KESONIA-LIFECYCLE-001. **Inputs:** synthetic. **Currency:** Kenya shillings, KES. All annual rates are decimals in the executable inputs.

This companion implements four accumulated review requirements: a dated principal-change calculation; a corrected fixing carried through an approved adjustment ledger; a recovery-evidence decision gate; and partial execution/settlement with durable event identity. The existing benchmark, funding and SQLite workflow examples provide the starting interfaces.

## 1. State the contract before changing the balance

The case elects a **benchmark-index account with a simple margin on funded principal**. Cash invested or withdrawn at an event date changes the principal and benchmark-account value by the same amount. Benchmark return remains in that account; the simple margin is recorded separately. The contract permits withdrawal of funded principal only. Settling accrued return or closing the account requires a further settlement event outside this profile.

This explicit hypothetical convention makes the balance-event mechanics reproducible. Applying it to a customer loan requires that loan's actual balance/accrual terms. The case does not establish a general right to capitalise unpaid customer interest. The existing constant-principal calculator remains available for its stated profile.

### Elected terms

| Term | Value or rule |
|---|---|
| Period | 1 September 2025 included to 8 September 2025 excluded |
| Opening principal | KES 1,000,000 |
| Principal events | Add KES 200,000 at the start of 3 September; withdraw KES 300,000 at the start of 6 September |
| Benchmark observations | Synthetic annual rates of 8%, 9%, 10%, 11% and 12% for 1–5 September; the Friday fixing spans the weekend |
| Benchmark floor/cap | Applied to each selected fixing: minimum 0%, maximum 20%; these limits are assumed contract terms |
| Day count | Actual calendar days divided by 365 |
| Observation mapping | Zero-lookback illustration; the function also accepts an explicit nonnegative business-day lookback and calendar |
| Margin | 3% initially, then 4% from 4 September under a scheduled reset authorised before that effective date |
| Contract timezone | UTC; each date-only effective event starts at 00:00 UTC |
| Reset permission | Authority identifier and matching contract version required by 00:00 UTC on the effective date; exact-midnight approval is permitted, later approval is rejected |
| Principal-event order | Effective at the start of a subinterval, before that subinterval earns return |
| Rounding | Decimal arithmetic at 40 significant digits; cash output rounded once to two decimal places, half up |

Observation-shift, a compounded customer margin, interest-payment allocation and alternative floor placement are separate contractual profiles. The function rejects an unsupported margin or balance convention. The illustrative zero-lookback fixture does not resolve the final CBK framework's five-day operating map for a live product.

### Mathematics and all symbols

| Symbol | Meaning | Unit |
|---|---|---|
| $a$ | Start date of one original fixing span | Calendar date |
| $s,e$ | Start and end dates of an event-created subinterval within that span | Calendar dates; $s$ included, $e$ excluded |
| $r$ | Selected annual decimal fixing after its elected floor/cap | Annual rate |
| $b$ | Day-count denominator, 365 here | Days per year |
| $J(t)$ | Benchmark index level at date $t$, relative to the start of the fixing span | Dimensionless |
| $g_{s,e}$ | Growth factor over the subinterval | Dimensionless |
| $P_s$ | Funded principal after start-of-subinterval principal events | KES |
| $V_s$ | Benchmark-account value after those events, including previously retained benchmark return | KES |
| $c_s$ | Signed principal addition at $s$; negative for a principal withdrawal | KES |
| $k_s$ | Authorised simple annual margin applicable from $s$ | Annual rate |
| $I^b_{s,e}$ | Benchmark return earned in the subinterval | KES |
| $I^m_{s,e}$ | Separately accrued simple margin in the subinterval | KES |
| $V_T,P_0$ | Terminal benchmark-account value and original funded principal | KES |
| $I^b$ | Total benchmark return for the case | KES |

Within one original fixing span, the index is interpolated according to that span's simple day weighting:

$$\frac{J(t)}{J(a)}=1+r\frac{t-a}{b},\qquad
g_{s,e}=\frac{1+r(e-a)/b}{1+r(s-a)/b}.$$

The date differences count actual calendar days. Principal events first update both funded principal and benchmark-account value by $c_s$. Then:

$$I^b_{s,e}=V_s(g_{s,e}-1),\qquad V_e=V_sg_{s,e},\qquad
I^m_{s,e}=P_sk_s\frac{e-s}{b}.$$

The benchmark return reconciles to:

$$I^b=V_T-P_0-\sum_s c_s.$$

Using index ratios is important when an event splits a weekend. A Friday-to-Monday fixing weighted for three days remains the same underlying factor. Merely inserting a zero-amount Saturday event does not turn it into extra daily compounding. An independent test also values the mid-span principal withdrawal by the benchmark-index units sold on the withdrawal date.

### Calculated original ledger

The table rounds each displayed increment for readability; the final total uses unrounded increments.

| Accrual dates | Funded principal, KES | Applied fixing | Margin | Benchmark increment, KES | Margin increment, KES |
|---|---:|---:|---:|---:|---:|
| 1–2 September | 1,000,000 | 8% | 3% | 219.18 | 82.19 |
| 2–3 September | 1,000,000 | 9% | 3% | 246.63 | 82.19 |
| 3–4 September | 1,200,000 | 10% | 3% | 328.89 | 98.63 |
| 4–5 September | 1,200,000 | 11% | 4% | 361.88 | 131.51 |
| 5–6 September | 1,200,000 | 12% | 4% | 394.90 | 131.51 |
| 6–8 September | 900,000 | 12% | 4% | 592.61 | 197.26 |

The case closes with KES 900,000 funded principal, KES 2,144.092488402175 benchmark return, and KES 723.287671232877 simple margin. Total interest is **KES 2,867.38** after cash rounding. Closing benchmark-account value is KES 902,144.092488402175; the separate margin is not included in that value.

## 2. A fixing correction becomes an approved adjustment

At the original 8 September information cutoff, the Friday fixing is 12%. A corrected 13% version becomes available on 9 September. The contract, principal events, margin schedule and cash-rounding policy are unchanged.

| Calculation/posting | Interest, KES | Result |
|---|---:|---|
| Original cutoff | 2,867.38 | Original result and evidence retained |
| Revised cutoff | 2,949.68 | Corrected fixing version, later cutoff and new result hash |
| Approved adjustment | 82.30 | Revised rounded amount less the already posted rounded amount |
| Posted accrual after adjustment | 2,949.68 | Original posting plus one adjustment |

`correction_case()` produces the proposal and two linked result hashes. `AccrualPostingBook` separately requires a maker/checker approval bound to the exact calculation JSON before recording a posting. Its durable ledger retains the original event and adjustment. The correction must identify the current predecessor and a later information cutoff. Replaying the same posting returns its original receipt; a new message identity cannot justify reposting the same calculation.

The cash adjustment uses the difference between the two **rounded posted amounts**. Independently rounding the change in unrounded values can differ by a cent. The output therefore retains both the unrounded change and the posting delta. A fixing-only correction also requires an unchanged contract-and-event hash, so an altered margin cannot be presented as a source correction.

This demonstrates a local accrual-control ledger. Institution-specific accounts, tax, recognition dates, customer notices and approved general-ledger mappings remain inputs to the operational implementation.

## 3. Recovery evidence has a verification clock

The evidence fixture deliberately holds borrower default probability and contract terms outside the gate. It tests whether new recovery evidence may enter an analytical review.

| Information cutoff | Source situation | Last verified recovery fraction | Gate result |
|---|---|---:|---|
| 1 September, 12:00 | Original rights confirmed and verified | 60% | Confirmed; eligible for analytical refresh |
| 2 September, 12:00 | Source unavailable | 60% | Request evidence; no new analytical assumption |
| 3 September, 12:00 | Changed evidence received, verification pending | 60% | Review pending |
| 4 September, 12:00 | Changed rights verified | 30% | Review verified change; analytical refresh allowed |

Evidence timestamps use Africa/Nairobi's stated UTC+03:00 offset in this fixture. The date-only accrual contract uses UTC, and reset authority is compared as a full timezone-aware instant against 00:00 UTC on its effective date. An approval later on that date cannot authorise the earlier interval. Each evidence record preserves economic effective time, availability time, verification time, source-result version and review owner. The age limit is an elected five-day policy parameter. Source failure does not refresh the verification date or prove deterioration. A known but stale record cannot authorise an analytical refresh.

The gate returns `contract_change_authorised = false` and `borrower_pd_changed_by_this_gate = false`. The purpose is to route a verified recovery change for the appropriate review. The existing Underwrite decision case supplies the broader borrower-authority and agreed-action workflow; this RegTech fixture is its narrow recovery-assumption interface.

## 4. Partial execution and partial settlement are separate

The durable `PartialSettlementBook` extends an already approved order handoff. It stores monetary fields as **integer minor units**; 100 minor units equal KES 1 in this case. Each persisted book fixes one currency and instrument claim. The default case is KES synthetic deposit placements. Orders for another currency or instrument are rejected; restarting a book with a different scope is also rejected. Every aggregate output carries the book currency and instrument.

| Event | Position, KES | Cash paid, KES | Unsettled payable, KES | Live unfilled order, KES |
|---|---:|---:|---:|---:|
| Approved order for KES 10,000; acknowledgement unknown | 0 | 0 | 0 | 10,000 |
| Confirmed partial fill of KES 6,000 | 6,000 | 0 | 6,000 | 4,000 |
| First settlement of KES 2,000 | 6,000 | 2,000 | 4,000 | 4,000 |
| Cancellation of the unfilled quantity confirmed | 6,000 | 2,000 | 4,000 | 0 |
| Final settlement of KES 4,000 | 6,000 | 6,000 | 0 | 0 |

Here a position is the booked synthetic placement asset, a payable is confirmed but unpaid settlement cash, and live unfilled quantity is an instruction that can still execute. Cancellation removes the latter. It does not erase the asset or settlement obligation created by an existing fill.

The invariant is **position + signed cash change − settlement payable = 0**. The first partial settlement therefore reconciles as KES 6,000 − 2,000 − 4,000 = 0. The code rejects cumulative settlement above the confirmed fill and rejects a repeated settlement business ID even when it arrives under a different event ID. Restarting SQLite and retrying the final event creates no second cash posting.

### Additional failure and amendment tests

- Unknown external acknowledgement never creates authority to send a second economic order. A repeated event returns the existing record. A confirmed fill can establish that execution happened despite the earlier missing acknowledgement.
- Every order/quantity amendment needs independent maker/checker identities and an approval tied to the exact terms. Reusing an approval identity for changed terms fails.
- The amendment fixture changes unfilled quantity only. It cannot reduce the total below confirmed fills or modify a cancelled order. A fill referencing pre-amendment terms is rejected.
- Increasing a fully filled order restores the partially filled state and exposes the new unfilled capacity; the confirmed position and payable remain unchanged until further fill/settlement events.
- Confirmed cancellation needs authority for the exact cancellation action and external cancellation evidence. Existing fills remain settleable.
- Money in floating units, booleans, nonpositive amounts, overfills, oversettlements and changed-content retries fail before durable economic effects are recorded.

The adapters are local mocks. Real authentication, external status queries, venue message mapping, matching tolerances, accrued interest on the placement, legal settlement finality and recovery operations require the chosen institution's interfaces.

## 5. Reproduction and review traceability

The calculations and SQLite examples use the Python standard library and the existing benchmark module:

```powershell
python -m unittest discover -s tests -p test_lifecycle_cases.py -v
python -c "import json; from research_lab.lifecycle_cases import lifecycle_examples; print(json.dumps(lifecycle_examples(), indent=2))"
```

| Accumulated requirement | Implemented artifact | Verification |
|---|---|---|
| Part 2 principal changes, caps/floors and explicit margin/reset conventions | `accrue_account`, `AccountProfile`, dated events | Existing constant-principal reference; independent index-units withdrawal; split-span invariance; permission and interval rejection |
| Part 4 original/corrected calculation and adjustment replay | `correction_case`, `AccrualPostingBook` | Same contract/events, exact-result approval, rounded reconciliation, predecessor order and restart-safe duplicate handling |
| Cross-project XB04 evidence freshness and recovery readiness | `freshness_gate` | No future verification leakage; outage preserves last verified state; stale/changed/no-change paths |
| R09 and Case F partial execution/settlement, unknown acknowledgements and amendments | `PartialSettlementBook` | Cumulative cash/position/payable invariants; cancellation retains confirmed obligations; approval/terms identity; restart/replay |

The 22 lifecycle tests close these elected reference fixtures, including timezone-aware reset-authority checks at the UTC day boundary. Institutional contract interpretation, production authentication, whole-system concurrency and live vendor/ledger acceptance retain their separate completion evidence.
