---
name: reference-manifest
description: Extract structured metadata from scholarly reference lists and generate a clean literature manifest for manual downloading or later curation. Use when the task is to parse a references section, normalize citations, recover fields like title/year/author/DOI, enrich entries with Crossref or OpenAlex hints, expose candidate article URLs that can directly open the paper landing page, detect likely duplicates, compare against an existing local PDF folder, and write `ref_manifest.json` / `ref_manifest.md` / `ref_manifest.csv`.
---

# Reference Manifest

Use this skill when the useful output is a **structured worklist of papers**.

## Core workflow

1. Start from a references file.
   - Prefer `.md` or `.txt`.
   - Numbered references are easiest, but plain one-line-per-reference input also works.
2. Normalize one noisy citation when needed.
   - Use `scripts/normalize_reference.py`.
3. Build the full manifest.
   - Use `scripts/extract_ref_manifest.py`.
4. Review the outputs.
   - `ref_manifest.json` for downstream scripts.
   - `ref_manifest.md` for quick human audit.
   - `ref_manifest.csv` for filtering, sorting, and manual literature tracking.
5. Check enrichment, duplicate hints, URL fields, and local-file matches.
   - The extractor emits likely duplicate groups.
   - It can compare entries against an existing local PDF folder.
   - It also exposes article/landing-page URLs that can be opened directly in a browser.

## Output expectations

A good row should include, when recoverable:
- index
- raw
- author
- first_author
- year
- title
- doi
- resolved_doi
- article_url — 文章网页入口 / article landing-page URL
- pdf_url_hint — PDF 链接线索 / PDF-oriented URL hint
- crossref summary
- openalex summary
- oa_pdf_hint
- needs_login_maybe
- duplicate_group
- duplicate_reason
- download_status
- local_pdf
- local_match_reason

## Scripts

- `scripts/normalize_reference.py` — normalize one citation string into a small JSON record.
- `scripts/extract_ref_manifest.py` — parse a references file and generate `ref_manifest.json` + `ref_manifest.md` + `ref_manifest.csv`.

## Good completion message

Report only:
- input file used
- output paths
- number of parsed references
- whether DOI / OA enrichment succeeded or partially failed
- whether article URLs were recovered
- whether likely duplicates were detected
- whether local PDF matching was performed
