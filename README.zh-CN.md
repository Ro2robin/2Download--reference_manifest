# 2Download--reference_manifest

## 这是什么

这是一个收窄后的 OpenClaw skill 仓库，目标非常明确：

**把参考文献列表整理成可继续手动下载和管理的 manifest。**

它现在主要能做这些事：
- 解析参考文献
- 提取作者、年份、标题、DOI
- 补充 Crossref / OpenAlex 元数据线索
- 给出可以直接打开文献网页的 `article_url`
- 给出偏向 PDF 入口的 `pdf_url_hint`
- 输出 `ref_manifest.json`
- 输出 `ref_manifest.md`
- 输出 `ref_manifest.csv`
- 做重复文献提示
- 可选地对比本地 PDF 文件夹

---

## `article_url` 和 `pdf_url_hint` 的区别

这是现在这个 skill 里最重要的两个 URL 字段：

- `article_url`：优先给你**文章网页 / DOI 页面 / landing page**  
  English note: **article landing-page URL**
- `pdf_url_hint`：优先给你**更像 PDF 入口的链接线索**  
  English note: **PDF-oriented URL hint**

简单说：
- `article_url` 适合先点开看文献网页
- `pdf_url_hint` 适合继续找 PDF 或直接尝试下载

如果后面你是手动下载文献，这两个字段会非常顺手。

---

## skill 有什么能力

### 1. 从参考文献文本生成结构化清单
支持输入：
- `.md`
- `.txt`

支持情况：
- 编号参考文献
- 未编号参考文献
- 一条文献跨多行的情况

### 2. 自动提取核心字段
尽量提取：
- index
- raw
- author
- first_author
- year
- title
- doi

### 3. 自动补元数据线索
会尝试查询：
- Crossref
- OpenAlex

并补充：
- `resolved_doi`
- `article_url`
- `pdf_url_hint`
- `oa_pdf_hint`
- `needs_login_maybe`

### 4. 自动提示重复文献
输出：
- `duplicate_group`
- `duplicate_reason`

### 5. 支持本地 PDF 比对
如果传入 `--local-pdf-dir`，会尝试根据：
- DOI
- 标题 token
- 年份
- 作者

去比对本地 PDF 文件名，并补充：
- `download_status`
- `local_pdf`
- `local_match_reason`

### 6. 同时输出三种文件
- `ref_manifest.json`：适合脚本处理
- `ref_manifest.md`：适合人工审查
- `ref_manifest.csv`：适合 Excel / Sheets 手动筛选和下载管理

---

## 这个 skill 适合什么场景

最适合的场景是：

1. 你已经有一份参考文献列表
2. 你想先得到一个干净、结构化、可筛选的工作清单
3. 你还希望顺手得到可打开的文献网页入口和 PDF 提示链接
4. 然后再手动下载、归档或补全

说白了，它是一个：

**下载前整理器 / 文献清单生成器 / 网页入口整理器**
