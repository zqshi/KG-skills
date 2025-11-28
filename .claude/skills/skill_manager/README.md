# Skill Manager - 使用指南

## 📖 概述

Skill Manager 是 Claude Agent Skills 的统一管理系统，提供手动创建、自动分析、模板管理、工作流发现等功能。通过单一入口，确保 Skill 创建的标准化和一致性。

## 🚀 快速开始

### 安装依赖

```bash
pip install pyyaml schedule requests
```

### 基本使用

#### 1. 手动创建 Skill

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

#### 2. 自动分析工作流

```bash
# 分析操作日志并推荐 Skill
python skill_manager/main.py analyze --log-file operations.json

# 分析并自动创建
python skill_manager/main.py analyze --auto-create
```

#### 3. 启动调度器

```bash
# 启动周期性分析（默认30天）
python skill_manager/main.py scheduler start

# 立即执行一次
python skill_manager/main.py scheduler run-once
```

## 📋 命令参考

### 创建命令

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
  --interactive        交互式创建
```

### 分析命令

```bash
python skill_manager/main.py analyze [选项]

选项：
  --log-file FILE      操作日志文件路径
  --auto-create        自动创建识别出的 Skill
  --threshold N        频率阈值（默认：5）
  --min-sequence N     最小序列长度（默认：3）
```

### 调度器命令

```bash
python skill_manager/main.py scheduler [命令]

命令：
  start                启动调度器
  stop                 停止调度器
  run-once            立即执行一次
  status              查看状态
```

### 模板命令

```bash
python skill_manager/main.py template [命令]

命令：
  list                列出所有模板
  show NAME           查看模板详情
  add NAME            添加自定义模板
  refresh             刷新模板列表
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

## 📊 配置文件

### 基本配置

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

### 高级配置

```yaml
# 日志配置
logging:
  level: "INFO"
  file: "skill_manager.log"
  max_size: "10MB"
  backup_count: 5

# 模板配置
templates:
  custom_template_path: "custom_templates/"
  auto_reload: true

# 插件配置
plugins:
  workflow_analyzer:
    enabled: true
    log_retention_days: 90
    analysis_depth: "detailed"
```

## 🎪 使用示例

### 示例1：创建数据处理 Skill

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

# 分析并创建 Skill
$ python skill_manager/main.py analyze --create-skills
识别出 1 个高频工作流
📋 Skill: data_processing_pipeline
   频率: 15次
   预估节省时间: 90分钟
是否创建？(y/N): y
🎉 成功创建 Skill: data_processing_pipeline
```

### 示例3：批量创建 Skill

```bash
# 创建批量配置文件 batch_skills.yaml
skills:
  - name: "data_validator"
    description: "数据验证和清洗"
    type: "data_processor"
    complexity: "simple"
    
  - name: "report_generator"
    description: "自动生成报告"
    type: "document_generator"
    complexity: "medium"

# 批量创建
$ python skill_manager/main.py batch-create --config batch_skills.yaml
✅ 批量创建完成: 2个Skill
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

# 刷新模板列表
python skill_manager/main.py template refresh
```

### 2. 插件系统

```bash
# 启用工作流分析插件
python skill_manager/main.py plugin enable workflow_analyzer

# 配置插件
python skill_manager/main.py plugin config workflow_analyzer --cycle-days 14

# 禁用插件
python skill_manager/main.py plugin disable workflow_analyzer
```

### 3. 迁移工具

```bash
# 从旧版 Skill 迁移
python skill_manager/main.py migrate --from old_skill_path

# 批量迁移
python skill_manager/main.py migrate --batch --source-dir old_skills/
```

## ⚠️ 注意事项

### 适用范围

✅ **支持的功能**：
- 手动创建标准化 Skill
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
2. **功能单一**：每个 Skill 专注于一个明确的功能
3. **定期分析**：保持调度器运行，定期发现工作流
4. **审查推荐**：即使自动创建，也应定期审查生成的 Skill
5. **模板维护**：根据使用反馈优化模板库

### 安全考虑

- **权限控制**：确保有权限访问相关目录和文件
- **输入验证**：验证所有输入参数的有效性
- **错误处理**：完善的错误处理和日志记录
- **备份策略**：重要操作前建议备份

## 📞 技术支持

### 常见问题

**Q: 如何迁移旧版 Skill？**
A: 使用 `python skill_manager/main.py migrate --from old_skill_path`

**Q: 如何禁用工作流分析？**
A: 在配置文件中设置 `workflow_analysis.enabled: false`

**Q: 如何添加自定义模板？**
A: 将模板放入 `templates/` 目录，运行 `python skill_manager/main.py template refresh`

**Q: 如何调试 Skill 创建问题？**
A: 使用 `--verbose` 参数查看详细日志

### 调试方法

```bash
# 详细日志
python skill_manager/main.py --verbose create --name test

# 测试配置
python skill_manager/main.py validate-config --config my_config.yaml

# 检查依赖
python skill_manager/main.py check-dependencies
```

### 错误处理

| 错误类型 | 原因 | 解决方案 |
|---------|------|---------|
| `SkillExistsError` | Skill 已存在 | 使用不同的名称或删除现有 Skill |
| `InvalidTemplateError` | 模板无效 | 检查模板名称和配置 |
| `WorkflowAnalysisError` | 工作流分析失败 | 检查日志文件格式和内容 |
| `PermissionError` | 权限不足 | 检查目录和文件权限 |

---

**Skill Manager** - 让 Skill 管理变得简单、标准、智能！ 🤖✨

**文档版本**: v1.0  
**最后更新**: 2025-11-28