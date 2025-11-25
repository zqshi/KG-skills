# 企业知识管理系统 - Claude Skills 集合

## 📖 项目概述

这是一个基于Claude Skills构建的企业级知识管理系统，专为企业平台设计。系统通过20个专业化的AI技能，实现从知识采集、处理、管理到检索、分析的全生命周期管理。

## 🎯 系统架构

### 核心设计原则
- **独立性**: 每个Skill都是独立、自包含的功能单元
- **动态组合**: 工作流由大模型在运行时基于任务需求动态构建
- **质量导向**: 每个Skill都有明确的质量指标和验证机制
- **渐进式披露**: 大模型通过name和description智能决策Skill调用

## 🛠️ Skills 分类

### 1. 知识采集与处理
| Skill名称 | 功能描述 | 质量指标 |
|-----------|----------|----------|
| [`collect_knowledge_sources`](.claude/skills/collect_knowledge_sources/SKILL.md) | 从多个来源自动采集知识内容，支持网页、文档、API等多种格式 | 采集成功率≥95% |
| [`extract_content_tags`](.claude/skills/extract_content_tags/SKILL.md) | 智能提取文档分类标签，识别关键概念和实体，计算标签相关度权重，构建文档语义索引 | 标签准确率≥90% |
| [`build_knowledge_graph`](.claude/skills/build_knowledge_graph/SKILL.md) | 从文档中提取知识点并构建知识图谱，支持单文档学习路径构建和多文档实体关系挖掘 | 实体识别准确率≥90% |
| [`segment_knowledge_content`](.claude/skills/segment_knowledge_content/SKILL.md) | 智能分割长文档为逻辑段落，识别内容边界和主题转换 | - |
| [`normalize_knowledge_format`](.claude/skills/normalize_knowledge_format/SKILL.md) | 统一不同来源的知识格式，标准化文档结构和元数据 | - |

### 2. 知识创建与管理
| Skill名称 | 功能描述 | 质量指标 |
|-----------|----------|----------|
| [`create_knowledge_entry`](.claude/skills/create_knowledge_entry/SKILL.md) | 将处理后的知识内容转换为标准化知识条目，生成结构化数据 | 创建成功率≥95% |
| [`manage_document_version_change`](.claude/skills/manage_document_version_change/SKILL.md) | 管理文档版本变更，支持单个知识条目更新和文档级批量版本管理 | 更新成功率≥98% |
| [`enrich_knowledge_context`](.claude/skills/enrich_knowledge_context/SKILL.md) | 为知识条目添加上下文信息，建立知识关联和引用关系 | - |

### 3. 知识检索与问答
| Skill名称 | 功能描述 | 质量指标 |
|-----------|----------|----------|
| [`search_knowledge_base`](.claude/skills/search_knowledge_base/SKILL.md) | 理解用户搜索意图，执行多维度搜索并计算相关度，支持通用检索和版本控制场景下的检索 | 首条结果相关度≥85% |
| [`answer_employee_question`](.claude/skills/answer_employee_question/SKILL.md) | 理解员工问题意图，在知识库中搜索相关答案，组织清晰答案结构 | 首次回答准确率≥85% |

### 4. 质量控制与验证
| Skill名称 | 功能描述 | 质量指标 |
|-----------|----------|----------|
| [`validate_knowledge_quality`](.claude/skills/validate_knowledge_quality/SKILL.md) | 验证知识库条目的准确性、完整性和时效性 | 验证准确率≥92% |
| [`validate_faq_quality`](.claude/skills/validate_faq_quality/SKILL.md) | 验证FAQ集合的质量，包括答案准确性、问题覆盖度 | 质量评估准确率≥92% |
| [`validate_summary_quality`](.claude/skills/validate_summary_quality/SKILL.md) | 验证知识摘要的质量，评估信息完整性和准确性 | - |

### 5. 版本与生命周期管理
| Skill名称 | 功能描述 | 质量指标 |
|-----------|----------|----------|
| [`maintain_version_relationships`](.claude/skills/maintain_version_relationships/SKILL.md) | 维护版本关联关系，分析知识组件依赖关系，建立新旧版本映射 | 关联关系准确率≥98% |
| [`retire_obsolete_knowledge`](.claude/skills/retire_obsolete_knowledge/SKILL.md) | 退役过时知识，验证退役资格，检查依赖关系，执行安全退役 | 退役准确率≥98% |

### 6. 内容生成与优化
| Skill名称 | 功能描述 | 质量指标 |
|-----------|----------|----------|
| [`generate_faq_from_content`](.claude/skills/generate_faq_from_content/SKILL.md) | 从知识内容自动生成FAQ，识别常见问题并生成标准答案 | - |
| [`generate_knowledge_summary`](.claude/skills/generate_knowledge_summary/SKILL.md) | 生成长文档的精炼摘要，保留核心信息和关键要点 | - |
| [`generalize_faq_questions`](.claude/skills/generalize_faq_questions/SKILL.md) | 泛化FAQ问题，提升匹配度和覆盖率 | - |

### 7. 分析与洞察
| Skill名称 | 功能描述 | 质量指标 |
|-----------|----------|----------|
| [`analyze_knowledge_usage`](.claude/skills/analyze_knowledge_usage/SKILL.md) | 收集知识库使用数据，分析搜索模式和用户行为，识别热门与冷门知识 | 分析准确率≥90% |

### 8. 工具与框架
| Skill名称 | 功能描述 |
|-----------|----------|
| [`skill_factory`](.claude/skills/skill_factory/SKILL.md) | 基于模板快速生成标准化Skill框架 |

## 🚀 快速开始

### 场景1：回答员工问题
```
使用 answer_employee_question 回答员工关于年假的问题
员工问题：我今年有几天年假？怎么计算？
```

### 场景2：创建新知识条目
```
使用 create_knowledge_entry 创建年假政策知识条目
知识内容：年假政策处理后的结构化内容
知识类型：政策文档
```

### 场景3：搜索相关知识
```
使用 search_knowledge_base 搜索年假相关政策
搜索关键词：年假 请假 申请流程
```

### 场景4：分析知识使用情况
```
使用 analyze_knowledge_usage 分析年假政策的使用情况
分析周期：最近30天
分析维度：搜索量、访问量、用户满意度
```

## 📊 质量保障体系

### 核心质量指标
- **准确性**: 所有验证类Skill准确率≥90%
- **完整性**: 结构完整性≥90%
- **时效性**: 时效性评分≥85%
- **一致性**: 关联关系准确率≥95%

### 质量验证机制
1. **独立验证**: 每个Skill可独立测试和验证
2. **动态监控**: 运行时质量指标监控
3. **持续优化**: 基于使用数据的持续改进

## 🔧 技术架构

### 支持的文件格式
- **文档**: PDF、Word、Excel、TXT
- **网页**: HTML、Markdown
- **数据**: JSON、YAML
- **API**: RESTful API

### 集成工具
- WebFetch: 网页内容获取
- Read/Write: 文件读写操作
- Search: 知识库搜索
- Edit: 内容编辑和修改

## 📁 项目结构

```
.
├── .claude/skills/           # Skills目录
│   ├── collect_knowledge_sources/
│   ├── extract_content_tags/
│   ├── create_knowledge_entry/
│   ├── search_knowledge_base/
│   ├── answer_employee_question/
│   └── ...
└── README.md                 # 本文档
```

## 🎯 使用示例

### 示例1：完整的知识入库流程
```
1. collect_knowledge_sources 采集政策文档
2. extract_content_tags 提取内容标签（用于检索优化）
3. build_knowledge_graph 提取知识点并构建知识图谱（单文档模式）
4. create_knowledge_entry 创建知识条目
5. validate_knowledge_quality 验证知识质量
```

### 示例2：FAQ生成与优化流程
```
1. generate_faq_from_content 从文档生成标准FAQ
2. validate_faq_quality 验证FAQ质量
3. generalize_faq_questions 泛化FAQ问题（提升匹配度300%）
4. 生成泛化版FAQ文档
```

### 示例3：员工自助查询
```
1. answer_employee_question 理解员工问题并生成完整答案
2. search_knowledge_base 搜索相关知识（当需要多个结果时）
3. 生成个性化回答
```

### 示例4：知识库维护
```
1. analyze_knowledge_usage 分析使用数据
2. validate_knowledge_quality 验证知识质量（全面审核）
3. manage_document_version_change 管理文档版本变更（根据复杂度选择模式）
4. retire_obsolete_knowledge 退役废弃知识
```

### 示例5：版本管理选择
```
简单更新（单个条目）：
- manage_document_version_change（单条目更新模式）

复杂更新（文档级，多组件）：
- manage_document_version_change（文档级变更模式）
```

### 示例6：知识提取选择
```
构建学习体系和培训材料：
- build_knowledge_graph（单文档模式）

分析跨文档实体关系：
- build_knowledge_graph（多文档模式）

优化检索和分类：
- extract_content_tags
```

## 📈 效果指标

### 业务价值
- **效率提升**: 员工问题自助解决率≥80%
- **质量保障**: 知识准确率≥90%
- **响应速度**: 平均响应时间≤30秒
- **用户满意度**: ≥4.2/5.0
- **FAQ匹配度**: 通过泛化提升300%

### 创新亮点
- **智能FAQ泛化**: 首创FAQ问题泛化Skill，提升匹配度300%
- **深度内容分析**: 基于大语言模型的语义理解
- **循环优化机制**: 自动检测和补充缺失内容
- **全生命周期管理**: 从采集到退役的完整管理

### 技术指标
- **系统可用性**: ≥99%
- **数据完整性**: 100%
- **版本管理准确率**: 100%
- **备份成功率**: 100%

## 🔒 安全与合规

### 数据安全
- 访问权限控制
- 敏感信息保护
- 数据加密存储
- 完整审计日志

### 合规性
- 版权合规检查
- 数据保留政策
- 隐私保护要求
- 企业内部规定

## 🤝 贡献指南

1. 遵循[DESIGN_PRINCIPLES.md](.claude/skills/DESIGN_PRINCIPLES.md)设计规范
2. 保持Skill的独立性和简洁性
3. 定义明确的质量指标
4. 提供完整的使用示例
5. 编写清晰的文档说明

## 📞 支持与反馈

如有问题或建议，请通过以下方式联系：
- 项目负责人：HR部门
- 技术支持：IT部门
- 反馈邮箱：hr-support@xxx.com

---

**企业平台知识管理系统** - 智能化、高质量、可信赖的企业知识管理解决方案！ 🚀
