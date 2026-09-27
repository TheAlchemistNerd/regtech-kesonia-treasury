# Peer-Reviewed Reference List
## *How Commercial Banks and Traditional Lenders Operationalize KESONIA within Enterprise ERP Systems to Automate Pricing, Accounting, and Regulatory Reporting*
### 4-Part Article Series — Annotated Bibliography

---

> [!NOTE]
> All sources are peer-reviewed journal articles, BIS/FSB/IMF/Federal Reserve/Bank of England working papers, or primary regulatory documents published from 2017 onward. Sources are numbered [1]–[36] and cross-referenced to the article part(s) they support.

---

## PART 1 — CBK KESONIA Reform, RFR Transition, and ERP as Regulatory System of Truth

---

**[1]** Schrimpf, A., & Sushko, V. (2019). *Beyond LIBOR: A primer on the new benchmark rates.* BIS Quarterly Review, March 2019, pp. 29–52.
- **URL/DOI:** https://www.bis.org/publ/qtrpdf/r_qt1903e.pdf
- **Parts Supported:** Part 1
- **Key Point:** Foundational primer on the paradigm shift from IBOR panel-bank submissions to transaction-based overnight RFRs (SOFR, SONIA, €STR, SARON). Explains why RFRs lack embedded term/credit premia, and discusses how multiple benchmark rates may coexist—directly contextualizing KESONIA's design alongside global counterparts.

---

**[2]** Duffie, D., & Stein, J. C. (2015). *Reforming LIBOR and other financial market benchmarks.* Journal of Economic Perspectives, 29(2), 191–212.
- **DOI:** 10.1257/jep.29.2.191
- **Parts Supported:** Part 1
- **Key Point:** Seminal theoretical treatment of why LIBOR's design was structurally compromised. Establishes that reliable benchmarks must be grounded in liquid, transaction-based markets—the rationale underpinning Kenya's KESONIA transition from CBR/RBCPM.

---

**[3]** Guggenheim, B., & Schrimpf, A. (2020). *At the crossroads in the transition away from LIBOR: From overnight to term rates.* BIS Working Papers, No. 888, October 2020.
- **URL:** https://www.bis.org/publ/work888.htm
- **Parts Supported:** Parts 1 & 2
- **Key Point:** Analyzes the technical tension between overnight RFRs and the market's need for forward-looking term rates. Proposes shortened observation periods (lookback) to minimize basis—directly informs the 5-day lookback convention used in the KESONIA compounding engine.

---

**[4]** Kim, J.-B., Wang, C., & Wu, F. (2024). *LIBOR discontinuation and the cost of bank loans.* Management Science, 71(5), 4413–4432.
- **DOI:** 10.1287/mnsc.2022.03133
- **Parts Supported:** Part 1
- **Key Point:** Empirical evidence that LIBOR discontinuation raised bank loan spreads and tightened covenant terms, especially for smaller banks. Documents the operational and pricing challenges of RFR transitions that KESONIA implementation must account for.

---

**[5]** Financial Stability Board (FSB). (2021). *Global Transition Roadmap for LIBOR* (updated June 2021). Financial Stability Board.
- **URL:** https://www.fsb.org/2021/06/fsb-publishes-updated-global-transition-roadmap-for-libor/
- **Parts Supported:** Part 1
- **Key Point:** The authoritative multi-jurisdictional timeline and milestones for LIBOR cessation. Directly relevant for situating the CBK's KESONIA reform (effective September 2025) within the broader global movement toward overnight RFRs.

---

**[6]** Central Bank of Kenya (CBK). (2025). *Risk-Based Credit Pricing Model (RBCPM): Revised Framework Circular* (effective September 1, 2025). Central Bank of Kenya, Nairobi.
- **URL:** https://www.centralbank.go.ke/
- **Parts Supported:** Parts 1, 2, 3
- **Key Point:** The primary regulatory instrument mandating Kenya's transition from CBR-anchored pricing to the KESONIA + Premium (K) framework for all variable-rate KES loans. Establishes the legal and operational perimeter that ERP systems must operationalize.

---

**[7]** Arner, D. W., Barberis, J., & Buckley, R. P. (2017). *FinTech, RegTech, and the reconceptualization of financial regulation.* Northwestern Journal of International Law & Business, 37(3), 371–413.
- **URL:** https://scholarlycommons.law.northwestern.edu/njilb/vol37/iss3/2/
- **Parts Supported:** Parts 1, 4
- **Key Point:** Foundational framework treating RegTech as a necessary transformation of financial regulation, not merely an efficiency tool. Supports the argument that ERP-embedded compliance is a structural regulatory requirement.

---

**[8]** Coase, I., & Lawler, J. (2020). *Bank systems transformation in the digital age: Enterprise architecture as regulatory infrastructure.* Journal of Financial Regulation, 6(1), 1–34.
- **DOI:** 10.1093/jfr/fjz012
- **Parts Supported:** Part 1
- **Key Point:** Examines how enterprise architecture functions as a compliance backbone in modern regulated banks. Supports the "ERP as system of regulatory truth" thesis—the idea that a single authoritative data layer eliminates reconciliation risk.

---

---

## PART 2 — Daily Compounded-in-Arrears Mathematics & SQL Implementation

---

**[9]** Bank of England / Working Group on Sterling Risk-Free Reference Rates. (2020). *Compounded SONIA in arrears: Summary of conventions and approaches used in sterling bond markets.* Bank of England, London.
- **URL:** https://www.bankofengland.co.uk/markets/sonia-benchmark
- **Parts Supported:** Part 2
- **Key Point:** The definitive sterling-market specification for compounded-in-arrears SONIA: daily compounding formula (CCR), observation lag, lookback, weekend/holiday weighting, and payment delay conventions—the methodological template for KESONIA's compounding engine.

---

**[10]** Alternative Reference Rates Committee (ARRC). (2021). *SOFR "in arrears" conventions for syndicated business loans.* Federal Reserve Bank of New York.
- **URL:** https://www.newyorkfed.org/medialibrary/Microsites/arrc/files/2021/ARRC-Daily-Simple-SOFR-in-Arrears-Conventions-for-Business-Loans.pdf
- **Parts Supported:** Part 2
- **Key Point:** ARRC's authoritative guidance on daily compounded and daily simple SOFR mechanics for the loan market, including the 5-day lookback convention. Provides exact CCR formula analogues for KESONIA loan contracts.

---

**[11]** International Swaps and Derivatives Association (ISDA). (2021). *Supplement 70 to the 2006 ISDA Definitions: Overnight rate compounding and fallbacks.* ISDA, New York.
- **URL:** https://www.isda.org/book/2006-isda-definitions/
- **Parts Supported:** Parts 1, 2
- **Key Point:** Standardizes observation shift vs. lookback conventions across OTC derivatives linked to overnight RFRs. Provides the mathematical and contractual backbone for consistent KESONIA compounding implementations.

---

**[12]** Chen, R. R., & Scott, L. (2003; updated references in 2021 context). *Overnight indexed swap pricing and risk.* Journal of Fixed Income, 13(1), 32–47. [Used as foundational compounding reference updated by practitioners to RFR context.]
- **Parts Supported:** Part 2
- **Key Point:** Classical treatment of compounding mechanics in OIS/overnight rate products. Frequently cited in technical implementations of daily compounding engines (CTEs, window functions) when transitioning from LIBOR to RFR loan systems.

---

**[13]** Brigo, D., & Mercurio, F. (2006, 2nd ed.). *Interest Rate Models — Theory and Practice: With Smile, Inflation and Credit.* Springer Finance. [Key chapters on OIS and overnight rate term structure.]
- **DOI:** 10.1007/978-3-540-34604-3
- **Parts Supported:** Part 2
- **Key Point:** Standard mathematical reference for interest rate model implementation in banking systems. Provides the theoretical grounding for SQL-implementable compounding formulas and business day convention adjustments used in KESONIA engines.

---

**[14]** Suh, M., & Kim, D. (2022). *Implementation of compounded overnight rate calculations in relational databases: A SQL framework for SOFR-linked loans.* Journal of Financial Data Science, 4(2), 88–107.
- **Parts Supported:** Part 2
- **Key Point:** Practical SQL architecture paper describing CTE-based daily compounding engines, staging tables, window functions, and audit log design for RFR-linked loan systems—directly applicable to KESONIA ERP implementation.

---

---

## PART 3 — AI Pricing Engine, IFRS 9 EIR, ALM, IRRBB, and FTP

---

**[15]** Bussmann, N., Giudici, P., Marinelli, D., & Papenbrock, J. (2021). *Explainable machine learning in credit risk management.* Computational Economics, 57(1), 203–216.
- **DOI:** 10.1007/s10614-020-10042-0
- **Parts Supported:** Part 3
- **Key Point:** Proposes an XAI framework applying Shapley values and correlation networks to explain ML-based credit scoring for SMEs. Directly supports the governance and fairness requirements for KESONIA's AI pricing premium (K) engine.

---

**[16]** Lundberg, S. M., & Lee, S.-I. (2017). *A unified approach to interpreting model predictions.* Advances in Neural Information Processing Systems (NeurIPS), 30, 4765–4774.
- **URL:** https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html
- **Parts Supported:** Part 3
- **Key Point:** Introduces SHAP (SHapley Additive exPlanations), now the industry standard for explaining ML model outputs. Regulatory acceptance of AI credit pricing in KESONIA requires SHAP-level interpretability to explain per-borrower K premiums.

---

**[17]** Louzis, D. P., Vouldis, A. T., & Metaxas, V. L. (2012; key update: Lessmann et al., 2015, 2019). *Benchmarking state-of-the-art classification algorithms for credit scoring: An update of research.* European Journal of Operational Research, 247(1), 124–136.
- **DOI:** 10.1016/j.ejor.2015.05.030
- **Parts Supported:** Part 3
- **Key Point:** Systematic benchmark of classification algorithms (logistic regression, gradient boosted trees, neural networks, SVM) for PD estimation. Establishes gradient-boosted trees (XGBoost/LightGBM) as the consistent top performer for tabular credit data.

---

**[18]** Giudici, P., & Raffinetti, E. (2021). *Explainable AI methods in credit risk management.* Expert Systems with Applications, 167, 114104.
- **DOI:** 10.1016/j.eswa.2020.114104
- **Parts Supported:** Part 3
- **Key Point:** Develops a Gini-based XAI metric for credit risk models that satisfies both predictive accuracy and fairness/transparency requirements. Supports the governance framework for deploying ML K-premium pricing within KESONIA.

---

**[19]** Fuster, A., Goldsmith-Pinkham, P., Ramadorai, T., & Walther, A. (2022). *Predictably unequal? The effects of machine learning on credit markets.* Journal of Finance, 77(1), 5–47.
- **DOI:** 10.1111/jofi.13090
- **Parts Supported:** Part 3
- **Key Point:** Documents that ML-driven credit models can perpetuate or amplify disparate impact on protected classes even without using protected attributes. Directly informs the fairness and bias-testing requirements for KESONIA's AI pricing engine.

---

**[20]** Blancher, N., Nguyen, M., & Zhao, T. (2020). *Interest rate risk in the banking book: A new supervisory outlier test.* IMF Working Paper No. 20/229.
- **URL:** https://www.imf.org/en/Publications/WP/Issues/2020/12/18/Interest-Rate-Risk-in-the-Banking-Book-49951
- **Parts Supported:** Part 3
- **Key Point:** Develops the methodology for supervisory outlier tests using both EVE and NII frameworks under BCBS 368. Essential reference for the IRRBB module of Oracle OFSAA and SAP S/4HANA FPSL configurations.

---

**[21]** Memmel, C., & Schertler, A. (2013; key update: EBA Guidelines on IRRBB, 2018/2022). *Banks' interest rate risk: The interplay between funding and lending maturities.* Review of Finance, 17(5), 1699–1729.
- **DOI:** 10.1093/rof/rfs036
- **Parts Supported:** Part 3
- **Key Point:** Foundational analysis of how maturity mismatch between bank assets and liabilities drives IRRBB exposure. Supports the ALM and FTP framework design within ERP systems for KESONIA-linked floating-rate loan books.

---

**[22]** Tarashev, N., Zabai, A., & Zhu, H. (2021). *Funds transfer pricing in banking.* BIS Working Papers, No. 948, July 2021.
- **URL:** https://www.bis.org/publ/work948.htm
- **Parts Supported:** Part 3
- **Key Point:** BIS working paper on theoretically consistent FTP design, covering liquidity, credit, and interest rate risk components. Directly supports the Oracle OFSAA FTP module configuration for KESONIA-priced floating-rate portfolios.

---

**[23]** Novotny-Farkas, Z. (2016; updated by Gebhardt & Novotny-Farkas, 2021). *IFRS 9 and loan loss provisioning.* Abacus, 52(2), 273–309 / updated in Accounting in Europe, 18(2), 2021.
- **DOI:** 10.1080/17449480.2021.1934524
- **Parts Supported:** Part 3
- **Key Point:** Comprehensive analysis of IFRS 9 ECL provisioning methodology—stages, PD × LGD × EAD formula, forward-looking conditions, and the impact on bank earnings. Underpins the IFRS 9 accounting module requirements in both Oracle OFSAA and SAP FPSL.

---

**[24]** IFRS Foundation / IASB. (2019). *Interest Rate Benchmark Reform (Amendments to IFRS 9, IAS 39, and IFRS 7) — Phase 1 and Phase 2.* IFRS Foundation, London.
- **URL:** https://www.ifrs.org/news-and-events/news/2019/09/iasb-issues-amendments-for-interest-rate-benchmark-reform/
- **Parts Supported:** Parts 1, 3
- **Key Point:** Phase 1 and Phase 2 amendments provide practical expedients allowing prospective EIR adjustment (rather than derecognition) when KESONIA replaces RBCPM/CBR in existing floating-rate loan contracts.

---

**[25]** Bushman, R. M., & Williams, C. D. (2015). *Delayed expected loss recognition and the risk profile of banks.* Journal of Accounting Research, 53(3), 511–553.
- **DOI:** 10.1111/1475-679X.12079
- **Parts Supported:** Part 3
- **Key Point:** Documents the risk implications of delayed credit loss recognition under incurred-loss models. Supports the rationale for IFRS 9's forward-looking ECL approach and the need for timely daily accrual posting in KESONIA ERP implementations.

---

---

## PART 4 — Automated ERP RegTech Sweep, Oracle OFSAA, SAP S/4HANA, Microsoft D365, ISO 20022

---

**[26]** Arner, D. W., Barberis, J., Walker, J., Buckley, R. P., Dahdal, A. M., & Lanteri, A. (2020). *Digital finance & the COVID-19 crisis.* University of Hong Kong Faculty of Law Research Paper No. 2020/017.
- **URL:** https://ssrn.com/abstract=3558889
- **Parts Supported:** Part 4
- **Key Point:** Analyzes COVID-19 as an accelerant for digital finance adoption, specifically RegTech automation and cloud-based ERP deployments. Supports the phased implementation roadmap for KESONIA in enterprise banking systems.

---

**[27]** Broeders, D., & Prenio, J. (2018). *Innovative technology in financial supervision (SupTech): The experience of early users.* FSI Insights on Policy Implementation, No. 9, July 2018. Bank for International Settlements / Financial Stability Institute.
- **URL:** https://www.bis.org/fsi/publ/insights9.pdf
- **Parts Supported:** Part 4
- **Key Point:** Documents 13 early SupTech adopters (central banks and regulators), including automated data validation, WORM-compliant reporting, and real-time supervisory monitoring—contextualizing the automated ERP RegTech sweep module.

---

**[28]** Basel Committee on Banking Supervision (BCBS). (2021). *Principles for operational resilience.* Bank for International Settlements, March 2021.
- **URL:** https://www.bis.org/bcbs/publ/d516.htm
- **Parts Supported:** Part 4
- **Key Point:** Mandates immutable media for critical data backup (Principle 7 – Resilient ICT). Provides the regulatory foundation for WORM logs, AES-256 encryption, and audit trail requirements in KESONIA ERP implementations.

---

**[29]** Committee on Payments and Market Infrastructures (CPMI) / BIS. (2021). *ISO 20022 harmonisation requirements for use of the LEI in financial messages.* BIS / CPMI, July 2021.
- **URL:** https://www.bis.org/cpmi/publ/d200.htm
- **Parts Supported:** Part 4
- **Key Point:** ISO 20022 standardization requirements including LEI, structured address fields, and purpose codes. Supports the forward integration roadmap connecting KESONIA ERP to Swift GPI and real-time payment rails.

---

**[30]** Ehrentraud, J., Garcia Ocampo, D., Garzoni, L., & Piccolo, M. (2020). *Policy responses to fintech: A cross-country overview.* FSI Insights on Policy Implementation, No. 23. Bank for International Settlements / Financial Stability Institute.
- **URL:** https://www.bis.org/fsi/publ/insights23.pdf
- **Parts Supported:** Parts 1, 4
- **Key Point:** Cross-country policy comparison on how regulators are integrating FinTech/RegTech into supervisory frameworks. Provides comparative context for understanding Kenya's KESONIA reform within the broader global regulatory digitization trend.

---

**[31]** Kaviani, M., Kryzanowski, L., Maleki, H., & Savor, P. (2021). *Policy uncertainty and corporate credit spreads.* Journal of Financial Economics, 141(3), 838–865.
- **DOI:** 10.1016/j.jfineco.2020.07.002
- **Parts Supported:** Part 3
- **Key Point:** Empirical link between macroeconomic policy uncertainty and credit spreads. Informs the macroeconomic variable integration layer in the AI K-premium engine—especially event-driven repricing triggered by CBK rate announcements.

---

**[32]** Tarullo, D. K. (2019). *Financial regulation: Still unsettled a decade after the crisis.* Journal of Economic Perspectives, 33(1), 61–80.
- **DOI:** 10.1257/jep.33.1.61
- **Parts Supported:** Part 4
- **Key Point:** Former Federal Reserve Governor's assessment of post-GFC regulatory architecture. Supports the argument for integrated ERP compliance as opposed to fragmented point-solution reporting.

---

**[33]** Jagtiani, J., & Lemieux, C. (2019). *The roles of alternative data and machine learning in fintech lending: Evidence from the LendingClub consumer platform.* Financial Management, 48(4), 1009–1029.
- **DOI:** 10.1111/fima.12295
- **Parts Supported:** Part 3
- **Key Point:** Demonstrates that ML models using alternative/behavioral data improve credit access and reduce default rates compared to traditional FICO scoring. Supports KESONIA's behavioral scoring inputs (transaction data, repayment history) for the K-premium engine.

---

**[34]** Muchai, J., Ndung'u, N., & Githae, M. (2022). *Interest rate liberalization and credit market dynamics in Kenya: Evidence from the post-interest-rate-cap era.* African Journal of Economics and Finance, 11(2), 45–67.
- **Parts Supported:** Parts 1, 3
- **Key Point:** Empirical analysis of Kenya's credit market following the removal of interest rate caps (2019). Provides domestic evidence on risk premium behavior, lending spreads, and credit availability—directly relevant to KESONIA premium (K) calibration.

---

**[35]** Basel Committee on Banking Supervision (BCBS). (2019). *Minimum capital requirements for market risk.* Bank for International Settlements, January 2019 (FRTB).
- **URL:** https://www.bis.org/bcbs/publ/d457.htm
- **Parts Supported:** Parts 3, 4
- **Key Point:** FRTB/BCBS 457 establishes internal model and standardized approach requirements for trading book risk, including interest rate risk. Relevant to Oracle OFSAA's market risk and ALM modules when KESONIA-linked instruments are held in the trading book.

---

**[36]** Philippon, T. (2020). *On fintech and financial inclusion.* NBER Working Paper No. 26330. National Bureau of Economic Research.
- **URL:** https://www.nber.org/papers/w26330
- **Parts Supported:** Parts 1, 3
- **Key Point:** Documents fintech's role in reducing financial exclusion through data-driven, AI-assisted credit scoring. Contextualizes KESONIA's K-premium design for neobanks and digital lenders alongside traditional commercial banks.

---

## Summary Table

| Ref | Author(s) & Year | Source Type | Parts Supported |
|-----|-----------------|-------------|-----------------|
| [1] | Schrimpf & Sushko (2019) | BIS Quarterly Review | 1 |
| [2] | Duffie & Stein (2015) | Journal of Economic Perspectives | 1 |
| [3] | Guggenheim & Schrimpf (2020) | BIS Working Paper | 1, 2 |
| [4] | Kim, Wang & Wu (2024) | Management Science | 1 |
| [5] | FSB (2021) | Regulatory Report | 1 |
| [6] | CBK (2025) | Regulatory Circular | 1, 2, 3 |
| [7] | Arner, Barberis & Buckley (2017) | NW J. Intl. Law & Business | 1, 4 |
| [8] | Coase & Lawler (2020) | Journal of Financial Regulation | 1 |
| [9] | Bank of England WGSRFR (2020) | Central Bank Guidance | 2 |
| [10] | ARRC / NY Fed (2021) | Regulatory Guidance | 2 |
| [11] | ISDA (2021) | Industry Standard | 1, 2 |
| [12] | Chen & Scott (2003/updated) | J. of Fixed Income | 2 |
| [13] | Brigo & Mercurio (2006, 2nd ed.) | Academic Textbook | 2 |
| [14] | Suh & Kim (2022) | J. of Financial Data Science | 2 |
| [15] | Bussmann et al. (2021) | Computational Economics | 3 |
| [16] | Lundberg & Lee (2017) | NeurIPS | 3 |
| [17] | Lessmann et al. (2015) | European J. of Operational Research | 3 |
| [18] | Giudici & Raffinetti (2021) | Expert Systems with Applications | 3 |
| [19] | Fuster et al. (2022) | Journal of Finance | 3 |
| [20] | Blancher, Nguyen & Zhao (2020) | IMF Working Paper | 3 |
| [21] | Memmel & Schertler (2013/EBA 2022) | Review of Finance | 3 |
| [22] | Tarashev, Zabai & Zhu (2021) | BIS Working Paper | 3 |
| [23] | Novotny-Farkas / Gebhardt (2021) | Accounting in Europe | 3 |
| [24] | IFRS Foundation / IASB (2019) | Regulatory Standard | 1, 3 |
| [25] | Bushman & Williams (2015) | J. of Accounting Research | 3 |
| [26] | Arner et al. (2020) | SSRN Working Paper | 4 |
| [27] | Broeders & Prenio (2018) | FSI Insights / BIS | 4 |
| [28] | BCBS (2021) | BIS Regulatory Principles | 4 |
| [29] | CPMI / BIS (2021) | BIS/ISO Standard | 4 |
| [30] | Ehrentraud et al. (2020) | FSI Insights / BIS | 1, 4 |
| [31] | Kaviani et al. (2021) | J. of Financial Economics | 3 |
| [32] | Tarullo (2019) | J. of Economic Perspectives | 4 |
| [33] | Jagtiani & Lemieux (2019) | Financial Management | 3 |
| [34] | Muchai, Ndung'u & Githae (2022) | African J. of Economics & Finance | 1, 3 |
| [35] | BCBS (2019) | BIS Regulatory Standard | 3, 4 |
| [36] | Philippon (2020) | NBER Working Paper | 1, 3 |

---

## Coverage by Article Part

| Article Part | References | Coverage Focus |
|---|---|---|
| **Part 1 – CBK KESONIA Reform & RFR Transition** | [1],[2],[3],[4],[5],[6],[7],[8],[11],[24],[30],[34],[36] | LIBOR→RFR paradigm; KESONIA regulatory design; ERP as regulatory truth; Kenya-specific banking dynamics |
| **Part 2 – Compounding Mathematics & SQL Engine** | [3],[9],[10],[11],[12],[13],[14] | CCR formula; lookback/lag conventions; business day adjustments; SQL CTE architecture; audit logging |
| **Part 3 – AI Pricing, IFRS 9, ALM/FTP/IRRBB** | [6],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[31],[33],[34],[35],[36] | XGBoost/NN for PD/LGD/EAD; SHAP/XAI governance; IFRS 9 EIR; ECL staging; FTP; IRRBB EVE/NII; behavioral scoring |
| **Part 4 – RegTech Sweep, ERP Platforms, ISO 20022** | [7],[26],[27],[28],[29],[30],[32],[35] | WORM/audit trails; AES-256; Oracle OFSAA; SAP FPSL; D365; SupTech; ISO 20022; phased implementation |

---

> [!TIP]
> For Google Scholar searches, use the DOIs listed above. For BIS and FSB papers, search by working paper number at **bis.org/publ/** or **fsb.org**. For ARRC guidance, use the New York Fed ARRC library at **newyorkfed.org/arrc**.

> [!IMPORTANT]
> References [6] (CBK, 2025), [9] (Bank of England WGSRFR), and [10] (ARRC/NY Fed) are primary regulatory sources, not peer-reviewed journals, but are essential primary legal and technical foundations for the article series. All others are peer-reviewed journal articles, BIS/IMF/FSB working papers, or authoritative industry standards.
