# 渐进式加载

{{ASSISTANT_NAME}}体系 Skill 采用三级加载机制,管理 context window。

## 三级加载表

| 层级 | 内容 | 何时加载 |
|------|------|----------|
| 第零层 | Frontmatter(`name` / `description`) | 始终加载(Skill 匹配阶段) |
| 第一层 | SKILL.md 正文 | 触发时加载 |
| 第二层 | `references/` | 被显式引用时按需读取 |

## 设计原则

- **不要把所有内容塞进 SKILL.md** —— 详细规则、模板、配置示例放 `references/`
- SKILL.md 正文保持 ≤ 500 行
- 第二层可以"无限"(`references/` 内容多不直接占 context,需 `Read` 才加载)
- `scripts/` 里的 Python/Bash 脚本**可不读 context 直接执行**

## 加载流程示意

```
用户提问
  ↓
daemon 扫描所有 skill 的 frontmatter
  ↓ (匹配 description 触发条件)
命中 skill
  ↓
加载 SKILL.md 正文
  ↓ (正文里 Read references/xxx.md)
按需加载 references
  ↓ (调 scripts/xxx.py)
执行脚本(可零 token)
```

## 写作时怎么用

1. **SKILL.md 写**:触发条件、定位、入口、工作流总览、引用链接
2. **references/ 写**:具体规范、参数表、模板、详细示例
3. **scripts/ 写**:可复用代码,稳定逻辑

## 跟 Mavis 体系的差异

Mavis(基于 Anthropic 规范)的三级是"metadata / SKILL.md / 资源"—— {{ASSISTANT_NAME}}的"第零层 / 第一层 / 第二层"是同一回事,只是命名不同。
