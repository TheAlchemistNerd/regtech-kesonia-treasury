# Regulatory treasury worked cases

**Reproducible synthetic calculations · reviewed 1 October 2026**

These cases connect liquidity eligibility, dated cash, interest earnings, value sensitivity, counterparty exposure and a bounded market-risk capital calculation. The opening bank balance is shared by the liquidity, cash, EVE and NII calculations. The derivative examples are separate, explicitly labelled teaching portfolios.

The calculations are in **research_lab/regulatory_cases.py**; **regulatory_examples()** returns every input, intermediate quantity and result as a serialisable dictionary. Monetary values in Sections 1–3 are **KES million**. Sections 4–7 use **KES**. Rates are decimal fractions; 1 basis point (bp) is 0.0001. Results below are rounded for reading; the code retains floating-point precision.

**Abbreviations:** LCR = liquidity coverage ratio; NSFR = net stable funding ratio; HQLA = high-quality liquid assets; ASF/RSF = available/required stable funding; SA-CCR = standardised approach to counterparty credit risk; CVA = credit valuation adjustment; BA-CVA = basic approach to CVA capital; FRTB = Fundamental Review of the Trading Book; GIRR = general interest-rate risk. EAD, RC and PFE mean exposure at default, replacement cost and potential future exposure.

## What this completes

| Review item | Executable coverage | Boundary still open |
|---|---|---|
| R16: LCR and NSFR | Eligibility, encumbrance, haircuts, both HQLA composition caps, 75% inflow cap, ASF/RSF and undrawn commitments; reconciliation to one dated cash and equity ledger | Complete institution classification, foreign-currency profile, secured financing unwind, supervisory reporting and real source data |
| R08: connected stress | Same opening balance produces base/shocked EVE and NII; dated cash response and exact reverse-stress cash threshold | Calibrated deposit behaviour, prepayment, options, full supervisory IRRBB scenarios and joint stochastic balance-sheet simulation |
| R07: counterparty and CVA | SA-CCR linear single-currency IR netting set, daily cash margin, independent CVA valuation/CS01, wrong-way experiment and reduced BA-CVA capital | Other asset classes and margin structures, full BA-CVA/SA-CVA hedges, market-calibrated exposure simulation and institutional adoption |
| R15: FRTB | Prescribed GIRR delta sensitivity, tenor weights/correlations, currency aggregation and three correlation scenarios | Other risk classes, applicable vega/curvature, DRC, RRAO, trading-book boundary and total FRTB capital |

The Kenyan liquidity factors come from CBK's April 2025 guideline. SA-CCR, BA-CVA and FRTB are pinned **Basel reference implementations**; their appearance here does not establish that the same chapters apply unchanged to every Kenyan institution. KESONIA can supply a benchmark or a curve input. It does not determine instrument eligibility, netting enforceability, collateral availability or a capital rule's institutional perimeter.

## 1. One opening balance: liquidity and stable funding

### 1.1 Inputs and classifications

The example bank begins with assets 1,000, liabilities 900 and book equity 100. Its government collateral pledge lasts two years and is unavailable for monetisation. The other securities satisfy the assumed HQLA quality and operational criteria. “Stable retail” is an aggregate of many qualifying insured KES deposits, not an assumption that an individual KES400 million account is fully insured.

| Opening asset | Carrying/market amount | LCR class and haircut | NSFR RSF factor | Required stable funding |
|---|---:|---|---:|---:|
| Cash | 20 | Level 1; 0% | 0% | 0 |
| Available government securities | 80 | Level 1; 0% | 5% | 4 |
| Qualifying securities A | 100 | Level 2A; 15% | 15% | 15 |
| Qualifying corporate securities B | 80 | Level 2B; 50% | 50% | 40 |
| Government securities pledged for two years | 20 | Excluded: encumbered | 100% | 20 |
| Performing retail loans due within 30 days | 350 | Separate cash inflow | 50% | 175 |
| Performing loans over one year, risk weight above 50% | 350 | No HQLA inclusion | 85% | 297.5 |
| **Assets** | **1,000** | | | **551.5** |

| Funding or capital | Amount | ASF factor | Available stable funding | 30-day runoff |
|---|---:|---:|---:|---:|
| Capital | 100 | 100% | 100 | 0 |
| Debt with maturity over one year | 50 | 100% | 50 | 0 |
| Stable KES retail deposits | 400 | 95% | 380 | 5%: 20 |
| Less stable KES retail deposits | 200 | 90% | 180 | 10%: 20 |
| Non-financial corporate deposits, below one year | 200 | 50% | 100 | 40%: 80 |
| Financial wholesale funding, below six months | 50 | 0% | 0 | 100%: 50 |
| **Funding plus capital** | **1,000** | | **810** | **170** |

An additional irrevocable **credit** commitment to a non-financial corporate has an undrawn amount of 100. Its 30-day draw assumption is 10%, and its NSFR required funding is 5%. A separate contractual collateral call of 10 is payable within 30 days. The performing retail amount due is 350, with eligible LCR inflow 50% × 350 = 175.

These categories use the body of the [CBK April 2025 liquidity guideline](https://www.centralbank.go.ke/wp-content/uploads/2025/04/GUIDELINES-ON-BASEL-III-LIQUIDITY-STANDARDS-AND-LEVERAGE-RATIO.pdf): LCR §§3.6, 3.16–3.28 and 3.54; NSFR §§3.10–3.15, 3.26–3.36 and Table 3. The case assumes no short securities-financing transactions requiring a 30-day unwind. The function rejects an input profile marked as requiring that unwind.

### 1.2 Both HQLA caps, applied together

Let $L$, $A$ and $B$ be eligible Level 1, Level 2A and Level 2B after-haircut amounts, in KES million. Let $a$ and $b$ be the accepted portions of $A$ and $B$, and $H=L+a+b$ the HQLA total. In this no-unwind profile:

$$
0\leq a\leq A,\quad 0\leq b\leq B,\quad a+b\le0.40H,\quad b\le0.15H.
$$

These constraints imply $H\leq L+A+B$, $H\leq(L+A)/0.85$ and $H\leq L/0.60$. Their feasible maximum is:

$$
H=\min\left(L+A+B,\frac{L+A}{0.85},\frac{L}{0.60}\right).
$$

Here $L=100$, $A=85$, $B=40$. Thus $H=166.666667$, with one valid allocation $b=25$, $a=41.666667$. The composition caps exclude 58.333333 of the 225 after-haircut pool. Pledged government securities contribute zero.

Let $O$ be weighted outflows, $I$ weighted eligible inflows and $I^*$ recognised inflows. Then:

$$
O=170+10+10=190,\quad I=175,\quad
I^*=\min(I,0.75O)=142.5,
$$

$$
N=O-I^*=47.5,\qquad
\mathrm{LCR}=\frac{H}{N}=3.50877193=\mathbf{350.877193\%}.
$$

$N$ is 30-day net outflow, in KES million. An HQLA asset cannot also generate an eligible inflow in the input ledger; duplicate identifiers on those sides raise an error. A zero net-outflow denominator is returned as an explicitly undefined ratio.

### 1.3 Stable funding

ASF is the sum of each funding amount multiplied by its available-stable-funding factor. RSF is the corresponding required-stable-funding sum for assets and commitments. These calculations use **carrying amounts**, rather than the LCR's haircut-reduced amounts:

$$
\mathrm{ASF}=810,\quad
\mathrm{RSF}=551.5+100(0.05)=556.5,
\qquad
\mathrm{NSFR}=\frac{810}{556.5}
=\mathbf{145.552561\%}.
$$

The off-balance-sheet commitment requires 5 of stable funding while contributing 10 to the different 30-day liquidity stress. Both originate from the same undrawn commitment of 100.

## 2. Dated cash, sale losses and reverse stress

### 2.1 Management response

The ratio calculations use a regulatory horizon. The following scenario adds transaction dates and management actions:

| Date | Event | Cash movement | Closing cash | Assets | Liabilities | Equity |
|---|---|---:|---:|---:|---:|---:|
| 1 October | Opening | — | 20 | 1,000 | 900 | 100 |
| 2 October | Sell government securities carrying 80 | +80 | 100 | 1,000 | 900 | 100 |
| 2 October | Sell A carrying 100 for 85 | +85 | 185 | 985 | 900 | 85 |
| 2 October | Sell B carrying 10 for 5 | +5 | 190 | 980 | 900 | 80 |
| 3 October | Deposit/wholesale withdrawals | −170 | 20 | 810 | 730 | 80 |
| 3 October | Commitment draw becomes a loan | −10 | 10 | 810 | 730 | 80 |
| 3 October | Post cash collateral, retained as an asset | −10 | 0 | 810 | 730 | 80 |
| 20 October | Collect performing loans | +175 | 175 | 810 | 730 | 80 |

Sale prices are deliberately assumed to equal the haircut-adjusted stress prices in this scenario. **A regulatory haircut alone does not create a realised accounting loss.** The assumed actual sale transactions create the 20 loss and reduce equity to 80. Remaining uncollected short loans of 175 stay on the asset ledger; the scenario has not established their impairment or write-off.

Every event satisfies assets = liabilities + equity. The final cash identity is:

$$
20+170+175-190=175.
$$

The dated scenario collects 175; the regulatory denominator recognises 142.5 because of its inflow cap. HQLA eligible after composition limits is 166.666667; the targeted sales generate 170. These measure different things, and the ledger makes their reconciliation visible.

Without the sale response, 3 October cash would be **−170** even though the calculated LCR is above 100%. No 20 October receipt can settle a 3 October obligation.

### 2.2 Reverse cash stress

Let $P$ be proceeds available by 3 October, $w$ a multiplier on the baseline withdrawals of 170, and $q$ an additional collateral call. All cash quantities are KES million:

$$
C_{\mathrm{early}}=20+P-170w-20-q.
$$

The fixed 20 is the commitment draw plus the original collateral call. With $q=0$, the withdrawal multiplier that exactly exhausts cash is:

$$
w^*=\frac{20+P-20}{170}.
$$

| Available response | Proceeds $P$ | Withdrawals exhausting cash | $w^*$ | Additional call capacity at baseline $w=1$ | Equity after assumed sales |
|---|---:|---:|---:|---:|---:|
| No sale | 0 | 0 | 0 | Already short 170 | 100 |
| Targeted sales above | 170 | 170 | 1.000000 | 0 | 80 |
| Sell all unencumbered securities at the same assumed prices | 205 | 205 | 1.205882 | 35 | 45 |

Equality means cash is exhausted; any greater withdrawal or collateral call creates a deficit. The last response converts the remaining securities to cash but crystallises total losses of 55. It illustrates the cash-versus-capital trade-off. Executability at those prices and same-day settlement still require market and operational evidence.

## 3. EVE and NII from that same opening balance

EVE is economic value of equity: asset present value minus liability present value. NII is interest income minus interest expense over one year. The amounts below equal the opening LCR/NSFR amounts, with explicit synthetic timing and interest assumptions added.

| Instrument | Balance | Final/behavioural life, years | Coupon/base discount rate | First repricing, years | Rate pass-through $\beta$ |
|---|---:|---:|---:|---:|---:|
| Cash | 20 | 0 | 0% | 0 | 0 |
| Government | 80 | 3 | 9% | 3 | 1 |
| A | 100 | 2 | 10% | 2 | 1 |
| B | 80 | 4 | 12% | 4 | 1 |
| Pledged government | 20 | 3 | 9% | 3 | 1 |
| Short retail loans | 350 | 19/365 | 15% | 19/365 | 1 |
| Long loans | 350 | 3 | 18% | 3 | 1 |
| Term debt | 50 | 2 | 11% | 2 | 1 |
| Stable retail deposits | 400 | 2 | 5% | 0 | 0.5 |
| Less stable retail deposits | 200 | 0.5 | 6% | 0 | 0.8 |
| Non-financial corporate deposits | 200 | 0.25 | 7% | 0 | 1 |
| Financial wholesale funding | 50 | 0.1 | 8% | 0 | 1 |

The deposit lives and betas are assumptions for examining the mechanism. They are neither estimated customer behaviour nor regulatory runoff factors. Encumbrance removes the pledged bond from available liquidity; its future payments still belong in EVE.

The short-loan life is the 19 calendar days from 1 to 20 October, divided by 365. The stressed liquidity ledger collects 175 of the 350 due and retains 175 as a loan asset; base EVE values the contractual payments, while constant-balance NII replaces maturities.

### Cash-flow definitions

For row $i$, $B_i$ is opening balance; $r_i$ the annual coupon and base annual-effective discount rate; $\tau_i$ first repricing time; $T_i$ final life; $\beta_i$ pass-through; and $x$ the parallel rate shock. Payment dates $t_j$ are annual dates plus any final stub, with $t_0=0$. Define the post-reset accrual interval:

$$
a_{ij}=\max(0,t_j-\max(t_{j-1},\tau_i)).
$$

At each date, the shocked cash flow is:

$$
CF_{ij}(x)=B_i r_i(t_j-t_{j-1})
 +B_i\beta_i x a_{ij}
 +B_i\mathbf{1}_{t_j=T_i}.
$$

$\mathbf{1}$ equals one when its condition holds and zero otherwise. Each principal is repaid exactly once. With $z_i=+1$ for assets and $-1$ for liabilities:

$$
\mathrm{EVE}(x)=\sum_i z_i
\sum_j\frac{CF_{ij}(x)}{(1+r_i+x)^{t_j}}.
$$

Cash of 20 is included at time zero; equity is the residual and is not discounted as a liability. Existing contracts run off in EVE. NII instead uses a one-year **constant balance** scenario: a maturing position is replaced at the shocked rate for the remaining year.

$$
\mathrm{NII}(x)=\sum_i z_i B_i
\left[r_i+\beta_i x\max(0,1-\tau_i)\right].
$$

| Output, KES million | Base | +200 bp parallel shock | Change |
|---|---:|---:|---:|
| EVE | 99.990652 | 81.161694 | **−18.828958** |
| One-year NII | 88.600000 | 83.035616 | **−5.564384** |

The small −0.009348 difference between base EVE and book equity 100 comes from prorated stub coupons discounted on an annual-effective basis. The long integer-year par instruments reconcile exactly. The NII change independently reconciles to:

$$
350(0.02)(1-19/365)
-0.02[400(0.5)+200(0.8)+200+50]
=-5.564384.
$$

These are different views of the same opening book: runoff EVE, constant-balance NII and a dated liquidity stress with realised sales. They should not be added together as three independent losses. This section establishes the numerical bridge for R08; a joint path model, calibrated behavioural assumptions and the full applicable supervisory shock suite remain further work.

## 4. SA-CCR: netting, collateral and margin

The calculation covers one enforceable interest-rate netting set in one currency, with fixed notionals, linear supervisory deltas and final contractual maturity equal to underlying end time. The three hypothetical derivatives below are measured in KES:

| Trade | Notional $N_i$ | Start $S_i$, years | End/maturity $E_i=M_i$, years | Supervisory delta $\delta_i$ | Market value |
|---|---:|---:|---:|---:|---:|
| Short positive-rate-direction trade | 5,000,000 | 0 | 0.5 | +1 | 150,000 |
| Medium opposite-direction trade | 8,000,000 | 0 | 3 | −1 | −250,000 |
| Long positive-rate-direction trade | 10,000,000 | 0 | 7 | +1 | 500,000 |

The rule reference is [Basel CRE52](https://www.bis.org/committees/bcbs/basel-framework/standard/cre/52/inforce/2023-01-01/published/2020-06-05), published 5 June 2020, effective 1 January 2023. Relevant paragraphs are 52.1–52.2, 52.10–52.23, 52.34, 52.48–52.53 and 52.57.

With 250 business days per year, supervisory duration $SD_i$, in years, and maturity factors $MF_i$, dimensionless, are:

$$
SD_i=\max\left(\frac{10}{250},
\frac{e^{-0.05S_i}-e^{-0.05E_i}}{0.05}\right),\qquad
MF_i^{U}=\sqrt{\min(\max(M_i,10/250),1)},
$$

$$
MF_i^{M}=1.5\sqrt{\mathrm{MPOR}/250},\qquad
d_i=N_iSD_i,\quad D_i=d_i\delta_iMF_i.
$$

MPOR is the margin period of risk in business days. The daily bilateral cash-margin example uses 10 days and assumes no longer floor is triggered by illiquidity, size or disputes. Calculated duration and unmargined remaining maturity have **separate** ten-business-day floors.

Let $D_1,D_2,D_3$ be summed effective notionals in end-time buckets below one year, one through five years, and over five years:

$$
EN=\sqrt{D_1^2+D_2^2+D_3^2+
1.4D_1D_2+1.4D_2D_3+0.6D_1D_3},
\qquad A_{\mathrm{CCR}}=0.005EN.
$$

$EN$ and $A_{\mathrm{CCR}}$ are currency amounts under the supervisory annual time convention. Let $V$ be net market value, $C$ net eligible cash collateral received, $TH$ threshold, $MTA$ minimum transfer amount, and $NICA$ net independent collateral amount, all in KES:

$$
RC_U=\max(V-C,0),\qquad
RC_M=\max(V-C,TH+MTA-NICA,0),
$$

$$
m=\min\left(1,\ 0.05+0.95
\exp\left[\frac{V-C}{1.9A_{\mathrm{CCR}}}\right]\right),
\quad
PFE=mA_{\mathrm{CCR}},\quad
EAD_{\rm raw}=1.4(RC+PFE).
$$

When the add-on is zero, the code directly sets PFE to zero and avoids division. Margined EAD is capped by the same netting set's unmargined EAD. The sample collateral is same-currency cash, so the same $C$ applies in both cap calculations. A non-cash implementation would need separate horizon-appropriate collateral haircuts.

| Quantity, KES unless stated | Unmargined | Daily cash margin |
|---|---:|---:|
| $V$ | 400,000 | 400,000 |
| $C$ | 0 | 450,000 |
| $TH,MTA,NICA$ | Not used | 0; 10,000; 50,000 |
| Bucket 1 effective notional | 1,745,852.863 | 740,702.639 |
| Bucket 2 | −22,286,723.772 | −6,686,017.132 |
| Bucket 3 | 59,062,382.056 | 17,718,714.617 |
| Aggregate add-on | 231,984.736 | 69,694.139 |
| Replacement cost | 400,000 | 0 |
| Multiplier $m$ | 1 | 0.701236 |
| PFE | 231,984.736 | 48,872.048 |
| **EAD** | **884,778.630** | **68,420.867** |

The daily margin consists of 400,000 variation margin plus 50,000 independent collateral. Its unmargined cap is 291,690.805 and is not binding. Calculating the three unmargined trades separately gives total EAD 1,388,963.115, so recognised netting reduces it by 504,184.485. That benefit requires the legal and operational netting assumptions to hold.

EAD is an exposure measure. It becomes a credit capital input only through the relevant counterparty risk-weighting framework; it is not itself a capital charge.

## 5. CVA valuation, spread sensitivity and wrong-way risk

This is a separate unilateral valuation model with deterministic discounting and synthetic exposure. Let recovery $R=0.4$, loss fraction $g=1-R=0.6$, annual spread $s=0.02$, flat intensity $\lambda=s/g$, and continuously compounded discount rate $r=0.09$. The spread/intensity relation is a model assumption.

For interval $j$, $t_{j-1}$ and $t_j$ are year boundaries, $q_j$ the marginal default probability, $EE_j$ exposure conditional on default in that interval, and $DF_j$ the discount factor:

$$
q_j=e^{-\lambda t_{j-1}}-e^{-\lambda t_j},\quad
DF_j=e^{-rt_j},\qquad
\mathrm{CVA}=\sum_j g\,EE_j DF_jq_j.
$$

CVA is reported as a positive loss in KES:

| $t_j$, years | $EE_j$, KES | $q_j$ | Discount factor | CVA contribution, KES |
|---|---:|---:|---:|---:|
| 1 | 600,000 | 0.032783900 | 0.913931185 | 10,786.402 |
| 2 | 900,000 | 0.031709115 | 0.835270211 | 14,302.267 |
| 3 | 400,000 | 0.030669567 | 0.763379494 | 5,619.004 |
| **Total** | | | | **30,707.674** |

Here CS01 is **KES change in CVA loss per one-basis-point spread increase**, with exposures and recovery held fixed. It is not the FRTB sensitivity divided by the decimal bump:

$$
\mathrm{CS01}=10^{-4}\frac{\partial\mathrm{CVA}}{\partial s}
=10^{-4}\sum_j EE_jDF_j
\left[t_je^{-\lambda t_j}
-t_{j-1}e^{-\lambda t_{j-1}}\right].
$$

The analytic CS01 is **146.736899**. A central ±1 bp calculation gives 146.736903; a one-sided +1 bp valuation change is 146.703901. Halving the central bump reduces derivative error approximately quadratically.

A hypothetical protection sensitivity of 88.042139 would offset 60% and leave 58.694759 KES/bp. This is a sensitivity allocation only. Executable hedge instrument valuation, basis risk, cost, eligibility and capital recognition require separate inputs.

### Preserving default marginals when testing wrong-way risk

Use two persistent states, each with probability 0.5. The calm state has spread 0.4% and exposure scale 500,000; the stress state has spread 3.6% and exposure scale 1,500,000. Both use exposure proportions $1,0.8,0.4$ at years $1,2,3$, recovery 40% and discount rate 9%.

The joint calculation averages state-specific $gEE_jDF_jq_j$. The independence comparator uses the **same** weighted marginal $q_j$ and the same weighted mean $EE_j$, then multiplies those means. Consequently the measured difference comes from dependence, rather than changing the marginal default curve.

| Result | KES |
|---|---:|
| CVA with positive exposure/default dependence | 49,411.850 |
| Independence CVA, identical marginal inputs | 35,438.254 |
| **Wrong-way increment** | **13,973.596** |

This valuation experiment explains a mechanism; it does not estimate a real counterparty's wrong-way risk.

## 6. Reduced BA-CVA capital: a distinct calculation

[Basel MAR50](https://www.bis.org/committees/bcbs/basel-framework/standard/mar/50/inforce/2023-01-01/published/2020-07-08), published 8 July 2020 and effective 1 January 2023, supplies the reduced basic-approach formulas in §§50.13–50.16. This version recognises no hedge benefit.

For counterparty $c$, $RW_c$ is its sector/credit-quality risk weight; netting set $n$ has EAD in KES and effective maturity $M_n$ in years. For the non-IMM profile, where IMM means internal models method:

$$
DF_n=\frac{1-e^{-0.05M_n}}{0.05M_n},\qquad
SCVA_c=\frac{RW_c}{1.4}\sum_n M_n EAD_n DF_n.
$$

With supervisory parameter $\rho=0.5$, discount scalar $d=0.65$, and capital $K_{\mathrm{BA}}$:

$$
K_{\rm reduced}=
\sqrt{\left(\rho\sum_c SCVA_c\right)^2+
(1-\rho^2)\sum_c SCVA_c^2},
\quad K_{\mathrm{BA}}=dK_{\rm reduced},
\quad RWA=12.5K_{\mathrm{BA}}.
$$

RWA denotes risk-weighted assets. It and capital are both currency amounts; they are different quantities.

The example uses one hypothetical investment-grade industrial counterparty, $RW=3\%$, with a single three-year, single-payment IR derivative: notional 3,000,000, market value 100,000, supervisory delta +1 and no collateral. The preceding SA-CCR implementation gives EAD 198,502.650. Effective maturity is 3 for this deliberately single-payment example; final maturity must not substitute automatically for effective maturity in a general portfolio.

| Quantity | Result |
|---|---:|
| Supervisory discount factor | 0.9286134905 |
| Maturity-adjusted exposure $M EAD DF$ | KES552,996.716 |
| Stand-alone $SCVA$ | KES11,849.930 |
| **Reduced BA-CVA capital** | **KES7,702.454** |
| **Associated RWA** | **KES96,280.678** |

EAD already contains the SA-CCR factor 1.4; the BA-CVA formula divides it out once. Neither the CVA valuation of Section 5 nor its illustrative 60% sensitivity offset is substituted into this capital formula. Full BA-CVA with qualifying hedges and SA-CVA remain separate extensions.

## 7. FRTB: a fully worked GIRR delta component

The pinned reference is [Basel MAR21](https://www.bis.org/committees/bcbs/basel-framework/standard/mar/21/inforce/2023-01-01/published/2026-03-23), publication **23 March 2026**, effective 1 January 2023. The source supplies netting/aggregation (§21.4), correlation scenarios (§21.6), sensitivity (§21.19), weights (§21.42), tenor correlations (§21.46) and currency correlation (§21.50).

This portfolio has one risk-free zero curve per currency. Its zero-coupon positions are synthetic, with all notionals already converted to the common KES reporting unit and FX held fixed. A negative notional is a short position.

For signed notional $n$, continuous zero rate $r$ and tenor $T$ in years:

$$
PV=n e^{-rT},\qquad
s_T=\frac{PV(r+0.0001)-PV(r)}{0.0001}
=\frac{n e^{-rT}(e^{-0.0001T}-1)}{0.0001}.
$$

$s_T$ is KES per unit **decimal** rate; multiplying it by 0.0001 gives the one-basis-point PV movement. The code uses the prescribed finite +1 bp shift. The analytic derivative $-Tne^{-rT}$ is retained as a separate numerical cross-check.

| Currency/tenor | Signed reporting notional, KES | Zero rate | $s_T$, KES per decimal | Risk weight | Weighted sensitivity $WS_T$, KES |
|---|---:|---:|---:|---:|---:|
| KES 1 year | 1,000,000 | 9% | −913,885.490 | 1.6% | −14,622.168 |
| KES 5 years | −700,000 | 10% | 2,122,326.683 | 1.1% | 23,345.594 |
| USD 2 years | 900,000 | 4% | −1,661,443.274 | 1.3% | −21,598.763 |
| USD 10 years | −400,000 | 5% | 2,424,909.982 | 1.1% | 26,674.010 |

The weights are unreduced. The optional division by $\sqrt{2}$ for specified currencies/domestic reporting currency is not elected.

Net same-factor sensitivities before weighting: $WS_k=RW_ks_k$, where $k$ indexes a currency/tenor factor and $RW_k$ is its decimal risk weight. For two different tenors $T_k,T_l$ on the same curve:

$$
\rho_{kl}=\max\left(
e^{-0.03|T_k-T_l|/\min(T_k,T_l)},0.4\right).
$$

Both 1-versus-5 and 2-versus-10 year pairs here have medium correlation $e^{-0.12}=0.886920437$. For currency bucket $b$:

$$
K_b=\sqrt{\max\left(0,\sum_{k\in b}WS_k^2+
2\sum_{k<l;\ k,l\in b}\rho_{kl}WS_kWS_l\right)},\quad
S_b=\sum_{k\in b}WS_k.
$$

Across currency buckets the medium correlation is $\gamma=0.5$:

$$
K_{\mathrm{GIRR},\Delta}=
\sqrt{\sum_bK_b^2+2\sum_{b<c}\gamma_{bc}S_bS_c}.
$$

If that aggregate radicand is negative, the implementation recomputes it using $S_b$ bounded to $[-K_b,K_b]$. Here that alternative is unnecessary.

For each correlation $c$, the high scenario uses $\min(1.25c,1)$, and the low scenario uses $\max(2c-1,0.75c)$. Apply the same scenario to tenor and currency correlations:

| Scenario | KES bucket $K_b$ | USD bucket $K_b$ | Across-currency correlation | Aggregate GIRR delta, KES |
|---|---:|---:|---:|---:|
| Medium | 12,381.460 | 12,492.165 | 0.500 | 18,805.007 |
| High | 8,723.426 | 5,075.247 | 0.625 | 12,537.871 |
| Low | 15,182.324 | 16,921.887 | 0.375 | **23,453.323** |

The low-correlation scenario dominates because long/short tenor offsets become less effective. This is the maximum for the **GIRR yield-curve delta component**. A complete portfolio selects its governing scenario after the required portfolio aggregation.

The calculation does not produce total FRTB capital. Inflation, cross-currency basis, other curves, FX risk and credit-spread risk are outside this example. Vega/curvature for optional instruments, default risk charge (DRC), residual risk add-on (RRAO), trading-book classification and local adoption require their own coverage. The hypothetical zero-coupon positions have no embedded option, but that fact does not settle those components for a real book.

## 8. Reproduction, tests and next evidence

From the repository root:

~~~text
python -m unittest discover -s tests -p test_regulatory_cases.py -v
python -c "import json; from research_lab.regulatory_cases import regulatory_examples; print(json.dumps(regulatory_examples(), indent=2, allow_nan=False))"
~~~

The module uses the Python standard library and writes nothing on import. All **30 tests passed** on 1 October 2026. The test suite checks:

- simultaneous HQLA cap feasibility, encumbrance, inflow double counting, undefined denominators and ratio scale invariance;
- ASF/RSF reconciliation and the cash/equity identity at every dated event;
- the shared opening balance, zero-shock EVE/NII identity, independent NII repricing arithmetic, one principal repayment per cash-flow schedule and exact reverse-stress boundary/breach;
- SA-CCR hand calculations, exact offsets, maturity/duration floors, margin cap, collateral multiplier bounds and currency scaling;
- a closed-form CVA benchmark, convergence of the numerical CS01, unchanged marginal probabilities in the wrong-way comparator, and BA-CVA alpha/scalar/diversification arithmetic;
- tenor correlations, exact risk-factor netting, two-factor hand calculations, scale/sign/order invariance and independent finite-shift/analytic sensitivity checks.

Completion evidence is therefore mathematical and computational for these stated profiles. Institution data, parameter estimation, market quotations, executable collateral operations and applicability approval are the next evidence layers. These calculations make those requirements concrete without treating the unfinished wider frameworks as completed.
