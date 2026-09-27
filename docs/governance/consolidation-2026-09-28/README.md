# RegTech repository consolidation — 28 September 2026

## Decision and current authority

The canonical working project is **`C:\Users\Nevo\Downloads\regtech-kesonia-treasury`**. It combines the original RegTech–KESONIA publication project with the later Treasury research and calculation pack. The four canonical manuscripts remain at `docs/research/kesonia/`; their working bytes were identical in the two repositories, and no financial content was changed in this consolidation.

The integration uses an actual Git merge of unrelated histories. It does not replace either history with a fresh snapshot.

| Checkpoint | Commit |
| --- | --- |
| Original Documents initial commit | `0ca6438b59630db233aede132298e3663d8b1bfd` |
| Previous Downloads initial commit | `dc4ef186b49b000724d998f3887805731badd039` |
| Original working files checkpointed on an isolated import branch | `bdc19f7366c264d246a792a85426f1094ebc31fe` |
| Publication layout reconciled before merging | `af443a0b3bef3e0af3eae6fc8bafa19173318024` |

The working checkpoint retains the original modifications, tracked deletions and untracked source/figure assets. The original repository was not committed, reset or cleaned during this process. Deleted legacy scripts and hashed diagrams remain recoverable through its original commit. The unusable NUL-filled Mermaid temporary is retained in the working checkpoint and archival copy, then removed from active source. Two ignored Word lock files are preserved only in the full archival copies.

## Where the material lives

| Original material | Canonical destination |
| --- | --- |
| Four core manuscripts | `docs/research/kesonia/Part*.md` — existing copies reused |
| Annotated bibliography | `docs/research/kesonia/KESONIA_ERP_Reference_List.md` |
| Four LinkedIn editions and promotional posts | `publications/linkedin/` |
| Eleven named diagrams | `publications/images/` |
| Mermaid / Pandoc filters and browser configuration | `publications/` and `publications/internal/` |
| Five historical drafts and text extracts | `source_library/regtech-origin/Drafts/` |
| Treasury reviews, cases and original pastes | Existing `docs/research/kesonia/` and `output/` paths |

[file-map.json](file-map.json) accounts for all **33 files outside `.git`** at the original location: 4 exact manuscript duplicates, 25 imported assets, 1 reconciled ignore file, and 3 archived intermediates. It records SHA-256 values and original-to-current paths. The ignore rules retain Downloads' exclusions and add generated PDF/DOCX exports, the publication build folder and the Mermaid temporary. Existing tracked publications would remain tracked.

## Preservation and retirement

Full filesystem recovery copies, including `.git`, hidden files and ignored locks, are at:

- `C:\Users\Nevo\Downloads\insuretech & embedded finance\_archive\regtech_consolidation_2026-09-28\documents`
- `C:\Users\Nevo\Downloads\insuretech & embedded finance\_archive\regtech_consolidation_2026-09-28\downloads`

Both histories also have verified standalone `.bundle` backups in `C:\Users\Nevo\Downloads\insuretech & embedded finance\_archive\regtech_consolidation_2026-09-28`. `before.json` there records the complete pre-integration file hashes, Git heads, branches, remotes and working status. After the merge and checks passed, Windows refused to move the original directory because another process has it open. The Documents copy is **marked retired in place** with a new `README.md`; a sibling `Regulatory Tech for Banks and neobanks - CONSOLIDATED.md` points to Downloads. All original files, history and pre-existing dirty entries remain unchanged. The retirement README is the only new untracked file in that old repository.

[retirement.json](retirement.json) records this limitation. Physical relocation to `C:\Users\Nevo\Downloads\insuretech & embedded finance\_archive\regtech_consolidation_2026-09-28\retired-documents` remains pending until the directory is released. The verified complete copy at `C:\Users\Nevo\Downloads\insuretech & embedded finance\_archive\regtech_consolidation_2026-09-28\documents` is already available; no recovery depends on moving the locked directory.

The September 26 `MIGRATION*` files and `SOURCE_HISTORY.txt` describe the earlier extraction and remain unchanged historical records. This consolidation record supplements them. No remote is configured, and no changes are pushed by this consolidation. Guest repositories are outside this task's write boundary.

## Publishing and verification boundary

[The publication build guide](../../../publications/README.md) documents portable rendering from the new layout. The imported Lua filters and PNG files are preserved unchanged. The new wrapper supplies the correct working directory, isolates intermediates and embeds the diagrams into generated HTML. Cached figures preserve the existing publication assets; `--refresh-diagrams` requests regeneration from source.

The original drafts were incomplete as rendered archives before the merge: `Drafts/regtech.md` references 104 distinct missing `media/` images, and the older ERP draft references 2. Those missing files were not present in either the original working tree or its archival copy. The drafts remain research source rather than validated publication output. No actual PDF or DOCX documents existed at the original path; its only `.docx` files were Word locks.

Validation covers file preservation, Git ancestry, arithmetic checks and HTML publication paths. It does not revalidate the manuscripts' regulatory assertions, establish production STP/ALM capabilities, or finish the 18-item Treasury development backlog.

## Completed checks

- Both original Git tips and the working-state checkpoint are ancestors of merge commit `50992cf08b9191c014436f6978275e9def541e52`; `git fsck --full` passes.
- All 33 original non-Git files are accounted for. All 29 active destinations match the original working bytes; 43 pre-existing canonical files other than the intentionally updated README and ignore rules are unchanged.
- Treasury arithmetic assertions pass; the existing eight-document HTML renderer produces unchanged outputs.
- The new publication wrapper was run from outside this repository. Ten standalone HTML files passed with zero Pandoc warnings, 22 embedded PNG images and all 51 source mathematics nodes represented in MathML. Independent QA verified source, asset and output hashes and found no external rendering-resource dependencies.
- [publication-build.json](publication-build.json) retains the checked render report. [validation.json](validation.json) records preservation and history checks.

Publication validation used the preserved diagram cache. The optional `--refresh-diagrams` path was not executed, and cached-image inclusion does not prove semantic agreement with edited diagram source. No PDF/Word pagination, visual browser layout or financial claims were revalidated. The build stages all renders before copying outputs; final copying is not a filesystem transaction against disk or permission failures.
