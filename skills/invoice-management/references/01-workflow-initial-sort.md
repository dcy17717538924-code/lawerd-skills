# 流程一：初始整理

> {{USER_SHORT_NAME}}把 PDF 发票丢在 `{发票根目录}` 时，批量解析 + 建表 + 归档。

## 前置条件

- `{发票根目录}` 下存在 `.pdf` 文件
- Python + pdfplumber + openpyxl 已安装

## 步骤

### 1. 扫描 PDF 文件

列出 `{发票根目录}` 下所有 `.pdf` 文件（排除 `未使用/` 和已存在的子目录）。

### 2. 逐文件解析

对每个 PDF：

```powershell
& "{{CODEX_PYTHON}}" -c "
import pdfplumber
with pdfplumber.open(r'{文件路径}') as pdf:
    for page in pdf.pages:
        t = page.extract_text()
        if t: print(t)
"
```

从提取文字中识别：
- **金额**：匹配 `价税合计[：:]?\s*¥?\s*([\d,]+\.\d{2})`
- **用途**：按 `references/category-rules.md` 映射关键词

### 3. 重命名

`{用途类型}{金额}.pdf`（如 `交通费1050.00.pdf`）。同名文件追加 `_2`。

### 4. 移入 `未使用/`

```powershell
Move-Item "{旧路径}" "未使用/{新文件名}"
```

### 5. 更新/创建 `发票统计表.xlsx`

- 若 xlsx 不存在 → 用 openpyxl 新建，写入表头行（9 列）
- 若已存在 → 读取最大序号，从 N+1 开始追加

每行写入：序号、新文件名、用途类型、金额、发票详情、原文件名、状态="未使用"

## 陷阱

- PDF 可能无文字层（扫描件/图片版）→ pdfplumber 返回空，降级用 markitdown，再失败用 mineru-ocr
- 金额可能有多个（如交通卡充值 + 服务费），取最大的一笔
