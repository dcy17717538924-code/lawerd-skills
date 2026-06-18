# step-02：信息映射

## 目的

收集模板填充所必需的信息，分类追问律师。

## 输入

- 步骤 01 产出的模板路径（如有）
- `references/placeholder-dictionary.md` 中的占位符分类表

## 输出

- 占位符对应信息汇总

## 执行

### 有模板路径

1. 加载 `.template.docx`，提取所有 `[占位符]`
2. 对照 `references/placeholder-dictionary.md` 分类列出需提供的信息
3. ⚡ 必填项 → 硬Hook 追问律师
4. ○ 选填项 → 有默认值自动填，无默认值跳过
5. △ 条件项 → 根据案件类型判断是否追问

### 无模板路径

1. 从知识库范文提取结构要素
2. 用 `references/placeholder-dictionary.md` 生成追问清单
3. 持续追问直至框架清楚

--
- 作者：杜重阳律师（微信Dcylawer8888）
