# Claude Skills 设计规范

## 📋 核心设计原则

### 1. 独立性原则 (Independence)
**每个Skill必须是独立、自包含的功能单元**
- Skill不应预设或硬编码对其他Skill的依赖
- Skill文档中不应包含"工作流"、"上下游依赖"、"典型工作流"等章节
- 移除所有暗示调用顺序的内容

**❌ 错误示例**
```yaml
description: 采集知识源，然后传递给extract_content_tags进行标签提取
# 包含工作流章节、上下游依赖描述
```

**✅ 正确示例**
```yaml
description: 从多个来源自动采集知识内容，支持网页、文档、API等多种格式
# 无工作流描述，无依赖关系
```

### 2. 渐进式披露原则 (Progressive Disclosure)
**大模型通过name和description判断是否调用Skill**
- description应简洁明了，聚焦核心功能
- 不包含实现细节、调用顺序、组合方式
- 让大模型基于任务上下文智能决策

**❌ 错误示例**
```yaml
description: 提取内容标签，为后续create_knowledge_entry创建条目做准备，支持多语言处理，使用先进的自然语言处理技术...
# 过长，包含实现细节和调用意图
```

**✅ 正确示例**
```yaml
description: 分析文档语义特征，自动识别关键概念和实体，生成高质量标签集合并计算相关度权重
# 简洁，聚焦核心功能
```

### 3. 动态组合原则 (Dynamic Composition)
**工作流由大模型在运行时基于任务需求动态构建**
- 不预设固定的工作流或调用链
- 大模型根据用户请求、上下文和可用Skills智能组合
- 同一任务在不同场景下可能有不同的Skill组合

**❌ 错误示例**
```
预设工作流：collect_knowledge_sources → extract_content_tags → create_knowledge_entry
```

**✅ 正确示例**
```
大模型动态决策：根据"回答员工问题"的任务，选择search_knowledge_base → answer_employee_question
```

### 4. 简洁性原则 (Simplicity)
**Skill文档结构简洁，信息密度高**
- 移除"工作流"、"上下游依赖"、"典型工作流"等章节
- 保留：核心功能、输入输出规范、使用示例、配置选项、质量指标
- 使用示例应简洁明了，不包含复杂的调用链

**允许的章节**：
- 🎯 核心功能
- 🚀 快速开始
- 📋 输入规范
- 📤 输出内容
- 🎪 使用示例
- 🔧 配置选项
- ⚠️ 注意事项
- 📊 质量指标

**移除的章节**：
- ❌ 工作流描述
- ❌ 上下游依赖
- ❌ 典型工作流
- ❌ 相关Skills（可保留为参考信息，但不作为依赖）

### 5. 质量导向原则 (Quality-Driven)
**每个Skill都有明确的质量指标**
- 定义可衡量的质量目标
- 不依赖其他Skill的质量
- 独立验证和监控

**质量指标示例**：
- 采集成功率 ≥95%
- 标签准确率 ≥90%
- 响应时间 ≤2秒

## 🏗️ Skill文档标准结构

```markdown
---
name: skill_name
description: 简洁的功能描述（不超过150字）
tools: [Tool1, Tool2]
---

# Skill名称

## 🎯 核心功能
[一句话说明核心功能]

## 🚀 快速开始
### 基本使用
[简单使用示例]

### 支持的功能类型
[功能类型列表]

## 📋 输入规范
### 必需输入
```json
{
  "required_field": "描述"
}
```

### 可选输入
```json
{
  "optional_field": "描述"
}
```

## 📤 输出内容
### 标准输出
```json
{
  "output_field": "描述"
}
```

## 🎪 使用示例
### 示例1: [场景描述]
[具体示例]

## 🔧 配置选项
### 主要配置
```yaml
config_option: value
```

### 高级配置
```yaml
advanced_option: value
```

## ⚠️ 注意事项
### [注意事项类别]
- [注意事项1]
- [注意事项2]

## 📊 质量指标
- **指标1**: ≥X%（目标值）
- **指标2**: ≤Y秒（目标值）

---
**Skill名称** - 简短标语！ [emoji]
```

## 🔄 动态组合示例

### 场景：回答员工关于年假的问题

**用户请求**："我今年有几天年假？怎么计算？"

**大模型决策过程**：
1. 分析意图：员工需要了解年假政策
2. 评估可用Skills：
   - search_knowledge_base: ✅ 可以搜索知识库
   - answer_employee_question: ✅ 可以直接回答问题
   - extract_knowledge_points: ❌ 不需要提取知识点
3. 选择最优路径：直接使用answer_employee_question
4. 动态执行：调用answer_employee_question并传入员工问题
5. 结果验证：如果需要更多信息，再考虑调用其他Skill

**不是预设路径**：
```
❌ 固定工作流：search_knowledge_base → answer_employee_question → validate_knowledge_quality
```

**而是动态决策**：
```
✅ 大模型根据上下文选择：answer_employee_question（因为可以直接回答问题）
```

### 场景：创建新的知识条目

**用户请求**："请帮我创建一个新的年假政策知识条目"

**大模型可能的工作流**（动态决定）：
```
方案A（简单）：
collect_knowledge_sources → create_knowledge_entry

方案B（完整）：
collect_knowledge_sources → extract_content_tags → extract_knowledge_points → 
generate_knowledge_summary → create_knowledge_entry → validate_knowledge_quality

大模型根据：
- 提供的材料完整性
- 用户期望的质量级别
- 可用时间和资源
动态选择方案A或B
```

## 📊 质量指标独立性

每个Skill的质量指标应独立可衡量：

**❌ 错误示例**
```yaml
质量指标：
- 端到端成功率：≥95%（依赖多个Skill）
- 整体准确率：≥90%（难以归因）
```

**✅ 正确示例**
```yaml
质量指标：
- 采集成功率：≥95%（仅collect_knowledge_sources）
- 标签准确率：≥90%（仅extract_content_tags）
- 回答准确率：≥85%（仅answer_employee_question）
```

## 🎯 设计检查清单

在创建或重构Skill时，请检查：

- [ ] description简洁明了，不超过150字
- [ ] 不包含"工作流"、"依赖"、"调用顺序"等词汇
- [ ] 没有"上下游依赖"章节
- [ ] 没有"典型工作流"章节
- [ ] 使用示例简洁，不包含多Skill调用链
- [ ] 质量指标独立可衡量
- [ ] Skill可以独立测试和验证

## 📝 重构示例对比

### 重构前（❌ 违反原则）
```markdown
---
name: collect_knowledge_sources
description: 采集知识源，为后续extract_content_tags和create_knowledge_entry提供数据
---

# collect_knowledge_sources

## 🎯 核心功能
采集知识内容，传递给下游Skill处理

## 🔗 相关Skills
### 下游依赖
- extract_content_tags
- create_knowledge_entry

### 典型工作流
collect_knowledge_sources → extract_content_tags → create_knowledge_entry
```

### 重构后（✅ 符合原则）
```markdown
---
name: collect_knowledge_sources
description: 从多个来源自动采集知识内容，支持网页、文档、API等多种格式
---

# collect_knowledge_sources

## 🎯 核心功能
自动从多个来源采集知识内容，验证来源可用性，执行多源并行采集，检查内容完整性，并进行格式化处理。
```

---

## 🔄 输入不完整处理机制

### 1. 输入验证原则 (Input Validation)
**每个Skill必须明确验证输入的完整性和有效性**

**处理流程**：
```
1. 接收调用请求
2. 验证必需输入字段
3. 识别缺失或无效的输入
4. 返回清晰的错误信息
5. 提供补全建议
```

**错误响应格式**：
```json
{
  "status": "error",
  "error_type": "missing_required_input",
  "missing_fields": ["field1", "field2"],
  "message": "缺少必需输入字段：field1, field2",
  "suggestions": {
    "field1": "请提供有效的field1，例如：...",
    "field2": "field2是必需的，用于..."
  }
}
```

### 2. 智能补全机制 (Intelligent Completion)
**大模型在检测到输入不完整时，应主动请求补全信息**

**处理策略**：
- **明确缺失**：识别具体缺少哪些必需输入
- **上下文推断**：基于已有信息推断可能的补全内容
- **交互式补全**：向用户询问缺失信息
- **默认值应用**：在适当时使用合理的默认值

**示例场景**：
```
用户：使用search_knowledge_base搜索年假政策

大模型检测：
- ✅ search_query: "年假政策"（已提供）
- ❌ search_filters: 未提供（可选，但推荐）
- ❌ result_limit: 未提供（可选，默认10）

响应：
我可以帮您搜索年假政策。为了更精确的搜索结果，您可以提供以下信息：
1. search_filters（可选）：如{"category": "假期管理"}
2. result_limit（可选）：返回结果数量，默认10条

是否立即搜索，还是需要补充这些信息？
```

### 3. 错误恢复策略 (Error Recovery)
**当输入无效或格式错误时，提供清晰的纠正指导**

**错误类型处理**：
- **类型错误**：字段类型不匹配
- **格式错误**：数据格式不符合要求
- **范围错误**：数值超出允许范围
- **引用错误**：引用的ID不存在

**恢复指导**：
```json
{
  "status": "error",
  "error_type": "invalid_input_format",
  "field": "source_urls",
  "provided_value": "invalid_url_format",
  "expected_format": "有效的URL或文件路径",
  "example": "https://example.com 或 /path/to/file.pdf"
}
```

### 4. 大模型调用决策机制
**大模型在调用Skill前的决策流程**：

```
1. 分析用户意图
2. 识别所需Skill
3. 检查必需输入：
   - 如果全部提供 → 直接调用Skill
   - 如果部分缺失 → 评估是否可以推断或补全
   - 如果关键缺失 → 向用户询问
4. 执行调用或请求补全
```

**动态决策示例**：
```
用户：创建知识条目

大模型分析：
- 意图：创建知识条目
- 所需Skill：create_knowledge_entry
- 必需输入：
  * knowledge_content: ❌ 未提供
  * knowledge_type: ❌ 未提供

响应：
我需要创建知识条目，但缺少以下必需信息：
1. knowledge_content：知识内容（必需）
2. knowledge_type：知识类型（必需，如：政策/流程/FAQ/指南）

请提供这些信息，或者您可以直接告诉我：
- 您想创建什么类型的知识？
- 知识的主要内容是什么？
```

---

**遵循这些设计原则，让Claude Skills真正发挥大模型的智能组合能力！** 🚀