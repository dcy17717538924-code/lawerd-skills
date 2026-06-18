# 信号判定细则

## 四类信号判定标准

### skill_issue

skill 指令本身有缺陷。

| 判定项 | 是 | 否 |
|--------|-----|----|
| SKILL.md 中的指令是否矛盾？（一步说做 A、另一步说做 B） | ✅ 提 signal | ❌ |
| steps/ 中的步骤是否有格式错误或缺失必填字段？ | ✅ | ❌ |
| 触发条件是否过宽（不该触发却触发）或过窄（该触发未触发）？ | ✅ | ❌ |
| agent 执行正确但结果仍不理想，根因是指令层面的问题？ | ✅ | ❌ |
| agent 自己执行错误导致问题？ | ❌ 归 execution_error | ➖ |

### memory_issue

经验文档缺失、过时或不精确。

| 判定项 | 是 | 否 |
|--------|-----|----|
| case-management 子文档缺步骤或错误经验？ | ✅ 提 signal | ❌ |
| 路由表缺条目导致意图未被覆盖？ | ✅ | ❌ |
| Hook 规则在实际执行中因表述模糊被 agent 跳过？ | ✅ | ❌ |
| 全局记忆（profile/identity/tech）内容过时？ | ✅ | ❌ |

### execution_error

agent 执行层面出错——但需分析是否暴露了上层设计缺陷。

| 判定项 | 是 | 否 |
|--------|-----|----|
| agent 理解错了律师的意思？ | ✅ 提 signal | ❌ |
| agent 调用了错误的 skill（应该调 A 却调了 B）？ | ✅ | ❌ |
| agent 跳过了某个应该执行的步骤？ | ✅ | ❌ |
| 同样的错误在同一个 skill/步骤重复出现？ | ✅ 提 signal + 上升为 skill_issue 或 memory_issue | ❌ |
| 一次性的、不会复现的执行失误？ | ❌ 不提 | ➖ |

### missing_capability

需要做但没有能力覆盖。

| 判定项 | 是 | 否 |
|--------|-----|----|
| 律师提出的需求没有 skill 覆盖？ | ✅ 提 signal | ❌ |
| 现有 skill 的功能链路有空白环节？ | ✅ | ❌ |
| 需要但缺失的具体能力（如某种文件格式支持）？ | ✅ | ❌ |
| 一次性的特殊任务？ | ❌ 不提 | ➖ |

## 提交模板

```text
名称：evo-{type}-{简短描述}
类型：feedback
范围：global

内容：
  - type: skill_issue | memory_issue | execution_error | missing_capability
  - scope: [skill名 / 经验文档路径 / 执行场景描述]
  - evidence: <会话原文摘录，≤200字>
  - impact: <实际后果，1-2句>
```

## 证据要求

- evidence 必须引述原文，不总结、不转述。
- impact 描述该问题导致的实际后果（如"导致分析方向偏离"、"跳过了Hook律师确认"）。
- 提交前用 `memory search query=evo-{type}` 查重，重复的不提。
