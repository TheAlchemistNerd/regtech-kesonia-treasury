# Hedge accounting and connected financing cases

**Edition: 1 October 2026.** Reproduce with `python -m research_lab.run_examples`. Machine-readable output is in `research_lab/results/checked_examples.json`, under `accounting` and `connected`. All amounts below are synthetic KES. Designation eligibility, actual fair values, legal transfer and distribution permissions require evidence from the relevant owner.

## 1. Fair-value hedge and subsequent amortisation

The example elects an amortised-cost asset with two remaining annual receipts: 50 and 1,050. Its carrying amount before the benchmark change is 1,000. A benchmark-only revaluation from 5% to 6% gives:

```text
adjusted carrying amount = 50 / 1.06 + 1,050 / 1.06^2 = 981.666073
hedged-item loss = 1,000 - adjusted carrying amount = 18.333927
derivative gain = 18.000000 (supplied valuation input)
net hedge ineffectiveness = 18.000000 - 18.333927 = -0.333927
```

The asset loss and derivative gain enter profit or loss separately. The journal record uses positive debits and negative credits; each event balances to zero. Derivative settlement exchanges an 18 derivative asset for 18 cash. On discontinuation, the asset adjustment remains in its carrying amount and is amortised using the recalculated 6% effective interest rate (EIR). The two-year roll-forward reaches zero after receipt of the contractual 1,100 total. The calculation measures the adjustment and amortisation; it assumes the hedge was properly designated and qualified.

| Event | Debit | Credit |
|---|---|---|
| Asset benchmark remeasurement | Hedge loss 18.333927 | Asset carrying adjustment 18.333927 |
| Derivative remeasurement | Derivative asset 18 | Hedge gain 18 |
| Derivative settlement | Cash 18 | Derivative asset 18 |
| Subsequent effective-interest recognition | Asset carrying amount: opening balance × 6% | Interest income: same amount |
| Subsequent coupon/principal receipt | Cash: 50 then 1,050 | Asset carrying amount: same amounts |

## 2. Cash-flow hedge: cumulative reserve and cash reconciliation

The designated instrument's supplied cumulative gains are 12, 17 and 20. The corresponding hypothetical hedged-item changes are -10, -16 and -19. The fixture keeps the same designation throughout this measurement sequence.

| Date | Derivative cumulative gain | Opposing item change | Cumulative OCI reserve | Cumulative ineffectiveness gain | Period ineffectiveness gain |
|---|---|---|---|---|---|
| 31 March 2027 | 12 | -10 | 10 | 2 | 2 |
| 30 June 2027 | 17 | -16 | 16 | 1 | -1 |
| 30 September 2027 | 20 | -19 | 19 | 1 | 0 |

OCI means other comprehensive income. The reserve is capped using the smaller absolute cumulative change, retaining the instrument's sign. The period journal uses differences between cumulative balances. Applying a fresh period-by-period minimum would give the wrong answer when prior ineffectiveness reverses.

At settlement, the borrower pays contractual interest of 100 and receives derivative cash of 20. Reclassifying 19 from the reserve reduces interest expense to 81. The separately recognised ineffectiveness gain of 1 gives total profit-or-loss cost of 80, matching net cash paid of 80. The reserve and derivative finish at zero. Underhedging is also tested: an instrument gain of 8 against an item loss of 10 creates a reserve of 8 without inventing an extra accounting loss of 2.

## 3. Rebalancing and discontinuation

The separate control example records designation D1 with 1,000 hedged units and 1,000 hedge units. An unchanged risk objective and completed effectiveness review permit a prospective version with 900 hedge units. Original quantities and prior ineffectiveness stay in the history. A changed objective fails this rebalancing gate. The fixture does not infer later fair values merely by changing the ratio; a new valuation is required.

At June discontinuation, the accumulated reserve is 16. If the forecast cash flows remain expected, it is retained for the appropriate later recognition. If they are no longer expected, 16 is reclassified immediately. These two branches are calculated independently of the completed September hedge; they are alternative histories, not extra journals added to it.

The measurement principles are checked against IFRS 9 §§6.4.1, 6.5.5–6.5.12 through the [New Zealand standard setter's published IFRS 9 text](https://standards.xrb.govt.nz/standards-navigator/nz-ifrs-9/?version=213). This is access to the accounting text, not a claim that New Zealand jurisdiction determines a Kenyan institution's obligations. Instrument eligibility, economic relationship, credit-risk dominance, documentation, hypothetical-derivative construction and approval remain inputs to a qualified accounting implementation.

## 4. A common borrower, originator, SPV and investor cash case

The borrower reuses Underwrite for Collection's on-time 60-day case: opening cash 250,000; operating receipts 1,000,000; operating payments 820,000; loan draw 500,000; upfront fee 10,000; final debt payment 515,000. Closing borrower cash is 405,000 and financing cost is 25,000. Every transfer has a payer, recipient, date and unique event identifier.

To demonstrate a claim transfer, the bank originates the 500,000 loan and an illustrative SPV buys it at par on the same date. These are new interface assumptions. The originator retains its 10,000 fee; the SPV receives the loan's 15,000 interest. An assumed 75/15/10 asset funding split supplies 375,000, 75,000 and 50,000. Class C supplies an additional 10,000 to fund the closing reserve. Thus the 510,000 cash raised funds both purchase and reserve. This small fixture does not replace Mwendo's complete waterfall or establish legal/accounting sale treatment.

On 30 November, the SPV's 515,000 collection plus 10,000 reserve pays, in order:

| Use of cash | KES |
|---|---:|
| Servicing | 2,000 |
| Class A coupon | 6,000 |
| Class B coupon | 1,500 |
| Class A principal | 375,000 |
| Class B principal | 75,000 |
| Class C asset principal | 50,000 |
| Final reserve release and residual to C | 15,500 |
| Total | 525,000 |

Class C receives 65,500 on its total 60,000 investment. Only 5,500 is residual profit before investor tax; returned capital and released reserve are not profit. The SPV closes with no assets, claims or cash in this successful termination case. Failure, trigger, delayed recovery and persistent arrears cases remain in Mwendo's canonical engine and its versioned evidence snapshot.

The originator incurs 8,000 operating cost and an assumed 600 tax on its 2,000 fee contribution. Its 1,400 profit supports 600 retention and a permitted 800 parent remittance on 15 December. The loan interest belongs to the SPV after the assumed transfer; adding it to the bank's fee again would overstate originator income. Borrower cost reconciles exactly to originator fee plus SPV loan interest.

## 5. Accepted refund, received cash and owner endpoints

The separate insurance interface assumes a 1,200 premium, twelve-month service period and elected pro-rata cancellation after three months. An accepted 900 refund on 31 March creates a right/payable, with zero SPV cash at that date. Settlement on 15 April extinguishes that right, transfers 900 cash and reduces a 1,000 loan to 100. Counting acceptance and settlement as two recoveries would fail this reconciliation. The illustrative service allocation of 300 is not asserted to be IFRS 17 insurance revenue. Contract groups, remaining/incurred coverage liabilities, onerous measurement, claims and insurer journals remain with the insurance accounting owner.

The owner example separately reconciles 1,590,000 reported benefit less replacement labour 300,000, maintenance 180,000 and required working capital 120,000 to earning power of 990,000. Today's 200,000 unrestricted cash less 80,000 near-term claims and 100,000 buffer permits only 20,000 distribution. Neither endpoint is silently relabelled as the other.

At the bank parent, 100 opening cash cannot meet a 300 obligation on 1 December. The 800 remittance on 15 December arrives later. A temporary 200 bridge is needed; after receiving the remittance and repaying that bridge, parent cash is 600. Costs and tax already deducted in the bank are not charged again to the net remittance.

## 6. Typed handoff and SokoIntel candidate

`EconomicQuantity` requires a finite Decimal value, unit, currency, legal entity, claim, period, scenario and source version. Addition requires all dimensions to match. Missing information fails validation; it is not converted to zero. The transfer ledger rejects overdrafts, out-of-order new events, unknown entities and changed payloads under reused identifiers; an exact duplicate has no second cash effect.

These are executable candidate contracts and acceptance fixtures for SokoIntel. The guest project was not edited and no SokoIntel runtime was certified. RegTech preserves a dated snapshot of the owning-project evidence so that the examples run independently of another user's Downloads folders.

| Symbol or field | Meaning and unit |
|---|---|
| KES | Kenya shillings; all money in this chapter |
| EIR | Annual effective interest rate; 0.06 in the fair-value amortisation fixture |
| FV | Fair value, in currency |
| OCI / P&L | Other comprehensive income / profit or loss; accounting presentation categories |
| D1 | Designation version identifier; not a discount factor |
| `derivative`, `reserve`, `ineffectiveness` | Cumulative instrument value change, effective OCI amount and residual gain; KES with explicit signs |
| `signed_debits` | Positive debit and negative credit amounts; sum zero for each journal |
| `event_id` | Unique transfer identifier whose payload is immutable |
| 75/15/10 | Percentage allocation of the 500,000 asset purchase; excludes separately funded reserve |
| `cash_residual` | Sum of entity cash after a transfer less the sum before it; KES, required zero |

**Implementation:** `accounting_cases.py` and `connected_cases.py`; tests in the corresponding test modules. Full contract-group IFRS 17, empirical loss models, live cash execution and institution-approved distribution rules remain separate completion requirements.
