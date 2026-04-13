# 2Download--reference_manifest

Language / 言語 / 语言:
- [中文说明](README.zh-CN.md)
- [English](README.en.md)
- [日本語](README.ja.md)

## What this repository is

This repository packages a small OpenClaw skill for one job:

**turn a references list into a structured manifest**

It is intentionally narrow.
It does **not** try to automatically log into publisher sites or download PDFs.
It focuses on the part that is stable and genuinely useful:

- parse references
- normalize citation metadata
- enrich entries with Crossref / OpenAlex hints
- generate `ref_manifest.json`
- generate `ref_manifest.md`
- generate `ref_manifest.csv`
- detect likely duplicates
- optionally compare against an existing local PDF folder

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
│   └── sample_ref_manifest.csv
└── scripts/
    ├── normalize_reference.py
    └── extract_ref_manifest.py
```

## License

MIT

## Examples

See `examples/` for a minimal input file and a sample CSV output.

## Quick start

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out
```

Optional local PDF comparison:

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out --local-pdf-dir ./papers
```

## Outputs

- `ref_manifest.json` — structured machine-readable manifest
- `ref_manifest.md` — quick audit summary
- `ref_manifest.csv` — easy manual review in Excel / Sheets

## Current capability

- numbered and unnumbered reference lines
- broken multi-line references merged before parsing
- title / year / author / DOI extraction
- Crossref lookup
- OpenAlex lookup
- duplicate grouping
- local PDF filename matching
- manual-download friendly CSV status fields

## What still needs improvement

- better support for more citation styles
- stronger parsing for messy Chinese / Japanese mixed references
- smarter local PDF matching beyond filename heuristics
- optional DOI-first verification mode
- richer duplicate detection for near-duplicate titles

## Intended usage model

This skill is best used as a **pre-download organizer**.
You feed it a references section, and it gives you a manifest that makes later manual downloading much faster and cleaner.
