"""Isolated publisher checks; no repository publication outputs are changed."""
import importlib.util
from pathlib import Path
import subprocess
import shutil
import tempfile
import hashlib
import sys
import unittest

HERE = Path(__file__).resolve().parents[1] / "publications"
spec = importlib.util.spec_from_file_location("publisher", HERE / "build_publications.py")
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


class PublishingChecks(unittest.TestCase):
    def test_command_success_and_bounded_timeout(self):
        completed = publisher.run([sys.executable, '-c', 'print(42)'], self.base, 10)
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout.strip(), '42')
        with self.assertRaisesRegex(RuntimeError, 'Tool exceeded'):
            publisher.run([sys.executable, '-c', 'import time; time.sleep(10)'], self.base, .2)

    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="kesonia-publication-tests-")
        cls.base = Path(cls.temporary.name)
        cls.source = cls.base / "docs" / "a.md"
        cls.other = cls.base / "docs" / "b.md"
        cls.out = cls.base / "build" / "a.html"
        cls.other_out = cls.base / "build" / "b.html"
        cls.source.parent.mkdir(parents=True, exist_ok=True)
        cls.out.parent.mkdir(parents=True, exist_ok=True)
        cls.source.write_text("# Section\n", encoding="utf-8")
        cls.other.write_text("# Other\n", encoding="utf-8")
        cls.mapping = {cls.source.resolve(): cls.out.resolve(), cls.other.resolve(): cls.other_out.resolve()}

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_relative_fragment_and_known_source(self):
        html, links = publisher.rewrite_links('<a href="b.md#other">B</a><a href="#section">self</a>',
                                             self.source, self.out, self.mapping)
        self.assertIn('href="b.html#other"', html)
        self.assertIn('href="a.html#section"', html)
        first, second = publisher.Images(), publisher.Images()
        first.feed('<h1 id="other">'); second.feed('<h1 id="section">')
        checks = publisher.validate_links(links, {self.other_out.resolve(): first, self.out.resolve(): second})
        self.assertEqual([c["fragment_check"] for c in checks], ["passed", "passed"])

    def test_external_schemes_and_query_are_preserved(self):
        html, links = publisher.rewrite_links('<a href="https://example.org/a?q=1&amp;b=2">x</a><a href="mailto:a@b.c">mail</a>',
                                             self.source, self.out, self.mapping)
        self.assertEqual(links, [])
        self.assertIn('https://example.org/a?q=1&amp;b=2', html)
        html, _ = publisher.rewrite_links('<a href="b.md?mode=1#other">B</a>', self.source, self.out, self.mapping)
        self.assertIn('b.html?mode=1#other', html)

    def test_editor_line_and_rebase_unconverted(self):
        path = self.other.resolve().as_posix() + ":42"
        html, links = publisher.rewrite_links('<a href="' + path + '">B</a>', self.source, self.out, {})
        self.assertNotIn(':42', html)
        self.assertEqual(links[0]["source_line"], 42)
        self.assertEqual(links[0]["target"], self.other.resolve())
        self.assertIn('../docs/b.md', html)
        publisher.validate_links(links, {})

    def test_missing_target_and_fragment_failure(self):
        _, links = publisher.rewrite_links('<a href="missing.md">x</a>', self.source, self.out, self.mapping)
        with self.assertRaisesRegex(ValueError, "Broken local link"):
            publisher.validate_links(links, {})
        _, links = publisher.rewrite_links('<a href="b.md#missing">x</a>', self.source, self.out, self.mapping)
        inspection = publisher.Images()
        with self.assertRaisesRegex(ValueError, "Missing local fragment"):
            publisher.validate_links(links, {self.other_out.resolve(): inspection})
        checks = publisher.validate_links(links, {self.other_out.resolve(): inspection}, strict_fragments=False)
        self.assertEqual(checks[0]["fragment_check"], "warning_missing_historical_fragment")

    def test_existing_directory_link_without_fragment(self):
        _, links = publisher.rewrite_links('<a href="../docs/">directory</a>',
                                             self.source, self.out, self.mapping)
        checks = publisher.validate_links(links, {})
        self.assertEqual(checks[0]["target_type"], "directory")
        self.assertTrue(checks[0]["target_exists"])
        self.assertEqual(checks[0]["fragment_check"], "not_applicable")
        _, links = publisher.rewrite_links('<a href="../docs/#unsupported">directory</a>',
                                             self.source, self.out, self.mapping)
        with self.assertRaises(ValueError):
            publisher.validate_links(links, {})

    @unittest.skipUnless(shutil.which("pandoc"), "Pandoc is optional for the financial test suite")
    def test_source_hash_changes_and_lua_cache_key(self):
        # Intentionally incomplete PNG-signature fixture: exercises only the
        # Lua cache path/signature guard, without rendering or embedding it.
        # This does not validate PNG decoding or the diagram's visual content.
        source = "graph TD\n  A --> B"
        ast = {"t": "CodeBlock", "c": [["", ["mermaid"], []], source]}
        digest = hashlib.sha1(source.encode()).hexdigest()
        self.assertEqual(publisher.diagram_hashes(ast), [digest])
        ast["c"][1] += "\n  B --> C"
        self.assertNotEqual(publisher.diagram_hashes(ast), [digest])
        images = self.base / "images"
        images.mkdir(exist_ok=True)
        (images / ("mermaid_" + digest + ".png")).write_bytes(b"\x89PNG\r\n\x1a\nfixture")
        markdown = self.base / "cache_fixture.md"
        markdown.write_text("```mermaid\n" + source + "\n```\n", encoding="utf-8")
        result = subprocess.run(["pandoc", str(markdown), "--from=markdown", "--to=html5",
                                 "--lua-filter=" + str(HERE / "mermaid.lua")],
                                cwd=self.base, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("images/mermaid_" + digest + ".png", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
