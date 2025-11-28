---
name: enrich_knowledge_context
description: 丰富知识上下文，分析上下文需求，补充背景信息，添加相关案例，建立外部引用，验证上下文相关性
tools: [Read, Write, Edit, WebFetch]
---

# enrich_knowledge_context - 知识上下文丰富器

## 🎯 概述

`enrich_knowledge_context` 是一个智能的知识上下文丰富Skill，能够分析知识内容的上下文需求，自动补充背景信息，添加相关案例和实例，建立外部引用，并验证上下文的相关性和价值。

## 📋 工作流SOP

**工作流SOP**：
```
1. 接收知识内容
2. 分析上下文需求
3. 补充背景信息
4. 添加相关案例
5. 建立外部引用
6. 验证上下文相关性
7. 返回增强内容
```

**核心步骤说明**：
- **需求分析**：识别背景信息、案例、引用需求
- **信息补充**：收集历史背景、政策依据、上下文解释
- **案例添加**：搜索筛选相关案例，确保实用性和相关性
- **引用建立**：识别外部资源，验证可靠性和时效性
- **相关性验证**：评估相关度，验证准确性和价值

详细流程说明请参考[REFERENCE.md](REFERENCE.md)

## 🚀 快速开始

### 基本使用
```
使用 enrich_knowledge_context 丰富年假政策上下文
知识内容：年假政策基础内容
上下文需求：补充背景信息、实际案例、相关法规
相关度阈值：0.8
```

### 支持的丰富类型
- **背景信息**: 历史背景、政策依据、制定目的
- **实际案例**: 具体案例、应用场景、实际操作
- **相关法规**: 法律法规、政策文件、标准规范
- **最佳实践**: 行业最佳实践、经验总结

### 丰富流程
1. **需求分析**: 分析知识的上下文需求
2. **信息补充**: 补充背景信息和相关案例
3. **引用建立**: 建立外部引用和参考
4. **相关性验证**: 验证上下文的相关性
5. **质量评估**: 评估丰富化质量

## 📋 输入规范

### 必需输入
```json
{
  "base_knowledge": {
    "title": "员工年假管理规定",
    "content": "员工根据工作年限享受年假..."
  },
  "context_requirements": {
    "background_info": true,
    "case_examples": true,
    "regulatory_references": true,
    "best_practices": true
  }
}
```

### 可选输入
```json
{
  "enrichment_sources": ["internal_db", "web", "industry_standards"],
  "relevance_threshold": 0.8,
  "max_enrichments": 5
}
```

## 📤 输出内容

### 标准输出
```json
{
  "enriched_knowledge": {
    "title": "员工年假管理规定",
    "content": "员工根据工作年限享受年假...",
    "background": "根据《劳动法》第45条规定，国家实行带薪年休假制度...",
    "case_examples": [
      {
        "case_title": "新员工年假计算示例",
        "description": "小王2023年3月1日入职，2024年3月1日后可享受年假...",
        "relevance_score": 0.92
      }
    ],
    "regulatory_references": [
      {
        "regulation": "《职工带薪年休假条例》",
        "reference": "国务院令第514号",
        "relevance_score": 0.95
      }
    ],
    "best_practices": [
      {
        "practice": "提前规划年假使用",
        "description": "建议员工在年初与主管沟通年假使用计划...",
        "relevance_score": 0.88
      }
    ]
  },
  "added_context": {
    "background_info": 2,
    "case_examples": 3,
    "regulatory_references": 2,
    "best_practices": 2
  },
  "relevance_scores": {
    "average_relevance": 0.89,
    "min_relevance": 0.82,
    "max_relevance": 0.95
  },
  "enrichment_quality": {
    "coverage_improvement": 0.35,
    "practical_value_score": 0.91,
    "overall_quality": 0.89
  }
}
```

## 🎪 使用示例

### 示例1: 丰富年假政策上下文
```
使用 enrich_knowledge_context 丰富年假政策

基础知识：年假天数计算规则
上下文需求：补充法律依据、实际案例、使用建议

丰富结果：
1. 背景信息：
   - 《劳动法》相关规定
   - 政策制定目的和意义

2. 实际案例：
   - 新员工年假计算示例
   - 工龄计算特殊情况处理
   - 年假与病假的关系案例

3. 法规引用：
   - 《职工带薪年休假条例》
   - 人力资源和社会保障部相关规定

4. 最佳实践：
   - 年假使用规划建议
   - 部门统筹安排方法
   - 特殊情况处理经验
```

## 🔧 配置选项

### 丰富化配置
```yaml
enrichment:
  background_info: true
  case_examples: true
  regulatory_references: true
  best_practices: true
  
sources:
  internal_db: true
  web_search: true
  industry_standards: true
  
quality:
  relevance_threshold: 0.8
  max_enrichments: 5
  verify_sources: true
```

### 高级配置
```yaml
advanced:
  context_analysis:
    identify_gaps: true
    predict_user_needs: true
    
  enrichment_strategy:
    prioritize_relevance: true
    balance_coverage: true
    
  verification:
    validate_sources: true
    check_credibility: true
```

详细高级配置请参考[REFERENCE.md](REFERENCE.md)

## ⚠️ 注意事项

- **信息质量**: 来源可靠、相关性高、时效性好
- **用户体验**: 避免冗余、保持焦点、易于理解
- **法律合规**: 版权注意、合规性、隐私保护

详细注意事项请参考[REFERENCE.md](REFERENCE.md)

## 📊 质量验证指标

### 核心指标
- **上下文相关度**: ≥85%（目标值）
- **信息价值提升**: ≥30%（目标值）
- **质量评分**: ≥4.0/5.0（目标值）
- **用户满意度**: ≥4.2/5.0（目标值）

### 评估维度
- **相关性**: 补充内容的相关程度
- **实用性**: 补充内容的实用价值
- **准确性**: 补充信息的准确性
- **完整性**: 上下文覆盖的完整程度

---

**enrich_knowledge_context** - 智能上下文丰富，提升知识价值！ 🌟

## 📚 相关文档

- [详细参考文档](REFERENCE.md) - 包含完整的工作流SOP、高级配置和注意事项详解