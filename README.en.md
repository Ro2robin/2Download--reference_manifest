# 2Download--reference_manifest

## What this is

This repository contains a narrowed-down OpenClaw skill with one clear purpose:

**turn a references list into a structured manifest for later manual downloading and curation.**

It no longer tries to:
- log into publisher websites
- automate browser-based PDF downloading
- maintain a fragile download state machine

It keeps only the stable and useful part:
- parse references
- extract author / year / title / DOI
- enrich metadata with Crossref / OpenAlex hints
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

---

## Best use case

This skill is best used when:
1. you already have a references section
2. you do not want brittle automated downloading
3. you want a clean, structured worklist first
4. you will then manually download, review, or archive papers

In plain terms, this is a:

**pre-download organizer / reference-manifest generator**

not an all-purpose downloader.

---

## What still needs improvement

Current improvement areas:
1. support for more citation styles
2. stronger parsing for mixed Chinese / English / Japanese references
3. more reliable local PDF matching beyond filename heuristics
4. richer near-duplicate detection
5. optional DOI-first validation mode
6. stronger manual workflow fields for larger corpora

---

## Repository structure

```text
2Download--reference_manifest/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── README.en.md
├── README.ja.md
└── scripts/
    ├── normalize_reference.py
    └── extract_ref_manifest.py
```

---

## One-line summary

The value of this skill is not “download every PDF automatically.”

Its value is:

**turn a messy references list into an actionable, traceable manifest for manual literature work.**
