# Changelog

> 作者：杜重阳律师（微信Dcylawer8888）
> 许可证：MIT

## [2.0.0] - 2026-06-02
### 新增
- Frontmatter 补齐 3 个必填字段:`author`({{USER_FULL_NAME}}) / `version`(SEMVER) / `license`(MIT)
- 新增 LICENSE.txt(MIT)
- SKILL.md 末尾"Mavis 本地化适配说明(2026-06-02)"段迁出
- SKILL.md 末尾"## 变更历史"段统一指向 [CHANGELOG.md](./CHANGELOG.md)
### 修改
- 修复 v1.0.0 条目"对齐 SKILL-DEV-GUIDE"声明与实际不一致的问题(本版本补齐)
### 迁移记录(原 SKILL.md 末尾 Mavis 适配说明段)
- 路径:全部从 `{{HOME_WIN}}\.Mavis\` 刷为 `~/.mavis/`
- 移除:双机协同 / WPS 云盘 / 符号链接相关内容(Mavis 单机,不需要)
- Frontmatter 移除 author / license / version 字段(后由 v2.0.0 规范化重新补回)
- 路由入口:仍以 workflow-orchestrator 为法律工作唯一入口
- 核心流程未变,所有 references/ 子文件原样保留
## [1.0.0] - 2026-05-31
### 新增
- 对齐 SKILL-DEV-GUIDE 书写规范，补全 Frontmatter（author/version/license/负向条件）