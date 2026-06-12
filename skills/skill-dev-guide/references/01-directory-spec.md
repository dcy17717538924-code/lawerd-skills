# 目录规范

{{ASSISTANT_NAME}}体系 Skill 的标准目录结构。

## 标准结构

```text
skill-name/
├── SKILL.md          # 必需：技能定义与工作流
├── CHANGELOG.md      # 必须：变更记录
├── LICENSE.txt       # 推荐：许可证
├── references/       # 可选：参考文档，按需加载
├── scripts/          # 可选：可执行代码
├── templates/        # 可选：输出模板
└── archive/          # 可选：操作归档记录
```

## 强制约束

- `references/`、`scripts/`、`templates/`、`archive/` 下必须**完全扁平**,禁止子目录
- ✅ `references/sms-patterns.json`
- ❌ `references/docs/api/guide.md`

**适用范围**:
- {{ASSISTANT_NAME}}律师助理体系(`~/.mavis/agents/lawyer-assistant/skills/`)下的 skill —— 强制完全扁平
- 技术顾问 skill 库(`~/.mavis/agents/coder/skills/`)下的 skill —— 允许用编号前缀(`01-` / `02-` ...)模拟扁平(本 skill 自身示范)
- Mavis 全局 builtin skill(`~/.mavis/.builtin-skills/`)—— 由系统决定,不在本规范范围

## 为什么扁平

- 子目录会让"按文件名匹配加载"变复杂
- 扁平 + 编号前缀兼顾"组织清晰"和"扫描简单"
- 避免目录嵌套导致 references/ 体积不可控
