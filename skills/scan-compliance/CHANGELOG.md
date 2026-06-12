# Changelog

## [1.0.0] - 2026-06-03

### 新增

- 初始版本,{{ASSISTANT_NAME}}工程师工具 skill
- `scripts/scan-compliance.ps1` PowerShell 脚本:
  - 扫描 `~/.mavis/agents/` 下所有 agent 目录的 skills
  - 自动识别并跳过**第三方 skill**:
    - **clawic 第三方**:`slug` / `homepage: https://clawic.com` 字段,或 frontmatter 提到 `clawhub` / `skillhub` / `ClawdHub`
    - **Anthropic 官方**:frontmatter 提到 `Claude` / `Anthropic` / `extends Claude`
  - 第三方识别只检查 frontmatter 区域(前两个 `---` 之间),不看正文,避免误判(如引用 Anthropic 官方作为参考时)
  - 检查 4 项合规:frontmatter 字段 / LICENSE.txt / CHANGELOG.md / 末尾 Mavis 段
  - frontmatter 检测用宽松正则(无 `^` 锚点),兼容某些文件 author 行无换行的特殊情况
  - 支持 3 种输出格式:table(默认) / csv / json
  - 纯 PowerShell 内置命令,无外部依赖
- SKILL.md 主入口 + scripts/README.md 用法说明
- LICENSE.txt(MIT)

### 验证

跑了一次 `scan-compliance.ps1`:
- 总扫描 23 个 skill
- {{ASSISTANT_NAME}}自有 18 个,全部合规
- clawic 第三方 4 个(find-skills, skill-vetter, excel-xlsx, word-docx),正确跳过
- Anthropic 官方 1 个(skill-creator),正确跳过
