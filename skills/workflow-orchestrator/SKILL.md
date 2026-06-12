---
name: workflow-orchestrator
author: 杜重阳律师（微信Dcylawer8888)
version: "2.0.0"
license: MIT
description: |
  本技能应在{{USER_SHORT_NAME}}发起任何与案件法律工作相关的请求时作为首个技能加载，统一接收并路由到 process-cases / draft-legal-docs 等子技能执行。其他技能不独立响应案件相关请求，全部经本引擎调度。
  不要用于：Mavis 技术配置、Skill 安装维护、非法律类任务。
---

## 功能概述

工作流编排引擎，{{ASSISTANT_NAME}}法律工作的唯一入口。统一接收{{USER_SHORT_NAME}}的所有案件相关请求，按意图路由到对应子技能，通过硬 Hooks / 软 Hooks 确保关键节点律师确认后再推进。

## 调用方式

由律师助理模式自动触发。当{{USER_SHORT_NAME}}说"看看材料""分析一下""处理这个案子"或发起任何案件法律工作请求时，本技能作为首个技能加载并路由。

---

# 工作流编排引擎

## 路由层级

**Tier 1 dispatcher**(本技能 [[workflow-orchestrator]])→ **Tier 2 下位 skill**([[process-cases]] / [[draft-legal-docs]] / [[case-progress-archive]] / [[court-sms]] / [[contract-review-pro]] / 等)

执行本技能前，务必严格遵守 Reasonix 全局记忆中的工作原则和本 skill 的 [[work-standards]]。

## 总则

开始任何法律工作（案件分析、文书起草、庭审辅导、证据分析等）前，严格按本技能制定的工作流程执行。执行过程中遇到 Hooks 必停，得到确认（或修改意见）后继续。

**本引擎是法律工作的唯一入口。** 当{{USER_SHORT_NAME}}说"看看材料"、"看一下"、"帮我看看"、"分析一下"、"处理这个案子"等模糊请求时，由本引擎统一接收并路由到对应子技能，子技能不独立响应。

### 路由规则

| 用户意图 | 路由目标 | 说明 |
|---------|---------|------|
| 提供文件/图片/PDF（无明确意图） | → 追问确认意图后路由 | 先 [[markitdown]] / LLM 多模态预处理，再请{{USER_SHORT_NAME}}说明需要做什么 |
| "看看材料"、"处理这个案子"、提供完整案情 | → 流程一（[[markitdown]] / LLM 多模态预处理 → [[process-cases]]） | 有完整材料，需全流程处理 |
| "接着某某案"、提及已有归档案件 | → 流程二（[[markitdown]] / LLM 多模态预处理 → 读案件工作区日志 + 跟进） | 已有案件进展记录 |
| "这个问题怎么看"、"是否构成 XX"、具体法条问题 | → [[process-cases]] | 具体法律问题，由 [[process-cases]] 简易模式处理 |
| "起草一份诉状/答辩状/代理词…" | → 流程一步骤 3（跳过分析步骤） | 直接起草，已有明确策略 |
| "理一下证据"、"证据分析"、"证据目录" | → [[legal-evidence-mapping-mctmilk]] | 证据梳理与分析 |
| "先搁置/归档" | → [[case-progress-archive]] | 阶段性归档 |
| 收到法院短信、粘贴短信内容/送达链接 | → 流程三（[[court-sms]]） | 法院短信→文书下载→归档 |
| "审一下这份合同"、"帮我看看这个合同" | → [[contract-review-pro]] | 合同审核七步工作流 |
| "模拟一下庭审"、"攻防演练"、"沙盘推演" | → [[legal-debate-simulation-mctmilk]] | 对方律师视角五维攻击 |
| "法官视角"、"庭审压力测试"、"模拟审查" | → [[mock-trial-review]] | 严苛裁判者极限施压 |
| "写一份案例分析报告"、"复盘这个案子" | → [[case-study-report]] | 专业案例研究报告 |
| 其他非案件类请求（知识整理/经验记录等） | → 放行不阻塞 | 由对应 Skill description 正常触发 |

---

## 流程一：案件全流程处理（起草→归档标准线）

> 详见 [[flow-01-new-case]]

## 流程二：已有案件进展日志的案件的跟进

> 详见 [[flow-02-existing-case]]

## 流程三：法院短信接收与文书处理

> 详见 [[flow-03-court-sms]]

---

## Hooks 规则

| 类型 | 行为 | 举例 |
|:----|:-----|:-----|
| **硬 Hooks** | 必须等律师回复，不回复不往下走 | 确认诉讼地位、确认诉请内容、确认策略 |
| **软 Hooks** | 提醒一次，未回复则跳过 | 追问补充材料、追问未回复的问题 |

---

## 错误处理

| 失败模式 | 行为 |
|---------|------|
| 路由表 13 条意图之外的模糊请求 | 追问确认意图，不进入主流程 |
| 子 skill（如 process-cases / MarkItDown）加载失败 | 提示"目标 skill 不可用，请手动指定" |
| 材料缺失 / {{USER_SHORT_NAME}}跳过确认 | 走硬 Hook 追问，不向下推进 |
| MarkItDown / LLM 多模态预处理失败 | 降级到"请{{USER_SHORT_NAME}}手写摘要"模式 |

## 当前范围

本流程覆盖以下场景：
- **流程一**：新案件全流程处理（收材料→分析→起草→定稿→归档）
- **流程二**：已有案件进展日志的案件的跟进（加载历史→分析新材→起草→归档）

- **流程三**：法院短信接收与文书处理（解析→下载→归档→衔接分析）

所有材料接收后自动进行 [[markitdown]] / LLM 多模态预处理（策略见 [[format-conversion]]，2026-06-05 重构自原 OCR 策略）。合同审核、庭前准备、案例报告等场景由路由表定向分发。

## 与现有技能的关系

```
{{USER_SHORT_NAME}}说"看看材料/分析一下/帮我看看" …

        ↓

[[workflow-orchestrator]]（聚合引擎/唯一入口——由它判断走哪条路）

        ↓

   ┌────┴──────────┐

   ↓               ↓

[[process-cases]]     [[court-sms]]

（全流程分析+轻咨询）（法院短信→文书下载）

   ↓               ↓

[[draft-legal-docs]] → [[docx]]     [[case-progress-archive]]

        ↓                       （归档收尾）

[[case-progress-archive]]

合同审核、庭前演练、案例报告 → 路由表定向分发

SOUL.md + WorkStandards.md（红线——全程约束）

```

---

## 变更历史

见 [CHANGELOG.md](./CHANGELOG.md)