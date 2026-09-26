# Working formulations and reusable examples

These formulations provide one consistent basis for borrowing useful material from both pastes. They are teaching and design conventions; actual contracts, measurement objectives and approved policies determine implementation. Examples were independently recalculated in [verify_examples.py](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/pricing_treasury_cross_project_review_2026-09-23/verify_examples.py>), with outputs in [verified_examples.json](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/pricing_treasury_cross_project_review_2026-09-23/verified_examples.json>).

## 1. Use a financial-quantity dictionary

| Quantity | Working meaning | Owner/use |
|---|---|---|
| Customer benchmark and premium | Contractual reference rate plus the approved lending premium; fees and charges shown separately | Lender/Product, contract and disclosure |
| FTP | Internal attribution of funding, liquidity, repricing and option costs or benefits | Treasury and business-unit economics |
| Expected credit loss | Expected loss under the specified horizon, probability measure, exposure and recovery convention | Pricing or research; IFRS 9 has its own measurement rules |
| Economic capital | Allocated adverse-loss capacity under a stated internal method | Risk and capital management |
| Regulatory capital | Requirement under the applicable entity, jurisdiction, method and approvals | Prudential reporting |
| Available cash | Settled funds available to the identified entity after restrictions | Treasury/operations |
| SPV note margin | Investor funding term for a particular note | Transaction parties |
| Insurance pure premium | Expected insured claim cost per stated exposure basis | Actuarial pricing |
| Insurance liability | Accounting measurement for the relevant contract group and service/incurred-claim obligation | Insurer Finance |

A shared source event can feed several quantities without making them interchangeable. This is already the direction of the controlled architecture and the stronger manuscript sections.

## 2. Price a loan in money before converting to a spread

For an introductory one-period case define:

\[
RAROC=\frac{I+F-C_{fund}-C_{op}-EL}{EC}.
\]

All numerator terms use the same period and currency. State whether income is contractual or expected to be collected, whether the measure is before tax, and how EC is allocated. Economic profit adds the hurdle explicitly:

\[
EP=I+F-C_{fund}-C_{op}-EL-hEC.
\]

Where interest is linear in rate, a simple required-rate illustration is

\[
r_{required}=\frac{C_{fund}+C_{op}+EL+hEC-F}{B_{interest}\Delta t}.
\]

Here the denominator is the defined interest-earning balance-time amount. If default, prepayment or interest collection makes it uncertain, solve the expected cash-flow model instead. The premium then reconciles to this required return after accounting for the contractual benchmark and approved adjustments. Funding and liquidity costs already included in FTP enter once.

CBK's RBCPM formulation is KESONIA plus K, with lending costs, shareholder return and borrower risk within the premium and fees/charges separately disclosed. It does not prescribe the above internal RAROC formula. [CBK, April 2026 MPC report, p.20](https://www.centralbank.go.ke/uploads/monetary_policy_reports/131378250_36th%20Monetary%20Policy%20Committee%20Report%2C%20April%202026.pdf).

### Teaching case A: exposure and loss protection

Common assumptions: KES 10m exposure, KES 1.5m revenue, KES 0.9m funding, KES 0.1m operating expense and 5% PD.

| Scenario | Assumed LGD | EL, KES | Contribution, KES | Assumed EC, KES | RAROC |
|---|---:|---:|---:|---:|---:|
| Unsecured | 70% | 350,000 | 150,000 | 1,500,000 | 10.00% |
| Secured | 20% | 100,000 | 400,000 | 600,000 | 66.67% |
| Illustrative mixed LGD | 45% | 225,000 | 275,000 | 900,000 | 30.56% |

The capital amounts are separate assumptions, not derived benefits of collateral. The 45% LGD is a mixture for exposition; a guarantee requires its actual loss-sharing terms. A richer case deducts protection fees and claim costs, projects settlement delay and models provider non-performance. Economic loss transfer, immediate liquidity and regulatory recognition are assessed separately. IFRS 9 treatment also depends on whether a credit enhancement is part of the contractual terms and separately recognised. [IFRIC, March 2019](https://www.ifrs.org/news-and-events/updates/ifric/2019/ifric-update-march-2019/).

### Teaching case B: a revolving commitment

Assume KES 4m drawn, KES 10m limit, CCF 56.4%, PD 6%, LGD 45%, interest 16% on drawn balance, commitment fee 1% on undrawn balance, funding 9% on drawn balance, operating cost KES 120,000 and EC 12% of EAD.

\[
EAD=4m+0.564(6m)=7.384m.
\]

EL is KES 199,368; annual illustrative revenue KES 700,000; contribution KES 20,632; EC KES 886,080; RAROC **2.33%**. The useful lesson is that a quoted loan rate and return on committed risk can tell different stories. The next version should model average drawn balances, future drawings, contingent liquidity cost and fees through time rather than freeze them for a year.

## 3. Join default timing to loss and cash

For a single first-default process without competing exits, conditional hazard \(h_m\), survival \(S_m\) and unconditional interval default probability \(q_m\) satisfy

\[
S_m=\prod_{j=1}^{m}(1-h_j),\qquad q_m=S_{m-1}h_m,
\qquad PD(1{:}H)=\sum_{m=1}^{H}q_m.
\]

With prepayment or other competing exits, survival must reflect all relevant exit hazards and the target event definition. A multi-state model additionally allows delinquency, cure and recurrence where required. First default may be absorbing for a first-event analysis while the servicing account continues to evolve.

A useful research loss expression is

\[
EL_t(H)=\sum_{m=1}^{H}q_{t,m}\,
E[DF_{t,m}EAD_{t,m}LGD_{t,m}\mid T_D\in m,\mathcal I_t].
\]

Keep the expectation of the product where exposure and severity co-vary. If LGD discounts recovery cash to default, discount from default to valuation once more as required; do not duplicate the same discount period. For IFRS 9, reconcile to applicable probability-weighted discounted cash shortfalls, staging, scenarios and effective-interest conventions. Twelve-month ECL concerns defaults possible in that horizon and their resulting losses, not simply cash shortfalls paid within twelve months. [IASB impairment review](https://www.ifrs.org/content/dam/ifrs/project/pir-9-impairment/rfi-iasb-2023-1-ifrs9-impairment.pdf).

For vintage displays, compare matched ages, follow-up and denominators. Record current delinquency, cumulative first entry, durable cure, recurrence, prepayment and terminal exits separately. Aggregate subtraction does not identify a cure transition.

### Teaching case C: transition matrices

Using the pricing paste's five-grade annual transition matrix and starting balances of KES 7bn, 5bn, 2bn, 1bn and zero, the three-step fixed-exposure result is:

| Grade | Year-three amount, KES bn |
|---|---:|
| 1 | 4.9387140 |
| 2 | 3.7463156 |
| 3 | 2.9506796 |
| 4 | 1.5525222 |
| Default | 1.8117686 |
| Total | 15.0000000 |

This demonstrates matrix propagation only. Amounts are allocations of the initial fixed balance, not a forecast of a real amortising loan book. A cash model introduces balance changes and observation/exit rules explicitly.

## 4. Separate benchmark accrual from curves and funding

For a specified overnight convention,

\[
G_{a,b}=\prod_i(1+r_i n_i/365),\qquad
R_{a,b}^{ann}=(G_{a,b}-1)365/d.
\]

The annualised realised period rate is not a forward yield curve or an all-in borrower APR. Observation date, publication availability, calendar weight, lookback or shift, rounding and fallback must match the contract. Index-ratio implementations must match those same conventions. CBK publishes the rate for the preceding business day's activity and supplies a compounded index. [CBK KESONIA](https://www.centralbank.go.ke/kesonia/).

| Curve | Useful interpretation |
|---|---|
| Par | Coupon making the specified instrument worth par under its conventions |
| Zero/spot | Discounting a cash flow at a specified maturity |
| Forward | Rate implied between dates by the chosen curve and compounding convention |
| Projection | Forecast index cash flows under the valuation framework |
| Discount | Present value under the currency/collateral/valuation convention |
| Funding/FTP | Institution-specific cost or benefit of funds, term, liquidity and options |
| Credit/basis | Spread relative to a specified reference, with instrument and risk meaning stated |

For annual compounding, \(1+f_{1,2}=(1+z_2)^2/(1+z_1)\). With spot rates 3%, 3.5% and 4% at years 1–3, implied one-year forwards are **4.002427%** and **5.007258%**. These are mathematical implications of the supplied curve, not predictions guaranteed to occur.

## 5. Behavioural funding, EVE and option ownership

Estimate deposit-rate pass-through and deposit-balance persistence separately. A replication ladder is an analytical allocation with actual rung dates and rollover rules; it does not make withdrawable deposits permanent funding.

For a 20%/30%/50% ladder in 3-month/2-year/5-year instruments at 3%/3.75%/4.5%, initial yield is **3.975%**. Under a 200bp parallel increase and evenly staggered monthly maturities, the month-one repriced fractions are 1/3, 1/24 and 1/60 of the respective buckets; the illustration gives **4.150%**. Different maturity schedules produce different first-month results.

With modified durations and a small parallel shock,

\[
\Delta EVE\approx(-D_A A+D_L L)\Delta y.
\]

For assets KES 10bn at duration 5, liabilities KES 9bn and a 200bp rise, liability duration 4 gives **−KES 280m**; duration 1.5 gives **−KES 730m**. This is an economic-value approximation, not immediate cash loss or an automatic accounting-capital charge. Full scenarios should include changing cash flows, non-parallel moves and options. Earnings and economic-value analysis are complementary. [BIS IRRBB application guidance](https://www.bis.org/committees/bcbs/basel-framework/standard/srp/98/inforce/2019-12-15/published/2019-12-15).

For OAS, use a model-consistent joint treatment of scenario cash flows and discount factors. Identify the option holder, exercise assumptions and calibration. For liquidity, retain separate views of available cash, LCR stress, structural funding and margin calls; a loss hedge can still require cash at an inconvenient time.

## 6. Carry project and SPV cash through an explicit waterfall

\[
DSCR_m=CFADS_m/DS_m,\qquad
LLCR_t=PV_t(CFADS\text{ over loan life})/Debt_t.
\]

Define CFADS from the actual project: operating receipts less relevant operating cash outflows, tax, working-capital investment and capital needs under the chosen covenant. A reserve drawing is a financing source, not additional operating CFADS. The covenant can define a separate supported debt-service measure.

For an SPV, the reusable sequence is:

**eligible receivables → controlled collections → fees/expenses → note interest/principal and reserve rules → residual distributions**, with actual ordering set by the documents. Add revolving versus amortising modes, cure periods, servicing interruption and recovery/refund delays. Legal transfer, accounting derecognition, consolidation and regulatory capital treatment require distinct assessments. The CMA's ABS guidance is a starting point for true-sale and enforceability questions, not a transaction opinion. [CMA ABS guidance](https://cma.or.ke/wp-content/uploads/2023/03/Policy-Guidance-Note-on-Asset-Backed-Securities-2017.pdf).

A useful reverse stress question is: which combination of delayed collections, increased drawings, weaker recoveries and funding shocks first breaches the specified cash, reserve, OC or note-payment constraint? Compare incremental losses and funding needs consistently with starting provisions, earnings and capital.

## 7. Preserve advanced valuation and capital as separate modules

A simplified unilateral CVA approximation is

\[
CVA\approx(1-R)\sum_m DF_m EE_m\Delta PD_m.
\]

Here EE is undiscounted expected positive exposure and \(\Delta PD\) is a marginal default probability under the valuation setup. The simplified factorisation requires assumptions about exposure/default dependence. Netting, collateral and wrong-way risk require richer treatment.

- Constant case: exposure KES 70m, default probability 1.5%, LGD 60%, no discounting → **KES 630,000**.
- Three-interval case: discount factors 0.95/0.90/0.85, exposures 5m/3.5m/1.5m and marginal PDs 1%/1.5%/2%, LGD 60% → **KES 72,150**.
- Specified stress exposures 12m/8m/4m and marginal PDs 6%/8%/10% with the same discount factors/LGD → **KES 960,000**.

Counterparty exposure, CVA valuation and CVA capital are separate outputs. SA-CCR uses a prescribed exposure framework; SA-CVA has eligibility and capital rules. Build full rule-versioned modules only if these become an approved product scope. [BIS CRE guidance](https://www.bis.org/committees/bcbs/basel-framework/standard/cre?allChapters=true&chapter=50), [BIS MAR50](https://www.bis.org/committees/bcbs/basel-framework/standard/mar/50/inforce/2023-01-01/published/2020-07-08).

For the Basel IRB notation used in the source, the capital fraction \(K_{cap}\) maps to \(RWA=12.5K_{cap}EAD\); the baseline 8% of those RWA is \(K_{cap}EAD\). Domestic applicability, floors and buffers remain additional considerations. Use a different symbol from the customer premium K. [BIS CRE31](https://www.bis.org/basel_framework/chapter/CRE/31.htm?inforce=20230101&published=20200327).

Structural compound-option models remain useful for a dedicated appendix. State the payoff and maturity structure before choosing the bivariate-normal expression; normal CDFs represent probabilities. Validate exercise boundaries, limiting cases and monotonicity before solving implied volatility. A model under a valuation measure does not directly provide a real-world SME default probability.

## 8. Connect insurance usage, accounting and cash rights

Use an event ledger with different destinations:

| Event | Useful interpretation |
|---|---|
| Usage recorded | Exposure evidence for insurance risk and potentially premium calculation |
| Premium billed/received | Contractual amount and actual cash, separately |
| Coverage provided | Insurance service relevant to revenue measurement |
| Cancellation effective | Change in future coverage under contractual terms |
| Refund approved/paid | Contractual cash entitlement and settlement, with recipient identified |
| Claim incurred/paid | Incurred obligation and later settlement |
| Refund allocated to IPF | Lender cash allocation under its rights; not an automatic mirror of insurer LRC |

PAA eligibility is assessed for the contract group using IFRS 17 criteria. Daily usage or billing does not by itself shorten the contract boundary. PAA insurance revenue follows service allocation rules rather than equalling each day's cash receipts. Claims already incurred remain relevant after future usage stops. [IFRS 17, paragraphs 53–59 and B126–B127](https://www.ifrs.org/content/dam/ifrs/project/amendments-to-ifrs-17/ifrs-17-incorporating-the-june-2020-amendments.pdf).

The Bayesian frequency–severity model supplies claim and expense forecasts; Finance owns their accounting use. Credit-default probability, insurance-claim probability, an IPF refund and insurer loss liability retain different meanings.

## 9. Reuse the modelling ideas through explicit interfaces

For genuine temporal cross-attention, retain multiple approved context tokens:

\[
Q\in\mathbb R^{1\times d},\quad K\in\mathbb R^{L\times d},\quad
V\in\mathbb R^{L\times d_v},\quad
A=softmax(QK^\top/\sqrt d)V.
\]

Document token timestamps, masks and availability. If only one pooled context vector is retained, use an explicit concatenation or gating interpretation: softmax over one key equals one. Compare this with the simpler approved baseline through ablation.

Keep regularised horseshoe shrinkage as a defined prior with its slab treatment, and dependence as a validated challenger after observed common factors. For discrete credit outcomes, use a suitable latent or probability-rectangle construction rather than assume continuous copula-density inputs. Evaluate fairness and explanation alongside calibration and decision outcomes; a penalty term or shrinkage prior alone is not a guarantee.

Finally, pseudonymous customer IDs, access control, tenant isolation, data minimisation and audited calculation lineage are different controls. The useful software outcome is a reproducible calculation contract with a known purpose and deployment boundary. It is not a claim of readiness simply because a demonstration produces a dashboard.
