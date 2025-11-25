# Excel数据处理示例

## 📋 示例概述

这个示例展示了如何使用 `excel_data_processor` Skill处理Excel文件，包括数据清洗、格式转换和报告生成。

## 🚀 快速开始

### 基本使用
```
使用 excel_data_processor 处理销售数据文件
输入文件: sales_data.xlsx
输出文件: cleaned_sales_data.xlsx
```

### 完整示例
```
使用 excel_data_processor 进行完整数据处理流程
输入: raw_data.xlsx
配置:
  - 清洗: 去除重复、填充缺失值
  - 转换: 计算总销售额、添加日期格式
  - 分析: 生成销售统计报告
输出:
  - processed_data.xlsx
  - sales_report.pdf
  - processing_log.json
```

## 📊 示例数据

### 输入数据格式
假设原始Excel文件包含以下列：
- `order_id`: 订单ID
- `customer_name`: 客户姓名
- `product_name`: 产品名称
- `quantity`: 数量
- `price`: 单价
- `order_date`: 订单日期

### 数据处理步骤

1. **数据导入**
   - 读取Excel文件
   - 验证数据完整性
   - 检测数据类型

2. **数据清洗**
   - 去除重复订单记录
   - 处理缺失的客户姓名
   - 纠正错误的价格数据
   - 标准化日期格式

3. **数据转换**
   - 计算总销售额: `quantity * price`
   - 添加产品分类
   - 生成月度汇总数据

4. **质量检查**
   - 验证数据一致性
   - 检查业务规则
   - 生成质量报告

5. **结果导出**
   - 导出处理后的Excel文件
   - 生成统计报告
   - 保存处理日志

## 🔧 配置选项

### 清洗配置
```yaml
cleaning:
  remove_duplicates: true
  fill_missing_names: "Unknown Customer"
  standardize_dates: true
  validate_prices: true
```

### 转换配置
```yaml
transformation:
  calculate_total_sales: true
  add_product_categories: true
  create_monthly_summary: true
```

### 输出配置
```yaml
output:
  format: xlsx
  include_reports: true
  save_logs: true
```

## 🎯 预期结果

### 处理后的数据
- 清洁、完整的数据集
- 标准化的格式
- 新增的计算字段

### 生成报告
- **数据质量报告**: 显示清洗结果和质量指标
- **销售统计报告**: 包含汇总统计和趋势分析
- **处理日志**: 详细的操作记录和错误信息

## ⚠️ 注意事项

### 文件大小限制
- 建议处理小于10MB的Excel文件
- 大文件请使用分块处理模式

### 数据类型支持
- 支持数字、文本、日期类型
- 公式计算可能需要额外配置

### 性能考虑
- 复杂操作可能需要较长时间
- 内存使用与数据量成正比

## 🔄 扩展用例

### 用例1: 客户数据分析
```
使用 excel_data_processor 分析客户购买行为
输入: customer_orders.xlsx
分析维度: 购买频率、平均订单价值、产品偏好
输出: customer_analysis_report.pdf
```

### 用例2: 库存管理
```
使用 excel_data_processor 处理库存数据
输入: inventory_data.xlsx
操作: 库存预警、周转率计算、补货建议
输出: inventory_report.xlsx
```

### 用例3: 财务报表
```
使用 excel_data_processor 生成财务报告
输入: financial_transactions.xlsx
计算: 收入、支出、利润、现金流
输出: financial_statements.xlsx
```

## 🐛 常见问题

### 问题1: 日期格式解析错误
**症状**: 日期列解析为文本格式
**解决方案**: 明确指定日期格式或使用日期标准化功能

### 问题2: 内存不足错误
**症状**: 处理大文件时内存溢出
**解决方案**: 使用分块处理模式或优化数据格式

### 问题3: 公式计算不更新
**症状**: Excel公式结果未重新计算
**解决方案**: 启用公式重新计算选项

## 📞 技术支持

如果遇到问题：
1. 检查输入文件格式是否正确
2. 确认有足够的系统资源
3. 参考详细错误日志
4. 查看Skill文档获取更多配置选项

---

**这个示例展示了Excel数据处理Skill的强大功能，您可以根据具体需求调整配置和扩展功能。** 📊