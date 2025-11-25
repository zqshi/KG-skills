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

**工作流SOP**：
```
1. 接收搜索请求
2. 识别检索模式（通用/版本）
3. 解析搜索意图
4. 执行多维度搜索
5. 计算相关度评分
6. 排序搜索结果
7. 过滤重复内容
8. 返回排序结果
```

### 详细流程说明

**步骤1：接收搜索请求**
- 验证搜索关键词的有效性
- 检查搜索过滤条件的合理性
- 解析返回数量和排序偏好
- 记录搜索请求基本信息

**步骤2：识别检索模式**
- **通用检索模式**：标准知识库搜索
- **版本检索模式**：带版本控制的知识检索
- 根据输入参数自动识别模式
- 生成模式识别结果

**步骤3：解析搜索意图**
- 分析搜索关键词的语义
- 识别用户的真实需求
- 确定搜索的类型和范围
- 生成搜索意图分析

**步骤4：执行多维度搜索**
- 执行关键词全文搜索
- 执行语义相似度搜索
- 执行标签分类搜索
- 综合多维度搜索结果

**步骤5：计算相关度评分**
- 计算关键词匹配度
- 评估语义相似度
- 考虑用户上下文
- 生成综合相关度评分

**步骤6：排序搜索结果**
- 按相关度评分排序
- 考虑知识的热度和时效性
- 应用用户偏好调整
- 生成排序后的结果列表

**步骤7：过滤重复内容**
- 识别重复和相似内容
- 合并重复结果
- 选择最优版本
- 生成去重后的结果

**步骤8：返回排序结果**
- 生成结构化的搜索结果
- 包含知识ID、标题、摘要、相关度
- 提供总结果数和搜索耗时
- 返回完整的搜索结果

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
- **版本检索**: 检索特定版本的知识
- **历史检索**: 检索历史版本的知识
- **对比检索**: 对比不同版本的知识
- **时间线检索**: 查看版本变更时间线

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
  "sort_preference": "relevance"
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
      "changes_from_current": ["申请流程简化", "取消部分限制"],
      "relevance_score": 0.88,
      "last_updated": "2023-06-10"
    },
    {
      "version": "v1.0",
      "title": "员工年假管理规定（2022年版）",
      "changes_from_current": ["申请流程较复杂", "审批层级更多"],
      "relevance_score": 0.75,
      "last_updated": "2022-01-20"
    }
  ],
  "version_comparison": {
    "v2.0_vs_v1.5": {
      "similarity": 0.85,
      "major_changes": ["申请流程简化", "增加特殊情况处理"],
      "affected_sections": ["第三章", "第五章"]
    },
    "v2.0_vs_v1.0": {
      "similarity": 0.65,
      "major_changes": ["全面流程重构", "增加在线申请"],
      "affected_sections": ["全文"]
    }
  },
  "change_timeline": [
    {
      "version": "v1.0",
      "date": "2022-01-20",
      "changes": "初始版本发布",
      "author": "HR部门"
    },
    {
      "version": "v1.5",
      "date": "2023-06-10",
      "changes": "流程简化，取消部分限制",
      "author": "HR部门"
    },
    {
      "version": "v2.0",
      "date": "2024-01-15",
      "changes": "增加特殊情况处理，优化申请流程",
      "author": "HR部门"
    }
  ]
}
```

## 📊 质量指标

- **搜索响应时间**: ≤2秒（目标值）
- **首条结果相关度**: ≥85%（目标值）
- **搜索成功率**: ≥95%（目标值）
- **版本检索准确率**: ≥95%（目标值）
- **上下文一致性**: ≥90%（目标值）
- **历史完整性**: ≥95%（目标值）

---

**search_knowledge_base** - 智能搜索，精准找到所需知识！ 🔍