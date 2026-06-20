---
name: package-sync
description: |
  技能包同步更新。当用户在另一个 Reasonix 窗口通过 skill-evolution 或其他方式调整了 skills/memory 后，
  调用此 skill 将变更同步到 zongbao-skills 仓库并推送到 GitHub。
  不要用于：首次安装、环境配置、案件处理。
---

# package-sync

## 触发条件

- 用户说"同步到技能包"、"更新技能包"、"发布更新"、"推一下"
- skill-evolution Review 完成后
- 手动调整了 skill 或 memory 文件后需要同步

## 排除规则

以下内容**永远不同步**：
- `casecloud/` 及任何包含 `案件云` 的文件（保持 zongbao-skills 不带案件云状态）
- 技术工具 skill：`mineru-ocr`、`markitdown`、`docx`、`excel-xlsx`、`word-docx`
- `.reasonix/` 内部文件

## 同步来源 → 目标映射

| 来源 | 目标 | 处理 |
|------|------|------|
| `~/.reasonix/skills/<skill-name>/` | `zongbao-skills/skills/<skill-name>/` | 复制后运行 `desensitize.py` 清理个人信息 |
| Reasonix 全局记忆（`memory/global/`） | `zongbao-skills/memory/global/` | 直接复制（已为源格式） |
| Reasonix 案件管理记忆（`D--wpsyunpan-.../memory/`） | `zongbao-skills/memory/project/case-management/` | 扁平化命名 → 目录结构映射 |
| `memory/project/` 其他项目记忆 | `zongbao-skills/memory/project/` | 直接复制 |

## 执行流程

### 1. 扫描变更
- `git status` 查看 zongbao-skills 中已有的未提交变更
- 对比 Reasonix skills 目录和 zongbao-skills/skills/ 的时间戳差异
- 列出所有待同步项，排除 casecloud 和技术工具

### 2. 同步 skill 文件
- 对每个变更的 skill，从 `~/.reasonix/skills/<name>/` 复制到 `skills/<name>/`
- 跳过 `casecloud` 和相关变体
- 跳过技术工具名单中的 skill
- **注意**：Reasonix 中的 skill 文件已经个性化（占位符已替换），需要判断是否需要还原占位符。如果 skill 内容中不含 `{{` 占位符，说明已是最终版本，直接复制即可。

### 3. 同步 memory 文件
- **全局记忆**：`memory/global/` 下的文件从 Reasonix 全局 workspace 复制或直接在 zongbao-skills 中编辑
- **案件管理项目记忆**：Reasonix 使用扁平命名（`case-management-archive-index.md`），zongbao-skills 使用目录结构（`archive/index.md`）。需要反向映射。
  - 映射规则：`case-management-{dir}-{file}.md` → `{dir}/{file}.md`
  - 去掉 YAML frontmatter
  - 更新内部引用：`case-management-xxx-yyy` → `xxx/yyy`

### 4. 清理与验证
- 运行 `python scripts/desensitize.py` 清理残留的个人信息
- `grep` 确认无 casecloud 文件被纳入
- `grep` 确认无硬编码的个人路径（如 `C:\Users\13062`）

### 5. 提交推送
- `git add -A`
- 确认 stage 中无 casecloud 文件
- `git commit -m "<type>: <简短描述>"`
- `git push`

## 映射速查表

### Reasonix 扁平化 → zongbao-skills 目录结构

| Reasonix（案件管理 workspace） | zongbao-skills |
|------|------|
| `case-management-archive-index.md` | `archive/index.md` |
| `case-management-archive-errors.md` | `archive/errors.md` |
| `case-management-new-case-index.md` | `new-case/index.md` |
| `case-management-new-case-errors.md` | `new-case/errors.md` |
| `case-management-new-case-step-01.md` | `new-case/step-01-预处理与分析.md` |
| `case-management-new-case-step-02.md` | `new-case/step-02-策略确认.md` |
| `case-management-new-case-step-03.md` | `new-case/step-03-起草文件.md` |
| `case-management-new-case-step-04.md` | `new-case/step-04-定稿交付.md` |
| `case-management-new-case-step-05.md` | `new-case/step-05-归档.md` |
| `case-management-followup-index.md` | `followup/index.md` |
| `case-management-followup-errors.md` | `followup/errors.md` |
| `case-management-followup-step-01.md` | `followup/step-01-加载历史.md` |
| `case-management-followup-step-02.md` | `followup/step-02-分析新材.md` |
| `case-management-followup-step-03.md` | `followup/step-03-起草归档.md` |
| `case-management-sms-index.md` | `sms/index.md` |
| `case-management-sms-errors.md` | `sms/errors.md` |
| `case-management-common-routing.md` | `common/routing.md` |
| `case-management-common-hooks.md` | `common/hooks.md` |
| `case-management-common-errors.md` | `common/errors.md` |
| `case-management-index.md` | `index.md` |

### ⛔ 永远排除

| Reasonix | 原因 |
|------|------|
| `case-management-casecloud-*.md` | 案件云 |
| `skills/casecloud/` | 案件云 |
| 任何含 `案件云` 的文件 | 案件云 |

--
- 作者：杜重阳律师（微信Dcylawer8888）
- 版本：1.0.0
- 许可证：MIT
