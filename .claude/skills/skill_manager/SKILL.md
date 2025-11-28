---
name: skill_manager
description: 统一的Skill管理系统 - 手动创建、自动分析、模板管理、工作流发现
---

# Skill Manager - 统一Skill管理系统

## 🎯 概述

`skill_manager` 是Claude Agent Skills的统一管理系统，整合了手动创建、自动分析、模板管理、工作流发现等功能。提供单一入口，确保Skill创建的标准化和一致性。

## 🚀 快速开始

### 安装

```bash
# 安装依赖
pip install pyyaml schedule requests

# 或者
pip install -r requirements.txt
```

### 基本使用

#### 方式1：手动创建Skill
```bash
# 交互式创建
python skill_manager/main.py create --interactive

# 命令行创建
python skill_manager/main.py create \
  --name data_processor \
  --description "数据处理Skill" \
  --type data_processor \
  --complexity medium
```

#### 方式2：自动分析工作流
```bash
# 分析操作日志并推荐Skill
python skill_manager/main.py analyze --log-file operations.json

# 分析并自动创建
python skill_manager/main.py analyze --auto-create
```

#### 方式3：启动调度器
```bash
# 启动周期性分析（默认30天）
python skill_manager/main.py scheduler start

# 立即执行一次
python skill_manager/main.py scheduler run-once
```

## 📁 项目结构

```
skill_manager/
├── SKILL.md                          # 主技能文件
├── README.md                         # 使用说明
├── main.py                           # 统一入口
├── core/
│   ├── __init__.py
│   ├── skill_creator.py              # Skill创建核心
│   ├── template_manager.py           # 模板管理
│   └── structure_generator.py        # 结构生成
├── cli/
│   ├── __init__.py
│   └── create_cli.py                 # 创建命令行界面
├── plugins/
│   └── workflow_analyzer/
│       ├── __init__.py
│       ├── analyzer.py               # 工作流分析
│       ├── scheduler.py              # 调度器
│       └── operation_logger.py       # 操作日志记录
├── templates/                        # 模板库
│   ├── data_processor/
│   ├── api_integrator/
│   ├── file_operator/
│   ├── content_creator/
│   └── document_generator/
├── utils/                            # 工具库
│   ├── __init__.py
│   ├── validation_rules.py
│   ├── file_helpers.py
│   └── logging_utils.py
└── config/
    └── skill_manager.yaml           # 配置文件
```

## 📋 输入规范

### 手动创建参数

```bash
python skill_manager/main.py create [选项]

选项：
  --name NAME           Skill名称（必需）
  --description DESC    Skill描述（必需）
  --type TYPE          Skill类型（data_processor/api_integrator/file_operator/content_creator/document_generator/workflow）
  --complexity LEVEL   复杂度（simple/medium/complex）
  --audience LEVEL     目标用户（beginner/intermediate/expert）
  --no-scripts         不包含脚本
  --templates          包含模板
  --requirements TEXT  自定义需求
```

### 配置文件格式

```yaml
# config/skill_manager.yaml
skill_creation:
  default_type: "knowledge_processor"
  default_complexity: "medium"
  auto_validate: true

workflow_analysis:
  cycle_days: 30
  frequency_threshold: 5
  min_sequence_length: 3

scheduler:
  enabled: true
  interval_days: 30
  execution_time: "02:00"
```

## 📤 输出内容

### 1. 创建的Skill结构

```
.claude/skills/<skill_name>/
├── SKILL.md                          # 主技能文件
├── README.md                         # 使用说明
├── scripts/                          # Python脚本
│   ├── __init__.py
│   └── main.py
├── examples/                         # 使用示例
│   └── basic_usage/
│       └── README.md
└── utils/                            # 工具函数（可选）
    ├── __init__.py
    ├── file_helpers.py
    └── validation_rules.py
```

### 2. 工作流分析报告

```json
{
  "generated_at": "2024-01-15T10:30:00Z",
  "analysis_period_days": 30,
  "total_workflows_identified": 5,
  "high_frequency_workflows": 2,
  "skills_created": 1,
  "summary": {
    "total_commands_analyzed": 1250,
    "unique_commands": 85,
    "estimated_time_saved_minutes": 450
  }
}
```

## 🎪 使用示例

### 示例1：创建数据处理Skill

```bash
# 交互式创建
$ python skill_manager/main.py create --interactive
Skill名称: data_processor
Skill描述: 处理CSV数据的Skill
Skill类型: data_processor
复杂度: medium
目标用户: intermediate
包含脚本: yes
✅ Skill创建成功: data_processor
📁 路径: .claude/skills/data_processor
```

### 示例2：自动发现工作流

```bash
# 记录操作
$ python skill_manager/plugins/workflow_analyzer/operation_logger.py interactive
/workspace $ python clean_data.py --input raw.csv
/workspace $ python analyze.py --data cleaned.csv
/workspace $ python report.py --results analysis.json
/workspace $ exit

# 分析并创建Skill
$ python skill_manager/main.py analyze --create-skills
识别出 1 个高频工作流
📋 Skill: data_processing_pipeline
   频率: 15次
   预估节省时间: 90分钟
是否创建？(y/N): y
🎉 成功创建Skill: data_processing_pipeline
```

### 示例3：使用创建的Skill

```bash
# 一键执行工作流
$ python .claude/skills/data_processing_pipeline/scripts/workflow_executor.py

# 带参数执行
$ python .claude/skills/data_processing_pipeline/scripts/workflow_executor.py \
    input_file=new_data.csv output_format=json
```

## 🔧 高级功能

### 1. 模板管理

```bash
# 列出所有模板
python skill_manager/main.py template list

# 查看模板详情
python skill_manager/main.py template show data_processor

# 添加自定义模板
python skill_manager/main.py template add my_template --base data_processor
```

### 2. 批量创建

```bash
# 从配置文件批量创建
python skill_manager/main.py batch-create --config batch_skills.yaml
```

### 3. 插件系统

```bash
# 启用工作流分析插件
python skill_manager/main.py plugin enable workflow_analyzer

# 配置插件
python skill_manager/main.py plugin config workflow_analyzer --cycle-days 14
```

## ⚠️ 注意事项

### 适用范围

✅ **支持的功能**：
- 手动创建标准化Skill
- 自动分析高频工作流
- 周期性审视和自动创建
- 模板管理和扩展
- 批量操作

❌ **限制**：
- 复杂交互式工作流（需要人工判断）
- 安全敏感操作
- 单次随机操作

### 最佳实践

1. **命名规范**：使用小写下划线格式（如 `data_processor`）
2. **功能单一**：每个Skill专注于一个明确的功能
3. **定期分析**：保持调度器运行，定期发现工作流
4. **审查推荐**：即使自动创建，也应定期审查生成的Skill
5. **模板维护**：根据使用反馈优化模板库

## 🔄 架构说明

### 统一架构优势

- **单一入口**：`main.py` 提供所有功能
- **插件化设计**：workflow_analyzer作为插件，可独立启用/禁用
- **标准化核心**：所有创建逻辑通过skill_creator统一处理
- **配置驱动**：通过配置文件控制行为
- **可扩展**：易于添加新功能或插件

### 与旧版对比

| 特性 | 旧版（分散） | 新版（统一） |
|------|-------------|-------------|
| 入口数量 | 3个 | 1个 |
| 代码重复 | 高 | 无 |
| 维护成本 | 高 | 低 |
| 学习曲线 | 陡峭 | 平缓 |
| 扩展性 | 差 | 好 |

## 📞 技术支持

### 常见问题

**Q: 如何迁移旧版Skill？**
A: 使用 `python skill_manager/main.py migrate --from old_skill_path`

**Q: 如何禁用工作流分析？**
A: 在配置文件中设置 `workflow_analysis.enabled: false`

**Q: 如何添加自定义模板？**
A: 将模板放入 `templates/` 目录，运行 `python skill_manager/main.py template refresh`

### 调试方法

```bash
# 详细日志
python skill_manager/main.py --verbose create --name test

# 测试配置
python skill_manager/main.py validate-config --config my_config.yaml
```

---

**Skill Manager** - 让Skill管理变得简单、标准、智能！ 🤖✨