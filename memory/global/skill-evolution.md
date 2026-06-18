---
name: skill-evolution
description: 经验演进引擎：四类信号收集、阈值软Hook、反例黑名单、升级项管理
type: reference
scope: global
created: 2026-06-18
priority: high
---

# 经验演进引擎

> ⛔ 在任何 workspace 中发现体系问题（skill 指令缺陷、经验文档缺失、执行错误模式、能力空白）时，按本文件记录信号。不使用 Darwin Skill 或任何第三方自进化工具——本文件定义的演进流程完全由人和 agent 协作驱动，不做自动修改。

## 四类信号

| 类型 | scope | 触发条件 | 例 |
|------|-------|---------|-----|
| `skill_issue` | skill 指令层面 | skill 指令错误/过时/矛盾/不完整，触发条件过宽或过窄 | step 缺步骤、Hook 位置不对 |
| `memory_issue` | 经验文档层面 | 经验文档缺失、过时、路由表缺条目、规则不清晰 | 缺错误经验、路由表遗漏 |
| `execution_error` | agent 执行层面 | 理解错意思、用错工具、分析错方向、漏读文件 | 该调 skill A 却调了 B |
| `missing_capability` | 能力空白 | 需要做某事但没有 skill 或经验覆盖 | 需要新 skill、新功能链路 |

## 信号提交格式

每次发现信号后，调用 `remember` 存入全局记忆池：

```text
名称：evo-{type}-{简短描述}
类型：feedback
范围：global
内容：
  - type: skill_issue | memory_issue | execution_error | missing_capability
  - scope: [skill名 | 经验文档路径 | 执行场景描述]
  - evidence: <会话原文摘录，≤200字>
  - impact: <该问题导致的实际后果，1-2句>
```

提交信号前检查 `memory search query=evo-{type}` 避免重复记录已存在信号。

## 阈值与软Hook

累计信号 ≥10 条后触发：

> 🔴 **软Hook**：体系演进信号已累计 N 条。是否需要提炼为升级项？

流程：分类信号 → 评估改进方向 → 列出升级计划 → 讨论确认 → 敲定 → 落实。

## 升级项存放

确认提炼的升级项写入 `skill-evolution-references/待升级.md`：

| 日期 | 类型 | 信号摘要 | 决策来源 | 评估方向 | 是否已融合 |
|------|------|---------|---------|---------|----------|
| YYYY-MM-DD | skill_issue | ... | 人工/agent建议 | 修改 step-X / 新增 错误经验.md | 否/是 |

## 反例黑名单（不可违反）

1. **禁止 AI 自评自改。** SkillLens 实证：LLM 自评准确率仅 46.4%。修改 skill 或经验文档必须经人工确认。
2. **禁止跳过人工确认。** 信号可以自动记，升级方案必须人审。
3. **禁止同一会话内记信号就出修复方案。** 发现问题和评估修复分开。
4. **禁止 signal 不带证据。** 每条信号必须引述原文，≤200字。
5. **禁止 attribution=agent_error 被忽略。** agent 执行错误也可能暴露经验文档或 skill 指令的设计缺陷——分析后再归类，不直接丢弃。

## 与 Darwin Skill 的关系

本文件的设计参考了 Darwin Skill v2.0（alchaincyf/darwin-skill）的核心原则（棘轮机制、独立评分、人在回路），但 scope 不同——Darwin 优化 SKILL.md 文本质量，本文件收集全栈运行时问题。互补，不冲突，不安装。

## 定期 Review

每周或会话结束时扫一眼：
- `memory search type=feedback` → 信号计数
- `skill-evolution-references/待升级.md` → 未融合的升级项
- 决定下一个升级周期处理哪些

## 参考

- 信号判定细则：`skill-evolution-references/signal-rubric.md`
- 用词词典：`skill-evolution-references/term-dictionary.md`
- lawerD 分发清单：`skill-evolution-references/lawerd-list.md`
