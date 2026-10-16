# Option valuation, priced hedges and collateral funding: reproducible cases

**1 October 2026.** This addition supplies executable reference cases for R04, R05 and R06, plus a compact R12 structural-credit baseline. It is designed to be read alongside [Worked examples](WORKED_EXAMPLES.md), [Symbols and units](SYMBOLS_AND_UNITS.md), and the [remaining-work register](REVIEW_INTEGRATION_AND_REMAINING_WORK.md).

The cases use synthetic inputs and standard-library Python. All monetary amounts are Kenya shillings (KES); all model rates are annual decimals. A displayed 0.01 means 1 percentage point or 100 basis points. The choice of KES as the reporting unit does not establish that these securities, hedge tenors, collateral agreements or model parameters are available or approved for any Kenyan institution.

## 1. What is executable now

| Register row | Executable evidence | Completion boundary |
|---|---|---|
| R04, prepayment and OAS | Monthly additive short-rate tree fitted to every synthetic discount factor; amortizing pool; rate-responsive prepayment; a separate optimal-exercise calculation; bracketed numerical OAS recovery | Market volatility calibration, permissioned borrower histories, physical-to-valuation-measure treatment and institutional validation remain open |
| R05, hedge selection | Actual synthetic swap valuations at two tenors, 25 candidate portfolios, basis and curve-shape shocks, finite-difference slope/curvature, transaction-fee and initial-cash limits | Tradable quotations, transaction sizes, bid/offer, liquidity, execution and approved risk limits remain open |
| R06, collateral and clearing | Netting, threshold, minimum transfer, haircuts, dated and intraday calls, settlement lag, IM increases, borrowing and two accounting identities | An institution's enforceable agreement, eligible collateral, custodian/CCP rules, disputes, real intraday feeds and legal conclusions remain open |
| R12, structural credit | Terminal-debt Merton valuation, debt/equity identity, limiting cases and recovery of synthetic asset value/volatility from equity observations | Compound options, coupon/default barriers, empirical estimation, and comparison with reduced-form models remain open |

No row is treated as an implemented institutional model merely because its reference calculation runs.

## 2. Reproduce the results

Run from the RegTech repository root with Python 3.10 or newer:

```powershell
python -m research_lab.option_cases
python -m unittest discover -s tests -p test_option_cases.py -v
```

The first command writes JSON to standard output. To preserve it with explicit UTF-8 encoding:

```powershell
python -c "import json; from pathlib import Path; from research_lab.option_cases import option_examples; p=Path('research_lab/results/option_cases.json'); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(option_examples(), indent=2, allow_nan=False), encoding='utf-8')"
```

The implementation is [research_lab/option_cases.py](../../research_lab/option_cases.py); the tests are [tests/test_option_cases.py](../../tests/test_option_cases.py). `option_examples()` returns ordinary JSON-serializable values and performs no file writes. Importing the module runs no examples. Twenty-nine tests cover numerical recovery, independent path enumeration, conservation of principal, option bounds, hedge constraints and funding/accounting identities.

## 3. R04: fit a curve before valuing the prepayment option

### 3.1 Synthetic curve and short-rate lattice

Use 36 monthly steps. The year fraction per step is $\Delta t=1/12$. At maturity $t_i=i/12$ years, the input discount factor is:

$$D_i=\exp[-(0.085+0.003t_i)t_i].$$

Here $i$ is the month index, $D_i$ is the price today of one KES paid at $t_i$, and $D_0=1$. The continuously compounded zero rate rises from 8.5% at the origin to 9.4% at year three. These are generated values, not observed KESONIA quotations.

The one-factor additive recombining tree has risk-neutral branch probability one half. At layer $i$, node $j$ records $j$ upward moves among $i$ moves:

$$r_{i,j}=a_i+(2j-i)\sigma\sqrt{\Delta t}.$$

$r_{i,j}$ is the annual continuously compounded short rate for the following month. $a_i$ is the fitted deterministic level, and $\sigma=0.015$ is the assumed absolute short-rate volatility: 150 basis points per square-root year. This is a **Ho–Lee-style lattice**, with no mean reversion; it is not a calibration of Hull–White or Black–Karasinski parameters.

Let $q_{i,j}$ be the time-zero price of one KES contingent on reaching node $(i,j)$. Begin with $q_{0,0}=1$. Fitting the next discount factor gives:

$$a_i=\frac{1}{\Delta t}\log\left(\frac{\sum_j q_{i,j}\exp[-(2j-i)\sigma\sqrt{\Delta t}\,\Delta t]}{D_{i+1}}\right).$$

Each branch carries half of $q_{i,j}\exp(-r_{i,j}\Delta t)$ into its child node. Consequently, summing next-layer state prices reproduces $D_{i+1}$. The largest absolute discount-factor repricing error in the case is **2.22×10⁻¹⁶**. The tests also fit negative-rate curves: the additive model allows negative nodes and does not silently floor them.

Fitting today's curve does not estimate volatility. Volatility must be supplied here; market-option calibration would require a separate quotation set and objective. The original [Ho and Lee paper](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1540-6261.1986.tb02528.x) supplies the model lineage; the lattice equations above state the exact implementation used here.

### 3.2 Scheduled principal and prepayment

The synthetic pool starts with KES 1,000,000, a nominal annual coupon of 14%, monthly payments and a 36-month remaining term. Borrowers are homogeneous surviving loans. Prepayment removes a fraction of otherwise identical loans from the pool; each remaining loan retains its ordinary amortization schedule. There is no default, recovery lag, servicing fee or heterogeneous burnout variable in this example.

At a node, let $B$ be opening surviving principal in KES, $c$ the nominal annual coupon, $u=c/12$ the monthly coupon rate, and $n$ the number of remaining payments. Scheduled payment per KES opening balance is $u/[1-(1+u)^{-n}]$; for $u=0$ it is $1/n$. The scheduled-principal fraction $g$ is this payment fraction minus $u$, clipped to the interval from zero to one to remove final-payment floating-point noise.

The assumed annual conditional prepayment rate is:

$$\operatorname{CPR}_{i,j}=\min[0.60,\;0.04+6\max(c-r_{i,j}-0.025,0)].$$

CPR is a fraction of surviving principal prepaid over a year. Here 0.04 is background prepayment, 6 is the response coefficient to the positive refinancing incentive, 0.025 is the assumed refinancing markup over the short rate, and 0.60 is the cap. The refinancing rule is a deliberately simple valuation assumption. It is not an estimated response to actual mortgage offers, nor does the short rate alone reconstruct a contractual refinancing term rate.

Convert annual CPR to single monthly mortality (SMM) as:

$$\operatorname{SMM}_{i,j}=1-(1-\operatorname{CPR}_{i,j})^{1/12}.$$

Interest is $uB$. Scheduled principal is $gB$. Prepayment is $\operatorname{SMM}_{i,j}(1-g)B$, applied after scheduled principal. Closing balance is $(1-g)(1-\operatorname{SMM}_{i,j})B$. The CPR/SMM relationship agrees with the convention described in [MathWorks' mortgage-pool documentation](https://www.mathworks.com/help/fininst/using-fixed-rate-mortgage-pool-functions.html).

Cash is paid at the month's end using the rate and CPR known at its start. Two balance arrays are propagated separately: probability-weighted balances for expected cash flows, and discounted probability-weighted balances for valuation. This preserves dependence between rates, prior prepayment and surviving balances. The aggregation is exact for this linear homogeneous-pool rule. The tests compare a six-month tree with exhaustive enumeration of all 64 paths. A model with borrower-specific refinancing friction or path-dependent burnout needs additional state variables.

### 3.3 Numerical OAS solve

The option-adjusted spread $s$ is a constant annual continuously compounded spread added to each short rate for discounting. A payment $CF_m$ at month $m$ is valued as:

$$P(s)=E_Q\left[\sum_{m=1}^{36}CF_m\exp\left(-\sum_{i=0}^{m-1}(r_i+s)\Delta t\right)\right].$$

$P(s)$ is the model price in KES; $E_Q$ is expectation under the stated valuation measure; $CF_m$ includes interest, scheduled principal and prepayment; and $r_i$ is the rate along the path. The prepayment rule remains fixed during the spread solve. A larger spread therefore discounts positive cash flows more heavily and produces a lower price. [MathWorks' OAS reference](https://www.mathworks.com/help/fininst/mbsprice2oas.html) gives the general price-to-spread use; the assumptions and solver here are explicit and independent of that software.

For a recovery test, generate a target price using a known spread of 175 basis points, then pass only the price to bracketed bisection over spreads from −5% to +20%. The solver rejects an unbracketed target and must reach an absolute price error below KES 0.0000001 within 100 iterations.

| Quantity | Reproduced value |
|---|---:|
| Synthetic target price at 175 bp | KES 1,037,135.316792 |
| Recovered OAS | 174.999999999955 bp |
| Price residual | KES 0.000000005472 |
| Solver iterations | 41 |
| Price at 75 bp | KES 1,049,720.716375 |
| Price at 275 bp | KES 1,024,771.515460 |
| Total expected principal paid | KES 1,000,000 |
| Final expected principal | KES 0, within floating-point tolerance |

The monthly cash-flow rows in JSON expose interest, scheduled principal, prepayment, opening/closing balance and the principal reconciliation residual. A known-price recovery test establishes implementation consistency; it does not establish empirical model accuracy or the economic uniqueness of an OAS inferred under different behavioural assumptions.

### 3.4 Exercise and baseline checks

A separate backward-induction calculation treats the borrower as choosing frictionless whole-loan repayment at par at the start of months 2–36. It compares the lender's continuation value with outstanding principal and takes the smaller. Immediate time-zero repayment is excluded. Its purpose is to demonstrate an explicit exercise decision as distinct from the CPR response rule.

| Model at zero OAS | Value, KES |
|---|---:|
| Scheduled mortgage with no prepayment | 1,072,762.685598 |
| Stated rate-responsive CPR policy | 1,059,308.030558 |
| Frictionless optimal borrower exercise at the stated call dates | 1,004,505.086704 |

The exercise engine identifies 469 exercise nodes, including nodes that may be unreachable after an earlier exercise; this is a count of the exercise region, not a count of borrowers or actual repayments. Its noncallable limit equals the scheduled cash-flow value from the fitted curve. With a zero coupon and positive deterministic rates, there is no optimal early exercise. These are useful economic checks independent of the OAS recovery calculation.

The CPR case assumes a valuation-measure prepayment process. A longitudinal physical-measure model of borrower decisions requires observed exposures, censoring/competing exits, out-of-time tests and an explicit treatment of unhedgeable behavioural risk before it can supply valuation assumptions. Curve fitting and mechanical spread recovery do not complete that empirical work.

## 4. R05: compare priced hedges and preserve basis risk

### 4.1 Instruments and price equations

The asset is a three-year annual-pay fixed-rate instrument: KES 1,000,000 principal and KES 110,000 coupon each year. Baseline continuous discount and projection zero rates are 8.5% and 9% respectively. Its base price is KES 1,053,996.793847.

Candidate hedges are annual pay-fixed/receive-floating synthetic swaps with two- and five-year tenors. The model uses annual unit accrual fractions, no principal exchange, deterministic projection from discount-factor ratios, and a fixed rate set to give zero inception value. With payment year $t$, notional $N$, fixed rate $K$, projection factor $D_P(t)$, and discount factor $D_D(t)$:

$$V_{\mathrm{swap}}=N\sum_{t=1}^{T}\left[\frac{D_P(t-1)}{D_P(t)}-1-K\right]D_D(t).$$

$T$ is the integer tenor in years. $V_{\mathrm{swap}}$ is positive for a payer whose projected floating receipts exceed fixed payments after discounting. Both inception fixed rates are approximately 9.417428% in this flat projection example. Interest payment forecasts are synthetic annual-period amounts; an implementation for actual resets and compounding must use the instrument's fixing and accrual conventions.

Parallel shocks move both curves. The basis shock raises the projection curve alone by 100 bp. The twist adds $\ell(t-3)/3$ to both zero curves with $\ell=0.01$. Here $\ell$ is an annual rate coefficient, and $t$ is maturity in years. The asset responds only to its discount curve. These scenarios therefore preserve distinct projection, discount and maturity effects.

### 4.2 Finite feasible set and objective

Each tenor can have notional 0, 250,000, 500,000, 750,000 or 1,000,000, giving 25 portfolios. Two-year and five-year fees are respectively 0.10% and 0.15% of notional. Initial-margin assumptions are respectively 3% and 6%. The fee limit is KES 2,000; total initial margin plus fees must fit KES 70,000. Initial margin is restricted liquidity, while fees are an expense.

The chosen candidate minimizes the worst absolute combined asset-and-hedge value change **after fees** across four specified shocks. It is a finite-grid comparison, not a claim of continuous global optimality. It selects KES 750,000 of the two-year payer swap, no five-year swap, fee KES 750 and assumed IM KES 22,500. Total initial cash use is KES 23,250.

| Stress | Asset change | Hedge change | Combined change after fee |
|---|---:|---:|---:|
| Both curves +100 bp | −28,264.44 | 14,320.36 | −14,694.09 |
| Both curves −100 bp | 29,085.87 | −14,603.44 | 13,732.43 |
| Projection curve alone +100 bp | 0.00 | 14,533.51 | 13,783.51 |
| Stated curve twist | 1,296.58 | −5,041.85 | −4,495.27 |

All values are KES. The basis scenario explains why cancelling parallel duration alone is insufficient. The full JSON includes every feasible and infeasible candidate with its assumptions and scenario prices. The initial-cash constraint does not cap subsequent margin calls; those are addressed separately below.

### 4.3 Slope and convexity diagnostics

For a scalar parallel shock $x$, let $V(x)$ be repriced value and $b=0.0001$ the 1 bp calculation bump. The signed slope is $[V(b)-V(-b)]/(2b)$; multiplying by 0.0001 gives KES change per bp. The curvature is $[V(b)-2V(0)+V(-b)]/b^2$, measured in KES per squared decimal rate. The second-order contribution at a 100 bp shock is half this curvature times $0.01^2$.

| Diagnostic | Unhedged | Selected hedge plus asset |
|---|---:|---:|
| Signed parallel price change per bp, KES | −286.711459 | −142.101793 |
| Second derivative, KES per squared rate | 8,213,664.78 | 5,382,893.58 |
| Second-order contribution at 100 bp, KES | 410.68 | 269.14 |

These derivatives are calculated from actual instrument prices. The test suite compares with an analytic zero-coupon benchmark and halves the bump to check convergence. Positive-duration bond terminology often quotes DV01 with the opposite sign; this module deliberately labels its measure `d_pv_per_bp` to keep the sign explicit.

## 5. R06: a value hedge can require more funding cash

### 5.1 Contract and time assumptions

This separate funding example uses a receive-fixed two-year swap on KES 250,000 and a pay-fixed five-year swap on KES 750,000, in one assumed legally valid netting set. It is a fixed portfolio chosen to illustrate offsetting contract marks; it is **not the candidate selected under the four-scenario objective above**.

The marked-value shocks occur at 09:00 and 15:00 between 5 and 8 October 2026. Rates fall cumulatively by 50, 100 and 200 bp. Prices use the preceding synthetic valuation equations with remaining tenors frozen across this short stress window. The dated ledger models call/settlement/funding timing; a complete dated security engine would also roll valuation dates, accrue coupons and use observed fixings. No coupon or maturity payment is included within this window.

Both cases begin with KES 40,000 cash. Funding costs 12% per year on ACT/365 including fractional days, charged on the previous event's borrowing over elapsed time. Costs are financed as they accrue. Required IM begins at KES 30,000 and rises according to the declared stress rule $30,000[1+|x|/0.02]$, where $x$ is the parallel rate shift. This is a transparent synthetic IM scenario, not a CCP risk model. IM is posted immediately and remains a restricted asset.

| Term | Bilateral illustration | Cleared illustration |
|---|---|---|
| Treatment of derivative variation | Collateral supporting an outstanding derivative mark | Final cash settlement to market; derivative mark reset to zero |
| VM exposure threshold | KES 5,000 | Zero |
| VM minimum transfer amount | KES 500, applied to changes after pending transfers | Zero in this teaching ledger |
| VM settlement | Following weekday at 09:00 | Same event, including intraday event |
| Collateral haircut | 2% on the eligible collateral market value | 2% on IM collateral; variation settles in cash |
| Reuse of restricted collateral | None | None |

The positive bilateral threshold is an assumed legacy/otherwise-permitted contract term, not a claim that it is permitted for covered counterparties under current margin rules. The [BCBS–IOSCO standard](https://www.bis.org/bcbs/publ/d475.pdf) specifies zero VM thresholds for covered entities and separately addresses IM and transfer minima. Actual scope requires jurisdictional and counterparty classification.

The cleared example deliberately uses **final settlement variation**. Its accounting differs from collateralized-to-market clearing arrangements. [CME's margining discussion](https://www.cmegroup.com/clearing/files/stability-in-times-of-stress-cme-clearings-anti-procyclical-margining-regime.pdf) explains the distinction between IM collateral and settlement variation. An implementation must read the chosen product's legal terms rather than infer treatment from the word “cleared.”

### 5.2 Calls, haircuts, netting and settlement

Let $V$ be the net derivative value to the institution, $\theta$ the bilateral threshold, and $h$ the collateral haircut. All three dollar-like quantities in this paragraph are KES; $h$ is dimensionless. Required bilateral VM credit is $\max(-V-\theta,0)$. Deliverable collateral market value equals required credit divided by $1-h$. The call is the change from posted collateral plus pending transfers. Changes below the minimum transfer amount remain uncalled until the threshold is met. IM is computed separately; it does not silently reduce VM exposure.

At the final 200 bp downward shock, individual swap marks are **+9,831.88** and **−67,136.37**, giving net value **−57,304.49**. Without the assumed netting agreement, the gross out-of-money mark is KES 67,136.37. The bilateral VM requirement is KES 52,304.49 after the KES 5,000 threshold; with a 2% haircut, posted VM collateral market value is KES 53,371.93. Pending transfers remain visible before the next morning's settlement. The code reports the residual exposure after settled VM and does not count a pending call as received collateral.

In the cleared case, cumulative final variation cash paid is KES 57,304.49. This payment realizes the derivative loss; it is not also booked as an owned collateral asset. IM market value is KES 61,224.49 against required credit of KES 60,000.

### 5.3 Funding and wealth reconcile

At every event, the implementation checks:

$$C_0+F=C+R+S+J.$$

$C_0$ is initial cash; $F$ is outstanding borrowing; $C$ is available cash; $R$ is restricted collateral market value; $S$ is cumulative final variation settlement paid, zero in the bilateral case; and $J$ is cumulative funding expense. Each is in KES. Borrowing is drawn only as needed to keep available cash nonnegative; available surplus first repays borrowing in the same identity.

The independent net-wealth check includes the asset's marked-value change and the derivative's remaining balance-sheet mark. In the bilateral case, the derivative liability remains outstanding alongside the collateral asset. In the cleared case, settled derivative variation has passed through cash, leaving a zero post-settlement derivative mark. Both routes reconcile to initial cash plus economic asset-and-hedge value change minus funding expense.

| Final event, 8 October at 15:00 | Bilateral | Cleared, final settlement |
|---|---:|---:|
| Asset value increase, KES | 59,017.59 | 59,017.59 |
| Derivative economic value change, KES | −57,304.49 | −57,304.49 |
| Combined economic value change, KES | 1,713.10 | 1,713.10 |
| Restricted collateral asset, KES | 114,596.42 | 61,224.49 |
| Cumulative final variation cash paid, KES | 0.00 | 57,304.49 |
| Cumulative funding expense, KES | 23.80 | 40.91 |
| Outstanding borrowing, KES | 74,620.23 | 78,569.89 |

The hedge substantially reduces the marked-value movement while causing funding demand. This numerical case makes that distinction operational: asset valuation gains cannot automatically pay a margin call. It does not conclude that one clearing arrangement is universally cheaper; terms, offsets, eligible assets, timing and funding rates determine the result.

## 6. R12: structural-credit baseline and inverse calibration

The single-period Merton case assumes one terminal zero-coupon debt claim, no dividends, no bankruptcy cost and no default before maturity. Asset value is KES 1,500,000, face debt KES 1,000,000, asset volatility 30%, continuous risk-free rate 8.5% and maturity three years. The asset process and valuation assumptions are those of the standard structural baseline described in [Merton's original paper](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1540-6261.1974.tb03058.x).

For asset value $A$, debt face $L$, volatility $\sigma_A$, rate $r$, maturity $T$ and standard normal distribution function $\Phi$:

$$d_1=\frac{\log(A/L)+(r+\sigma_A^2/2)T}{\sigma_A\sqrt{T}},\qquad d_2=d_1-\sigma_A\sqrt{T}.$$

$$E=A\Phi(d_1)-Le^{-rT}\Phi(d_2),\qquad B=A-E.$$

$E$ is equity value and $B$ is risky debt value, both KES. The risk-neutral terminal default probability is $\Phi(-d_2)$. It is not an empirical one-year borrower PD. The implied equity volatility is $\sigma_E=A\Phi(d_1)\sigma_A/E$, measured per square-root year. The continuous credit spread over $r$ is $-\log(B/L)/T-r$.

The example generates synthetic equity value and volatility from the known asset inputs, then recovers $A$ and $\sigma_A$ using nested bracketed solves. For each trial asset volatility, equity value determines an asset-value bracket between $E$ and $E+Le^{-rT}$; the outer solve matches equity volatility within $10^{-12}$. Recovered asset value is KES 1,500,000 and volatility 0.30 within the displayed solver tolerances. [MathWorks' Merton documentation](https://www.mathworks.com/help/risk/mertonmodel.html) describes the corresponding equity/asset relation and inverse-estimation problem.

The tests separately verify $A=B+E$, the zero-volatility limit, terminal payoffs, and the increase in equity option value when asset volatility rises. `put_credit_discount` is $Le^{-rT}-B$, a present-value credit discount in KES. `equity_delta` is $\Phi(d_1)$, a dimensionless derivative. `credit_spread_continuous` is an annual decimal rate. At maturity or zero volatility, the implementation uses explicit limiting payoffs and the strict default event $A<L$ at maturity.

Actual balance-sheet assets are not automatically market asset value, and observed equity volatility is not asset volatility. Coupon debt, covenants, refinancing, early default, recovery costs, multiple maturities and compound options require a richer model. This new baseline advances R12's reproducibility; it does not close the broader research item.

## 7. Implementation and validation limits to carry forward

1. Supply permissioned borrower histories and a market option/curve quotation set before claiming empirical prepayment or volatility calibration.
2. Compare the CPR valuation assumption with the separate exercise model and test stability to refinancing costs, burnout and unhedgeable prepayment risk.
3. Replace frozen-tenor collateral stress marks with actual contractual event schedules, fixing accrual, date rolls and live valuation inputs.
4. Bind each derivative to its enforceable netting, collateral and settlement agreement; verify eligible assets, legal haircuts, segregation, reuse rights and call disputes.
5. Expand the hedge feasible set using executable quotations and stressed cash constraints, while preserving basis and convexity exposures.
6. Keep structural-credit valuation and empirical default forecasting explicitly labelled by measure and horizon. Compound options and comparison with reduced-form models remain advanced work.

These are concrete remaining inputs and extensions. The reference code, formulas, symbol definitions and tests above can now be reused in the articles and future institution-specific work.
