---
name: answer_employee_question
description: 理解员工问题意图，在知识库中搜索相关答案，组织清晰答案结构并验证准确性
tools: [Read, Write, Edit, Search]
---

# answer_employee_question - 员工问题智能回答器

## 🎯 核心功能

理解员工提出的问题，分析问题的意图和关键词，在知识库中搜索相关答案，提取最相关的知识片段，组织清晰的答案结构，并验证答案的准确性。

## 🚀 快速开始

### 基本使用
```
使用 answer_employee_question 回答员工关于年假的问题
员工问题：我今年有几天年假？怎么计算？
```

### 支持的回答类型
- **政策咨询**: 公司政策、规章制度相关问题
- **流程咨询**: 操作流程、申请步骤相关问题
- **条件咨询**: 资格条件、申请条件相关问题

## 📋 输入规范

### 必需输入
```json
{
  "question": "我今年有几天年假？怎么计算？",
  "employee_context": {
    "role": "普通员工",
    "seniority_years": 2
  }
}
```

## 📤 输出内容

### 标准输出
```json
{
  "direct_answer": "根据您的工作年限，您享有5天年假。",
  "detailed_explanation": {
    "calculation_method": "根据《员工年假管理规定》第三条...",
    "your_situation": "您已入职2年，符合工作满1年不满10年的条件。"
  },
  "confidence_score": 0.92,
  "related_questions": [
    "如何申请年假？",
    "年假可以累积到下一年吗？"
  ]
}
```

## 📊 质量指标

- **首次回答准确率**: ≥85%（目标值）
- **响应时间**: ≤30秒（目标值）
- **用户满意度**: ≥4.2/5.0（目标值）

---

**answer_employee_question** - 智能回答员工问题，提升服务体验！ 💬