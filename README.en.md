# 2Download--reference_manifest

## What this is

This repository contains a narrowed-down OpenClaw skill with one clear purpose:

**turn a references list into a structured manifest for later manual downloading and curation.**

Its current capabilities are:
- parse references
- extract author / year / title / DOI
- enrich metadata with Crossref / OpenAlex hints
- expose `article_url` for the paper landing page
- expose `pdf_url_hint` for a likely PDF-oriented entry point
- write `ref_manifest.json`
- write `ref_manifest.md`
- write `ref_manifest.csv`
- detect likely duplicates
- optionally compare against a local PDF folder

---

## `article_url` vs `pdf_url_hint`

These are now two separate URL-style outputs:

- `article_url` — best-effort article webpage / DOI page / landing page
- `pdf_url_hint` — best-effort PDF-oriented hint, usually closer to a direct PDF route

In practice:
- use `article_url` when you want to open the paper webpage first
- use `pdf_url_hint` when you want a faster path toward the PDF

---

## Capabilities

### 1. Build a structured manifest from references text
Supported input:
- `.md`
- `.txt`

Supported patterns:
- numbered references
- unnumbered one-line references
- broken multi-line references merged before parsing

### 2. Extract core metadata
It tries to recover:
- index
- raw
- author
- first_author
- year
- title
- doi

### 3. Enrich metadata
It queries:
- Crossref
- OpenAlex

And can add:
- `resolved_doi`
- `article_url`
- `pdf_url_hint`
- `oa_pdf_hint`
- `needs_login_maybe`

### 4. Detect likely duplicates
It outputs:
- `duplicate_group`
- `duplicate_reason`

### 5. Compare with local PDFs
If `--local-pdf-dir` is provided, it tries to match local files using:
- DOI
- title tokens
- year
- author

And adds:
- `download_status`
- `local_pdf`
- `local_match_reason`

### 6. Generate three outputs
- `ref_manifest.json` — machine-friendly
- `ref_manifest.md` — human audit summary
- `ref_manifest.csv` — spreadsheet-friendly worklist
