#!/usr/bin/env python3
"""Build the Integral Humanism static site into ./public via pandoc.

Source markdown is never modified; a normalized temp copy is used so the
inconsistent "### Lecture N" / "# Lecture N" headings become one clean level.
"""
import re, shutil, subprocess, tempfile, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "integral-humanism.md"
TEMPLATE = ROOT / "template.html"
STYLES = ROOT / "styles.css"
OUT = ROOT / "public"
SITE_URL = "https://integral-humanism.chiti.network/"
LASTMOD = "2026-07-01"

def normalize(md: str) -> str:
    # Promote "### Lecture N" -> "# Lecture N" for a consistent heading tree.
    md = re.sub(r"^###\s+(Lecture\s+\d+)\s*$", r"# \1", md, flags=re.M)
    return md

def main():
    OUT.mkdir(exist_ok=True)
    md = normalize(SRC.read_text(encoding="utf-8"))

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tf:
        tf.write(md)
        tmp = tf.name

    try:
        cmd = [
            "pandoc", tmp,
            # disable $...$ math so OCR artifacts like ($[V) aren't parsed as math
            "-f", "markdown-tex_math_dollars-tex_math_single_backslash",
            "-t", "html5",
            "-s",
            "--template", str(TEMPLATE),
            "--toc", "--toc-depth=2",
            "-o", str(OUT / "index.html"),
        ]
        subprocess.run(cmd, check=True)
    finally:
        os.unlink(tmp)

    shutil.copyfile(STYLES, OUT / "styles.css")

    (OUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % SITE_URL,
        encoding="utf-8",
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url>\n'
        '    <loc>%s</loc>\n'
        '    <lastmod>%s</lastmod>\n'
        '    <changefreq>yearly</changefreq>\n'
        '    <priority>1.0</priority>\n'
        '  </url>\n'
        '</urlset>\n' % (SITE_URL, LASTMOD),
        encoding="utf-8",
    )
    print("Built:", *(p.name for p in sorted(OUT.iterdir())))

if __name__ == "__main__":
    main()
