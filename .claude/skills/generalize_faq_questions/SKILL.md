---
name: generalize_faq_questions
description: 为FAQ问题生成多种表达方式，包括同义词替换、句式变换、口语化表达和场景化问题，提高用户问题匹配度和系统理解能力
tools: [Read, Write, LLM]
---

# generalize_faq_questions - FAQ问题泛化器

## 🎯 核心功能

基于大语言模型的语义理解能力，为每个标准FAQ问题生成多种表达方式，包括同义词替换、句式变换、口语化表达和场景化问题，显著提升用户问题匹配准确率和智能问答系统的理解能力。

## 📋 工作流SOP

**工作流SOP**：
```
1. 接收标准FAQ文档
2. 分析问题语义和意图
3. 生成多种表达方式
4. 验证泛化质量
5. 输出泛化版FAQ
```

### 详细流程说明

**步骤1：接收标准FAQ文档**
- 验证FAQ文档的格式和完整性
- 提取问答对内容
- 解析泛化要求（数量、风格、场景）
- 记录文档基本信息

**步骤2：分析问题语义和意图**
- 分析每个问题的核心语义
- 识别用户意图类型（概念理解、流程咨询、规则确认等）
- 提取关键概念和术语
- 生成语义分析图谱

**步骤3：生成多种表达方式**
- **同义词替换**：使用同义词和近义词替换关键词
- **句式变换**：陈述句、疑问句、反问句等多种句式
- **口语化表达**：增加日常口语化问法
- **场景化问题**：增加具体场景描述和特殊情况

**步骤4：验证泛化质量**
- 检查泛化问题是否保留原意
- 验证语义一致性
- 评估表达方式的多样性
- 计算泛化质量评分

**步骤5：输出泛化版FAQ**
- 生成结构化的泛化FAQ文档
- 包含标准问题和泛化问题列表
- 提供泛化统计和质量评估
- 返回完整的泛化结果

## 🚀 快速开始

### 基本使用
```
使用 generalize_faq_questions 对员工手册FAQ进行泛化
FAQ文档：金山软件员工手册FAQ.md
泛化数量：每个问题5种表达方式
泛化风格：正式+口语+场景
```

### 支持的泛化类型
- **同义词替换**: 使用同义词和近义词替换关键词
- **句式变换**: 陈述句、疑问句、反问句等多种句式
- **口语化表达**: 增加日常口语化问法
- **场景化问题**: 增加具体场景描述和特殊情况

### 泛化流程
1. **语义分析**: 分析问题的核心语义和用户意图
2. **表达生成**: 基于大语言模型生成多种表达方式
3. **质量验证**: 验证泛化问题的质量和语义一致性
4. **结果输出**: 生成泛化版FAQ文档

## 📋 输入规范

### 必需输入
```json
{
  "faq_document": {
    "file_path": "员工手册FAQ.md",
    "format": "markdown"
  },
  "generalization_config": {
    "questions_per_faq": 5,
    "styles": ["formal", "casual", "scenario-based"]
  }
}
```

### 可选输入
```json
{
  "semantic_threshold": 0.85,
  "diversity_score_target": 0.8,
  "preserve_intent": true,
  "include_metadata": true
}
```

## 📤 输出内容

### 标准输出
```json
{
  "generalized_faq": [
    {
      "standard_question": "忘记打卡怎么办？可以补卡吗？",
      "generalized_questions": [
        "漏打卡了怎么处理？",
        "忘记打卡能补吗？",
        "没打上卡怎么办？",
        "打卡异常怎么补救？",
        "忘记打卡会扣钱吗？"
      ],
      "answer": "忘记打卡属于考勤异常，需要在KOA中提交考勤说明流程...",
      "semantic_consistency": 0.95,
      "diversity_score": 0.88
    }
  ],
  "statistics": {
    "total_faqs": 28,
    "total_generalized_questions": 140,
    "average_per_faq": 5,
    "quality_score": 0.92
  },
  "quality_report": {
    "semantic_consistency_avg": 0.94,
    "diversity_score_avg": 0.85,
    "overall_quality": 0.91
  }
}
```

## 🎪 使用示例

### 示例1: 对员工手册FAQ进行泛化
```
使用 generalize_faq_questions 对员工手册FAQ进行泛化

输入：
- FAQ文档：金山软件员工手册FAQ.md（28个问题）
- 泛化数量：每个问题5种表达方式
- 泛化风格：正式+口语+场景

处理过程：
1. 读取并解析FAQ文档
2. 分析每个问题的语义和意图
3. 生成同义词替换（如：忘记打卡→漏打卡）
4. 生成句式变换（如：怎么办？→怎么处理？）
5. 生成口语化表达（如：没打上卡怎么办？）
6. 生成场景化问题（如：打卡异常怎么补救？）
7. 验证语义一致性
8. 输出泛化版FAQ

输出结果：
- 标准问题：28个
- 泛化问题：140个（每个5种）
- 语义一致性：平均0.94
- 多样性评分：平均0.85
```

### 示例2: 针对特定场景进行深度泛化
```
使用 generalize_faq_questions 进行场景化泛化

输入：
- FAQ文档：绩效考核FAQ.md
- 泛化数量：每个问题8种表达方式
- 重点场景：紧急求助、特殊情况、政策咨询

输出特点：
- 包含"如果...怎么办？"场景
- 包含"紧急情况下..."问法
- 包含"特殊情况下..."问法
- 包含"请问..."正式问法
```

## 🔧 配置选项

### 泛化策略配置
```yaml
generalization:
  questions_per_faq: 5
  styles:
    - formal      # 正式表达
    - casual      # 口语化表达
    - scenario    # 场景化表达
    - emergency   # 紧急求助表达
    - confirm     # 确认性表达
    
semantic:
  consistency_threshold: 0.85
  intent_preservation: true
  key_concept_protection: true

quality:
  diversity_target: 0.8
  uniqueness_check: true
  redundancy_filter: true
```

### 高级配置
```yaml
advanced:
  llm_config:
    model: "gpt-4"
    temperature: 0.7
    max_tokens: 500
    
  semantic_analysis:
    extract_key_concepts: true
    identify_user_intent: true
    analyze_question_type: true
    
  generation_strategy:
    prioritize_diversity: true
    maintain_clarity: true
    avoid_ambiguity: true
    
  validation:
    semantic_consistency_check: true
    human_review_recommendation: true
    quality_score_calculation: true
```

## ⚠️ 注意事项

### 语义一致性
- **核心概念保护**: 确保关键概念不被曲解
- **意图保持**: 保持原始问题的用户意图
- **准确性验证**: 验证泛化问题的准确性

### 多样性平衡
- **避免过度泛化**: 防止生成过于偏离原意的问题
- **保持相关性**: 确保所有泛化问题都与原问题相关
- **控制数量**: 根据问题复杂度调整泛化数量

### 质量控制
- **人工审核建议**: 对低质量泛化建议人工审核
- **持续优化**: 基于用户反馈持续优化泛化策略
- **A/B测试**: 建议进行A/B测试验证效果

## 📊 质量指标

### 核心指标
- **语义一致性**: ≥90%（目标值）
- **多样性评分**: ≥80%（目标值）
- **匹配度提升**: ≥200%（目标值）
- **生成效率**: ≤5秒/问题（目标值）

### 评估维度
- **语义保留**: 泛化问题是否保留原意
- **表达多样性**: 表达方式的多样程度
- **实用性**: 泛化问题的实际匹配效果
- **用户体验**: 是否贴近用户真实提问方式

---

**generalize_faq_questions** - 智能FAQ泛化，让问答更智能！ 🎯