---
name: extract_content_tags
description: 智能提取文档分类标签，识别关键概念和实体，生成高质量标签集合并计算相关度权重
tools: [Read, Write, Edit]
---

# extract_content_tags - 内容标签提取器

## 🎯 核心功能

通过分析文档的语义特征，识别关键概念和实体，生成高质量的标签集合，并计算每个标签的相关度权重。

## 📁 项目结构

```
.claude/skills/extract_content_tags/
├── SKILL.md                    # 主技能文件
├── README.md                   # 使用说明
├── scripts/                    # Python脚本
│   ├── __init__.py
│   └── main.py                 # 主执行脚本
├── examples/                   # 使用示例
│   └── basic_usage/
│       └── README.md
└── config/                     # 配置文件
    └── tagging_config.yaml
```

## 🚀 快速开始

### 模式1：基于现有标签体系的标签提取（推荐）
```bash
# 使用示例
使用 extract_content_tags 为HR政策文档提取标签
文档内容：员工请假政策全文
工作模式：标签提取（基于现有标签体系）
标签分类体系：业务领域、内容标签、适用人群
```

### 模式2：基于文档内容的标签挖掘
```bash
# 使用示例
使用 extract_content_tags 挖掘技术文档标签
文档内容：大模型安全漏洞分析报告
工作模式：标签挖掘（基于文档内容）
最大标签数：100
```

## 📋 输入规范

### 必需输入

**模式1：标签提取（推荐）**
```json
{
  "document_content": "需要提取标签的文档内容",
  "mode": "extraction",
  "tagging_taxonomy": {
    "categories": ["业务领域", "内容标签", "适用人群"]
  }
}
```

**模式2：标签挖掘**
```json
{
  "document_content": "需要提取标签的文档内容",
  "mode": "mining",
  "max_new_tags": 10
}
```

### 可选输入
```json
{
  "max_tags": 10,
  "confidence_threshold": 0.7,
  "enable_correctness_check": true,
  "correctness_threshold": 0.8
}
```

## 📤 输出内容

```json
{
  "mode": "extraction",
  "assigned_tags": [
    {
      "tag_name": "年假",
      "confidence": 0.95,
      "category": "假期管理",
      "relevance": 0.92,
      "source": "existing_taxonomy",
      "correctness_check": {
        "passed": true,
        "content_evidence": "文档中明确提到年假相关规定",
        "confidence": 0.93
      }
    }
  ],
  "tagging_coverage": 0.89,
  "processing_stats": {
    "total_candidates": 25,
    "selected_tags": 8,
    "correctness_check_passed": 8,
    "correctness_check_failed": 0
  },
  "correctness_summary": {
    "overall_accuracy": 1.0,
    "recommendations": []
  }
}
```

## 🎪 使用示例

### 示例1: HR政策文档标签提取
```
使用 extract_content_tags 提取请假政策标签

文档内容：员工请假政策全文
工作模式：标签提取（基于现有标签体系）
标签分类体系：业务领域、内容标签、适用人群

输出标签：
1. 年假 (置信度: 0.95, 分类: 假期管理, 正确性: 通过)
2. 请假流程 (置信度: 0.88, 分类: HR政策, 正确性: 通过)
3. 病假 (置信度: 0.85, 分类: 假期管理, 正确性: 通过)

正确性检测结果：3/3 通过
```

### 示例2: 工作居住证文档标签提取
```
使用 extract_content_tags 为工作居住证文档提取标签

文档内容：新工居系统新办操作流程
工作模式：标签提取（基于现有标签体系）
标签分类体系：业务领域、内容标签、适用人群、办公地点、文档类型

输出标签：
1. 工作居住证 (置信度: 0.98, 分类: 业务领域, 正确性: 通过)
2. 操作流程 (置信度: 0.95, 分类: 内容标签, 正确性: 通过)
3. 申请材料 (置信度: 0.93, 分类: 内容标签, 正确性: 通过)

过滤标签：2025年（无业务价值）、3330（纯数字）
正确性检测结果：10/10 通过
```

## ⚠️ 核心原则

### 架构设计原则

1. **数据驱动优先**：先查询现有标签体系，基于实际数据决策
2. **模式必须明确**：强制用户选择 extraction（提取）或 mining（挖掘）模式
3. **通用化而非定制化**：通过配置实现场景适配，避免硬编码
4. **防重复机制**：查询现有标签，检测语义相似度（≥0.8）
5. **业务价值评估**：过滤无意义标签，提取流程类/材料类/要求类/政策类标签

### 质量保证机制

- **输入验证**：检查必需字段、模式相关参数、内容有效性
- **标签正确性检测**：内容匹配验证、证据支持检查、分类合理性评估
- **质量指标**：准确率≥90%、覆盖率≥85%、处理效率≤3秒/千字

## 🔧 配置选项

```yaml
# 标签提取配置
tagging:
  max_tags: 10
  confidence_threshold: 0.7
  min_frequency: 2

# 业务价值评估配置
business_value:
  enabled: true
  filter_patterns:
    - "^\d+$"  # 纯数字
    - "^\d{4}年$"  # 年份
  high_value_categories:
    - "流程类"
    - "材料类"
    - "要求类"
    - "政策类"

# 防重复检查配置
deduplication:
  enabled: true
  similarity_threshold: 0.8
  normalization:
    lowercase: true
    remove_special_chars: true
```

## 📊 质量评估

### 评估标准
1. **标签提取模式**：标签体系匹配度、内容相关性
2. **标签挖掘模式**：内容覆盖度、新颖性
3. **正确性检测**：检测准确率、误报率

### 持续改进
- 用户反馈收集与错误案例库
- 阈值调优与A/B测试
- 定期评估和优化算法

---

**extract_content_tags v2.0** - 智能标签提取，让知识组织更高效！ 🏷️

*基于架构反思和实践教训，强化了数据驱动、模式明确、通用化、防重复和业务价值评估等核心原则。*

## 📚 相关文档

- [详细参考文档](REFERENCE.md) - 包含完整的工作流SOP、核心原则详解和质量保证机制