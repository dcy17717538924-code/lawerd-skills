# step-05：生成定卷文件

## 执行

```powershell
python $skill_dir/scripts/fill_templates.py -CasePath <案件根>
python $skill_dir/scripts/fill_closed_case_table.py -CasePath <案件根>
python $skill_dir/scripts/export_print_pdf.py -CasePath <案件根>
```

非诉案件：
```powershell
python $skill_dir/scripts/fill_templates.py -CasePath <案件根> -Type non-litigation
```

## 输入

- 必填：`-CasePath` 案件根绝对路径
- 可选：`-Type` 案件类型（`litigation` 诉讼 / `non-litigation` 非诉，默认 `litigation`）
