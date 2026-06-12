# CHANGELOG 与版本号规范

{{ASSISTANT_NAME}}体系 Skill 的变更记录格式与版本号演进规则。

## 每次修改必须做的事

在 `CHANGELOG.md` 顶部新增一条记录,**不删旧记录**。

## CHANGELOG.md 格式

```markdown
# Changelog

## [1.1.0] - 2026-06-01
### 新增
- xxx

### 修改
- xxx

### 修复
- xxx
```

## 版本号规则(SEMVER)

| 变更类型 | 版本演进 | 例 |
|---|---|---|
| 小修改 / Bug 修复 | 尾号 +1 | 1.0.0 → 1.0.1 |
| 新增功能 / 章节 | 中号 +1 | 1.0.1 → 1.1.0 |
| 重大重构 / 不兼容变更 | 首号 +1 | 1.1.0 → 2.0.0 |

## 三类变更分类

- **新增**(Added):新文件、新章节、新功能
- **修改**(Changed):既有内容的调整(描述、参数、结构)
- **修复**(Fixed):错误修正
- **删除**(Removed) —— 视情况单列或并入"修改"
- **弃用**(Deprecated) —— 警告未来会删除,可选

## 与 agent CHANGELOG 的同步

Skill 修改后,如果该 skill 归属某 agent,**必须同步追加一条到该 agent 的 `CHANGELOG.md`**,因为:
- 用户的全局规则:每个 agent 的全部更新日志都写在 agent 自己的 CHANGELOG.md 里
- skill 归属某 agent 时,skill 的变更属于该 agent 的活动

例:修改 `coder/skills/skill-dev-guide/`,要同步追加到 `coder/CHANGELOG.md`。

## 模板片段(直接复制)

```markdown
## [X.Y.Z] - YYYY-MM-DD

### 新增
-

### 修改
-

### 修复
-
```
