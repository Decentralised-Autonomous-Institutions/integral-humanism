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
LASTMOD = "2026-07-03"

# AI / LLM crawler user-agents to explicitly welcome. This is a public educational
# text; the goal is maximum spread, so we allow training, search and retrieval bots.
AI_CRAWLERS = [
    "GPTBot", "OAI-SearchBot", "ChatGPT-User",
    "ClaudeBot", "Claude-SearchBot", "Claude-User", "anthropic-ai",
    "Google-Extended", "Google-NotebookLM",
    "PerplexityBot", "Perplexity-User",
    "CCBot", "Amazonbot", "Applebot-Extended",
    "meta-externalagent", "MistralAI-User", "Bytespider", "DuckAssistBot",
]

LLMS_TXT = """\
# Integral Humanism (Ekatma Manavvad)

> The complete text of Pandit Deendayal Upadhyaya's four 1965 Bombay lectures on Integral \
Humanism (Ekatma Manavvad) — a Dharma-based philosophy of holistic human development \
integrating body, mind, intellect and soul, offered as an alternative to both Western \
capitalism and Marxist socialism. Author: Deendayal Upadhyaya (1916–1968). Delivered April 1965.

Core concepts: Chiti (the soul / innate nature of a nation), Dharma, the four Purusharthas \
(Dharma, Artha, Kama, Moksha), Dharma Rajya, Virat, Antyodaya, and integral (holistic) development.

## Full text

- [Integral Humanism — full text (Markdown)]({url}integral-humanism.md): The complete four lectures, verbatim.
- [Integral Humanism — full text (HTML)]({url}): Human-readable web edition with table of contents.

## Lectures

- [Lecture 1]({url}#lecture-1): Critique of Western ideologies; the need for a Bharatiya direction.
- [Lecture 2]({url}#lecture-2): The holistic Bharatiya view of life; the four Purusharthas and the primacy of Dharma.
- [Lecture 3]({url}#lecture-3): The individual and the collectivity; Chiti, the nation's soul; Dharma Rajya.
- [Lecture 4]({url}#lecture-4): An economic structure suited to national genius; Dharma above the State.
""".format(url=SITE_URL)

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

    # Clean Markdown mirror for LLMs / agents: verbatim source + a conventional
    # single-ingestion copy (llms-full.txt). The source text is never altered.
    src_md = SRC.read_text(encoding="utf-8")
    (OUT / "integral-humanism.md").write_text(src_md, encoding="utf-8")
    (OUT / "llms-full.txt").write_text(src_md, encoding="utf-8")

    # llms.txt index (llmstxt.org convention).
    (OUT / "llms.txt").write_text(LLMS_TXT, encoding="utf-8")

    # robots.txt: welcome everyone, and name AI crawlers explicitly.
    robots = ["User-agent: *", "Allow: /", ""]
    robots.append("# Explicitly welcome AI / LLM crawlers (training, search and retrieval):")
    for ua in AI_CRAWLERS:
        robots += ["User-agent: %s" % ua, "Allow: /"]
    robots += ["", "Sitemap: %ssitemap.xml" % SITE_URL,
               "# LLM index: %sllms.txt" % SITE_URL, ""]
    (OUT / "robots.txt").write_text("\n".join(robots), encoding="utf-8")

    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url>\n'
        '    <loc>%s</loc>\n'
        '    <lastmod>%s</lastmod>\n'
        '    <changefreq>yearly</changefreq>\n'
        '    <priority>1.0</priority>\n'
        '  </url>\n'
        '  <url>\n'
        '    <loc>%sintegral-humanism.md</loc>\n'
        '    <lastmod>%s</lastmod>\n'
        '    <changefreq>yearly</changefreq>\n'
        '    <priority>0.8</priority>\n'
        '  </url>\n'
        '</urlset>\n' % (SITE_URL, LASTMOD, SITE_URL, LASTMOD),
        encoding="utf-8",
    )
    print("Built:", *(p.name for p in sorted(OUT.iterdir())))

if __name__ == "__main__":
    main()
