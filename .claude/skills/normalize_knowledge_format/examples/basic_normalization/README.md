# 知识格式规范化示例

本示例演示如何使用 `normalize_knowledge_format` 规范化知识内容的格式。

## 📋 示例文件说明

### 示例文件
- `sample_content.md` - 待规范化的知识内容样本
- `terminology_dict.json` - 术语词典配置
- `normalize_script.py` - 规范化脚本示例

## 🚀 快速开始

### 1. 准备内容文件
确保你有一个Markdown格式的知识内容文件。

### 2. 运行规范化
```bash
cd .claude/skills/normalize_knowledge_format/examples/basic_normalization
python ../../scripts/format_normalizer.py sample_content.md
```

### 3. 查看结果
规范化完成后会生成：
- 控制台报告：显示规范化评分和变更详情
- `normalized_content.md`：规范化后的内容
- `format_normalization_report.json`：详细的JSON格式报告

## 📊 预期输出示例

```
============================================================
知识格式规范化报告
============================================================

📊 一致性评分: 0.85/1.0
📊 术语统一性: 0.92/1.0
📋 总变更数: 15

📈 变更统计:
  • terminology_changes: 8
  • structure_changes: 4
  • format_changes: 3

🔍 详细变更 (15个):
1. 术语统一: 年假 → 年度休假
2. 术语统一: 主管 → 直接主管
3. 结构优化: title_format_normalization
4. 表达优化: 被批准 → 获得批准
5. 术语统一: 搞定 → 完成

💡 改进建议:
1. [medium] 统一了 8 个术语，建议建立术语词典
   预计工作量: 2小时
2. [low] 优化了 4 处文档结构
   预计工作量: 1小时
```

## 🎯 规范化维度

### 1. 术语统一 (Terminology)
- 统一专业术语的使用
- 替换不一致的词汇
- 建立标准术语词典

### 2. 结构优化 (Structure)
- 统一标题格式
- 规范列表样式
- 优化段落间距

### 3. 表达优化 (Expression)
- 统一语言风格
- 优化句式结构
- 规范用词标准

## 🔧 自定义规范化

### 调整术语词典
```python
from scripts.format_normalizer import KnowledgeFormatNormalizer

# 自定义术语标准
custom_standards = {
    "terminology": {
        "年假": "年度休假",
        "请假": "申请休假",
        "主管": "直接主管"
    },
    "expression_patterns": {
        "passive_to_active": {
            "被批准": "获得批准",
            "被要求": "需要"
        }
    }
}

# 创建规范化器
normalizer = KnowledgeFormatNormalizer(custom_standards)

# 执行规范化
normalized_content, changes = normalizer.normalize_content(original_content)
```

### 配置选项
- **terminology**: 术语映射词典
- **document_structure**: 文档结构标准
- **expression_patterns**: 表达方式转换规则

## 📈 质量指标

- **格式一致性**: ≥95%（目标值）
- **术语统一性**: ≥90%（目标值）
- **结构规范性**: ≥92%（目标值）

## 💡 最佳实践

### 1. 内容编写建议
- 使用标准术语
- 保持结构一致
- 遵循表达规范
- 定期规范化检查

### 2. 术语管理
- 建立企业术语词典
- 定期更新术语标准
- 培训内容创作者
- 自动化术语检查

### 3. 持续改进
- 收集规范化反馈
- 优化标准规则
- 更新转换模式
- 提升一致性评分

## 🐛 常见问题

### Q: 规范化后内容变化太大怎么办？
A: 可以调整术语词典，只保留最必要的术语统一，减少不必要的变更。

### Q: 如何保持特定表达方式？
A: 在expression_patterns中定义例外规则，或者将特定内容用标记保护起来。

### Q: 术语统一性评分低如何处理？
A: 扩充术语词典，确保覆盖所有常用术语，并定期更新维护。

## 📚 相关文档
- [normalize_knowledge_format SKILL.md](../../SKILL.md) - 完整的Skill文档
- [术语管理标准](../../templates/terminology_guide.md) - 术语管理最佳实践