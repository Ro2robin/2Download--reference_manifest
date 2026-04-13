---
name: reference-manifest
description: Extract structured metadata from scholarly reference lists and generate a clean literature manifest for manual downloading or later curation. Use when the task is to parse a references section, normalize citations, recover fields like title/year/author/DOI, enrich entries with Crossref or OpenAlex hints, detect likely duplicates, compare against an existing local PDF folder, and write `ref_manifest.json` / `ref_manifest.md` / `ref_manifest.csv`.
---

# Reference Manifest

Use this skill when the useful output is a **structured worklist of papers**, not automatic downloading.

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
   - `ref_manifest.csv` for filtering, sorting, and manual download tracking.
5. Check duplicate hints and local-file matches.
   - The extractor emits likely duplicate groups.
   - It can also compare entries against an existing local PDF folder and mark likely matches.
6. Use the manifest for manual download, deduplication, or later annotation.

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
- whether likely duplicates were detected
- whether local PDF matching was performed
