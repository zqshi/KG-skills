# 知识质量验证示例

本示例演示如何使用 `validate_knowledge_quality` 验证知识条目的质量。

## 📋 示例文件说明

### 示例文件
- `knowledge_sample.json` - 待验证的知识条目样本
- `validate_script.py` - 验证脚本示例

## 🚀 快速开始

### 1. 准备知识数据
确保你有一个JSON格式的知识数据文件，包含以下字段：
- `title`: 知识标题
- `content`: 知识内容
- `category`: 知识分类
- `tags`: 标签列表
- `create_time`: 创建时间
- `update_time`: 更新时间（可选）

### 2. 运行验证
```bash
cd .claude/skills/validate_knowledge_quality/examples/basic_validation
python ../../scripts/knowledge_quality_validator.py knowledge_sample.json
```

### 3. 查看结果
验证完成后会生成：
- 控制台报告：显示质量评分和详细分析
- `knowledge_quality_report.json`：详细的JSON格式报告

## 📊 预期输出示例

```
============================================================
知识质量验证报告
============================================================

📊 综合质量评分: 82.5/100

📈 各维度评分:
  • completeness: 90.0/100
  • accuracy: 85.0/100
  • timeliness: 75.0/100
  • consistency: 80.0/100

🔍 发现的问题 (2个):
  • [medium] 内容创建时间超过1年（400天前）
  • [low] 标签与分类可能不匹配

💡 改进建议:
1. [medium] 处理 1 个中优先级问题
   预计工作量: 0.3 小时
2. [low] 优化 1 个低优先级问题
   预计工作量: 0.2 小时
```

## 🎯 验证维度说明

### 1. 完整性 (Completeness) - 权重30%
- 检查必需字段是否存在
- 验证内容长度是否充足
- 确保关键信息不缺失

### 2. 准确性 (Accuracy) - 权重30%
- 检查逻辑矛盾
- 验证数据一致性
- 识别可能的错误

### 3. 时效性 (Timeliness) - 权重20%
- 检查内容创建时间
- 评估是否需要更新
- 识别过时信息

### 4. 一致性 (Consistency) - 权重20%
- 验证标签与分类匹配
- 检查格式一致性
- 确保元数据准确

## 🔧 自定义验证

### 调整验证参数
```python
from scripts.knowledge_quality_validator import KnowledgeQualityValidator

# 加载知识数据
with open('knowledge.json', 'r', encoding='utf-8') as f:
    knowledge_data = json.load(f)

# 创建验证器
validator = KnowledgeQualityValidator(knowledge_data)

# 执行验证
report = validator.generate_report()

# 查看结果
print(f"质量评分: {report['quality_score']}")
```

### 质量阈值配置
可以修改验证器中的阈值：
- 内容最小长度：默认100字符
- 时效性阈值：默认1年
- 评分权重：可调整各维度权重

## 📈 质量指标目标

- **综合质量评分**: ≥85分（目标值）
- **完整性**: ≥90%（目标值）
- **准确性**: ≥92%（目标值）
- **时效性**: ≥85%（目标值）
- **一致性**: ≥88%（目标值）

## 💡 最佳实践

### 1. 知识条目编写建议
- 确保包含所有必需字段
- 提供完整详细的内容
- 使用准确的分类和标签
- 定期更新维护

### 2. 验证频率
- 新知识点：入库前验证
- 现有知识：每季度验证一次
- 政策更新后：立即验证相关知识点

### 3. 持续改进
- 根据验证报告修正问题
- 补充缺失的字段信息
- 更新过时内容
- 优化标签分类

## 🐛 常见问题

### Q: 验证结果显示完整性低怎么办？
A: 检查是否缺少必需字段，补充title、content、category、tags等信息。

### Q: 时效性评分低如何处理？
A: 检查知识的创建时间，如果内容过时需要进行更新，或者更新update_time字段。

### Q: 一致性评分如何提高？
A: 确保标签与分类匹配，例如policy分类的知识应该有相关政策相关的标签。

## 📚 相关文档
- [validate_knowledge_quality SKILL.md](../../SKILL.md) - 完整的Skill文档
- [知识管理标准](../../templates/knowledge_template.md) - 知识条目编写标准