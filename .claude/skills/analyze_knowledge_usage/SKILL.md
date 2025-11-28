---
name: analyze_knowledge_usage
description: 收集知识库使用数据，分析搜索模式和用户行为，识别热门与冷门知识，发现使用瓶颈，生成深度洞察和优化建议
tools: [Read, Write, Edit, Search]
---

# analyze_knowledge_usage - 知识使用分析器

## 🎯 概述

`analyze_knowledge_usage` 是一个专业的知识使用分析Skill，能够收集知识库的使用数据，分析用户的搜索模式，识别热门知识和冷门知识，发现使用过程中的瓶颈，生成深度的使用洞察，并提出针对性的优化建议。

## 📋 工作流SOP

**工作流SOP**：
```
1. 收集使用数据
2. 分析搜索模式
3. 识别热门知识
4. 发现使用瓶颈
5. 生成使用洞察
6. 提出优化建议
7. 返回分析报告
```

详细流程说明请参考[REFERENCE.md](REFERENCE.md)

## 🚀 快速开始

### 基本使用
```
使用 analyze_knowledge_usage 分析年假政策的使用情况
分析周期：最近30天
分析维度：搜索量、访问量、用户满意度
重点关注：热门问题、使用瓶颈、改进机会
```

### 支持的分析类型
- **使用频率分析**: 知识的搜索和访问频率
- **用户行为分析**: 用户的搜索行为和模式
- **满意度分析**: 用户对知识的满意度
- **趋势分析**: 使用趋势和变化

### 分析流程
1. **数据收集**: 收集知识库使用数据
2. **模式分析**: 分析搜索和使用模式
3. **热门识别**: 识别热门和冷门知识
4. **瓶颈发现**: 发现使用瓶颈
5. **洞察生成**: 生成使用洞察
6. **优化建议**: 提出优化建议

## 📋 输入规范

### 必需输入
```json
{
  "analysis_period": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  },
  "usage_metrics": ["search_volume", "access_count", "user_satisfaction"],
  "focus_areas": ["popular_knowledge", "usage_bottlenecks", "improvement_opportunities"]
}
```

### 可选输入
```json
{
  "analysis_granularity": "daily",
  "user_segments": ["all_employees", "managers", "hr_staff"],
  "comparison_period": {
    "start_date": "2023-12-01",
    "end_date": "2023-12-31"
  }
}
```

## 📤 输出内容

### 标准输出
```json
{
  "usage_patterns": {
    "search_volume": {
      "total_searches": 1250,
      "daily_average": 40.3,
      "peak_days": ["2024-01-15", "2024-01-22"],
      "trend": "increasing",
      "growth_rate": 0.15
    },
    "popular_knowledge": [
      {
        "knowledge_id": "knl_001",
        "title": "员工年假管理规定",
        "search_count": 180,
        "access_count": 165,
        "satisfaction_score": 4.2,
        "trend": "stable"
      },
      {
        "knowledge_id": "knl_002",
        "title": "请假申请流程",
        "search_count": 145,
        "access_count": 132,
        "satisfaction_score": 3.8,
        "trend": "increasing"
      }
    ],
    "performance_issues": [
      {
        "issue_type": "low_satisfaction",
        "knowledge_id": "knl_003",
        "title": "报销政策规定",
        "satisfaction_score": 2.9,
        "user_feedback": ["内容不够清晰", "缺少实际案例"]
      },
      {
        "issue_type": "low_findability",
        "search_terms": ["病假工资计算"],
        "failed_searches": 25,
        "suggestion": "添加相关FAQ或优化标签"
      }
    ]
  },
  "popular_knowledge": [
    {
      "rank": 1,
      "knowledge_id": "knl_001",
      "title": "员工年假管理规定",
      "category": "假期管理",
      "search_volume": 180,
      "user_satisfaction": 4.2,
      "key_factors": ["政策更新", "年终假期规划"]
    }
  ],
  "performance_issues": [
    {
      "issue_id": "issue_001",
      "type": "content_quality",
      "severity": "medium",
      "affected_knowledge": ["knl_003"],
      "user_feedback": ["内容复杂难懂", "缺少示例"],
      "impact": "用户满意度下降15%"
    },
    {
      "issue_id": "issue_002",
      "type": "search_effectiveness",
      "severity": "low",
      "affected_queries": ["病假工资计算", "特殊假期申请"],
      "failed_rate": 0.18,
      "suggested_actions": ["添加相关FAQ", "优化搜索关键词"]
    }
  ],
  "optimization_recommendations": [
    {
      "priority": "high",
      "recommendation": "优化报销政策规定的内容清晰度",
      "expected_impact": "用户满意度提升20%",
      "effort_estimate": "2小时",
      "specific_actions": [
        "添加实际案例",
        "简化语言表述",
        "增加流程图示"
      ]
    },
    {
      "priority": "medium",
      "recommendation": "补充病假工资计算相关FAQ",
      "expected_impact": "减少搜索失败率50%",
      "effort_estimate": "1小时",
      "specific_actions": [
        "创建病假工资计算FAQ",
        "优化相关标签",
        "添加交叉引用"
      ]
    }
  ]
}
```

使用示例请参考[REFERENCE.md](REFERENCE.md)

## 🔧 配置选项

### 分析配置
```yaml
analysis:
  period: "30d"  # 7d/30d/90d/custom
  granularity: "daily"  # hourly/daily/weekly
  metrics:
    - search_volume
    - access_count
    - user_satisfaction
    - search_success_rate
    
focus_areas:
  - popular_knowledge
  - usage_bottlenecks
  - improvement_opportunities
  - user_satisfaction_trends
```

高级配置请参考[REFERENCE.md](REFERENCE.md)

注意事项请参考[REFERENCE.md](REFERENCE.md)

## 📊 质量验证指标

### 核心指标
- **分析准确率**: ≥90%（目标值）
- **洞察价值评分**: ≥4.0/5.0（目标值）
- **建议采纳率**: ≥80%（目标值）
- **处理效率**: ≤5秒/千条记录（目标值）

### 评估维度
- **准确性**: 分析结果的准确性
- **深度**: 分析的深度和广度
- **实用性**: 建议的实用性
- **及时性**: 分析的及时性

---

**analyze_knowledge_usage** - 深度分析知识使用，驱动持续优化！ 📊