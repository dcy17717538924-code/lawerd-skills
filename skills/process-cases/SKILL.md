---
name: process-cases
description: |
  案件全流程处理技能（子技能，由 case-management 经验库调度）。覆盖两大场景：①简易模式——具体法律问题快速解答（结论先行→依据陈列→风险提示）；②深度模式——完整案情材料的深度分析（事实梳理、法律关系定性、证据评估、结果预判）。
  不要用于：直接响应用户法律请求（必须经由 case-management 经验库路由，本 skill 不接受直接调用）。
---

# process-cases

> 上游：case-management-index（project memory，auto-injected）
> 下游：[[skills/draft-legal-docs]] | [[skills/case-progress-archive]]

## 工作流

按案件复杂度与材料完整度选择模式（默认简易模式）：

| 模式 | 适用场景 | 详细流程 |
|------|---------|---------|
| **简易模式** | 事实清晰、争点明确，或仅有具体法律问题无完整材料 | `references/01-simple-mode.md` |
| **深度模式** | 复杂争议、证据多、金额大 | `references/02-deep-mode.md` |

两种模式最终汇总为"案件分析报告"，模板见 `references/03-report-template.md`。

## 关联

- [[skills/contract-review-pro]] — 合同审阅专项
- [[skills/legal-evidence-mapping-mctmilk]] — 证据梳理专项
- [[skills/legal-debate-simulation-mctmilk]] / [[skills/mock-trial-review]] — 庭审/辩论专项

## 配置

- 检索规则：`references/04-rules-and-prohibitions.md`

--
- 作者：杜重阳律师（微信Dcylawer8888）
- 版本：2.0.0
- 许可证：MIT
