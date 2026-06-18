# CHANGELOG

> 作者：杜重阳律师（微信Dcylawer8888）
> 许可证：MIT

## [1.0.0] — 2026-06-09

### 新增
- 从 WorkBuddy 版 `invoice-management` 转为 Reasonix 格式
- 融合邮件下载流程（流程二）：IMAP 连接 163 邮箱，搜索发票邮件，下载附件
- `scripts/fetch_invoices.py`：完整 IMAP→下载→pdfplumber解析→重命名→写xlsx 链路
- `scripts/match_invoices.py`：贪心金额组合算法
- `references/01-workflow-initial-sort.md`：初始整理流程
- `references/02-workflow-email-fetch.md`：邮件下载流程
- `references/03-workflow-match-invoices.md`：凑票流程
- `references/04-workflow-check-stock.md`：查库存流程
- `references/category-rules.md`：用途分类规则
- `references/config-template.md`：user-config.json 模板
- SKILL.md 主入口：四流程总览 + 触发路由表 + 渐进式披露 references/
