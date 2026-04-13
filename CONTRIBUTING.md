# Contributing

## Scope

Please keep this repository focused.
This project is for **reference parsing and manifest generation**, not full browser-driven literature downloading.

## Good contributions

- improve citation parsing robustness
- improve duplicate detection
- improve local PDF matching
- improve multilingual documentation
- improve manifest output structure

## Avoid scope creep

Please do not re-expand this repository into:
- fragile browser automation
- publisher login workflows
- download state machines
- account / cookie handling

## Development quick check

```bash
python scripts/normalize_reference.py --help
python scripts/extract_ref_manifest.py --help
python scripts/extract_ref_manifest.py examples/sample_references.md --out-dir examples/out --sleep 0
```
