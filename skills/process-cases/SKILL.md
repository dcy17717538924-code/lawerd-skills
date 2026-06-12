---
name: process-cases
author: 杜重阳律师（微信Dcylawer8888)
version: "2.0.0"
license: MIT
description: |
  案件全流程处理技能(子技能,由 workflow-orchestrator 调度触发)。覆盖两大场景:①轻分析——具体法律问题快速解答(结论先行→依据陈列→风险提示);②全流程——完整案情材料的深度分析(事实梳理、法律关系定性、证据评估、结果预判),输出案情摘要与分析报告。
  不要用于:Mavis 技术配置(请用 coder 技术顾问子 agent);直接响应用户法律请求(必须经由 workflow-orchestrator 路由,本 skill 不接受直接调用)。
---

# 案件全流程处理

## 功能概述

{{ASSISTANT_NAME}}体系下案件处理的核心子 skill。覆盖从"轻量法律咨询"到"复杂案件深度分析"的全光谱,输出结论先行的分析报告。**本 skill 不直接响应用户请求**,由 `workflow-orchestrator` 统一调度。

## 调用方式

**重要**:本 skill **不**接受直接调用,所有路径必须经由 `workflow-orchestrator` 路由。

调用链:

1. 用户向{{ASSISTANT_NAME}}提出法律请求
2. 由 `workflow-orchestrator` skill 按场景路由到本 skill 或其他子 skill
3. 路由逻辑详见 `workflow-orchestrator` skill

**直接调用本 skill 会跳过必要的入口校验和路由决策,产生不规范行为,严禁。**

## 工作流(总览)

按案件复杂度与材料完整度,可选两个模式(默认简易模式):

| 模式 | 适用场景 | 详细流程 |
|---|---|---|
| **简易模式** | 事实清晰、争点明确,或仅有具体法律问题无完整材料 | `references/01-simple-mode.md` |
| **深度模式** | 复杂争议、证据多、金额大 | `references/02-deep-mode.md` |

最终汇总为"案件分析报告",模板见 `references/03-report-template.md`。

## 与其他技能配合

- **上游**:[[workflow-orchestrator]](强制入口,所有调用必由其路由)
- **下游**:起草文书 → [[draft-legal-docs]];案件归档 → [[case-progress-archive]]
- **关联**(平级,可由 [[workflow-orchestrator]] 互补调用):
  - [[contract-review-pro]] —— 合同审阅专项
  - [[legal-evidence-mapping-mctmilk]] —— 证据梳理专项
  - [[legal-debate-simulation-mctmilk]] / [[mock-trial-review]] —— 庭审/辩论专项
  - [[case-study-report]] —— 案例报告
  - [[court-sms]] —— 法院短信处理

## 配置

- 检索与引用规则 + 禁止项:`references/04-rules-and-prohibitions.md`
- 法条核验:IMA 国家法律知识库
- 案例检索:IMA 人民法院案例库
- {{USER_SHORT_NAME}}手册:IMA 律师手册知识库(凭证见主 agent `memory/tech-environment.md`)

## 变更历史

见 [CHANGELOG.md](./CHANGELOG.md)
