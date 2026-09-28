# RegTech–KESONIA Treasury

Research, articles and executable reference examples for Kenyan benchmark-linked credit pricing, treasury analysis and controlled financial workflows. The repository was extracted on 26 September 2026 and consolidated with the original publishing project on 28 September, retaining both histories.

**28 September research revision:** all four manuscripts and their LinkedIn reading editions have been revised against the introduced reviews. The new standard-library Python laboratory develops dated compounding, curve construction, pricing, FTP, deposit estimation, cash/equity reconciliation and a durable local STP workflow. Synthetic demonstrations are clearly distinguished from institutional implementation.

## Start here

- [Worked examples and reproduction instructions](docs/methods/WORKED_EXAMPLES.md)
- [Current rule, contract and accounting scope](docs/methods/SCOPE_AND_SOURCE_REGISTER.md)
- [Cross-project boundaries and existing coverage](docs/methods/CROSS_PROJECT_BOUNDARIES.md)
- [All review families and 18 remaining-work items](docs/methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md)
- [Dated FTP, deposit and STP methodology](docs/methods/OPERATIONS_METHODOLOGY.md)
- [Reproduced numerical output](research_lab/results/checked_examples.json)

## Revised series

1. [KESONIA and enterprise architecture](docs/research/kesonia/Part1_KESONIA_Reform_and_Enterprise_Architecture.md)
2. [Compounding, curves and SQL boundaries](docs/research/kesonia/Part2_Daily_Compounding_Engine_Mathematics_and_SQL.md)
3. [Pricing, treasury and IFRS 9](docs/research/kesonia/Part3_AI_Pricing_Engine_and_IFRS9_Integration.md)
4. [Software, STP and development roadmap](docs/research/kesonia/Part4_RegTech_Sweep_Platform_Deep_Dives_and_Roadmap.md)

[Publication guide and LinkedIn editions](publications/README.md). HTML renders preserve formulas and source-aware links. Generated HTML lives under `publications/build/` and is ignored by Git; this revision creates no PDFs.

## Run the reference laboratory

Python 3.10+; no external Python packages:

```text
python -m unittest discover -s tests -v
python -m research_lab.run_examples
python publications/build_publications.py --refresh-diagrams
```

The publication command additionally needs Pandoc and Mermaid CLI. The laboratory writes a deterministic result file with source hashes and uses a temporary local SQLite database. It makes no external trades or reporting submissions.

The historical `output/kesonia_treasury_deep_review_2026-09-25/verify_examples.py` remains available for the earlier teaching calculations. Historical reading/copy manifests and pasted originals retain their dates and provenance; new work does not recertify them by changing their timestamps.

## Boundaries

KESONIA observations, compounded coupon factors, customer K, note coupons, FTP and discount curves are distinct. A bank rule does not automatically govern an SPV or non-bank lender. The latest source register identifies verified Kenyan pricing and liquidity requirements. A reference calculation is not regulatory approval, empirical calibration, an accounting policy or a live vendor integration.

Mwendo owns its financing structure and waterfall; Underwrite owns credit-lifecycle and collectability methods; Bayesian relativities owns insurance ratemaking; business/owner-earnings analysis retains its claim and cash definitions. SokoIntel's current specification already adopts the relevant analytical interfaces. Guest repositories were read for this review and are not modified by this repository's build commands.

## Provenance and preserved work

- [Current revision evidence](docs/governance/revision-2026-09-28/README.md)
- [Superseded review originals](source_library/review-history/2026-09-28/README.md)
- [September 25 review pack](output/kesonia_treasury_deep_review_2026-09-25/00_READ_ME.md)
- [Original publication consolidation](docs/governance/consolidation-2026-09-28/README.md)
- [Extraction provenance](MIGRATION.md)
- [Historical drafts](source_library/regtech-origin/README.md)

The inherited bibliography is retained as historical research material. Freshly checked authority is identified in the current source register; inherited titles and links are not all newly verified.
