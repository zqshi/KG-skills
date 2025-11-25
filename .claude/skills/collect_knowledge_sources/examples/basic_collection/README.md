# 基础采集示例

本示例展示如何使用 `collect_knowledge_sources` 进行基础的知识源采集。

## 📋 示例场景

采集HRSSC相关的政策文档和培训资料。

## 🚀 使用步骤

### 1. 准备配置文件

创建 `collection_config.json`:

```json
{
  "source_urls": [
    "https://hr.company.com/policies/leave",
    "https://hr.company.com/policies/benefits",
    "/data/hr-docs/2024_training_manual.pdf",
    "/data/hr-docs/onboarding_guide.docx"
  ],
  "content_types": ["web", "pdf", "doc"],
  "quality_requirements": {
    "min_content_length": 300,
    "required_fields": ["title", "content"],
    "encoding": "utf-8"
  },
  "collection_strategy": "parallel",
  "max_concurrent": 3,
  "timeout_seconds": 45,
  "retry_attempts": 2
}
```

### 2. 执行采集

```bash
python scripts/knowledge_collector.py --config collection_config.json
```

### 3. 查看结果

采集完成后，会生成类似如下的输出：

```json
{
  "collected_content": [
    {
      "source_id": "source_001",
      "source_url": "https://hr.company.com/policies/leave",
      "source_type": "web",
      "title": "请假政策",
      "content": "完整的请假政策内容...",
      "metadata": {
        "collection_time": "2024-01-15T10:30:00Z",
        "content_length": 3200,
        "language": "zh-CN"
      },
      "status": "success"
    },
    {
      "source_id": "source_002",
      "source_url": "/data/hr-docs/2024_training_manual.pdf",
      "source_type": "pdf",
      "title": "2024培训手册",
      "content": "[PDF内容: 15420 bytes]",
      "metadata": {
        "collection_time": "2024-01-15T10:30:15Z",
        "content_length": 15420,
        "file_size": 15420,
        "file_path": "/data/hr-docs/2024_training_manual.pdf"
      },
      "status": "success"
    }
  ],
  "collection_status": {
    "total_sources": 4,
    "successful_sources": 4,
    "failed_sources": 0,
    "success_rate": 1.0
  },
  "quality_report": {
    "completeness_score": 0.95,
    "format_consistency": 0.98,
    "issues_found": []
  }
}
```

## 📊 结果分析

### 采集统计
- **总来源数**: 4个
- **成功采集**: 4个
- **采集成功率**: 100%
- **平均内容长度**: 约5000字符

### 质量评估
- **完整性评分**: 95% - 所有内容都满足最小长度要求
- **格式一致性**: 98% - 输出格式统一
- **问题发现**: 无重大问题

## 🎯 关键要点

1. **多源支持**: 同时支持网页、PDF、Word文档等多种来源
2. **并行采集**: 提高采集效率，缩短总体耗时
3. **质量控制**: 自动验证内容完整性和格式一致性
4. **错误处理**: 单个来源失败不影响整体采集

## 🔧 自定义配置

### 调整并发数
对于响应较慢的来源，可以减少并发数：

```json
{
  "collection_strategy": "parallel",
  "max_concurrent": 2,  // 从3减少到2
  "timeout_seconds": 60  // 增加超时时间
}
```

### 设置质量门槛
提高内容质量要求：

```json
{
  "quality_requirements": {
    "min_content_length": 500,  // 从300增加到500
    "required_fields": ["title", "content", "author", "publish_date"]
  }
}
```

### 处理编码问题
对于非UTF-8编码的文件：

```json
{
  "quality_requirements": {
    "encoding": "gbk"  // 对于中文Windows系统生成的文件
  }
}
```

## 🐛 常见问题

### 问题：PDF文件采集失败

**症状**: PDF文件显示采集失败

**可能原因**:
1. PDF文件损坏或加密
2. 文件路径错误
3. 缺少PDF解析库

**解决方案**:
1. 验证PDF文件是否可以正常打开
2. 检查文件路径是否正确
3. 安装PyPDF2库: `pip install PyPDF2`

### 问题：网页内容采集不完整

**症状**: 网页内容比实际看到的少

**可能原因**:
1. 网页使用JavaScript动态加载内容
2. 采集超时导致内容截断

**解决方案**:
1. 增加超时时间: `"timeout_seconds": 60`
2. 对于动态网页，考虑使用专门的网页抓取工具

## 📈 扩展应用

### 定期自动采集
结合系统定时任务，实现定期自动采集：

```bash
# 每天凌晨2点执行采集
0 2 * * * cd /path/to/collect_knowledge_sources && python scripts/knowledge_collector.py --config daily_collection.json
```

### 增量采集
只采集新增或修改的内容：

```json
{
  "source_urls": [...],
  "incremental_mode": true,
  "last_collection_time": "2024-01-14T00:00:00Z"
}
```

这个基础示例展示了 `collect_knowledge_sources` 的核心功能和使用方法。根据实际需求，可以进一步定制配置和扩展功能。