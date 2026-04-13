# 2Download--reference_manifest

## 这是什么

这是一个收窄后的 OpenClaw skill 仓库，目标非常明确：

**把参考文献列表整理成可继续手动下载和管理的 manifest。**

它现在主要能做这些事：
- 解析参考文献
- 提取作者、年份、标题、DOI
- 补充 Crossref / OpenAlex 元数据线索
- 给出可以直接打开文献网页的 `article_url`
- 输出 `ref_manifest.json`
- 输出 `ref_manifest.md`
- 输出 `ref_manifest.csv`
- 做重复文献提示
- 可选地对比本地 PDF 文件夹

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
- `oa_pdf_hint`
- `needs_login_maybe`

### 4. URL 可以直接打开文献网页
这是这个 skill 很关键的一点。

输出里的：
- `article_url`
- `crossref.url`

通常都可以直接作为**文献落地页 / DOI 页面 / 文章网页入口**来打开。

也就是说，这个 skill 不只是帮你“抽元数据”，它还会尽量把**能点开的文章网页入口**给你整理出来，方便后续手动下载。

### 5. 自动提示重复文献
输出：
- `duplicate_group`
- `duplicate_reason`

### 6. 支持本地 PDF 比对
如果传入 `--local-pdf-dir`，会尝试根据：
- DOI
- 标题 token
- 年份
- 作者

去比对本地 PDF 文件名，并补充：
- `download_status`
- `local_pdf`
- `local_match_reason`

### 7. 同时输出三种文件
- `ref_manifest.json`：适合脚本处理
- `ref_manifest.md`：适合人工审查
- `ref_manifest.csv`：适合 Excel / Sheets 手动筛选和下载管理

---

## 如何使用

### 基本用法

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out
```

### 加本地 PDF 比对

```bash
python scripts/extract_ref_manifest.py references.md --out-dir ./out --local-pdf-dir ./papers
```

### 只测试单条引用解析

```bash
python scripts/normalize_reference.py "Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. Human Factors, 46(1), 50-80."
```

---

## 输出说明

### `ref_manifest.json`
机器友好版本，适合后续脚本继续处理。

### `ref_manifest.md`
人工友好版本，适合快速浏览和核对。

### `ref_manifest.csv`
表格版本，适合：
- Excel 打开
- 手动标记已下载/未下载
- 排序筛选
- 后续下载管理

### `article_url`
这是新增强调的关键字段。

它通常可以直接打开：
- DOI 页面
- 文章 landing page
- 文献网页入口

如果你后面要手动下载文献，这个字段会非常省事。

---

## 这个 skill 适合什么场景

最适合的场景是：

1. 你已经有一份参考文献列表
2. 你想先得到一个干净、结构化、可筛选的工作清单
3. 你还希望顺手得到可打开的文献网页入口
4. 然后再手动下载、归档或补全

说白了，它是一个：

**下载前整理器 / 文献清单生成器 / 网页入口整理器**

---

## 还需要改进的地方

目前还有这些可以继续优化：

1. 对更多引用格式的兼容性可以更强
2. 中英文混排、日文混排参考文献的解析仍可继续加强
3. 本地 PDF 比对目前主要依赖文件名启发式，后续可加入更稳的元数据校验
4. 重复检测目前偏保守，后续可以加近似标题匹配
5. `article_url` 目前优先取 Crossref / OpenAlex / DOI，可继续提升排序策略
