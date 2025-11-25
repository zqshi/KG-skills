---
name: collect_knowledge_sources
description: 从多个来源采集知识内容，支持网页、文档、API等多种格式，验证来源可用性并标准化输出
tools: [WebFetch, Read, Write, Bash]
---

# collect_knowledge_sources - 知识源采集器

## 🎯 核心功能

自动从多个来源采集知识内容，验证来源可用性，执行多源并行采集，检查内容完整性，并进行格式化处理。

## 📋 工作流SOP

**工作流SOP**：
```
1. 接收采集请求
2. 验证来源可用性
3. 执行多源并行采集
4. 检查内容完整性
5. 进行格式化处理
6. 返回采集结果
```

### 详细流程说明

**步骤1：接收采集请求**
- 验证输入参数的完整性和有效性
- 检查来源URL和文件路径格式
- 解析内容类型和采集策略
- 记录采集请求基本信息

**步骤2：验证来源可用性**
- 检查网络来源的连通性
- 验证文件路径的有效性
- 确认API接口的可访问性
- 验证访问权限和认证信息
- 生成来源可用性报告

**步骤3：执行多源并行采集**
- 根据采集策略启动并行任务
- 网页内容：使用WebFetch获取
- 文档文件：读取并解析文件内容
- API接口：调用API获取数据
- 监控采集进度和状态
- 处理采集过程中的异常

**步骤4：检查内容完整性**
- 验证采集内容的完整性
- 检查必需字段是否存在
- 验证内容格式是否符合要求
- 检查内容长度是否达标
- 识别和标记不完整内容

**步骤5：进行格式化处理**
- 统一内容编码格式（UTF-8）
- 标准化内容结构
- 提取元数据信息（标题、来源、时间等）
- 处理特殊字符和格式
- 生成标准化输出格式

**步骤6：返回采集结果**
- 生成结构化的采集结果
- 包含成功和失败统计
- 提供质量评估报告
- 返回完整的采集数据

## 🚀 快速开始

### 基本使用
```
使用 collect_knowledge_sources 采集HR政策文档
来源：公司内部网站、政策PDF、相关API
```

### 支持的来源类型
- **网页内容**: 通过WebFetch获取网页知识
- **文档文件**: 支持PDF、Word、Excel、TXT等格式
- **API接口**: 通过REST API获取结构化知识

## 📋 输入规范

### 必需输入
```json
{
  "source_urls": ["https://example.com/policy", "/path/to/document.pdf"],
  "content_types": ["web", "pdf", "api"]
}
```

**输入验证说明**：
- `source_urls`: 必需，需提供有效的URL或文件路径
- `content_types`: 必需，需与source_urls一一对应
- 如果缺少必需输入，将返回错误并提示补全信息

### 可选输入
```json
{
  "quality_requirements": {
    "min_content_length": 100,
    "required_fields": ["title", "content", "source"]
  },
  "collection_strategy": "parallel",
  "timeout_seconds": 30
}
```

## 📤 输出内容

### 标准输出
```json
{
  "collected_content": [
    {
      "source_id": "source_001",
      "source_url": "https://example.com/policy",
      "content_type": "web",
      "title": "HR政策文档",
      "content": "完整的知识内容...",
      "collection_time": "2024-01-15T10:30:00Z"
    }
  ],
  "collection_status": {
    "total_sources": 5,
    "successful_sources": 4,
    "success_rate": 0.8
  },
  "quality_report": {
    "completeness_score": 0.92,
    "format_consistency": 0.95
  }
}
```

### 错误输出（输入不完整）
```json
{
  "status": "error",
  "error_type": "missing_required_input",
  "missing_fields": ["source_urls", "content_types"],
  "message": "缺少必需输入字段：source_urls, content_types",
  "suggestions": {
    "source_urls": "请提供有效的来源地址列表，如：['https://example.com', '/path/to/file.pdf']",
    "content_types": "请提供内容类型列表，如：['web', 'pdf', 'api']"
  }
}
```

## 🎪 使用示例

### 示例1: 采集HR政策文档
```
使用 collect_knowledge_sources 采集最新HR政策
来源：
- 公司内部网站: https://hr.company.com/policies
- 政策PDF文档: /data/policies/2024_hr_policy.pdf
- API接口: https://api.company.com/knowledge/policies
```

## 🔧 配置选项

### 采集策略配置
```yaml
collection:
  strategy: parallel
  max_concurrent: 5
  timeout: 30
  
quality:
  min_content_length: 100
  required_fields: ["title", "content", "source"]
  encoding: "utf-8"
```

## ⚠️ 注意事项

### 安全考虑
- **访问权限**: 确保有权限访问所有指定的来源
- **敏感信息**: 采集内容可能包含敏感信息，需妥善处理
- **合规性**: 遵守数据来源的使用条款和版权规定

### 性能优化
- **并发控制**: 合理设置并发数，避免对来源服务器造成压力
- **缓存策略**: 对频繁访问的来源启用缓存
- **增量采集**: 定期采集时只处理新增或修改的内容

### 输入验证
- **必需字段检查**: 自动验证source_urls和content_types
- **格式验证**: 检查URL格式和文件路径有效性
- **类型匹配**: 验证content_types与来源的匹配性
- **缺失处理**: 发现缺失时返回明确的补全建议

## 📊 质量指标

- **采集成功率**: ≥95%（目标值）
- **内容完整性**: ≥90%（目标值）
- **格式一致性**: ≥95%（目标值）

---

**collect_knowledge_sources** - 让知识采集变得简单、可靠、高效！ 📚

## 🚀 快速开始

### 基本使用
```
使用 collect_knowledge_sources 采集HR政策文档
来源：公司内部网站、政策PDF、相关API
```

### 支持的来源类型
- **网页内容**: 通过WebFetch获取网页知识
- **文档文件**: 支持PDF、Word、Excel、TXT等格式
- **API接口**: 通过REST API获取结构化知识

## 📋 输入规范

### 必需输入
```json
{
  "source_urls": ["https://example.com/policy", "/path/to/document.pdf"],
  "content_types": ["web", "pdf", "api"]
}
```

### 可选输入
```json
{
  "quality_requirements": {
    "min_content_length": 100,
    "required_fields": ["title", "content", "source"]
  },
  "collection_strategy": "parallel",
  "timeout_seconds": 30
}
```

## 📤 输出内容

### 标准输出
```json
{
  "collected_content": [
    {
      "source_id": "source_001",
      "source_url": "https://example.com/policy",
      "content_type": "web",
      "title": "HR政策文档",
      "content": "完整的知识内容...",
      "collection_time": "2024-01-15T10:30:00Z"
    }
  ],
  "collection_status": {
    "total_sources": 5,
    "successful_sources": 4,
    "success_rate": 0.8
  },
  "quality_report": {
    "completeness_score": 0.92,
    "format_consistency": 0.95
  }
}
```

## 🎪 使用示例

### 示例1: 采集HR政策文档
```
使用 collect_knowledge_sources 采集最新HR政策
来源：
- 公司内部网站: https://hr.company.com/policies
- 政策PDF文档: /data/policies/2024_hr_policy.pdf
- API接口: https://api.company.com/knowledge/policies
```

## 🔧 配置选项

### 采集策略配置
```yaml
collection:
  strategy: parallel
  max_concurrent: 5
  timeout: 30
  
quality:
  min_content_length: 100
  required_fields: ["title", "content", "source"]
  encoding: "utf-8"
```

## ⚠️ 注意事项

### 安全考虑
- **访问权限**: 确保有权限访问所有指定的来源
- **敏感信息**: 采集内容可能包含敏感信息，需妥善处理
- **合规性**: 遵守数据来源的使用条款和版权规定

### 性能优化
- **并发控制**: 合理设置并发数，避免对来源服务器造成压力
- **缓存策略**: 对频繁访问的来源启用缓存
- **增量采集**: 定期采集时只处理新增或修改的内容

## 📊 质量指标

- **采集成功率**: ≥95%（目标值）
- **内容完整性**: ≥90%（目标值）
- **格式一致性**: ≥95%（目标值）

---

**collect_knowledge_sources** - 让知识采集变得简单、可靠、高效！ 📚