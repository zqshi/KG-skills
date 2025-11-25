---
name: data_processor_template
description: 数据处理类型Skill的标准模板，适用于数据清洗、转换、分析等场景
---

# 数据处理Skill模板

## 🎯 模板概述

这是一个标准的数据处理Skill模板，适用于各种数据操作场景。基于此模板创建Skill可以确保符合最佳实践和规范要求。

## 📋 模板特性

### 标准功能组件
- **数据导入**: 支持多种数据格式导入
- **数据清洗**: 自动化数据质量检查和处理
- **数据转换**: 格式转换和计算功能
- **数据导出**: 多种输出格式支持
- **质量验证**: 数据质量检查和报告

### 技术架构
- **模块化设计**: 清晰的职责分离
- **错误处理**: 完善的异常处理机制
- **性能优化**: 内存和性能考虑
- **可扩展性**: 易于添加新功能

## 🏗️ 推荐文件结构

```
data_processor_skill/
├── SKILL.md                      # 主技能文件
├── README.md                     # 使用说明
├── scripts/
│   ├── data_importer.py          # 数据导入模块
│   ├── data_cleaner.py           # 数据清洗模块
│   ├── data_transformer.py       # 数据转换模块
│   ├── data_exporter.py          # 数据导出模块
│   └── quality_checker.py        # 质量检查模块
├── templates/
│   └── report_template.md        # 报告模板
├── examples/
│   ├── basic_cleaning/           # 基础清洗示例
│   ├── advanced_analysis/        # 高级分析示例
│   └── custom_transformation/    # 自定义转换示例
└── utils/
    ├── file_helpers.py           # 文件操作工具
    ├── validation_rules.py       # 验证规则
    └── logging_utils.py          # 日志工具
```

## 📝 SKILL.md 模板内容

```yaml
---
name: your_data_processor
description: [在此填写具体的数据处理功能描述]
---

# [Skill名称]

## 🎯 概述

[详细描述Skill的数据处理功能]

## 🚀 快速开始

### 基本使用
```
使用 [skill_name] 处理数据文件
```

### 输入格式支持
- **CSV文件**: 逗号分隔值格式
- **Excel文件**: .xlsx, .xls 格式
- **JSON文件**: JavaScript对象表示法
- **数据库**: SQL查询结果

### 输出格式
- 处理后的数据文件
- 数据质量报告
- 统计分析结果

## 📊 数据处理流程

### 1. 数据导入
- 验证文件格式和完整性
- 解析数据到内存结构
- 基础数据验证

### 2. 数据清洗
- 处理缺失值
- 纠正数据类型
- 去除重复记录
- 标准化数据格式

### 3. 数据转换
- 计算衍生字段
- 数据聚合操作
- 格式转换
- 数据 enrichment

### 4. 质量检查
- 数据完整性验证
- 业务规则检查
- 异常值检测

### 5. 结果导出
- 生成处理报告
- 导出处理结果
- 保存中间状态

## 🎪 使用示例

### 示例1: 基础数据清洗
```
使用 data_processor 清洗客户数据文件
输入: customers.csv
输出: cleaned_customers.csv
```

### 示例2: 高级数据分析
```
使用 data_processor 分析销售数据
输入: sales_data.xlsx
输出: sales_report.pdf, analysis_results.json
```

## 🔧 配置选项

### 数据处理参数
```yaml
cleaning:
  remove_duplicates: true
  fill_missing: mean
  standardize_dates: true

transformation:
  create_derived_fields: true
  aggregate_by: ["category", "date"]
  normalize_values: true
```

### 性能配置
```yaml
performance:
  chunk_size: 1000
  max_memory_mb: 512
  parallel_processing: true
```

## ⚠️ 注意事项

### 数据安全
- 确保敏感数据加密处理
- 遵守数据隐私法规
- 定期清理临时文件

### 性能考虑
- 大文件处理使用流式读取
- 内存使用监控和限制
- 超时处理机制

### 错误处理
- 详细的错误日志记录
- 优雅的错误恢复机制
- 用户友好的错误信息

---

**基于此模板创建专业的数据处理Skill！** 📊
```

## 🐍 Python脚本模板

### 数据导入模块模板
```python
#!/usr/bin/env python3
"""
数据导入模块 - 支持多种数据格式导入
"""

import pandas as pd
from pathlib import Path
from typing import Union, Dict, Any


class DataImporter:
    """数据导入器"""

    @staticmethod
    def import_csv(file_path: Union[str, Path]) -> pd.DataFrame:
        """导入CSV文件"""
        try:
            return pd.read_csv(file_path, encoding='utf-8')
        except Exception as e:
            raise ValueError(f"CSV导入失败: {e}")

    @staticmethod
    def import_excel(file_path: Union[str, Path]) -> Dict[str, pd.DataFrame]:
        """导入Excel文件"""
        try:
            return pd.read_excel(file_path, sheet_name=None)
        except Exception as e:
            raise ValueError(f"Excel导入失败: {e}")

    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> bool:
        """验证DataFrame有效性"""
        if df.empty:
            raise ValueError("数据框为空")

        if df.shape[0] == 0:
            raise ValueError("数据框没有行数据")

        return True
```

### 数据清洗模块模板
```python
#!/usr/bin/env python3
"""
数据清洗模块 - 自动化数据质量处理
"""

import pandas as pd
import numpy as np
from typing import List, Dict


class DataCleaner:
    """数据清洗器"""

    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
        """处理缺失值"""
        if strategy == 'drop':
            return df.dropna()
        elif strategy == 'fill_mean':
            return df.fillna(df.mean(numeric_only=True))
        elif strategy == 'fill_median':
            return df.fillna(df.median(numeric_only=True))
        else:
            return df

    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        """去除重复记录"""
        return df.drop_duplicates()

    @staticmethod
    def standardize_dates(df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
        """标准化日期格式"""
        result = df.copy()

        for col in date_columns:
            if col in result.columns:
                result[col] = pd.to_datetime(result[col], errors='coerce')

        return result
```

## 📊 质量检查模板

### 数据质量报告模板
```markdown
# 数据质量报告

## 基本信息
- 处理时间: [timestamp]
- 数据文件: [filename]
- 记录数量: [record_count]

## 质量指标

### 完整性
- 总记录数: [total_records]
- 缺失值数量: [missing_count]
- 完整性得分: [completeness_score]%

### 准确性
- 数据类型错误: [type_errors]
- 范围违规: [range_violations]
- 准确性得分: [accuracy_score]%

### 一致性
- 重复记录: [duplicate_count]
- 格式不一致: [format_issues]
- 一致性得分: [consistency_score]%

## 问题详情

### 严重问题
- [问题描述1]
- [问题描述2]

### 建议改进
- [改进建议1]
- [改进建议2]

## 处理建议

[根据质量指标给出的处理建议]
```

## 🔄 自定义扩展指南

### 添加新的数据格式支持
1. 在 `DataImporter` 类中添加新的导入方法
2. 更新输入格式文档
3. 添加相应的测试用例

### 添加新的清洗规则
1. 在 `DataCleaner` 类中添加新的清洗方法
2. 更新配置选项
3. 验证清洗效果

### 性能优化建议
1. 对于大数据集使用分块处理
2. 实现并行处理逻辑
3. 添加内存使用监控

---

**使用此模板，快速构建专业的数据处理Skill！** 🚀