# Scope and primary-source register

**Reviewed 28 September 2026.** This is the current authority map for the revised four-part series. It distinguishes an issued requirement, an institution's contract or policy, a research convention, and a future capability. A local calculation passing tests does not establish compliance.

## 1. Kenyan benchmark and credit-pricing perimeter

The final [CBK revised credit-pricing framework](https://www.centralbank.go.ke/wp-content/uploads/2025/08/Revised-Risk-based-Credit-Pricing-Model.pdf), section 4 and Appendix I, adopts compounded-in-arrears KESONIA for the banking sector's variable-rate Kenya-shilling loans. Fixed-rate and foreign-currency loans are outside that stated scope. The customer premium K includes operating-cost, return and borrower-risk components. Separate charges require separate disclosure. Comment letters reproduced in the paper do not create final exemptions.

The Appendix specifies a five-day lookback; its wording alone does not resolve every business/calendar-day and observation-weight convention. The laboratory's five-business-day cases are explicitly illustrative profiles. Fallback, contractual resets and day mapping require approved interpretation and records. The CBR alternative must be authorised rather than silently substituted by code. [CBK framework, Appendix I](https://www.centralbank.go.ke/wp-content/uploads/2025/08/Revised-Risk-based-Credit-Pricing-Model.pdf).

The [issuance notice](https://www.centralbank.go.ke/uploads/press_releases/2044081907_Press%20Release%20-%20Issuance%20of%20a%20Revised%20Risk-Based%20Credit%20Pricing%20Model.pdf) gives the new/existing-loan transition dates. These are historical milestones, not future implementation promises. The [August 2026 MPC background presentation](https://www.centralbank.go.ke/uploads/presentations/2005474214_Monetary%20Policy%20Committee%20Meeting%20Background%20Data%20August%202026.pdf) subsequently reports full implementation in March 2026.

**Research inference:** applying a KESONIA-linked coupon to an SPV note or non-bank facility does not, by itself, put that entity inside the banking framework. Identify the lender, borrower, currency, product, contract and governing authority before transferring a requirement.

## 2. Historical inputs and synthetic inputs

The historical verification uses the [CBK fixing series](https://www.centralbank.go.ke/kesonia/) and [compounded index](https://www.centralbank.go.ke/kesonia-compounded-index/): 5 September 2025 fixing 9.4618%, index 100.10451025; 8 September index 100.18235974. The publication timestamp in the fixture represents the documented next-business-day publication convention, not an independently captured historical timestamp. Index rounding causes a small expected difference from raw fixing arithmetic.

All deposit panels, curve quotations, bank balances, hedge sensitivities and workflow events are invented and labelled. They demonstrate estimation, reconciliation and failure handling. None proves a Kenyan market curve, bank profitability, borrower outcome or feasible hedge transaction.

## 3. Liquidity and capital scope

Kenya's [April 2025 LCR, NSFR and leverage guidelines](https://www.centralbank.go.ke/wp-content/uploads/2025/04/GUIDELINES-ON-BASEL-III-LIQUIDITY-STANDARDS-AND-LEVERAGE-RATIO.pdf) apply to institutions licensed under the Banking Act and took effect on 1 October 2025. The laboratory's cash buffer is an internal scenario assumption; it is not an LCR or NSFR calculation. Full returns still need eligible-asset, encumbrance, funding and exposure classifications. These requirements do not transfer automatically to an independent SPV.

For additional topics use the [Basel Framework](https://www.bis.org/committees/bcbs/basel-framework) with an explicit Kenyan implementation/version assessment. IRRBB, trading-book market risk/FRTB, derivative counterparty exposure, CVA valuation, CVA capital, regulatory capital and economic capital are distinct quantities. Showing a cash loss or a duration hedge does not calculate all of them. The leverage guidance's derivative references should be checked when developing local exposure measures; they are not evidence that the repository implements a complete SA-CCR return.

## 4. Accounting scope

Use the [IFRS 9 standard and implementation resources](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/). Asset modification, derecognition, floating-rate re-estimation, contractual reset and liability modification are separate assessments. The liability ten-percent test cannot serve as a universal asset-modification rule. The original-EIR shortfall case here is a fixed-rate teaching example; accounting ownership must determine the treatment for the actual instrument.

A prediction update does not itself authorise a customer repricing, stage transfer, journal or trade. Economic hedging does not automatically meet hedge-accounting conditions. [IFRS Interpretations Committee, April 2021](https://www.ifrs.org/news-and-events/updates/ifric/2021/ifric-update-april-2021/).

An insurer's [IFRS 17](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-17-insurance-contracts/) measurement is not the lender's IFRS 9 asset and not the SPV waterfall. Premium/refund/claim rights require a holder, trigger and timing. Intermediary receivables need a fact-specific accounting assessment; see [IFRIC March 2023](https://www.ifrs.org/news-and-events/updates/ifric/2023/ifric-update-march-2023/).

## 5. Financial quantity dictionary

| Quantity | Unit and owner | Boundary |
|---|---|---|
| Published KESONIA | Annual decimal; benchmark administrator | Historical observation, not a forward curve |
| Compounded period factor | Dimensionless; contract engine | Requires day weights and observation mapping |
| Customer K | Annual rate; approved pricing/contract process | Not simply EL, note coupon or FTP |
| Expected principal loss | Currency over a stated horizon; risk/pricing | Do not charge missing interest again if already absent from expected income |
| FTP | Dated internal currency transfer; Treasury | Eliminates on bank consolidation; external funding remains |
| Regulatory/economic capital | Currency stock; distinct policy owners | A capital hurdle is a rate multiplied by capital, not another principal loss |
| ECL | Discounted expected shortfall; accounting | Timing, scenarios, scope and measurement policy matter |
| SPV residual | Currency at a waterfall date; legal vehicle | Neither borrower cash nor automatically sponsor-distributable earnings |
| Owner earnings/SDE | Normalised business/owner analysis | Not cash available for debt service without a bridge |
| OAS | Model-dependent spread | Not observable solely from the current overnight fixing |

## 6. Acceptance gates

Every proposed deployment must identify: legal entity and instrument; rule/contract version; units and dates; source and availability time; approved conventions; model and data validation; independent reconciliation; change owner; and controlled posting/settlement interface. These are design requirements. Only the subset demonstrated in [worked examples](WORKED_EXAMPLES.md) is implemented here.

The older gap and enhancement reports are preserved under `source_library/review-history/2026-09-28/`; their replacement landing pages link to this register. Historical review packs and pasted sources remain dated evidence, not live authority.
