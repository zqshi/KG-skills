# create_knowledge_entry - 知识条目创建器

## 🎯 快速开始

`create_knowledge_entry` 是一个智能知识条目创建工具，基于数据驱动推荐和插件化架构，帮助您快速创建标准化的知识条目。

### 安装要求

```bash
# 确保Python 3.8+
python --version

# 安装依赖
pip install -r requirements.txt  # 如有需要
```

### 基本使用

```python
# 示例：创建年假政策知识条目
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

## 📋 功能特性

### 核心功能
- ✅ **智能推荐**：基于历史数据推荐最佳skill组合
- ✅ **防重复检查**：自动检测相似内容，避免重复创建
- ✅ **插件化架构**：灵活扩展，容错执行
- ✅ **业务价值评估**：多维度评估知识价值
- ✅ **决策模式**：支持自动、辅助、手动三种模式

### 支持的知识类型
- 政策文档
- 流程指南
- FAQ
- 培训材料

## 🚀 使用场景

### 场景1：完整知识创建
```python
# 创建包含标签、FAQ、摘要的完整知识条目
result = engine.create_knowledge_entry(
    knowledge_content=content,
    knowledge_type="政策文档",
    creation_options={
        "extract_tags": True,
        "generate_faq": True,
        "generate_summary": True,
        "build_knowledge_graph": False
    }
)
```

### 场景2：简单知识创建
```python
# 仅创建标签的简单知识条目
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

### 场景3：复杂知识体系
```python
# 创建包含知识图谱的复杂知识体系
result = engine.create_knowledge_entry(
    knowledge_content=content,
    knowledge_type="培训材料",
    creation_options={
        "extract_tags": True,
        "generate_faq": True,
        "generate_summary": True,
        "build_knowledge_graph": True
    }
)
```

## 🔧 配置说明

### 决策模式配置
```yaml
# config/selection_modes.yaml
modes:
  auto:
    name: "自动模式"
    description: "完全基于数据驱动推荐"
    user_confirmation: false
    
  assisted:
    name: "辅助模式"
    description: "系统推荐+用户确认"
    user_confirmation: true
    
  manual:
    name: "手动模式"
    description: "用户完全手动选择"
    user_confirmation: true
```

### 插件配置
```yaml
# config/plugins.yaml
plugins:
  tag_extraction:
    enabled: true
    fallback: "simple_keyword_extraction"
    
  faq_generation:
    enabled: true
    max_questions: 50
    
  summary_generation:
    enabled: true
    target_length: "medium"
```

## 📊 质量指标

| 指标维度 | 目标值 |
|---------|--------|
| 推荐准确率 | ≥85% |
| 重复检测准确率 | ≥95% |
| 业务价值评分 | ≥0.75 |
| 插件复用率 | ≥90% |

## 🔍 故障排查

### 常见问题

**问题1：插件执行失败**
```bash
# 检查插件健康状态
python scripts/plugin_executor.py --health-check
```

**问题2：重复检测不准确**
```bash
# 调整相似度阈值
# 修改 config/governance.yaml
deduplication:
  similarity_threshold: 0.8
```

**问题3：推荐准确率偏低**
```bash
# 检查历史数据质量
python scripts/skill_recommender.py --analyze-data
```

## 📚 相关文档

- [SKILL.md](SKILL.md) - 核心功能和使用说明
- [PRINCIPLES.md](PRINCIPLES.md) - 五大核心原则详解
- [ARCHITECTURE.md](ARCHITECTURE.md) - 架构设计和技术实现
- [examples/](examples/) - 使用示例和最佳实践

## 🤝 贡献指南

欢迎提交Issue和Pull Request！在贡献代码前，请确保：
1. 遵循现有的代码规范
2. 添加相应的测试用例
3. 更新相关文档
4. 通过所有质量检查

## 📄 许可证

MIT License

---

**create_knowledge_entry** - 让知识创建更智能、更高效！ 📚✨