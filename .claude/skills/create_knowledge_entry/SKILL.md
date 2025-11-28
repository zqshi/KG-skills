---
name: create_knowledge_entry
description: 将处理后的知识内容转换为标准化知识条目，基于数据驱动智能推荐所需功能，支持插件化扩展和防重复机制
tools: [Read, Write, Edit]
---

# create_knowledge_entry - 知识条目创建器

## 🎯 核心功能

将处理后的知识内容转换为标准化的知识条目，基于历史数据智能推荐所需功能，支持插件化架构和防重复机制，确保业务价值最大化。

## 📋 工作流SOP

**工作流SOP**：
```
1. 接收知识创建请求
2. 防重复检查（基于内容指纹）
3. 分析知识内容和类型
4. 数据驱动智能推荐所需skills
5. 用户选择决策模式（自动/辅助/手动）
6. 验证skill可用性（健康检查）
7. 执行启用的插件（容错模式）
8. 创建交叉引用关系
9. 生成唯一标识
10. 执行业务价值评估
11. 整合所有生成内容
12. 返回创建结果与价值评估
```

## 🚀 快速开始

### 场景1：完整知识创建（标签+FAQ+摘要）
```python
from scripts.plugin_executor import KnowledgeCreationEngine

engine = KnowledgeCreationEngine()

result = engine.create_knowledge_entry(
    knowledge_content={
        "title": "员工年假管理规定",
        "content": "完整的政策内容..."
    },
    knowledge_type="政策文档",
    creation_options={
        "extract_tags": True,
        "generate_faq": True,
        "generate_summary": True
    },
    selection_mode="assisted"  # 自动/辅助/手动
)

print(f"知识条目ID: {result['knowledge_id']}")
print(f"业务价值评分: {result['value_assessment']['overall_score']}")
```

### 场景2：简单知识创建（仅标签）
```python
result = engine.create_knowledge_entry(
    knowledge_content=content,
    knowledge_type="流程指南",
    creation_options={
        "extract_tags": True,
        "generate_faq": False,
        "generate_summary": False
    }
)
```

### 支持的知识类型
- **政策文档**: 公司政策、规章制度
- **流程指南**: 操作指南、工作流程
- **FAQ**: 常见问题解答
- **培训材料**: 培训文档、学习资料

## 📋 输入规范

### 必需输入
```json
{
  "knowledge_content": {
    "title": "员工年假管理规定",
    "content": "完整的政策内容..."
  },
  "knowledge_type": "政策文档",
  "creation_options": {
    "extract_tags": true,
    "generate_faq": true,
    "generate_summary": true
  }
}
```

### 可选输入
```json
{
  "tag_taxonomy": {
    "categories": ["业务领域", "内容标签", "适用人群"]
  },
  "faq_config": {
    "max_questions": 10,
    "target_audience": "全体员工"
  },
  "summary_config": {
    "target_length": "medium",
    "focus_areas": ["申请条件", "审批流程"]
  }
}
```

## 📤 输出内容

### 标准输出
```json
{
  "knowledge_id": "knl_015",
  "structured_content": {
    "title": "员工年假管理规定",
    "content": "完整的政策内容...",
    "knowledge_type": "政策文档",
    "created_at": "2025-11-27T07:50:00Z",
    "version": "1.0"
  },
  "creation_results": {
    "tags": {
      "status": "completed",
      "extracted_tags": [
        {
          "tag_name": "年假",
          "category": "假期管理",
          "confidence": 0.95,
          "relevance": 0.92
        }
      ],
      "processing_time": 0.8
    },
    "faq": {
      "status": "completed",
      "generated_faqs": [
        {
          "question": "年假天数如何计算？",
          "answer": "根据工龄计算...",
          "confidence": 0.88
        }
      ],
      "processing_time": 1.2
    },
    "summary": {
      "status": "completed",
      "generated_summary": "本政策规定了员工年假的天数计算标准...",
      "processing_time": 0.5
    }
  },
  "value_assessment": {
    "overall_score": 0.85,
    "approval_status": "approved"
  }
}
```

## 📊 质量指标

| 指标维度 | 具体指标 | 目标值 |
|---------|----------|--------|
| **数据驱动** | 推荐准确率 | ≥85% |
| **模式明确** | 决策记录完整性 | 100% |
| **通用化** | 插件复用率 | ≥90% |
| **防重复** | 重复率 | <5% |
| **业务价值** | 业务价值评分 | ≥0.75 |

详细质量指标和治理机制请参考 [PRINCIPLES.md](PRINCIPLES.md) 和 [ARCHITECTURE.md](ARCHITECTURE.md)。

## 📚 相关文档

- [README.md](README.md) - 快速入门指南
- [PRINCIPLES.md](PRINCIPLES.md) - 五大核心原则详解
- [ARCHITECTURE.md](ARCHITECTURE.md) - 架构设计和技术实现
- [examples/](examples/) - 使用示例和最佳实践

---

**create_knowledge_entry** - 标准化知识条目创建，构建结构化知识库！ 📚