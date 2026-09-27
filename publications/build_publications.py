#!/usr/bin/env python3
"""Build the ten inherited KESONIA publications as self-contained HTML."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


PARTS = (
    "Part1_KESONIA_Reform_and_Enterprise_Architecture.md",
    "Part2_Daily_Compounding_Engine_Mathematics_and_SQL.md",
    "Part3_AI_Pricing_Engine_and_IFRS9_Integration.md",
    "Part4_RegTech_Sweep_Platform_Deep_Dives_and_Roadmap.md",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=False)


def mermaid_count(node: object) -> int:
    if isinstance(node, list):
        return sum(mermaid_count(item) for item in node)
    if not isinstance(node, dict):
        return 0
    if node.get("t") == "CodeBlock" and "mermaid" in node["c"][0][1]:
        return 1
    return sum(mermaid_count(value) for value in node.values())


class Images(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sources: list[str] = []
        self.unrendered_mermaid = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "img":
            self.sources.append(attributes.get("src") or "")
        if tag in {"code", "pre"} and "mermaid" in (attributes.get("class") or ""):
            self.unrendered_mermaid = True


def write_report(path: Path, report: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-diagrams", action="store_true",
                        help="Render diagrams using mmdc instead of inherited cached PNGs.")
    args = parser.parse_args()
    publication_root = Path(__file__).resolve().parent
    repository_root = publication_root.parent
    core = repository_root / "docs" / "research" / "kesonia"
    sources = [(core / name, Path("core") / (Path(name).stem + ".html")) for name in PARTS]
    sources += [(publication_root / "linkedin" / name,
                 Path("linkedin") / (Path(name).stem + ".html")) for name in PARTS]
    sources += [
        (publication_root / "linkedin" / "linkedin_posts.md", Path("linkedin/linkedin_posts.html")),
        (core / "KESONIA_ERP_Reference_List.md", Path("references/KESONIA_ERP_Reference_List.html")),
    ]
    output_root = publication_root / "build"
    output_root.mkdir(parents=True, exist_ok=True)
    report = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "running", "mode": "refresh" if args.refresh_diagrams else "cached",
        "scope": "HTML rendering and embedded-image checks; no financial or PDF validation",
        "source_count": len(sources), "sources": [], "published": False,
    }
    try:
        pandoc = shutil.which("pandoc")
        if not pandoc:
            raise RuntimeError("Pandoc is required and must be available on PATH.")
        if args.refresh_diagrams and not shutil.which("mmdc"):
            raise RuntimeError("--refresh-diagrams requires Mermaid CLI (mmdc) on PATH.")
        assets = [publication_root / "mermaid.lua", publication_root / "pagebreak.lua",
                  publication_root / "internal" / "puppeteer-config.json"]
        for path in [source for source, _ in sources] + assets:
            if not path.is_file():
                raise FileNotFoundError(f"Required publication source or asset is missing: {path}")
        if not (publication_root / "images").is_dir():
            raise FileNotFoundError("Required inherited publications/images directory is missing.")
        report["pandoc_version"] = run([pandoc, "--version"], publication_root).stdout.splitlines()[0]
        report["inherited_asset_hashes"] = {
            path.relative_to(publication_root).as_posix(): sha256(path)
            for path in assets + sorted((publication_root / "images").glob("*")) if path.is_file()
        }
        # Each run and document owns its workspace. The inherited filter's fixed
        # temp_mermaid.mmd name never crosses a process or document boundary.
        with tempfile.TemporaryDirectory(prefix="kesonia-publishing-") as temporary:
            workspace = Path(temporary)
            staged: list[tuple[Path, Path]] = []
            for number, (source, relative_output) in enumerate(sources, start=1):
                job = workspace / f"document-{number:02d}"
                job.mkdir()
                (job / "internal").mkdir()
                for asset in assets:
                    shutil.copy2(asset, job / asset.relative_to(publication_root))
                if args.refresh_diagrams:
                    (job / "images").mkdir()
                else:
                    shutil.copytree(publication_root / "images", job / "images")
                local_source = job / source.name
                shutil.copy2(source, local_source)
                record = {
                    "source": source.relative_to(repository_root).as_posix(),
                    "sha256": sha256(source), "output": relative_output.as_posix(),
                    "status": "running", "inline_image_count": 0, "warnings": [],
                }
                report["sources"].append(record)
                parsed = run([pandoc, str(local_source), "--from=markdown", "--to=json"], job)
                if parsed.returncode:
                    raise RuntimeError(f"Pandoc could not parse {source.name}: {parsed.stderr.strip()}")
                expected_diagrams = mermaid_count(json.loads(parsed.stdout))
                record["mermaid_diagram_count"] = expected_diagrams
                output = job / "publication.html"
                heading = re.search(r"^#\s+(.+)$", local_source.read_text(encoding="utf-8-sig"), re.M)
                title = heading.group(1).strip() if heading else source.stem.replace("_", " ")
                command = [
                    pandoc, str(local_source), "--from=markdown", "--to=html5",
                    "--standalone", "--embed-resources", "--mathml",
                    "--metadata", f"pagetitle={title}",
                    "--lua-filter=mermaid.lua", "--lua-filter=pagebreak.lua",
                    f"--resource-path={os.pathsep.join([str(job), str(source.parent)])}",
                    f"--output={output}",
                ]
                rendered = run(command, job)
                warnings = [text.strip() for text in (parsed.stderr, rendered.stderr) if text.strip()]
                record["warnings"] = warnings
                if rendered.returncode or not output.is_file():
                    raise RuntimeError(f"Rendering failed for {source.name}: {'; '.join(warnings)}")
                html = output.read_text(encoding="utf-8")
                inspection = Images()
                inspection.feed(html)
                inline = [src for src in inspection.sources if src.startswith("data:image/")]
                record["inline_image_count"] = len(inline)
                if inspection.unrendered_mermaid:
                    raise RuntimeError(f"Unrendered Mermaid block remains in {source.name}.")
                if len(inline) != len(inspection.sources):
                    raise RuntimeError(f"Missing or nonembedded image remains in {source.name}.")
                if len(inline) < expected_diagrams:
                    raise RuntimeError(f"Expected {expected_diagrams} diagrams in {source.name}; found {len(inline)} embedded images.")
                if not html.lstrip().lower().startswith("<!doctype html>"):
                    raise RuntimeError(f"Output is not a standalone HTML document: {source.name}")
                record["output_sha256"] = sha256(output)
                record["status"] = "passed"
                staged.append((output, output_root / relative_output))
                print(f"Rendered {record['source']}: {len(inline)} embedded images", flush=True)
            # Publish only after all ten documents pass. Existing build outputs
            # survive a parsing/rendering failure unchanged.
            for staged_output, destination in staged:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(staged_output, destination)
        report["status"] = "passed"
        report["published"] = True
    except (OSError, ValueError, RuntimeError) as error:
        report["status"] = "failed"
        report["error"] = str(error)
        if report["sources"] and report["sources"][-1]["status"] == "running":
            report["sources"][-1]["status"] = "failed"
        print(f"Build failed: {error}", file=sys.stderr)
    finally:
        report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        write_report(output_root / "build_report.json", report)
    if report["status"] == "passed":
        print(f"Built {len(sources)} standalone HTML files in {output_root}")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
