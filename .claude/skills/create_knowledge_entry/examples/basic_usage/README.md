# create_knowledge_entry 基础使用示例

## 📋 示例1：创建年假政策知识条目

### 场景描述
创建一份完整的员工年假政策知识条目，包含标签提取、FAQ生成和摘要生成。

### 输入内容
```python
knowledge_content = {
    "title": "员工年假管理规定",
    "content": """
    员工年假管理规定
    
    第一章 总则
    
    第一条 为规范员工年假管理，保障员工合法权益，根据国家相关法律法规，结合公司实际情况，制定本规定。
    
    第二条 本规定适用于公司全体正式员工。
    
    第二章 年假天数
    
    第三条 员工年假天数根据累计工作年限确定：
    （一）累计工作满1年不满10年的，年休假5天；
    （二）累计工作满10年不满20年的，年休假10天；
    （三）累计工作满20年的，年休假15天。
    
    第四条 员工在试用期内不享受年假。试用期满后，按在本单位剩余日历天数折算确定当年度年假天数。
    
    第三章 年假申请
    
    第五条 员工申请年假应提前3个工作日通过OA系统提交申请，经部门经理审批后方可休假。
    
    第六条 员工申请年假时应确保工作已妥善交接，不影响部门正常工作。
    
    第四章 年假安排
    
    第七条 部门应根据工作情况合理安排员工年假，确保员工权益的同时保障业务正常运转。
    
    第八条 年假原则上应在当年内休完，确因工作需要不能安排的，经员工同意，可跨1个年度安排。
    
    第五章 附则
    
    第九条 本规定由人力资源部负责解释。
    
    第十条 本规定自发布之日起施行。
    """
}
```

### 执行代码
```python
from scripts.plugin_executor import KnowledgeCreationEngine

# 创建引擎
engine = KnowledgeCreationEngine()

# 创建知识条目
result = engine.create_knowledge_entry(
    knowledge_content=knowledge_content,
    knowledge_type="政策文档",
    creation_options={
        "extract_tags": True,
        "generate_faq": True,
        "generate_summary": True,
        "build_knowledge_graph": False
    },
    selection_mode="assisted"  # 辅助模式
)

# 输出结果
print(f"知识条目ID: {result['knowledge_id']}")
print(f"处理时间: {result['creation_status']['total_processing_time']:.2f}秒")
print(f"业务价值评分: {result['value_assessment']['overall_score']:.2f}")
```

### 预期输出
```json
{
  "knowledge_id": "knl_abc123",
  "structured_content": {
    "title": "员工年假管理规定",
    "content": "...",
    "knowledge_type": "政策文档",
    "created_at": "2025-11-27T08:00:00Z",
    "version": "1.0"
  },
  "creation_results": {
    "tag_extraction": {
      "status": "completed",
      "result": [
        {
          "tag_name": "年假",
          "category": "政策类",
          "confidence": 0.95,
          "relevance": 0.92
        },
        {
          "tag_name": "工龄计算",
          "category": "流程类",
          "confidence": 0.88,
          "relevance": 0.85
        },
        {
          "tag_name": "申请流程",
          "category": "流程类",
          "confidence": 0.92,
          "relevance": 0.90
        }
      ],
      "processing_time": 0.8
    },
    "faq_generation": {
      "status": "completed",
      "result": [
        {
          "question": "年假天数如何计算？",
          "answer": "根据累计工作年限确定：满1年不满10年的5天，满10年不满20年的10天，满20年的15天。",
          "confidence": 0.88,
          "source": "第二章 年假天数"
        },
        {
          "question": "如何申请年假？",
          "answer": "应提前3个工作日通过OA系统提交申请，经部门经理审批后方可休假。",
          "confidence": 0.85,
          "source": "第三章 年假申请"
        },
        {
          "question": "年假可以累积到下一年吗？",
          "answer": "年假原则上应在当年内休完，确因工作需要不能安排的，经员工同意可跨1个年度安排。",
          "confidence": 0.82,
          "source": "第四章 年假安排"
        }
      ],
      "processing_time": 1.2
    },
    "summary_generation": {
      "status": "completed",
      "result": "本规定明确了员工年假的计算标准、申请流程和安排原则。年假天数根据累计工作年限分为5天、10天、15天三档，申请需提前3个工作日审批，原则上当年休完，特殊情况可跨年度安排。",
      "processing_time": 0.5
    }
  },
  "value_assessment": {
    "overall_score": 0.85,
    "approval_status": "approved",
    "dimension_scores": {
      "tag_value": {
        "score": 0.88,
        "level": "高"
      },
      "faq_utility": {
        "score": 0.85,
        "level": "高"
      },
      "summary_completeness": {
        "score": 0.82,
        "level": "高"
      },
      "type_value": {
        "score": 0.9,
        "level": "高"
      }
    },
    "optimization_suggestions": [
      "知识条目质量良好，建议定期更新以保持时效性"
    ]
  },
  "creation_status": {
    "overall_status": "success",
    "total_processing_time": 2.5,
    "selection_mode": "assisted",
    "recommendations": {
      "confidence": 0.85,
      "rationale": "基于120条历史记录，用户满意度85%"
    },
    "plugins_executed": ["tag_extraction", "faq_generation", "summary_generation"]
  }
}
```

## 📋 示例2：创建简单流程指南

### 场景描述
创建一份简单的办公用品申请流程，仅需要标签提取。

### 输入内容
```python
knowledge_content = {
    "title": "办公用品申请流程",
    "content": """
    办公用品申请流程
    
    1. 员工需要办公用品时，填写《办公用品申请表》
    2. 部门经理审核签字
    3. 提交至行政部门
    4. 行政部门统一采购
    5. 领取办公用品
    
    注意事项：
    - 每月15日前提交申请
    - 紧急情况可特殊处理
    - 贵重物品需额外审批
    """
}
```

### 执行代码
```python
# 创建知识条目（仅标签）
result = engine.create_knowledge_entry(
    knowledge_content=knowledge_content,
    knowledge_type="流程指南",
    creation_options={
        "extract_tags": True,
        "generate_faq": False,
        "generate_summary": False
    },
    selection_mode="auto"  # 自动模式
)

print(f"知识条目ID: {result['knowledge_id']}")
print(f"提取标签: {len(result['creation_results']['tag_extraction']['result'])}个")
```

### 预期输出
```json
{
  "knowledge_id": "knl_def456",
  "creation_results": {
    "tag_extraction": {
      "status": "completed",
      "result": [
        {
          "tag_name": "办公用品",
          "category": "流程类",
          "confidence": 0.9,
          "relevance": 0.88
        },
        {
          "tag_name": "申请流程",
          "category": "流程类",
          "confidence": 0.85,
          "relevance": 0.82
        }
      ],
      "processing_time": 0.3
    },
    "faq_generation": {
      "status": "skipped",
      "reason": "未启用FAQ生成"
    },
    "summary_generation": {
      "status": "skipped",
      "reason": "未启用摘要生成"
    }
  },
  "value_assessment": {
    "overall_score": 0.75,
    "approval_status": "approved"
  }
}
```

## 📋 示例3：防重复检查示例

### 场景描述
尝试创建一份与现有知识相似的内容，触发防重复机制。

### 输入内容
```python
# 与示例1相似的内容
knowledge_content = {
    "title": "员工年假管理细则",
    "content": """
    员工年假管理细则
    
    根据员工工龄确定年假天数：
    - 工龄1-10年：5天年假
    - 工龄10-20年：10天年假
    - 工龄20年以上：15天年假
    
    申请年假需提前3个工作日提交申请，经部门经理审批。
    """
}
```

### 执行代码
```python
# 尝试创建知识条目
result = engine.create_knowledge_entry(
    knowledge_content=knowledge_content,
    knowledge_type="政策文档",
    creation_options={
        "extract_tags": True,
        "generate_faq": True,
        "generate_summary": True
    }
)

# 检查是否触发重复检测
if result['creation_status']['overall_status'] == 'duplicate_detected':
    print("检测到相似内容！")
    print(f"建议: {result['recommendation']}")
    print("相似知识:")
    for dup in result['duplicates']:
        print(f"  - {dup['title']} (相似度: {dup['similarity']:.2f})")
```

### 预期输出
```
检测到相似内容！
建议: update_existing
相似知识:
  - 员工年假管理规定 (相似度: 0.88)
```

## 🚀 运行示例

### 方式1：直接运行
```bash
cd .claude/skills/create_knowledge_entry/examples/basic_usage
python run_example.py
```

### 方式2：交互式使用
```bash
# 启动交互式创建向导
python interactive_creator.py
```

## 📊 结果验证

### 验证标签质量
```bash
# 检查提取的标签
python verify_tags.py --knowledge-id knl_abc123
```

### 验证FAQ完整性
```bash
# 检查FAQ覆盖度
python verify_faq.py --knowledge-id knl_abc123
```

### 验证业务价值
```bash
# 评估业务价值
python assess_value.py --knowledge-id knl_abc123
```

## 🔧 故障排查

### 问题1：插件执行失败
```bash
# 检查插件健康状态
python ../../scripts/plugin_executor.py --health-check
```

### 问题2：推荐准确率偏低
```bash
# 分析历史数据
python ../../scripts/skill_recommender.py --analyze-data
```

### 问题3：重复检测不准确
```bash
# 调整相似度阈值
# 修改 config/governance.yaml
# deduplication:
#   similarity_threshold: 0.8
```

## 📈 最佳实践

### 1. 选择合适的决策模式
- **自动模式**: 历史数据充足，标准化程度高
- **辅助模式**: 推荐大多数场景，平衡效率和质量
- **手动模式**: 特殊场景，需要精细控制

### 2. 优化知识内容
- 结构清晰，章节分明
- 包含完整的上下文信息
- 使用标准术语和表述

### 3. 定期评估效果
- 监控推荐准确率
- 收集用户反馈
- 持续优化历史数据

---

**通过这些示例，您可以快速掌握 create_knowledge_entry 的使用方法，创建高质量的知识条目！** 📚✨