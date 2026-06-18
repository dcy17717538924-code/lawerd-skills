# step-03：起草归档

## 目的

根据律师确认的分析结果，执行起草→定稿→归档标准线。

## 输入

- step-02 产出的分析结果
- 律师指定的文书类型

## 输出

- 定稿 DOCX 文件（远程归档）

## 前置条件

- step-02 的硬Hook 已完成
- 律师已确认分析结果和文书类型

## 执行

本步骤引用 new-case 的 step-03→04→05 标准线，不重复写：

1. 起草文件：执行 new-case `step-03-起草文件.md`，`run_skill("draft-legal-docs")`
2. 定稿交付：执行 new-case `step-04-定稿交付.md`，展示→修改→DOCX 生成
3. 归档：执行 new-case `step-05-归档.md`，`run_skill("case-progress-archive")`

--
- 作者：{{USER_FULL_NAME}}（微信{{USER_WECHAT}}）
- 版本：1.0.0
- 许可证：MIT
