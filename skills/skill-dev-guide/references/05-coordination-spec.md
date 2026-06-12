# 跨 Skill 协作规范

{{ASSISTANT_NAME}}体系 Skill 之间的引用、配合、上下游关系表达规范。

## 在 SKILL.md 的"与其他技能配合"章节描述

```markdown
## 与其他技能配合

- 上游：由 [[workflow-orchestrator]] 调度
- 下游：[[draft-legal-docs]] 起草文书
- 关联：[[case-progress-archive]] 归档
```

## 引用原则

- **只引用 Skill 名称**,不引用其内部实现细节
- 不在 SKILL.md 里"复制粘贴"其它 skill 的内容
- 跨 skill 的具体参数/接口,通过 references/ 详细定义,不在主入口展开

## 三种关系

| 关系 | 含义 | 写作建议 |
|---|---|---|
| **上游** | 谁调度本 skill | "由 X 调度"、"被 X 触发" |
| **下游** | 本 skill 调用谁 | "完成后调用 X"、"结果交给 X" |
| **关联** | 平行/参考关系 | "类似 X"、"与 X 配合" |

## {{ASSISTANT_NAME}}律师助理体系的典型调用链

```
[[workflow-orchestrator]] (路由入口)
  ├→ [[draft-legal-docs]] (起草)
  ├→ [[contract-review-pro]] (审合同)
  ├→ [[legal-evidence-mapping-mctmilk]] (证据)
  ├→ [[case-study-report]] (案例)
  └→ [[case-progress-archive]] (归档)
```

子 skill 之间通常不直接互相调用,而是经由 [[workflow-orchestrator]] 调度。

## 工程师 skill 库的典型调用链

```
[[workflow-orchestrator]] 入口
  ├→ [[skill-dev-guide]] (查规范)         ← 本 skill
  ├→ [[skill-creator]] (用方法论)
  ├→ [[skill-vetter]] (校验)
  └→ [[archive-skill-update]] (归档)
```

## 协作中的 CHANGELOG 同步

修改一个 skill 影响了其它 skill 的预期行为时:
- 本 skill 的 CHANGELOG 写"修改了 X 行为"
- 通知上游/下游 skill 的 agent 同步更新其 CHANGELOG(若适用)
