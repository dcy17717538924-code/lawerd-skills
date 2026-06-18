# 归档助手

## 功能入口

案件结案后需要纸质卷宗订卷归档（按律所 7 大类（诉讼）/ 3 大类（非诉）归类入卷材料）时进入本流程。

本功能委托 `run_skill("case-archive-orchestrator")` 完整执行。本文件仅定义触发条件和纸质卷宗规范摘要。

## 前置条件

- 案件已结案或达到订卷条件
- 案件根目录存在待归档的材料文件
- `run_skill("case-archive-orchestrator")` 可正常调用

## 执行

1. 加载 `errors.md`，注入上下文避免重复踩坑
2. 委托 `run_skill("case-archive-orchestrator")` 完整执行。case-archive-orchestrator 内部含：
   - 在案件根目录建 `00-定卷/` 子目录
   - 按律所 7 大类（诉讼）/ 3 大类（非诉）归类入卷材料
   - 复制并按 `{大类序号}-{文件序号}_{材料名}_p{页码}.{ext}` 命名规范改名
   - 用律所原版模板生成案卷目录.docx 和办案小结（草稿）.docx
   - 填写 `诉讼案件已结案表.xlsx`
   - 按案卷目录 → 办案小结 → 入卷材料顺序合并生成打印版 PDF

## 异常处理

- `IF` 案件根目录无可归档材料 `THEN` 提示"未找到待归档材料，请确认案件目录"
- `IF` 模板文件缺失 `THEN` 提示手动补全模板

## 参考

- 路由表：[[memory/project/case-management/common/routing]]
- 错误处理：[[memory/project/case-management/common/errors]]

--
- 作者：{{USER_FULL_NAME}}（微信{{USER_WECHAT}}）
- 版本：1.0.0
- 许可证：MIT
