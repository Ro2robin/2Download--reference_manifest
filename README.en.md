# 2Download--reference_manifest

## What this is

This repository contains a narrowed-down OpenClaw skill with one clear purpose:

**turn a references list into a structured manifest for later manual downloading and curation.**

Its current capabilities are:
- parse references
- extract author / year / title / DOI
- enrich metadata with Crossref / OpenAlex hints
- expose `article_url` that can directly open the paper landing page
- write `ref_manifest.json`
- write `ref_manifest.md`
- write `ref_manifest.csv`
- detect likely duplicates
- optionally compare against a local PDF folder

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
- `oa_pdf_hint`
- `needs_login_maybe`

### 4. URL is a key output
This is an important point.

The manifest tries to expose:
- `article_url`
- `crossref.url`

These fields can often be opened directly as:
- DOI page
- article landing page
- journal/paper webpage

So the skill does not only extract metadata. It also tries to give you a **clickable web entry point to the paper**.

### 5. Detect likely duplicates
It outputs:
- `duplicate_group`
- `duplicate_reason`

### 6. Compare with local PDFs
If `--local-pdf-dir` is provided, it tries to match local files using:
- DOI
- title tokens
- year
- author

And adds:
- `download_status`
- `local_pdf`
- `local_match_reason`

### 7. Generate three outputs
- `ref_manifest.json` — machine-friendly
- `ref_manifest.md` — human audit summary
- `ref_manifest.csv` — spreadsheet-friendly worklist

---

## Usage

### Basic

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out
```

### With local PDF comparison

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out --local-pdf-dir ./papers
```

### Parse a single reference

```bash
python scripts/normalize_reference.py "Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. Human Factors, 46(1), 50-80."
```

---

## Outputs

### `ref_manifest.json`
Best for downstream automation and scripting.

### `ref_manifest.md`
Best for quick manual review.

### `ref_manifest.csv`
Best for Excel / Sheets workflows, filtering, sorting, and manual download tracking.

### `article_url`
This is now emphasized as a first-class field.

It often points to:
- a DOI page
- an article landing page
- a paper webpage that can be opened directly in a browser

That makes later manual downloading much easier.

---

## Best use case

This skill is best used when:
1. you already have a references section
2. you want a clean, structured worklist first
3. you also want direct article web entry points where possible
4. you will then manually download, review, or archive papers

In plain terms, this is a:

**pre-download organizer / reference-manifest generator / article-entry-point extractor**

---

## What still needs improvement

Current improvement areas:
1. support for more citation styles
2. stronger parsing for mixed Chinese / English / Japanese references
3. more reliable local PDF matching beyond filename heuristics
4. richer near-duplicate detection
5. smarter ranking for `article_url` selection across Crossref / OpenAlex / DOI
