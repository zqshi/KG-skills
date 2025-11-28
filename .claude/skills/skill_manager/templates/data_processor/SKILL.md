---
name: data_processor_template
description: 数据处理Skill模板
---

# Data Processor Template

这是一个数据处理Skill的标准化模板，用于处理和分析各种数据格式。

## 模板特性

- 支持CSV、JSON、Excel等常见数据格式
- 数据清洗和预处理功能
- 数据分析和统计功能
- 结果导出和报告生成

## 使用说明

1. 复制此模板到新的Skill目录
2. 修改SKILL.md中的名称和描述
3. 根据需求调整scripts/中的处理逻辑
4. 添加示例数据到examples/
5. 测试并验证功能

## 快速开始

```bash
# 使用模板创建新Skill
cp -r data_processor_template my_data_processor

# 修改配置
cd my_data_processor
# 编辑 SKILL.md 和 scripts/data_processor.py

# 测试
python scripts/data_processor.py --input sample.csv
```

## 目录结构

```
data_processor_template/
├── SKILL.md              # 主技能文件
├── README.md             # 使用说明
├── scripts/              # Python脚本
│   ├── data_processor.py # 主处理脚本
│   └── __init__.py
├── examples/             # 示例数据
│   └── sample_data/
│       ├── input.csv
│       └── output.json
└── utils/                # 工具函数
    ├── __init__.py
    └── data_helpers.py
```

## 配置选项

- `input_format`: 输入数据格式 (csv, json, excel)
- `output_format`: 输出数据格式 (csv, json, excel)
- `processing_steps`: 处理步骤列表

## 注意事项

- 确保输入数据格式正确
- 大数据集处理时注意内存使用
- 敏感数据需要脱敏处理