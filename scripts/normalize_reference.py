from __future__ import annotations

import argparse
import json
import re


def clean(text: str) -> str:
    text = text or ""
    text = text.replace("−", "-").replace("–", "-").replace("—", "-")
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_reference(raw: str) -> dict:
    raw = clean(raw)
    m = re.match(r"^(?P<author>.+?)\.\s*\((?P<year>\d{4}[a-z]?)\)\.\s*(?P<title>.+?)\.\s*(?P<rest>.*)$", raw)
    if not m:
        return {"raw": raw, "parsed": False, "reason": "pattern_miss"}
    doi_match = re.search(r"(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", raw, re.I)
    return {
        "raw": raw,
        "parsed": True,
        "author": m.group("author").strip(),
        "year": m.group("year").strip(),
        "title": m.group("title").strip(),
        "rest": m.group("rest").strip(),
        "doi": doi_match.group(1) if doi_match else "",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize one literature reference into a simple JSON record")
    ap.add_argument("reference")
    args = ap.parse_args()
    print(json.dumps(parse_reference(args.reference), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
