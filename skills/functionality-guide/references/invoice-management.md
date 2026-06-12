# invoice-management

## 路径

```
~/.reasonix/skills/invoice-management/
├── SKILL.md
├── CHANGELOG.md
├── LICENSE.txt
├── references/
│   ├── 01-workflow-initial-sort.md
│   ├── 02-workflow-email-fetch.md
│   ├── 03-workflow-match-invoices.md
│   ├── 04-workflow-check-stock.md
│   ├── category-rules.md
│   └── config-template.md
├── scripts/
│   ├── fetch_invoices.py
│   └── match_invoices.py
└── archive/
```

## 字段

- **name**: `invoice-management`
- **author**: {{USER_FULL_NAME}}（微信{{USER_WECHAT}}）
- **version**: `1.0.0`
- **license**: MIT

## 触发词

"拉发票"、"下载发票"、"凑发票"、"凑XX元发票"、"发票库存"、"看发票"、"整理发票"

## 四个流程

1. **初始整理** — PDF批量解析→分类→重命名→建统计表
2. **邮件下载** — POP3连163邮箱→搜索发票→下载PDF→pdfplumber解析→归档
3. **凑票** — 贪心金额组合→创建日期文件夹→移入→更新统计表→费用报销单→合并PDF
4. **查库存** — 读取统计表→分类汇总→汇报

## 工作目录

`D:\wpsyunpan\229601413\WPS云盘\01 - 法律工作文件\报销发票\`

## 依赖

- Python 3.12+ (codex runtime)
- pdfplumber, openpyxl, pypdf (pip install)
- 163邮箱 IMAP授权码（POP3用）
