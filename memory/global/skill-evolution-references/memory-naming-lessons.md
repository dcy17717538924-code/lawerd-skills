# Memory 命名三条硬规则

> 来源：实战中因违反规则导致的 `memory read` 失败 bug。
> Windows 项目记忆路径：`C:\Users\<用户名>\AppData\Roaming\reasonix\projects`
> macOS 项目记忆路径：`~/Library/Application Support/reasonix/projects`

| # | 规则 | 代价（不遵守的后果） |
|:--:|------|------|
| 1 | **文件名 = name + .md，全部平铺** | `memory read` 找不到文件 |
| 2 | **name 纯 ASCII** | 工具层截断中文，返回错误或错文件 |
| 3 | **改名同步更新交叉引用** | wiki 链接 / `read_file` 路径断链 |

## 案例

- `待升级.md` → 违反规则 #2，已更名为 `upgrade-queue.md`
- `memory/project/case-management/` 六大子目录全中文命名（`归档助手/` `新案件办理/` `案件云助手/` `短信助手/` `老案件跟进/` `通用/`）→ 违反规则 #1（子目录）、#2（中文），已全量改为 ASCII：`archive/` `new-case/` `casecloud/` `sms/` `followup/` `common/`
- 同目录中文文件名（`错误经验.md`×5、`hooks参考.md`、`路由表.md`、`错误处理总则.md`）→ 统一改为 ASCII
