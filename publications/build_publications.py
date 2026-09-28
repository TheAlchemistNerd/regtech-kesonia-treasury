#!/usr/bin/env python3
"""Build KESONIA technical, LinkedIn, bibliography and method publications."""

from __future__ import annotations

import argparse
import hashlib
import html as html_tools
import json
import os
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit, urlunsplit


PARTS = (
    "Part1_KESONIA_Reform_and_Enterprise_Architecture.md",
    "Part2_Daily_Compounding_Engine_Mathematics_and_SQL.md",
    "Part3_AI_Pricing_Engine_and_IFRS9_Integration.md",
    "Part4_RegTech_Sweep_Platform_Deep_Dives_and_Roadmap.md",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path, timeout_seconds: float = 600) -> subprocess.CompletedProcess[str]:
    """Bound each tool invocation, including Mermaid/Chromium descendants."""
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, encoding="utf-8", errors="replace",
                               start_new_session=os.name != "nt")
    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            # Only this invocation's PID and descendant tree; never kill by
            # executable name, which could interrupt unrelated browser work.
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15, check=False)
        else:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        try:
            stdout, stderr = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.stdout.close()
            process.stderr.close()
            stdout, stderr = "", "Tool pipes did not close after process-tree termination."
        raise RuntimeError(f"Tool exceeded {timeout_seconds:g}s: {command[0]}. "
                           f"Its process tree was terminated. Output: {(stdout + stderr)[-4000:]}")
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def mermaid_count(node: object) -> int:
    if isinstance(node, list):
        return sum(mermaid_count(item) for item in node)
    if not isinstance(node, dict):
        return 0
    if node.get("t") == "CodeBlock" and "mermaid" in node["c"][0][1]:
        return 1
    return sum(mermaid_count(value) for value in node.values())


def diagram_hashes(node: object) -> list[str]:
    if isinstance(node, list):
        return [value for item in node for value in diagram_hashes(item)]
    if not isinstance(node, dict):
        return []
    if node.get("t") == "CodeBlock" and "mermaid" in node["c"][0][1]:
        return [hashlib.sha1(node["c"][1].encode("utf-8")).hexdigest()]
    return [value for item in node.values() for value in diagram_hashes(item)]


def local_target(url: str, source: Path):
    """Resolve a hyperlink in the source document's coordinate system."""
    # Windows drive paths must not be mistaken for a URI scheme.
    windows_path = bool(re.match(r"^[A-Za-z]:[\\/]", url))
    parts = urlsplit(url if not windows_path else "file:///" + url.replace("\\", "/"))
    if parts.scheme and parts.scheme.lower() != "file":
        return None
    if parts.netloc and parts.scheme != "file":  # e.g. //example.org/reference
        return None
    if parts.scheme == "file" and parts.netloc:
        raise ValueError(f"UNC/network file links are not supported by this local publisher: {url}")
    path = unquote(parts.path)
    # Repository review notes may use editor-style file.md:123 references.
    # Line numbers are retained in the report, not sent to a browser as a
    # nonexistent filename or an invented HTML fragment.
    line_match = re.search(r":(\d+)$", path)
    source_line = int(line_match.group(1)) if line_match else None
    if line_match:
        path = path[:line_match.start()]
    if parts.scheme == "file" and re.match(r"^/[A-Za-z]:/", path):
        path = path[1:]
    if not path:
        target = source
    else:
        candidate = Path(path)
        target = candidate if candidate.is_absolute() else source.parent / candidate
    return target.resolve(), parts.query, unquote(parts.fragment), source_line


def rewrite_links(document: str, source: Path, output: Path, source_outputs: dict[Path, Path]):
    """Rebase all quoted HTML anchor hrefs, including raw-HTML source anchors."""
    links = []

    def replace(match):
        original = html_tools.unescape(match.group(3))
        resolved = local_target(original, source)
        if resolved is None:
            return match.group(0)
        target_source, query, fragment, source_line = resolved
        target_output = source_outputs.get(target_source, target_source)
        try:
            relative = Path(os.path.relpath(target_output, output.parent)).as_posix()
            rewritten = urlunsplit(("", "", quote(relative, safe="/"), query, quote(fragment, safe="-._~:!$&'()*+,;=@/?")))
        except ValueError:  # A different Windows drive cannot have a relative URL.
            rewritten = target_output.as_uri()
            if query:
                rewritten += "?" + query
            if fragment:
                rewritten += "#" + quote(fragment)
        links.append({"original": original, "href": rewritten, "source_target": target_source,
                      "target": target_output, "fragment": fragment,
                      "source_line": source_line,
                      "converted_source": target_source in source_outputs})
        return match.group(1) + match.group(2) + html_tools.escape(rewritten, quote=True) + match.group(2)

    rewritten = re.sub(r'(<a\b[^>]*?\bhref\s*=\s*)([\"\'])(.*?)(?:\2)', replace,
                       document, flags=re.IGNORECASE | re.DOTALL)
    return rewritten, links


class Images(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sources: list[str] = []
        self.unrendered_mermaid = False
        self.identifiers: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.identifiers.add(attributes["id"])
        if tag == "a" and attributes.get("name"):
            self.identifiers.add(attributes["name"])
        if tag == "img":
            self.sources.append(attributes.get("src") or "")
        if tag in {"code", "pre"} and "mermaid" in (attributes.get("class") or ""):
            self.unrendered_mermaid = True


def validate_links(records: list[dict], inspections: dict[Path, Images],
                   strict_fragments: bool = True) -> list[dict]:
    checked = []
    for link in records:
        target, fragment = link["target"], link["fragment"]
        target_type = "file"
        if target in inspections:
            identifiers = inspections[target].identifiers
        elif target.is_dir() and not fragment:
            identifiers = None
            target_type = "directory"
        elif not target.is_file():
            raise ValueError(f"Broken local link: {link['original']} resolves to missing file {target}")
        elif target.suffix.lower() in {".html", ".htm"}:
            inspection = Images()
            inspection.feed(target.read_text(encoding="utf-8"))
            identifiers = inspection.identifiers
        else:
            identifiers = None
        missing_fragment = bool(fragment and identifiers is not None and fragment not in identifiers)
        if missing_fragment and strict_fragments:
            raise ValueError(f"Missing local fragment #{fragment} in {target}")
        checked.append({"original": link["original"], "href": link["href"],
                        "source_line": link.get("source_line"),
                        "converted_source": link["converted_source"],
                        "target_type": target_type,
                        "target_exists": True,
                        "fragment_check": "warning_missing_historical_fragment" if missing_fragment else
                                          "passed" if fragment and identifiers is not None else
                                          "not_applicable" if not fragment else "not_checked_non_html_target"})
    return checked


def write_report(path: Path, report: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-diagrams", action="store_true",
                        help="Render diagrams using mmdc instead of inherited cached PNGs.")
    parser.add_argument("--command-timeout-seconds", type=float, default=600,
                        help="Maximum seconds per Pandoc invocation, including diagram rendering (default: 600).")
    args = parser.parse_args()
    if args.command_timeout_seconds <= 0:
        parser.error("--command-timeout-seconds must be positive")
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
    sources += [(path, Path("methods") / (path.stem + ".html"))
                for path in sorted((repository_root / "docs" / "methods").glob("*.md"))]
    output_root = publication_root / "build"
    output_root.mkdir(parents=True, exist_ok=True)
    report = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "running", "mode": "refresh" if args.refresh_diagrams else "cached",
        "scope": "HTML rendering, embedded images and local link targets/fragments; no financial or PDF validation",
        "source_count": len(sources), "sources": [], "published": False,
        "command_timeout_seconds": args.command_timeout_seconds,
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
        report["pandoc_version"] = run([pandoc, "--version"], publication_root,
                                       args.command_timeout_seconds).stdout.splitlines()[0]
        report["inherited_asset_hashes"] = {
            path.relative_to(publication_root).as_posix(): sha256(path)
            for path in assets + sorted((publication_root / "images").glob("*")) if path.is_file()
        }
        # Each run and document owns its workspace and source-addressed cache.
        with tempfile.TemporaryDirectory(prefix="kesonia-publishing-") as temporary:
            workspace = Path(temporary)
            staged: list[tuple[Path, Path]] = []
            staged_cache: dict[str, Path] = {}
            source_outputs = {source.resolve(): (output_root / relative).resolve() for source, relative in sources}
            inspections: dict[Path, Images] = {}
            link_records: list[list[dict]] = []
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
                # Reuse only diagrams freshly generated/verified in this same
                # sequential run; refresh ignores all pre-existing hash caches.
                for name, cached in staged_cache.items():
                    shutil.copy2(cached, job / "images" / name)
                local_source = job / source.name
                shutil.copy2(source, local_source)
                record = {
                    "source": source.relative_to(repository_root).as_posix(),
                    "sha256": sha256(source), "source_sha256": sha256(source), "output": relative_output.as_posix(),
                    "status": "running", "inline_image_count": 0, "warnings": [],
                }
                report["sources"].append(record)
                print(f"Rendering {record['source']} (limit {args.command_timeout_seconds:g}s per tool call)", flush=True)
                parsed = run([pandoc, str(local_source), "--from=markdown", "--to=json"], job,
                             args.command_timeout_seconds)
                if parsed.returncode:
                    raise RuntimeError(f"Pandoc could not parse {source.name}: {parsed.stderr.strip()}")
                tree = json.loads(parsed.stdout)
                expected_diagrams = mermaid_count(tree)
                hashes = diagram_hashes(tree)
                record["mermaid_diagram_count"] = expected_diagrams
                record["diagram_source_sha1"] = hashes
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
                rendered = run(command, job, args.command_timeout_seconds)
                warnings = [text.strip() for text in (parsed.stderr, rendered.stderr) if text.strip()]
                record["warnings"] = warnings
                if rendered.returncode or not output.is_file():
                    raise RuntimeError(f"Rendering failed for {source.name}: {'; '.join(warnings)}")
                html, links = rewrite_links(output.read_text(encoding="utf-8"), source.resolve(),
                                           (output_root / relative_output).resolve(), source_outputs)
                output.write_text(html, encoding="utf-8")
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
                for digest in hashes:
                    name = f"mermaid_{digest}.png"
                    cached = job / "images" / name
                    if not cached.is_file() or cached.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
                        raise RuntimeError(f"Missing or invalid source-hash diagram cache: {name}")
                    staged_cache[name] = cached
                record["output_sha256"] = sha256(output)
                record["status"] = "rendered_pending_link_validation"
                inspections[(output_root / relative_output).resolve()] = inspection
                link_records.append(links)
                staged.append((output, output_root / relative_output))
                print(f"Rendered {record['source']}: {len(inline)} embedded images", flush=True)
            for record, links in zip(report["sources"], link_records):
                record["status"] = "validating_links"
                strict = (record["source"].startswith("docs/methods/") or
                          Path(record["source"]).name in PARTS and record["source"].startswith("docs/"))
                record["local_links"] = validate_links(links, inspections, strict_fragments=strict)
                for link in record["local_links"]:
                    if link["fragment_check"] == "warning_missing_historical_fragment":
                        record["warnings"].append("Historical fragment not found: " + link["original"])
                record["status"] = "passed"
            report["diagram_cache_hashes"] = {name: sha256(path) for name, path in sorted(staged_cache.items())}
            # Source-hash caches become reusable only after every render/link
            # passes; caption-named inherited PNGs are never trusted or replaced.
            for name, cached in staged_cache.items():
                shutil.copy2(cached, publication_root / "images" / name)
            # Existing HTML survives parsing, rendering or link-check failure.
            for staged_output, destination in staged:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(staged_output, destination)
        report["status"] = "passed"
        report["published"] = True
    except (OSError, ValueError, RuntimeError) as error:
        report["status"] = "failed"
        report["error"] = str(error)
        for record in report["sources"]:
            if record["status"] in {"running", "validating_links"}:
                record["status"] = "failed"
                record["error"] = str(error)
        print(f"Build failed: {error}", file=sys.stderr)
    finally:
        report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        write_report(output_root / "build_report.json", report)
    if report["status"] == "passed":
        print(f"Built {len(sources)} standalone HTML files in {output_root}")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
