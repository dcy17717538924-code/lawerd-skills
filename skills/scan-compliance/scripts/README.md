# {{ASSISTANT_NAME}} Skill 合规扫描脚本

> 用于批量检查{{ASSISTANT_NAME}}体系下所有 skill 是否符合 SKILL-DEV-GUIDE 规范。

## 用法

```powershell
# 默认扫描 ~/.mavis/agents
& ".\scan-compliance.ps1"

# 指定其他路径
& ".\scan-compliance.ps1" -Path "D:\other-mavis\agents"

# 输出 JSON
& ".\scan-compliance.ps1" -OutputFormat json

# 输出 CSV(适合导入 Excel)
& ".\scan-compliance.ps1" -OutputFormat csv
```

## 检查项

对每个{{ASSISTANT_NAME}}自有 skill,检查 4 项:

1. **Frontmatter 字段**:`author` / `version` / `license` / `description` 必填
2. **LICENSE.txt**:必须存在
3. **CHANGELOG.md**:必须存在
4. **末尾 Mavis 段**:不能有"## Mavis 本地化适配说明"段(应已迁至 CHANGELOG)

clawic 第三方 skill(通过 `slug` / `homepage: https://clawic.com` 字段识别)自动跳过,不计入合规检查。

## 输出示例

```
========= {{ASSISTANT_NAME}} Skill 合规扫描报告 ==========
扫描时间: 2026-06-03 00:05:06
扫描范围: {{HOME_WIN}}\.mavis\agents

[律师助理] 14 个 skill
  ✓ workflow-orchestrator           全部合规
  ✗ draft-legal-docs                缺 LICENSE.txt
  ...

[工程师] 7 个 skill
  ✓ coder                           全部合规
  ...

========= 摘要 ==========
总扫描: 21
{{ASSISTANT_NAME}}自有: 15(其中合规 12,缺项 3)
clawic 第三方(跳过): 5
无 SKILL.md: 1
```

## 依赖

- PowerShell 5.1+ (Windows 自带)
- 无外部模块
