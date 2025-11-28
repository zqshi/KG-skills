---
name: generate_faq_from_content
description: 基于大语言模型的智能FAQ生成器，支持全量内容分析和多维度问题生成
tools: [Read, Write, LLM]
---

# generate_faq_from_content - 智能FAQ生成器

## 🎯 核心功能

基于深度内容分析和用户意图预测，从知识内容中自动识别潜在问题点，提取对应答案，生成标准问答对并分类整理。

## 📋 工作流SOP

```
1. 接收内容输入 → 2. 识别潜在问题点 → 3. 提取对应答案 → 4. 生成标准问答对 → 5. 验证问答质量 → 6. 执行覆盖度检测 → 7. 评估覆盖度达标情况 → 8. 如未达标，大模型重新挖掘缺失内容 → 9. 持续循环检测直至覆盖度达标 → 10. 分类整理FAQ → 11. 返回FAQ集合
```

**核心步骤说明**：
- **问题识别**：分析关键概念和规则，识别可能产生疑问的复杂点
- **覆盖度检测**：调用 [`faq_completeness_checklist.py`](scripts/faq_completeness_checklist.py) 检测章节覆盖情况
- **循环优化**：调用 [`auto_faq_enrichment.py`](scripts/auto_faq_enrichment.py) 自动补充缺失内容，最多5次迭代
- **质量标准**：章节覆盖率≥80%，关键点覆盖率≥85%，高优先级章节100%覆盖

详细流程说明请参考[REFERENCE_QUALITY_CONTROL.md](REFERENCE_QUALITY_CONTROL.md)

## 📋 输入规范

### 必需输入
```json
{
  "document_content": "完整的文档内容",
  "target_audience": "目标用户群体（如：全体员工、新员工、管理层）"
}
```

### 可选输入
```json
{
  "document_type": "文档类型（policy/manual/guide）",
  "depth_level": "挖掘深度（basic/standard/comprehensive）",
  "max_questions": "最大生成问题数量（默认：50）",
  "focus_areas": ["重点关注领域列表"]
}
```

## 📤 输出内容

### FAQ集合
```json
{
  "faq_collection": [
    {
      "question": "问题文本",
      "answer": "答案文本",
      "category": "问题分类",
      "confidence": 0.95,
      "source_section": "来源章节",
      "question_type": "概念解释",
      "user_intent": "了解公司基本信息"
    }
  ],
  "metadata": {
    "total_questions": 25,
    "coverage_score": 0.92,
    "quality_score": 0.89,
    "processing_time": 12.5
  }
}
```

## 🎪 使用示例

### 示例1: 从员工手册生成FAQ
```
使用 generate_faq_from_content 从员工手册生成FAQ
文档内容：员工手册完整内容
目标用户：全体员工
挖掘深度：comprehensive
最大问题数：50
```

### 示例2: 重点关注某些领域
```
使用 generate_faq_from_content 生成绩效考核FAQ
文档内容：绩效管理制度
目标用户：全体员工
重点关注：考核标准、考核流程、申诉机制
```

## 🔧 配置选项

### 生成策略配置
```yaml
generation:
  depth_level: comprehensive
  max_questions: 50
  question_types: [concept, process, rule, obligation, scenario]
  coverage_threshold: 0.85
```

## 📊 质量指标

- **内容覆盖率**: ≥ 90%（目标值）
- **问题相关性**: ≥ 85%（目标值）
- **答案准确性**: ≥ 95%（目标值）
- **生成效率**: ≤ 15秒/文档（目标值）

## ⚠️ 注意事项

### 质量保证
- 生成后建议人工审核
- 定期更新以保持时效性
- 收集用户反馈持续优化

### 覆盖度保证机制
- **自动检测**：通过完整性检查脚本自动识别未覆盖的重要章节
- **循环优化**：使用 [`auto_faq_enrichment.py`](scripts/auto_faq_enrichment.py) 持续循环检测，确保覆盖度达标
- **大模型补充**：当检测到重要章节未覆盖时，大模型分析缺失内容并重新生成
- **质量标准**：确保章节覆盖率≥80%，关键点覆盖率≥85%，高优先级章节100%覆盖

详细技术实现和大模型工作模式请参考[REFERENCE_QUALITY_CONTROL.md](REFERENCE_QUALITY_CONTROL.md)

---

**generate_faq_from_content v2.0** - 智能FAQ生成，让知识服务更高效！ 🚀

## 📚 相关文档

- [详细参考文档](REFERENCE_QUALITY_CONTROL.md) - 包含完整的工作流SOP、大模型工作模式和质量保证机制