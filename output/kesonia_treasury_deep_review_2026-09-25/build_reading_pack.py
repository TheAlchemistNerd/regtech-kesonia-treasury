"""Render this repository's existing review notes locally; no cross-project writes."""
from pathlib import Path
import argparse
import html
import re
import shutil
import subprocess
from urllib.parse import unquote

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pandoc', default=shutil.which('pandoc'))
    args = parser.parse_args()
    if not args.pandoc:
        parser.error('Pandoc is required; pass --pandoc with its executable path')
    pack = Path(__file__).resolve().parent
    docs = sorted(pack.glob('[0-9][0-9]_*.md'))
    for md in docs:
        title = re.search(r'^# (.+)$', md.read_text(encoding='utf-8-sig'), re.M).group(1)
        run = subprocess.run([args.pandoc, str(md), '--standalone', '--toc', '--mathml',
            '--from=markdown+tex_math_single_backslash', '--css=review.css',
            '--metadata', 'pagetitle='+title], check=True, capture_output=True, encoding='utf-8')
        def link(match):
            raw = html.unescape(match.group(1))
            target, sep, fragment = unquote(raw).partition('#')
            p = Path(target)
            if target == '../../docs/methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.md':
                return 'href="../../publications/build/methods/REVIEW_INTEGRATION_AND_REMAINING_WORK.html"'
            if p.is_absolute():
                raw = p.as_uri()+('#'+fragment if sep else '')
            elif target.endswith('.md') and (md.parent/target).with_suffix('.html').exists():
                raw = target[:-3]+'.html'+('#'+fragment if sep else '')
            return 'href="'+html.escape(raw, quote=True)+'"'
        rendered = re.sub(r'href="([^"]+)"', link, run.stdout)
        md.with_suffix('.html').write_text(rendered, encoding='utf-8')
    print(f'Rendered {len(docs)} local review documents')

if __name__ == '__main__':
    main()
