# 2Download--reference_manifest

## これは何か

このリポジトリは、用途を絞った OpenClaw skill です。
目的はとても明確です。

**参考文献リストを、後で手動ダウンロードや整理に使える structured manifest に変換すること。**

以下のことは、もう目的にしていません。
- 出版社サイトへのログイン
- ブラウザ経由の PDF 自動ダウンロード
- 壊れやすいダウンロード状態管理

残しているのは、安定していて実用的な部分です。
- 参考文献の解析
- 著者 / 年 / タイトル / DOI の抽出
- Crossref / OpenAlex によるメタデータ補強
- `ref_manifest.json` の生成
- `ref_manifest.md` の生成
- `ref_manifest.csv` の生成
- 重複候補の検出
- ローカル PDF フォルダとの照合（任意）

---

## 主な機能

### 1. 参考文献テキストから manifest を作成
入力対応:
- `.md`
- `.txt`

対応パターン:
- 番号付き参考文献
- 番号なしの 1 行 1 文献
- 複数行に分かれた参考文献の結合

### 2. 基本メタデータの抽出
できるだけ以下を抽出します:
- index
- raw
- author
- first_author
- year
- title
- doi

### 3. メタデータ補強
以下を照会します:
- Crossref
- OpenAlex

追加される可能性がある項目:
- `resolved_doi`
- `oa_pdf_hint`
- `needs_login_maybe`

### 4. 重複候補の検出
出力項目:
- `duplicate_group`
- `duplicate_reason`

### 5. ローカル PDF との照合
`--local-pdf-dir` を指定すると、以下を使って照合します:
- DOI
- タイトル token
- 年
- 著者

追加項目:
- `download_status`
- `local_pdf`
- `local_match_reason`

### 6. 3 種類の出力
- `ref_manifest.json` — スクリプト向け
- `ref_manifest.md` — 人が確認しやすい要約
- `ref_manifest.csv` — Excel / Sheets 向け

---

## 使い方

### 基本

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out
```

### ローカル PDF 照合あり

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out --local-pdf-dir ./papers
```

### 単一文献の解析

```bash
python scripts/normalize_reference.py "Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. Human Factors, 46(1), 50-80."
```

---

## 出力

### `ref_manifest.json`
後続スクリプト処理向け。

### `ref_manifest.md`
素早い目視確認向け。

### `ref_manifest.csv`
Excel / Sheets での確認、ソート、手動ダウンロード管理向け。

---

## 向いている使い方

この skill は次のような場面に向いています。

1. すでに参考文献リストがある
2. 壊れやすい自動ダウンロードは避けたい
3. まずは整理された worklist が欲しい
4. その後で手動ダウンロードや保管を行いたい

つまり、これは

**ダウンロード前整理ツール / 参考文献 manifest 生成器**

であり、万能ダウンローダーではありません。

---

## 今後の改善点

今後の改善候補:
1. より多くの引用スタイルへの対応
2. 中国語 / 英語 / 日本語混在文献の解析強化
3. ファイル名依存を超えたローカル PDF 照合の改善
4. 類似タイトル重複検出の強化
5. DOI 優先の検証モード追加
6. 大規模文献管理向けの手動ワークフロー列の強化

---

## リポジトリ構成

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

## サンプル

`examples/` ディレクトリには以下を入れています。
- 最小の参考文献入力例
- 最小の CSV 出力例

---

## 一言で言うと

この skill の価値は「PDF を全部自動ダウンロードすること」ではありません。

価値は、

**散らかった参考文献リストを、手動文献作業に使える manifest に変換すること**

にあります。
