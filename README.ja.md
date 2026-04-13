# 2Download--reference_manifest

## これは何か

このリポジトリは、参考文献リストを structured manifest に変換する OpenClaw skill です。

現在できることは次の通りです。
- 参考文献の解析
- 著者 / 年 / タイトル / DOI の抽出
- Crossref / OpenAlex によるメタデータ補強
- 文献ページを直接開ける `article_url` の出力
- `ref_manifest.json` の生成
- `ref_manifest.md` の生成
- `ref_manifest.csv` の生成
- 重複候補の検出
- ローカル PDF フォルダとの照合（任意）

---

## `article_url` が重要な理由

この skill は単にメタデータを抽出するだけではありません。
可能な場合、以下のような URL も整理します。
- `article_url`
- `crossref.url`

これらは多くの場合、次のようなページを直接開けます。
- DOI ページ
- 論文の landing page
- ジャーナル / 論文のウェブページ

そのため、後で手動ダウンロードするときにかなり便利です。

---

## 主な機能

### 1. 参考文献テキストから manifest を作成
入力対応:
- `.md`
- `.txt`

### 2. 基本メタデータの抽出
抽出対象:
- index
- raw
- author
- first_author
- year
- title
- doi

### 3. メタデータ補強
照会先:
- Crossref
- OpenAlex

追加される可能性がある項目:
- `resolved_doi`
- `article_url`
- `oa_pdf_hint`
- `needs_login_maybe`

### 4. 重複候補の検出
出力項目:
- `duplicate_group`
- `duplicate_reason`

### 5. ローカル PDF との照合
追加項目:
- `download_status`
- `local_pdf`
- `local_match_reason`

### 6. 3 種類の出力
- `ref_manifest.json`
- `ref_manifest.md`
- `ref_manifest.csv`

---

## 使い方

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out
```

ローカル PDF 照合あり:

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out --local-pdf-dir ./papers
```

単一文献の解析:

```bash
python scripts/normalize_reference.py "Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. Human Factors, 46(1), 50-80."
```

---

## 一言で言うと

これは

**参考文献 manifest 生成器 + 文献ウェブ入口抽出器**

です。
