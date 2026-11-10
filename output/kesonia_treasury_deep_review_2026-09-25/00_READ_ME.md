> **Historical review, 25 September 2026.** For current executable evidence and open requirements, use the [1 October implementation register](../../docs/methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md). The dated review below retains its original scope.

# KESONIA and treasury: detailed review pack

**25 September 2026**

The review develops the treasury paste into useful additions to the KESONIA series, drawing on the business-credit and Owner Earnings context already gathered.

## Read in this order

1. [Detailed material review](<01_DETAILED_MATERIAL_REVIEW.md>) — existing coverage, curve purposes, improvements to all four articles and connections to neighbouring projects.
2. [Derivations and checked cases](<02_CALCULATION_AND_CASEBOOK.md>) — historical KESONIA reconciliation, spot/forward/par rates, money-to-margin pricing, deposit replication, NII/EVE/cash and CVA.
3. [Revision blueprint and proposed paragraphs](<03_REVISION_BLUEPRINT_AND_INSERTS.md>) — exact section placements, article-ready additions, data requirements and delivery gates.
4. [Reading map and references](<04_READING_MAP_AND_REFERENCES.md>) — complete local reading coverage and the primary-source basis.
5. [STP and ALM/FTP software review](<05_STP_AND_ALM_FTP_SOFTWARE_REVIEW.md>) — the targeted check requested during the review, including MORS, Abrigo, Bloomberg/LSEG and the existing enterprise-platform discussions.
6. [What remains to be developed](<06_WHAT_REMAINS_TO_BE_DEVELOPED.md>) — eighteen concrete work items, including explicit FRTB, liquidity-ratio, hedge-accounting and local-applicability work.
7. [FRTB scope and development note](<07_FRTB_SCOPE_AND_DEVELOPMENT_NOTE.md>) — book boundaries, standardised and internal-model approaches, data, validation and project placements.

## Main finding

The next useful step is to connect **contract cash flows, funding and behaviour to decisions**. The articles already contain much of the underlying architecture. The treasury material supplies examples that make the relationship between borrower payments, lender earnings, economic value, liquidity and shareholder cash clearer.

The software review adds an important operational layer: analysis can feed a governed transaction workflow with traceable identities and reconciliation. Vendor documentation supports specific capabilities; deployment, local instrument support and licensed integrations remain to be established.

## What was completed

- Full sequential reading of all nine existing KESONIA Markdown files, the complete treasury paste and the controlled Mwendo pricing/capital chapter.
- Section-by-section development recommendations and proposed paragraphs.
- Independent arithmetic verification of six groups of examples, including a historical CBK observation-span reconciliation.
- Primary-source checks for benchmark conventions, the selected accounting distinctions, ALM/FTP guidance and software capabilities.
- Markdown and HTML reading versions, with project copies of the main review, software note, remaining-work register and FRTB note in `docs/research/kesonia`.

The existing manuscripts were preserved. This is a review and development package, not an empirical experiment, deployed calculation engine, software procurement or live-trading integration. The earlier image-string cleanup is complete; its backup and record remain in the September 23 review folder.

## Verification records

- [Source hashes and reading coverage](<reading_manifest.json>)
- [Calculation script](<verify_examples.py>)
- [Checked numerical results](<checked_examples.json>)
- [Delivery and verification report](<delivery_verification.json>)

The cumulative screenshot catalogue remains a separate follow-up, consistent with the instruction to focus on the latest pasted material first.
