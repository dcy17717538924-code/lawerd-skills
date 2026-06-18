# Changelog

> 作者：杜重阳律师（微信Dcylawer8888）
> 许可证：MIT

## [1.1.0] - 2026-06-09

### 融合自曾科律师版本的新增功能

- 新增 `scripts/scan_required_materials.py`：归档前扫描四项必查材料（律师费发票、律师聘用合同、已结案表、散群截图）
- 新增 `scripts/fill_closed_case_table.py`：自动填写 `诉讼案件已结案表.xlsx`（38 个字段，从案卷目录读取元数据后自动填充）
- 新增 `scripts/export_print_pdf.py`：按"案卷目录 → 办案小结 → 入卷材料"顺序合并生成直接打印用 PDF
- 新增 `scripts/fix_catalog_sequence.py`：修复案卷目录材料清单合并单元格/序号错位问题
- 新增 `_references/templates/closed_case_table_template.xlsx`：律所结案总表模板
- SKILL.md 工作流从 5 步扩展至 7 步（Step 2.5 四项必查 + Step 6 结案表 + Step 7 打印 PDF）
- 增强律师聘用合同识别规则：合同常在 `面谈材料/面谈交接` 目录中以随机图片文件名保存
- 更新关键依赖：新增 `openpyxl`、`Pillow`、可选 `PyMuPDF`

### 适配

- 承办律师默认值改为{{USER_FULL_NAME}}
- 已知坑更新：用 `fix_catalog_sequence.py` 替代旧的手动修复方式

## [1.0.0] - 2026-06-07

### 新增

- 试点 S 施玲玲离婚案跑通（16KB 案卷目录 + 10KB 办案小结）
- 律所原版 7 大类（诉讼）归类支持
- 律所原版 docx 模板填字段（1:1 格式保留）
- 4 个核心脚本：
  - `scripts/build_archive.py` — 复制 + 改名（幂等）
  - `scripts/fill_templates.py` — 填律所模板
  - `scripts/parse_templates.py` — 解析律所模板结构（辅助）
  - `scripts/verify_filled.py` — 验证填后结构
- 律所模板备份：
  - `_references/templates/template_catalog.docx`（19KB）
  - `_references/templates/template_summary.docx`（11KB）
- 元数据自动提取（pypdf）：
  - 案号 / 法院 / 承办律师（从调解书 / 律师函）
  - 立案 / 结案 / 收案日期
- 命名规范：`{大类序号}-{文件序号}_{材料名}_p{页码}.{ext}`
- 3 条用户规则沉淀：
  - 1-3 在材料备份文件夹，以图片方式存在
  - 4-5 在案件目录或司法送达等文件夹
  - 6 是用户自己截图放在案件文件夹

### 新增（非诉支持）

- 3 大类非诉支持（律师合同 + 发票 + 散群截图）
- `-Type=non-litigation` 参数触发
- 案卷目录模板复用诉讼版（只换材料清单内容）

### 已知坑

- 材料清单"本大类内序号"列（列 0）python-docx 覆盖可能不生效，需打开手动改
- 扫描 PDF 需 OCR 兜底（matrix MCP 或 computer use）
- 案号格式不强校验（律所差异大）

### 范围

- 仅律所物理卷宗归档（7 大类诉讼 + 3 大类非诉）
- 不包含：心智归档（case-progress-archive）、案例研究（case-study-report）
