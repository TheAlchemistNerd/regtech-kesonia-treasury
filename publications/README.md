# KESONIA publication rendering

The four canonical articles live in `docs/research/kesonia/`. LinkedIn reading editions preserve their technical content and formulas, with source-relative links adjusted for their location. Launch-post copy is separate and has not been posted externally.

## Build

Python 3.10+, Pandoc with embedded-resource support, and Mermaid CLI/browser for diagram generation are required. The wrapper installs nothing. Run from the repository root:

```text
python publications/build_publications.py --refresh-diagrams
python publications/build_publications.py
```

Paths are resolved from the script, so an absolute script path also works from another working directory. The output is ignored `publications/build/`: four `core/` editions, five `linkedin/` documents, one historical bibliography in `references/`, and every Markdown file in `docs/methods/` under `methods/`.

## Checks

HTML embeds images and renders mathematics as MathML. The builder rebases hyperlinks from the original Markdown location and maps known source documents to their corresponding HTML. Local file targets are checked; core/method HTML fragments are strict. Historical fragment issues are reported. Windows editor `file.md:line` suffixes are retained as report metadata and removed from browser filenames.

Mermaid PNG names use the full diagram-source SHA1. Old caption-based images remain preserved but are not trusted as caches for changed diagrams. Refresh ignores pre-existing caches. Newly generated caches are persisted only after all documents render and local link checks pass; later cached builds can reuse them. Each document has an isolated working directory.

`build_report.json` records source SHA256, output hashes, diagram-source hashes, image counts, local-link checks and warnings. All renders and link checks pass before HTML is copied into its final locations. This preserves earlier HTML on a parse/render/link failure; it is not a transaction against a disk failure during final copying. Avoid simultaneous builds into the same destination.

The build validates rendering and local navigation, not external URL availability, financial assertions, regulatory applicability, or PDF/Word pagination. No PDFs or Word files are created. Browser support determines MathML display. Guest project files are only linked, never copied or edited by the build.

## Browser and timeout configuration

Each tool call has a bounded timeout (default 600 seconds), configurable with `--command-timeout-seconds`. A timed-out renderer and its descendants are terminated; unrelated browser processes are not targeted.

The bundled headless browser stalled in the September 28 verification. Using an already installed Chrome executable completed the fresh render. On this Windows host the verified invocation was:

```powershell
$env:PUPPETEER_EXECUTABLE_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
python publications/build_publications.py --refresh-diagrams --command-timeout-seconds 120
```

Choose the executable path present on your own machine. Ordinary cached builds use the checked source-hash PNGs and do not need a browser unless a diagram changes or its cache is missing.
