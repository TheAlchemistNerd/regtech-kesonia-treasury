# KESONIA publication rendering

This directory preserves the inherited publishing assets and LinkedIn editions. The four canonical technical articles and reference list live in `../docs/research/kesonia/`. Edit the intended source edition; a LinkedIn file is an editorial edition, not the canonical technical article.

## Prerequisites

- Python 3.10 or later (standard library only).
- Pandoc with `--embed-resources` support, available on `PATH`.
- For `--refresh-diagrams`, Mermaid CLI (`mmdc`) and its compatible browser installation must already be available. The wrapper installs nothing.

## Build from any working directory

```powershell
python 'C:/Users/Nevo/Downloads/regtech-kesonia-treasury/publications/build_publications.py'
```

Or, from the repository root:

```powershell
python publications/build_publications.py
python publications/build_publications.py --refresh-diagrams
```

The wrapper resolves paths from its own file, so the first command works from any directory. It sequentially renders ten standalone HTML files into ignored `publications/build/`:

- `core/`: four technical articles.
- `linkedin/`: four LinkedIn editions and `linkedin_posts.html`.
- `references/`: the bibliography.
- `build_report.json`: run status, source/output SHA-256 hashes, source-relative paths, output paths, embedded-image counts and Pandoc diagnostics for each attempted source.

The HTML uses embedded images and MathML. No external image files or JavaScript mathematics service are needed for reading it. MathML display depends on the reader's browser support. External hyperlinks still open their destinations normally.

## Cached and refreshed diagrams

The default build copies the inherited `images/` cache into an isolated workspace and invokes the original `mermaid.lua`. This supports building with the existing PNGs when Mermaid CLI is unavailable. If a needed cache file is missing, the inherited filter attempts `mmdc`; an unresolved or nonembedded image causes the wrapper to fail. Cached PNGs are publication assets; reusing them does not prove they match subsequently edited diagram code.

`--refresh-diagrams` starts with an empty diagram cache and requires `mmdc`, rendering each document's diagrams afresh. This is appropriate after Mermaid source edits. The rendered images are embedded into the resulting HTML; this mode does **not** overwrite the inherited PNGs. Every document receives a separate working directory, including the required `internal/puppeteer-config.json`, which prevents the inherited filter's fixed temporary filename from being shared. The inherited Lua filters, configuration and source assets remain unchanged.

## Checks and limits

The build fails for missing required sources/assets, a failed Pandoc render, unrendered Mermaid blocks, missing images, nonembedded images or fewer embedded images than diagram blocks. All ten renders must pass before outputs are copied to `build/`. A failed rendering run writes a failed report and leaves previously published HTML unchanged. Inspect `build_report.json`; a zero exit code establishes these rendering checks, not that every warning is harmless. Avoid simultaneous builds into the same final `build/` directory.

The wrapper verifies HTML production and diagram inclusion. It does not validate financial claims, regulatory applicability, numerical models, source citation accuracy, or PDF/Word pagination and layout. It neither edits source documents nor creates PDF or Word publications.
