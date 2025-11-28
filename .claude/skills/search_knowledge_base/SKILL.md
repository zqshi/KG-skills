---
name: search_knowledge_base
description: 理解用户搜索意图，执行多维度搜索并计算相关度，支持通用检索和版本控制场景下的检索
tools: [Read, Write, Edit, Search]
---

# search_knowledge_base - 知识库搜索引擎

## 🎯 核心功能

理解用户的搜索意图，执行多维度搜索，计算搜索结果的相关度评分，提供排序和过滤后的搜索结果。支持两种模式：
1. **通用检索模式**：快速、精准的知识库搜索
2. **版本检索模式**：支持版本切换、对比和变更历史追溯

## 📋 工作流SOP

```
1. 接收搜索请求 → 2. 深度理解查询意图 → 3. 识别检索模式 → 4. 查询语义泛化与扩展 → 5. 执行多维度搜索 → 6. 计算相关度评分 → 7. 排序搜索结果 → 8. 过滤重复内容 → 9. 返回排序结果
```

**核心步骤说明**：
- **意图理解**：使用NLP技术分析查询语义，识别查询类型和关键实体
- **模式识别**：自动识别通用检索或版本检索模式
- **语义扩展**：基于知识库标签体系扩展同义词和相关概念
- **多维度搜索**：综合关键词、语义、标签、意图等多维度搜索
- **智能评分**：计算综合相关度评分（关键词30%、语义25%、意图20%、标签15%、上下文10%）

详细流程说明请参考[REFERENCE.md](REFERENCE.md)

## 🚀 快速开始

### 基本使用（通用检索模式）
```
使用 search_knowledge_base 搜索年假相关政策
搜索关键词：年假 请假 申请流程
```

### 基本使用（版本检索模式）
```
使用 search_knowledge_base 检索年假政策v2.0
检索查询：年假申请流程
版本偏好：最新版本
包含历史：是
```

### 支持的检索类型
- **关键词搜索**: 基于关键词的全文搜索
- **语义搜索**: 基于语义理解的智能搜索
- **标签搜索**: 基于标签的分类搜索
- **意图驱动搜索**: 基于深度意图理解的精准搜索
- **智能联想搜索**: 基于查询泛化的扩展搜索
- **版本检索**: 检索特定版本的知识
- **历史检索**: 检索历史版本的知识
- **对比检索**: 对比不同版本的知识
- **时间线检索**: 查看版本变更时间线

详细检索机制请参考[REFERENCE.md](REFERENCE.md)

## 📋 输入规范

### 必需输入（通用检索模式）
```json
{
  "search_query": "年假申请流程",
  "search_filters": {
    "category": "假期管理"
  }
}
```

### 必需输入（版本检索模式）
```json
{
  "search_query": "年假申请流程",
  "version_context": {
    "preferred_version": "latest",
    "include_historical": true
  }
}
```

### 可选输入
```json
{
  "search_mode": "general",
  "version_preference": "v2.0",
  "comparison_versions": ["v1.0", "v1.5"],
  "include_change_history": true,
  "show_impact_analysis": true,
  "result_limit": 10,
  "sort_preference": "relevance",
  "enable_intent_understanding": true,
  "enable_query_expansion": true,
  "user_context": {
    "role": "普通员工",
    "department": "技术部",
    "seniority_years": 2
  }
}
```

## 📤 输出内容

### 标准输出（通用检索模式）
```json
{
  "search_results": [
    {
      "knowledge_id": "knl_001",
      "title": "员工年假管理规定",
      "summary": "详细规定了年假申请流程",
      "relevance_score": 0.95,
      "content_type": "政策文档"
    }
  ],
  "total_count": 15,
  "search_time": 1.2
}
```

### 标准输出（版本检索模式）
```json
{
  "current_version_results": {
    "knowledge_id": "knl_001",
    "version": "v2.0",
    "title": "员工年假管理规定（2024年修订）",
    "content": "更新后的年假申请流程...",
    "relevance_score": 0.95,
    "last_updated": "2024-01-15"
  },
  "historical_versions": [
    {
      "version": "v1.5",
      "title": "员工年假管理规定（2023年修订）",
      "relevance_score": 0.88,
      "last_updated": "2023-06-10"
    }
  ],
  "version_comparison": {
    "v2.0_vs_v1.5": {
      "similarity": 0.85,
      "major_changes": ["申请流程简化", "增加特殊情况处理"]
    }
  }
}
```

完整版本检索输出示例请参考[REFERENCE.md](REFERENCE.md)

## 📊 质量指标

- **搜索响应时间**: ≤2秒（目标值）
- **首条结果相关度**: ≥85%（目标值）
- **搜索成功率**: ≥95%（目标值）
- **版本检索准确率**: ≥95%（目标值）
- **上下文一致性**: ≥90%（目标值）
- **历史完整性**: ≥95%（目标值）

---

**search_knowledge_base** - 智能搜索，精准找到所需知识！ 🔍

## 📚 相关文档

- [详细参考文档](REFERENCE.md) - 包含完整的工作流SOP、查询意图理解详解和多维度搜索机制