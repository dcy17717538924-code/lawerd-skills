---
name: scan-compliance
author: 杜重阳律师（微信Dcylawer8888)
version: "1.0.0"
license: MIT
description: |
  本技能用于扫描{{ASSISTANT_NAME}}体系下所有 skill 的合规性——检查 frontmatter 字段、LICENSE.txt 存在、CHANGELOG.md 存在、SKILL.md 末尾无遗留 Mavis 适配段。
  当{{ASSISTANT_NAME}}工程师需要批量检查{{ASSISTANT_NAME}}自有 skill 是否符合 SKILL-DEV-GUIDE 规范时使用。
  不要用于：clawic 第三方 skill(本扫描器自动识别并跳过);单个 skill 的精确诊断(请用 read/edit 工具查看具体文件)。
---

# Skill 合规扫描

## 功能概述

{{ASSISTANT_NAME}}工程师工具。批量扫描 `~/.reasonix/skills/` 下的所有 skill，检查它们是否符合 `SKILL-DEV-GUIDE` 规范。

**核心能力**:
- 区分"{{ASSISTANT_NAME}}自有"vs"clawic 第三方"skill
- 检查 4 项硬性合规项:frontmatter 字段 / LICENSE.txt / CHANGELOG.md / 末尾 Mavis 段
- 输出控制台表格报告 + 摘要

## 调用方式

直接调用脚本:

```powershell
# 默认扫描 ~/.reasonix/skills
& "{{REASONIX_SKILLS}}scan-compliance\scripts\scan-compliance.ps1"

# 指定其他路径
& "scan-compliance.ps1" -Path "D:\other-mavis\agents"
```

## 工作流

1. 工程师主动触发脚本
2. 脚本扫描 `~/.reasonix/skills/` 目录
3. 对每个 skill:
   - 通过 `slug` / `homepage` 字段识别 clawic 第三方 → **跳过**(不归{{ASSISTANT_NAME}}维护)
   - {{ASSISTANT_NAME}}自有 → 检查 4 项合规,记录 issue
4. 输出表格 + 摘要

## 与其他技能配合

- **关联**:`skill-dev-guide`(本扫描器对照的规范来源)
- **关联**:`skill-creator`(新建 skill 时,可用本扫描器预检)

## 配置

无外部依赖,纯 PowerShell 内置命令。

## 变更历史

见 [CHANGELOG.md](./CHANGELOG.md)
