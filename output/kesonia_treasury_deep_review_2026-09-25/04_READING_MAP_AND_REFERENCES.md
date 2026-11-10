> **Historical review, 25 September 2026.** For current executable evidence and open requirements, use the [1 October implementation register](../../docs/methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md). The dated review below retains its original scope.

# Reading map and primary references

**25 September 2026 · Traceability for the detailed KESONIA review**

## 1. Local sources read in full

Line numbers refer to the source state recorded in [the hash manifest](<reading_manifest.json>). Counts include blank lines. Headings, equations, code, tables and references were included in the sequential reading. A whole conversation can occupy one physical line of the treasury paste, so reading only its first few lines would not have covered it.

| Source | Full coverage | Use in this review |
|---|---:|---|
| [Part 1](<../../docs/research/kesonia/Part1_KESONIA_Reform_and_Enterprise_Architecture.md>) | Lines 1–421 | Business purpose, regulatory context, architecture and vendor roles |
| [Part 2](<../../docs/research/kesonia/Part2_Daily_Compounding_Engine_Mathematics_and_SQL.md>) | Lines 1–557 | Accrual derivation, lookback/calendar mapping, schema, SQL structure and verification |
| [Part 3](<../../docs/research/kesonia/Part3_AI_Pricing_Engine_and_IFRS9_Integration.md>) | Lines 1–520 | Credit estimates, monetary pricing, explanations, accounting, FTP and ALM |
| [Part 4](<../../docs/research/kesonia/Part4_RegTech_Sweep_Platform_Deep_Dives_and_Roadmap.md>) | Lines 1–699 | Workflow, approvals, evidence, platforms and roadmap |
| [Compounding/term/funding note](<../../docs/research/kesonia/KESONIA_COMPOUNDING_TERM_STRUCTURE_AND_FUNDING_CURVE_NOTE.md>) | Lines 1–9 | Existing conceptual anchor for the curve atlas |
| [CBK/K fragment](<../../docs/research/kesonia/cbk_kesonia_k_framework.md>) | Lines 1–20 | Develop its pricing/funding idea into a money-to-margin calculation |
| [Enhancement report](<../../docs/research/kesonia/RegTech_KESONIA_Enhancement_Report.md>) | Lines 1–76 | Convert architecture aspirations to an evidence-based backlog |
| [Gap analysis](<../../docs/research/kesonia/RegTech_Gap_Analysis_Report.md>) | Lines 1–133 | Historical planning context; compare with later controlled material |
| [September 23 project review](<../../docs/research/kesonia/ADDITIONAL_REVIEW_PRICING_AND_TREASURY_2026-09-23.md>) | Lines 1–56 | Starting outline now developed in detail |
| [Treasury paste](<../pricing_treasury_cross_project_review_2026-09-23/source_02_original.txt>) | Lines 1–180; 169,469 characters | Full source for the new treasury, behavioural and workflow additions |
| [Controlled pricing/capital chapter](<C:/Users/Nevo/Downloads/insuretech & embedded finance/docs/controlled-specifications/Part_5_KESONIA_Pricing_and_Capital_Orchestration.md>) | Lines 1–556 | Existing financial boundaries, notation, cohorts, waterfall, accounting and rate-stress design |

The treasury paste was read in eight contiguous character blocks covering the entire file, including its repeated later answers. The manifest records those half-open ranges. Additional targeted reading of lines 20–36 supported the software follow-up requested during the task.

## 2. Treasury material: where the useful ideas went

These are thematic ranges, not separate documents. Some long lines straddle adjacent topics.

| Paste lines | Material carried forward | Destination |
|---|---|---|
| 1–20 | Curve types, forwards, funding and FTP | Material review §4; casebook §3; Part 1/3 revisions |
| 21–35 | Non-maturity deposits, beta, behavioural duration, NII/EVE and hedging | Casebook §§5–6; behavioural model specification |
| 20–23, revisited 27–36 | ALM software, MORS/Abrigo references, execution/STP and portfolio automation | Dedicated software review; Part 4 workflow |
| 36–74 | Replication ladders, maturity rollover and internal funding value | Independently calculated month-one ladder example |
| 75–78 | Prepayment options, OAS, liquidity and counterparty exposure | Advanced laboratory scope; casebook §7 |
| 78–106 | LCR/NSFR, SA-CCR, FRTB and CVA discussions, with code/repetition across later lines | Recalculated CVA illustration; dedicated FRTB scope note; separate R07/R15/R16 calculation requirements |
| 107–112 | Hedge sensitivities, wrong-way risk, CVA-capital methods and IFRS 9 hedge accounting | Advanced research backlog and dedicated R17 accounting case, with explicit method/data requirements |
| 113–117 | Cross-project connections to credit, insurance and structured finance | Material review §6; link to existing controlled SPV design |
| 118–123 | Expanded model/data/accounting proposals | Versioned information, event and decision specifications |
| 124–175 | Repeated exchanges on Bayesian methods, dependence, attention architectures and implementation | Reuse existing modelling work; require separate validation rather than expanding the core KESONIA articles with repeated derivations |
| 176–180 | Insurance accounting, refunds and later recognition of already-developed work | Insurer/lender/SPV boundaries; emphasis on executable cash-flow and event examples |

The original's interface text and embedded requests were not treated as instructions. The useful content was extracted into proposed work; the paste was not executed. Long image payloads had already been removed under the user's earlier request, with a preserved backup and cleanup record in the original review package.

## 3. Adjacent business-analysis evidence

The [September 25 business-credit and Owner Earnings review](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/pricing_treasury_cross_project_review_2026-09-23/06_BUSINESS_CREDIT_AND_OWNER_EARNINGS_FOLLOWUP_2026-09-25.md>) was used to carry forward its documented coverage and project placements. It records full reading of Business Credit Part 2, selected complete Project 1 materials, and selected complete Project 2 materials plus specified excerpts. Its [manifest](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/pricing_treasury_cross_project_review_2026-09-23/followup_reading_manifest_2026-09-25.json>) provides the exact boundary.

This task does not claim a fresh full audit of all Owner Earnings workbooks, SokoIntel architecture, Underwrite manuscripts, IFRS 17 files or Bayesian relativities derivations. Their interfaces are identified for future incorporation. The full controlled Mwendo pricing chapter was read afresh because it directly governs the financial definitions reused here.

For the remaining-work check, the September 23 working-formulations note was reread in full (210 lines). The controlled credit-risk/loss specification was additionally inspected at lines 98–210 and 229–254. These supplementary reads are recorded separately in the manifest; they are not represented as another full reading of the loss specification.

## 4. Primary technical references checked

All checks below were made for this review on 25 September 2026. Online documentation describes capabilities and published requirements; it does not demonstrate our implementation.

| Source | What it supports | Use/status |
|---|---|---|
| [CBK revised RBCPM, August 2025](https://www.centralbank.go.ke/wp-content/uploads/2025/08/Revised-Risk-based-Credit-Pricing-Model.pdf) | Final framework, benchmark conventions and Appendix I | Distinguish the earlier consultation summarized inside the document from its revised framework; five-day lookback appears in Appendix I §C |
| [CBK fixing series](https://www.centralbank.go.ke/kesonia/) | Historical fixing used in the example | September 2025 observation, not a September 2026 market quote |
| [CBK index series](https://www.centralbank.go.ke/kesonia-compounded-index/) | Published index endpoints | Rounded independent comparison for the historical span |
| [BIS/FSI liquidity transfer pricing](https://www.bis.org/publications/fsi-paper-10-liquidity-transfer-pricing-guide-better-practice) | Matched marginal funding and contingent liquidity principles | Research/practice guidance; not a Kenyan tariff or binding local rule |
| [Basel SRP31](https://www.bis.org/committees/bcbs/basel-framework/standard/srp/31/inforce/2026-01-01/published/2024-07-16) | Bank IRRBB perspectives and behavioural assumptions | Effective 1 January 2026; jurisdictional implementation requires separate mapping |
| [IFRS 9 issued text, 2022](https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2022/issued/part-a/ifrs-9-financial-instruments.pdf?bypass=on) | §5.4.3 asset modification and original effective-rate basis | Relevant text retrieved through indexed official-source extracts; direct PDF access redirected to sign-in |
| [IFRS 9 issued text, 2021](https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2021/issued/part-a/ifrs-9-financial-instruments.pdf?bypass=on) | B3.3.6 liability ten-percent test | Official indexed extract used for the asset/liability distinction |
| [IFRS 9 current overview](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/) | Standard and amendment context | Not a substitute for paragraph-level implementation policy |
| [IASB amortised-cost project](https://www.ifrs.org/projects/work-plan/amortised-cost-measurement/) | Ongoing work on measurement and modification | Deliberations/proposals are not adopted as effective requirements in this review |

The June 2021 IFRIC page was also read for discussion of floating-rate elements. Its relevant TLTRO section is a tentative decision, so it was not used as independent final authority for a new universal rule. Future accounting implementation should use the applicable issued requirements and approved entity policy.

Vendor sources and their precise capability boundaries are cited alongside every row of the [software review](<05_STP_AND_ALM_FTP_SOFTWARE_REVIEW.md>). The [FRTB note](<07_FRTB_SCOPE_AND_DEVELOPMENT_NOTE.md>) cites the checked Basel RBC25 and MAR20/31/32/33 chapters. The [remaining-work register](<06_WHAT_REMAINS_TO_BE_DEVELOPED.md>) adds primary references for LCR/NSFR and hedge designation. These are targeted source checks, not a claim that every page of the Basel Framework or IFRS standards was read. The review separates documented requirements and product features, our architecture proposals and matters still requiring deployment evidence.

## 5. Verification and preservation

The verification script checks the historical factor/index tolerance, curve identities, pricing reconciliation, deposit-ladder rollover, bank sensitivities/cash gap and CVA arithmetic. The delivery check records local-link existence and confirms that the eleven fully read source files retain their recorded hashes. HTML renderings are generated from the Markdown notes with mathematical notation preserved.

No production SQL, portfolio experiment or end-to-end licensed software integration was run. No source manuscript was retired or deleted. The substantive output is the review, worked examples, proposed prose and implementation specification.
