# RegTech–KESONIA Treasury

Authoritative standalone working repository, extracted on 26 September 2026. Initial scope: the four-part RegTech–KESONIA series, benchmark compounding, curve and FTP teaching cases, and governed Treasury workflows. The remaining-work register is a development backlog, not a claim of completed banking models or integrations.

## Start here

- [Part 1: enterprise architecture](docs/research/kesonia/Part1_KESONIA_Reform_and_Enterprise_Architecture.md)
- [Part 2: compounding mathematics and SQL](docs/research/kesonia/Part2_Daily_Compounding_Engine_Mathematics_and_SQL.md)
- [Part 3: pricing and IFRS 9](docs/research/kesonia/Part3_AI_Pricing_Engine_and_IFRS9_Integration.md)
- [Part 4: platform and roadmap](docs/research/kesonia/Part4_RegTech_Sweep_Platform_Deep_Dives_and_Roadmap.md)
- [Review pack and worked cases](output/kesonia_treasury_deep_review_2026-09-25/00_READ_ME.md)
- [18-item remaining-work register](docs/research/kesonia/TREASURY_REMAINING_WORK_REGISTER_2026-09-25.md)
- [Migration provenance](MIGRATION.md)

## Evidence and local checks

`python output/kesonia_treasury_deep_review_2026-09-25/verify_examples.py` checks illustrative arithmetic and regenerates its result JSON. `python output/kesonia_treasury_deep_review_2026-09-25/build_reading_pack.py` renders the eight local review notes with Pandoc. The renderer writes only within this repository; it no longer distributes files to other projects or modifies historical reading manifests.

The two original pasted texts and the earlier formulations note are preserved in `output/pricing_treasury_cross_project_review_2026-09-23/`. Treat them as research evidence. Historical reading/delivery manifests retain their original paths and hashes. The current ownership and copy verification are in `MIGRATION_MANIFEST.json`.

The four manuscripts and notes in `docs/research/kesonia` are working source. The September 25 reading pack is a dated review edition; coordinate revisions explicitly if publishing a new edition. Broader credit, SPV and accounting specifications remain in Mwendo and are external research dependencies. Financial Material and the SokoIntel website project remain guest repositories; this repository does not write to them.
