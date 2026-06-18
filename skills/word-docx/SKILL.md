---
name: Word / DOCX
slug: word-docx
homepage: https://clawic.com/skills/word-docx
description: >
  Word 文档创建/编辑/格式转换/定稿输出。
changelog: >
  Kept only for reference and comparison.
metadata: {"clawdbot":{"emoji":"📘","os":["linux","darwin","win32"]}}
---



## {{USER_SHORT_NAME}}默认排版配置（法律文书专用）

当用户明确要求按{{USER_SHORT_NAME}}风格排版，或任务描述涉及中国法律文书格式时，使用以下配置。

> **注意**：本配置仅在路径 A（无模板）时生效。给了模板时以模板样式为准。

### 页面布局
- 页边距：上下 2.54cm，左右 1.91cm
- 页脚：页码居中，格式"第 X 页"

### 字体字号
- 全文：仿宋
- 文书主标题：三号（16pt）加粗居中
- 正文：四号（14pt），首行缩进2字符
- 正文内各节标题：四号（14pt）加粗

### 段落
- 行距：固定值24磅（WD_LINE_SPACE.EXACTLY）
- 段落间无空行

### 此致/落款格式
- "此致"缩进2字符，与正文最后一段之间空2行
- "此致"与法院名称紧挨着（之间无空行），法院名称左对齐
- 法院名称下方空2行再写落款人和日期
- 落款人和日期右侧对齐

### 文书风格
- 简洁利落，不设章节小标题
- 当事人信息简写在一段内
- 诉讼请求用"1 2 3"顶格
- 事实与理由一段到底不拆分
- 策略性论述不上文书正文

### 文件名
- 格式：`[案件名]-[文书类型]（定稿）.docx`


## When to Use

Use when the main artifact is a Microsoft Word document or `.docx` file, especially when tracked changes, comments, headers, numbering, fields, tables, templates, or compatibility matter.

## Core Rules

### 1. Treat DOCX as OOXML, not plain text

- A `.docx` file is a ZIP of XML parts, so structure matters as much as visible text.
- The critical parts are usually `word/document.xml`, `styles.xml`, `numbering.xml`, headers, footers, and relationship files.
- Text may be split across multiple runs; never assume one word or sentence lives in one XML node.
- Use different workflows on purpose: structured extraction for quick reading, style-driven generation for new files, and OOXML-aware editing for fragile existing documents.
- If the job is mainly reading, extracting, or reviewing, prefer a structure-preserving read path before touching OOXML.
- For deep edits, inspect the package layout instead of relying only on rendered output.
- Reading, generating, and preserving an existing reviewed document are different jobs even when the format is the same.
- Legacy `.doc` inputs usually need conversion before you can trust modern `.docx` assumptions.

### 2. Preserve styles and direct formatting deliberately

- Prefer named styles over direct formatting so the document stays editable.
- Styles layer: paragraph styles, character styles, and direct formatting do not behave the same.
- Removing direct formatting is often safer than stacking more inline formatting on top.
- When editing an existing file, extend the current style system instead of inventing a parallel one.
- Copying content between documents can silently import foreign styles, theme settings, and numbering definitions.

### 3. Lists and numbering are their own system

- Bullets and numbering belong to Word's numbering definitions, not pasted Unicode characters.
- `abstractNum`, `num`, and paragraph numbering properties all matter, so restart behavior is rarely "visual only".
- Indentation and numbering are related but not identical; a list can have broken numbering even if the indent looks right.
- A list that looks correct in one editor can restart, flatten, or renumber itself later if the underlying numbering state is wrong.

### 4. Page layout lives in sections

- Margins, orientation, headers, footers, and page numbering are section-level behavior.
- First-page and odd/even headers can differ inside the same document, so one header fix may not fix the document.
- Set page size explicitly because A4 and US Letter defaults change pagination and table widths.
- Use section breaks for layout changes; manual spacing and stray page breaks usually create drift.
- Header and footer media use part-specific relationships, so copied IDs often break images or links.
- Tables, page breaks, and headers often drift together, so treat layout fixes as document-wide, not local cosmetic edits.
- Table geometry depends on page width, margins, and fixed widths, so "close enough" table edits often break later in Google Docs or LibreOffice.

### 5. Track changes, comments, and fields need precise edits

- Visible text is not the full document when tracked changes are enabled.
- Insertions, deletions, and comments carry metadata that can survive careless edits.
- Deleted text may still exist in the XML even when it no longer appears on screen.
- Comment anchors and review ranges can break if edits move text without preserving the surrounding structure.
- Comment markers and review wrappers do not behave like inline formatting, so moving text carelessly can orphan or misplace them.
- Comments, footnotes, bookmarks, and linked media may live in separate parts, not only in the main document body.
- Tables of contents, page numbers, dates, cross-references, and mail merge placeholders are fields.
- Edit the field source carefully and expect cached display values to lag until refresh.
- Hyperlinks, bookmarks, and references can break if IDs or relationships stop matching.
- Bookmarks, footnotes, comment ranges, and cross-references depend on stable anchors even when the visible text seems untouched.
- A document can look correct while still containing stale field output that refreshes later into something different.
- For review workflows, make minimal replacements instead of rewriting whole paragraphs.
- In tracked-change workflows, only the changed span should look changed; broad rewrites create noisy reviews and can destroy the original formatting context.
- For legal, academic, or business review documents, default to review-style edits over wholesale paragraph rewrites unless the user explicitly wants a rewrite.

### 6. Verify round-trip compatibility before delivery

- Complex documents can shift between Word, LibreOffice, Google Docs, and conversion tools.
- Tables, headers, embedded fonts, and copied styles are common sources of layout drift.
- Treat `.docm` as macro-bearing and higher risk; treat `.doc` as legacy input that may need conversion first.
- When layout matters, explicit table widths are safer than auto-fit or percentage-style behavior that different editors reinterpret.
- A document that passes a text check can still fail on pagination, table widths, or reference refresh after the recipient opens it.

## Common Traps

- Copy-paste can import unwanted styles and numbering definitions.
- Header or footer images use part-specific relationships, so reusing IDs blindly breaks them.
- Empty paragraphs used as spacing make templates fragile; spacing belongs in paragraph settings.
- A clean-looking export can still hide unresolved revisions, comments, or stale field values.
- Restarting lists "by eye" usually fails because numbering state lives outside the paragraph text.
- One visible phrase can be split across several runs, bookmarks, revision tags, or field boundaries.
- Replacing a whole paragraph to change one clause often breaks review quality, bookmarks, comments, or nearby inline formatting.
- Deleting all visible text from a paragraph or list item can still leave behind an empty paragraph mark, empty bullet, or unstable numbering.
- Table auto-fit and percentage-like width behavior can look acceptable in Word and still drift in Google Docs or LibreOffice.
- LibreOffice and Google Docs can shift complex tables, section behavior, and embedded fonts even when Word looks perfect.
- Compatibility mode can silently cap newer features or change pagination behavior.
- A single change in page size or margin defaults can ripple through tables, headers, TOC, and cross-references.
- A revision workflow can look accepted on screen while leftover metadata, comments, or field caches still make the file unstable later.
- TOC entries, footnotes, and cross-references can look correct until the recipient updates fields and exposes broken anchors.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `documents` — General document handling and format conversion.
- `brief` — Concise business writing and structured summaries.
- `article` — Long-form drafting and editorial structure.

## Feedback

- If useful: `clawhub star word-docx`
- Stay updated: `clawhub sync`


---

## 变更历史

见 [CHANGELOG.md](./CHANGELOG.md)