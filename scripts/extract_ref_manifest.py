from __future__ import annotations

import argparse
import csv
import json
import re
import time
from pathlib import Path
from typing import Optional
from urllib.parse import quote

import requests

TIMEOUT = 25
S = requests.Session()
S.headers.update(
    {
        "User-Agent": "OpenClaw-ref-manifest/1.4 (mailto:none)",
        "Accept": "application/json, text/plain, */*",
    }
)


def norm(text: str) -> str:
    text = text or ""
    text = text.lower()
    text = text.replace("−", "-").replace("–", "-").replace("—", "-")
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"doi:\s*", "", text, flags=re.I)
    text = re.sub(r"[^\w\s\u4e00-\u9fff-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def merge_broken_lines(text: str) -> list[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    merged: list[str] = []
    buf = ""
    for line in lines:
        numbered = bool(re.match(r"^\[?\d+[\].、.]\s+", line) or re.match(r"^\d+\s+", line))
        if numbered and buf:
            merged.append(buf.strip())
            buf = re.sub(r"^\[?\d+[\].、.]\s+", "", line)
        elif numbered:
            buf = re.sub(r"^\[?\d+[\].、.]\s+", "", line)
        else:
            if not buf:
                buf = line
            else:
                joiner = "" if re.match(r"^[,.;:)\]]", line) else " "
                buf += joiner + line
    if buf:
        merged.append(buf.strip())
    return merged


def extract_title(raw: str) -> str:
    patterns = [
        r"\(\d{4}[a-z]?\)\.\s*(.+?)\.\s*[A-Z\u4e00-\u9fff]",
        r"\(\d{4}[a-z]?\)\s*(.+?)\.\s*[A-Z\u4e00-\u9fff]",
        r"\.\s*([^\.]{8,220}?)\.\s*(?:[A-Z][a-z]+|[\u4e00-\u9fff]{2,})",
    ]
    for pat in patterns:
        m = re.search(pat, raw)
        if m:
            return m.group(1).strip()
    parts = [p.strip() for p in raw.split(". ") if p.strip()]
    if len(parts) >= 2:
        return parts[1][:220]
    return raw[:220]


def parse_refs(text: str) -> list[dict]:
    refs: list[dict] = []
    entries = merge_broken_lines(text)
    for i, raw in enumerate(entries, start=1):
        author = raw.split(".", 1)[0].strip()
        first_author = author.split(",")[0].split("&")[0].split("等")[0].strip()
        year_m = re.search(r"\((\d{4}[a-z]?)\)", raw)
        if not year_m:
            year_m = re.search(r"\b(19\d{2}|20\d{2})\b", raw)
        year = year_m.group(1) if year_m else ""
        doi_m = re.search(r"(10\.\d{4,9}/[^\s;]+)", raw, re.I)
        doi = doi_m.group(1).rstrip(" .);,") if doi_m else ""
        title = extract_title(raw)
        refs.append(
            {
                "index": i,
                "raw": raw,
                "author": author,
                "first_author": first_author,
                "year": year,
                "doi": doi,
                "title": title,
            }
        )
    return refs


def score_candidate(title: str, first_author: str, year: str, item: dict) -> dict:
    cand_title = item.get("title", [""]) if isinstance(item.get("title"), list) else item.get("title", "")
    if isinstance(cand_title, list):
        cand_title = cand_title[0] if cand_title else ""
    cand_authors = item.get("author", []) or []
    cand_year = ""
    issued = item.get("issued", {}).get("date-parts", [])
    if issued and issued[0]:
        cand_year = str(issued[0][0])
    cand_doi = item.get("DOI", "")
    t1 = norm(title)
    t2 = norm(cand_title)
    overlap = 0
    if t1 and t2:
        toks = [t for t in t1.split() if len(t) >= 3]
        overlap = sum(1 for t in toks if t in t2)
    first_author_hit = False
    if cand_authors:
        fam = norm(cand_authors[0].get("family", ""))
        given = norm(cand_authors[0].get("given", ""))
        a = norm(first_author)
        if (fam and fam in a) or (given and given.split(" ")[0] in a):
            first_author_hit = True
    year_hit = bool(year and cand_year == year)
    score = overlap + (4 if first_author_hit else 0) + (2 if year_hit else 0) + (2 if cand_doi else 0)
    return {
        "score": score,
        "title": cand_title,
        "doi": cand_doi,
        "year": cand_year,
        "first_author_hit": first_author_hit,
        "year_hit": year_hit,
        "container": (item.get("container-title") or [""])[0]
        if isinstance(item.get("container-title"), list)
        else item.get("container-title", ""),
        "url": item.get("URL", ""),
        "type": item.get("type", ""),
    }


def crossref_lookup(title: str, first_author: str, year: str) -> Optional[dict]:
    url = f"https://api.crossref.org/works?rows=5&query.title={quote(title)}"
    r = S.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    items = r.json().get("message", {}).get("items", [])
    best = None
    for item in items:
        cand = score_candidate(title, first_author, year, item)
        if best is None or cand["score"] > best["score"]:
            best = cand
    return best


def openalex_lookup(title: str, first_author: str, year: str) -> Optional[dict]:
    url = f"https://api.openalex.org/works?per-page=5&search={quote(title)}"
    r = S.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    results = r.json().get("results", [])
    best = None
    for item in results:
        item2 = {
            "title": item.get("display_name", ""),
            "DOI": (item.get("doi") or "").replace("https://doi.org/", ""),
            "URL": item.get("id", ""),
            "type": item.get("type", ""),
            "container-title": [item.get("primary_location", {}).get("source", {}).get("display_name", "")],
            "author": [{"family": a.get("author", {}).get("display_name", "")} for a in (item.get("authorships") or [])[:3]],
            "issued": {"date-parts": [[str(item.get("publication_year") or "")]]},
        }
        cand = score_candidate(title, first_author, year, item2)
        cand["open_access"] = item.get("open_access", {})
        cand["openalex_url"] = item.get("id", "")
        if best is None or cand["score"] > best["score"]:
            best = cand
    return best


def pick_article_url(rec: dict) -> str:
    if rec.get("crossref") and rec["crossref"].get("url"):
        return rec["crossref"].get("url") or ""
    if rec.get("openalex") and rec["openalex"].get("url"):
        return rec["openalex"].get("url") or ""
    if rec.get("resolved_doi"):
        return f"https://doi.org/{rec['resolved_doi']}"
    return ""


def build_manifest(refs: list[dict], sleep_s: float = 0.6) -> list[dict]:
    rows = []
    total = len(refs)
    for i, ref in enumerate(refs, start=1):
        rec = dict(ref)
        rec["lookup"] = "given_doi" if ref["doi"] else "searched"
        rec["crossref"] = None
        rec["openalex"] = None
        rec["resolved_doi"] = ref["doi"]
        rec["article_url"] = f"https://doi.org/{ref['doi']}" if ref["doi"] else ""
        rec["needs_login_maybe"] = False
        rec["oa_pdf_hint"] = ""
        rec["duplicate_group"] = ""
        rec["duplicate_reason"] = ""
        rec["download_status"] = "pending"
        rec["local_pdf"] = ""
        rec["local_match_reason"] = ""
        if not ref["doi"] and ref["title"]:
            try:
                cr = crossref_lookup(ref["title"], ref["first_author"], ref["year"])
                rec["crossref"] = cr
                if cr and cr.get("score", 0) >= 8 and cr.get("doi"):
                    rec["resolved_doi"] = cr["doi"]
            except Exception as e:
                rec["crossref_error"] = type(e).__name__
            time.sleep(sleep_s)
        if ref["title"]:
            try:
                oa = openalex_lookup(ref["title"], ref["first_author"], ref["year"])
                rec["openalex"] = oa
                if oa and isinstance(oa.get("open_access"), dict):
                    rec["oa_pdf_hint"] = oa["open_access"].get("oa_url") or ""
            except Exception as e:
                rec["openalex_error"] = type(e).__name__
        rec["article_url"] = pick_article_url(rec)
        if rec["resolved_doi"] and not rec["oa_pdf_hint"]:
            rec["needs_login_maybe"] = True
        rows.append(rec)
        print(f"[{i}/{total}] {ref['index']} {ref['title'][:80]}")
        time.sleep(sleep_s)
    return rows


def detect_duplicates(rows: list[dict]) -> list[dict]:
    groups: dict[str, list[int]] = {}
    for i, row in enumerate(rows):
        if row.get("resolved_doi"):
            key = f"doi::{norm(row['resolved_doi'])}"
        else:
            key = f"title::{norm(row.get('title',''))}::{norm(row.get('year',''))}::{norm(row.get('first_author',''))}"
        groups.setdefault(key, []).append(i)
    group_id = 1
    for key, idxs in groups.items():
        if len(idxs) <= 1:
            continue
        reason = "same_resolved_doi" if key.startswith("doi::") else "same_title_year_author"
        gid = f"dup_{group_id:03d}"
        for idx in idxs:
            rows[idx]["duplicate_group"] = gid
            rows[idx]["duplicate_reason"] = reason
        group_id += 1
    return rows


def build_local_pdf_index(local_pdf_dir: Path) -> list[dict]:
    rows = []
    for p in local_pdf_dir.rglob("*.pdf"):
        stem = p.stem
        rows.append({"path": str(p), "stem_norm": norm(stem), "name": p.name})
    return rows


def match_local_pdfs(rows: list[dict], local_pdf_dir: Optional[Path]) -> list[dict]:
    if not local_pdf_dir:
        return rows
    pdfs = build_local_pdf_index(local_pdf_dir)
    for row in rows:
        title_n = norm(row.get("title", ""))
        year_n = norm(row.get("year", ""))
        author_n = norm(row.get("first_author", ""))
        for pdf in pdfs:
            stem = pdf["stem_norm"]
            if row.get("resolved_doi") and norm(row["resolved_doi"]).replace("/", "") in stem.replace("/", ""):
                row["local_pdf"] = pdf["path"]
                row["local_match_reason"] = "resolved_doi_in_filename"
                row["download_status"] = "exists_local"
                break
            title_tokens = [t for t in title_n.split() if len(t) >= 4][:6]
            hit_count = sum(1 for t in title_tokens if t in stem)
            if hit_count >= max(2, min(4, len(title_tokens))) and ((year_n and year_n in stem) or (author_n and author_n in stem)):
                row["local_pdf"] = pdf["path"]
                row["local_match_reason"] = "title_token_match"
                row["download_status"] = "exists_local"
                break
    return rows


def write_csv(rows: list[dict], csv_path: Path) -> None:
    fieldnames = [
        "index",
        "title",
        "first_author",
        "year",
        "doi",
        "resolved_doi",
        "article_url",
        "oa_pdf_hint",
        "needs_login_maybe",
        "duplicate_group",
        "duplicate_reason",
        "download_status",
        "local_pdf",
        "local_match_reason",
        "lookup",
        "raw",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})


def write_outputs(rows: list[dict], out_dir: Path, json_name: str, md_name: str, csv_name: str) -> tuple[Path, Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / json_name
    md_path = out_dir / md_name
    csv_path = out_dir / csv_name
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(rows, csv_path)
    lines = ["# Reference manifest", ""]
    dup_count = len({r['duplicate_group'] for r in rows if r.get('duplicate_group')})
    local_count = sum(1 for r in rows if r.get('local_pdf'))
    url_count = sum(1 for r in rows if r.get('article_url'))
    lines.append(f"- total_refs: {len(rows)}")
    lines.append(f"- duplicate_groups: {dup_count}")
    lines.append(f"- local_pdf_matches: {local_count}")
    lines.append(f"- article_urls: {url_count}")
    lines.append("")
    for r in rows:
        lines.append(f"- [{r['index']}] {r['title']}")
        lines.append(f"  - year: {r['year']} | first_author: {r['first_author']}")
        lines.append(f"  - doi: {r['doi'] or '(none)'} | resolved_doi: {r['resolved_doi'] or '(none)'}")
        if r.get("article_url"):
            lines.append(f"  - article_url: {r['article_url']}")
        if r.get("crossref"):
            lines.append(f"  - crossref: score={r['crossref'].get('score')} | title={r['crossref'].get('title')} | container={r['crossref'].get('container')} | url={r['crossref'].get('url')}")
        if r.get("oa_pdf_hint"):
            lines.append(f"  - oa_pdf_hint: {r['oa_pdf_hint']}")
        lines.append(f"  - needs_login_maybe: {r['needs_login_maybe']}")
        lines.append(f"  - download_status: {r['download_status']}")
        if r.get("local_pdf"):
            lines.append(f"  - local_pdf: {r['local_pdf']} | local_match_reason: {r['local_match_reason']}")
        if r.get("duplicate_group"):
            lines.append(f"  - duplicate_group: {r['duplicate_group']} | reason: {r['duplicate_reason']}")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path, csv_path


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract a structured literature manifest from a references file")
    ap.add_argument("references_file", help="Path to a .md or .txt references file")
    ap.add_argument("--out-dir", default=".", help="Output directory for manifest files")
    ap.add_argument("--json-name", default="ref_manifest.json")
    ap.add_argument("--md-name", default="ref_manifest.md")
    ap.add_argument("--csv-name", default="ref_manifest.csv")
    ap.add_argument("--local-pdf-dir", default="", help="Optional local PDF directory for existence matching")
    ap.add_argument("--limit", type=int, default=0, help="Only process the first N references")
    ap.add_argument("--sleep", type=float, default=0.6, help="Sleep between API calls to avoid bursts")
    args = ap.parse_args()
    refs_path = Path(args.references_file)
    refs = parse_refs(refs_path.read_text(encoding="utf-8"))
    if args.limit > 0:
        refs = refs[: args.limit]
    rows = build_manifest(refs, sleep_s=args.sleep)
    rows = detect_duplicates(rows)
    rows = match_local_pdfs(rows, Path(args.local_pdf_dir) if args.local_pdf_dir else None)
    json_path, md_path, csv_path = write_outputs(rows, Path(args.out_dir), args.json_name, args.md_name, args.csv_name)
    print(json.dumps({
        "count": len(rows),
        "references_file": str(refs_path),
        "manifest_json": str(json_path),
        "manifest_md": str(md_path),
        "manifest_csv": str(csv_path),
        "duplicate_groups": len({r['duplicate_group'] for r in rows if r.get('duplicate_group')}),
        "local_pdf_matches": sum(1 for r in rows if r.get('local_pdf')),
        "article_urls": sum(1 for r in rows if r.get('article_url'))
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
