# RegTech worked-examples PDF: TeX revision

**Typesetting revision:** 16 October 2026. **Numerical edition:** 1 October 2026.

## Delivered PDF

`output/pdf/RegTech_KESONIA_Worked_Examples_2026-10-01.pdf`

60 pages; 49 numbered displayed equations; native TeX inline mathematics; symbols and units in Part III and beside the relevant equations. Simple Segoe UI body typography, linked contents and chapter navigation.

## Source scope

The existing casebook uses these nine files under `docs/methods/`:

- `WORKED_EXAMPLES.md`
- `OPERATIONS_METHODOLOGY.md`
- `SYMBOLS_AND_UNITS.md`
- `LIFECYCLE_WORKED_CASES.md`
- `OPTION_AND_COLLATERAL_CASES.md`
- `REGULATORY_WORKED_CASES.md`
- `ACCOUNTING_AND_CONNECTED_CASES.md`
- `REVIEW_INTEGRATION_AND_REMAINING_WORK.md`
- `SOKOINTEL_CANDIDATE_MAP.md`

The research manuscripts and numerical implementations were preserved. Presentation processing converts code-style formulas and glossary notation to TeX, defines the equivalent local aliases used in the deposit and accounting equations, repairs known damaged display characters, and rebases links. The original operations source-reading inventory remains in Markdown; its explanatory methodology remains in the casebook.

## Rebuild and verification

`python publications/build_worked_examples_pdf.py`

Pandoc produces a standalone TeX document; XeLaTeX runs three passes. The build replaces the PDF after compilation and writes source/output hashes. Intermediate TeX, logs and page previews are under `publications/build/worked_examples_tex/`.

- Zero missing-glyph, undefined-reference and overfull-box warnings.
- 96 internal PDF links resolve to named destinations; 40 external links retained; no local-machine URI targets.
- All 60 pages reviewed in contact sheets; final corrected notation reviewed on individual pages 5, 8, 15, 16 and 19.
- Source hashes checked against the build manifest. Numerical tests were outside this typesetting-only revision.
- Current `.manifest.json` and `.validation.json` accompany the PDF and identify this exact output hash.

**SHA-256:** `0bf84c5eeb448d221c2f42e436123360694919a7708d919c82405e480010146a`
