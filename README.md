# 2Download--reference_manifest

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](./SKILL.md)
[![Language](https://img.shields.io/badge/Docs-zh--CN%20%7C%20en%20%7C%20ja-orange)](./README.zh-CN.md)

Language / 言語 / 语言:
- [中文说明](README.zh-CN.md)
- [English](README.en.md)
- [日本語](README.ja.md)

## What this repository is

This repository packages a focused OpenClaw skill for one job:

**turn a references list into a structured manifest**

It is intentionally narrow and stable.
It does **not** try to automate fragile publisher logins or browser-driven PDF downloading.
It keeps only the part that is genuinely reusable:

- parse references
- normalize citation metadata
- enrich entries with Crossref / OpenAlex hints
- generate `ref_manifest.json`
- generate `ref_manifest.md`
- generate `ref_manifest.csv`
- detect likely duplicates
- optionally compare against an existing local PDF folder

## Feature overview

| Feature | Status | Notes |
|---|---|---|
| Numbered reference parsing | ✅ | `1. ...` style works well |
| Unnumbered one-line parsing | ✅ | Basic support |
| Broken multi-line reference merge | ✅ | Merges before parsing |
| DOI extraction | ✅ | Direct DOI + resolved DOI |
| Crossref enrichment | ✅ | Best-effort |
| OpenAlex enrichment | ✅ | Best-effort |
| JSON output | ✅ | Main machine-readable manifest |
| MD output | ✅ | Human audit summary |
| CSV output | ✅ | Spreadsheet workflow |
| Duplicate grouping | ✅ | Conservative heuristics |
| Local PDF folder matching | ✅ | Filename heuristic |
| Automatic PDF downloading | ❌ | Deliberately removed |

## Workflow

```text
references.md / references.txt
        ↓
parse + normalize
        ↓
Crossref / OpenAlex enrichment
        ↓
duplicate detection
        ↓
optional local PDF matching
        ↓
ref_manifest.json / .md / .csv
```

## Quick start

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out
```

Optional local PDF comparison:

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out --local-pdf-dir ./papers
```

Parse a single reference:

```bash
python scripts/normalize_reference.py "Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. Human Factors, 46(1), 50-80."
```

## Outputs

- `ref_manifest.json` — structured machine-readable manifest
- `ref_manifest.md` — quick audit summary
- `ref_manifest.csv` — easy manual review in Excel / Sheets

## Repository structure

```text
2Download--reference_manifest/
├── SKILL.md
├── LICENSE
├── README.md
├── README.zh-CN.md
├── README.en.md
├── README.ja.md
├── examples/
│   ├── README.md
│   ├── sample_references.md
│   ├── sample_ref_manifest.json
│   ├── sample_ref_manifest.md
│   ├── sample_ref_manifest.csv
│   └── sample_run.sh
└── scripts/
    ├── normalize_reference.py
    └── extract_ref_manifest.py
```

## Examples

See `examples/` for:
- minimal input references
- sample JSON output
- sample MD output
- sample CSV output
- a minimal run command

## Intended usage model

This skill is best used as a **pre-download organizer**.
You feed it a references section, and it gives you a manifest that makes later manual downloading much faster and cleaner.

## What still needs improvement

- better support for more citation styles
- stronger parsing for messy Chinese / Japanese mixed references
- smarter local PDF matching beyond filename heuristics
- optional DOI-first verification mode
- richer duplicate detection for near-duplicate titles
- stronger spreadsheet workflow fields for large corpora

## License

MIT
