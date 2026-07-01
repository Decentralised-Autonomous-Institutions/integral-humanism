# Integral Humanism — integral-humanism.chiti.network

A static web edition of Pandit Deendayal Upadhyaya's 1965 lectures on
**Integral Humanism** (*Ekatma Manavvad*), published for study and search-engine
discoverability.

## Layout

| Path | Purpose |
|------|---------|
| `integral-humanism.md` | Source text (Markdown). The single source of truth. |
| `build.py` | Build script: Markdown → static HTML via pandoc. |
| `template.html` | Pandoc HTML template (SEO head, fonts, layout, TOC slot). |
| `styles.css` | Reading typography + responsive layout + Devanagari font. |
| `public/` | Built, deployable static site (upload this to the host). |

## Build

Requires [`pandoc`](https://pandoc.org) and Python 3.

```bash
python3 build.py
```

This regenerates `public/{index.html,styles.css,robots.txt,sitemap.xml}`.

## Deploy (Cloudflare Pages)

- **Direct upload:** Cloudflare dashboard → Workers & Pages → Create → Pages →
  Upload assets → drag the `public/` folder.
- **Git integration:** connect this repo, set *build output directory* to `public`
  and leave the build command empty (the built `public/` is committed).

Custom domain: `integral-humanism.chiti.network` (DNS at Namecheap → CNAME to the
`*.pages.dev` target, or move the zone to Cloudflare).

## Notes

The Devanagari terms (चिति *Chiti*, विकृति *vikṛti*, सर्वोपरि *sarvopari*,
निधर्मी *NiDharn*, धर्मनिरपेक्ष *Dharmanirapekha*, etc.) were transcribed to proper
Unicode from the source PDF, which stored them in a legacy non-Unicode font.
