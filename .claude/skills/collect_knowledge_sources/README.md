# collect_knowledge_sources - 使用指南

## 📖 概述

collect_knowledge_sources 是一个专业的知识源采集工具，支持从网页、文档、API 等多种来源自动采集知识内容，验证来源可用性，执行多源并行采集，检查内容完整性，并进行格式化处理。

## 🚀 快速开始

### 基本使用

```bash
# 使用 Python 脚本采集
python .claude/skills/collect_knowledge_sources/scripts/knowledge_collector.py \
  --sources https://example.com/policy /path/to/document.pdf \
  --types web pdf \
  --output collected_knowledge.json
```

### 在 Claude Agent 中使用

```python
使用 collect_knowledge_sources 采集HR政策文档
来源：
- 公司内部网站: https://hr.company.com/policies
- 政策PDF文档: /data/policies/2024_hr_policy.pdf
- API接口: https://api.company.com/knowledge/policies
```

## 📋 功能特性

### 支持的来源类型

- **网页内容**: 通过 WebFetch 获取网页知识
- **文档文件**: 支持 PDF、Word、Excel、TXT、Markdown 等格式
- **API接口**: 通过 REST API 获取结构化知识
- **数据库**: 从数据库中查询和提取知识

### 核心功能

- ✅ **多源并行采集**: 同时从多个来源采集，提高效率
- ✅ **来源可用性验证**: 自动验证来源的可用性和访问权限
- ✅ **内容完整性检查**: 验证采集内容的完整性和质量
- ✅ **格式标准化**: 统一编码格式和内容结构
- ✅ **错误处理和重试**: 自动处理错误和失败重试
- ✅ **质量评估**: 提供采集质量报告

## 📊 输入输出

### 输入参数

```json
{
  "source_urls": [
    "https://example.com/policy",
    "/path/to/document.pdf",
    "https://api.company.com/knowledge"
  ],
  "content_types": ["web", "pdf", "api"],
  "quality_requirements": {
    "min_content_length": 100,
    "required_fields": ["title", "content", "source"]
  },
  "collection_strategy": "parallel",
  "timeout_seconds": 30
}
```

### 输出结果

```json
{
  "collected_content": [
    {
      "source_id": "source_001",
      "source_url": "https://example.com/policy",
      "content_type": "web",
      "title": "HR政策文档",
      "content": "完整的知识内容...",
      "metadata": {
        "author": "HR部门",
        "publish_date": "2024-01-01",
        "word_count": 1500
      },
      "collection_time": "2024-01-15T10:30:00Z",
      "quality_score": 0.95
    }
  ],
  "collection_status": {
    "total_sources": 5,
    "successful_sources": 4,
    "failed_sources": 1,
    "success_rate": 0.8,
    "total_time_seconds": 45
  },
  "quality_report": {
    "completeness_score": 0.92,
    "format_consistency": 0.95,
    "average_quality": 0.935
  }
}
```

## 🔧 配置说明

### 基本配置

```yaml
# config/collection.yaml
collection:
  strategy: parallel          # 采集策略：parallel/sequential
  max_concurrent: 5          # 最大并发数
  timeout: 30                # 超时时间（秒）
  retry_attempts: 3          # 重试次数
  retry_delay: 5             # 重试延迟（秒）
  
quality:
  min_content_length: 100    # 最小内容长度
  required_fields: ["title", "content", "source"]  # 必需字段
  encoding: "utf-8"          # 编码格式
  validate_encoding: true    # 验证编码
```

### 来源特定配置

```yaml
# 网页采集配置
source:
  web:
    user_agent: "KnowledgeCollector/1.0"
    timeout: 30
    follow_redirects: true
    verify_ssl: true
    handle_javascript: false
    
  # 文件采集配置
  file:
    supported_formats: ["pdf", "docx", "xlsx", "txt", "md"]
    max_file_size: 10485760  # 10MB
    encoding_detection: true
    
  # API采集配置
  api:
    default_timeout: 30
    retry_on_error: true
    rate_limit: 100  # 请求/分钟
    authentication: "token"  # none/token/basic/oauth
```

### 错误处理配置

```yaml
error_handling:
  continue_on_error: true    # 遇到错误时继续采集
  error_log_level: "warning"  # 错误日志级别
  notify_on_failure: true    # 失败时通知
  failure_threshold: 0.2     # 失败率阈值
  max_failures: 10          # 最大失败次数
```

## 🎪 使用示例

### 示例1：采集HR政策文档

```python
使用 collect_knowledge_sources 采集最新HR政策
来源：
- 公司内部网站: https://hr.company.com/policies
- 政策PDF文档: /data/policies/2024_hr_policy.pdf
- API接口: https://api.company.com/knowledge/policies

配置：
- 最小内容长度：200字
- 必需字段：标题、内容、来源、作者
- 编码验证：UTF-8
- 并发数：3（避免服务器压力）
```

### 示例2：增量采集

```python
使用 collect_knowledge_sources 增量采集更新内容

策略：
- 只采集最近7天修改的内容
- 对比已有内容，跳过重复
- 更新已有条目的变更部分
- 记录采集历史，避免重复采集
```

### 示例3：带质量要求的采集

```python
使用 collect_knowledge_sources 采集高质量内容

质量要求：
- 最小内容长度：300字
- 必需字段完整性：100%
- 内容相关性评分：≥0.8
- 来源权威性：官方文档优先
- 时效性：最近1年内
```

### 示例4：错误恢复采集

```python
使用 collect_knowledge_sources 采集（带错误恢复）

错误处理：
- 单个来源失败时继续采集其他来源
- 记录失败原因和重试建议
- 失败率超过20%时停止并报警
- 支持断点续采
```

## 📊 质量指标

### 采集成功率
- **定义**：成功采集的来源数 / 总来源数
- **目标值**：≥95%
- **影响因素**：网络稳定性、权限配置、来源可用性

### 内容完整性
- **定义**：符合质量要求的内容数 / 总采集内容数
- **目标值**：≥90%
- **评估维度**：必需字段完整性、内容长度、格式规范性

### 格式一致性
- **定义**：标准化格式内容数 / 总采集内容数
- **目标值**：≥95%
- **评估维度**：编码一致性、结构标准化、元数据完整性

### 处理效率
- **定义**：平均每个来源的采集时间
- **目标值**：≤10秒/来源
- **优化方向**：并发控制、缓存策略、增量采集

## 🔍 故障排除

### 常见问题

#### 问题1：采集超时
- **原因**：网络延迟、来源响应慢、文件过大
- **解决方案**：
  - 增加 timeout 值
  - 减少并发数
  - 分批采集大文件
  - 检查网络连接

#### 问题2：编码错误
- **原因**：来源编码不标准、特殊字符处理
- **解决方案**：
  - 启用编码验证
  - 使用 chardet 检测编码
  - 手动指定编码
  - 处理特殊字符

#### 问题3：权限不足
- **原因**：API密钥无效、文件访问权限不足
- **解决方案**：
  - 检查认证信息
  - 验证文件权限
  - 联系管理员
  - 更新访问凭证

#### 问题4：内容不完整
- **原因**：来源内容缺失、动态加载内容
- **解决方案**：
  - 检查必需字段
  - 使用浏览器自动化
  - 联系内容提供方
  - 设置内容完整性阈值

### 日志和监控

#### 日志级别
- **DEBUG**：详细的调试信息
- **INFO**：正常的操作信息
- **WARNING**：警告信息（非致命错误）
- **ERROR**：错误信息（采集失败）
- **CRITICAL**：严重错误（系统故障）

#### 监控指标
- 采集成功率趋势
- 平均采集时间
- 错误类型分布
- 来源可用性统计
- 内容质量评分

## 🔧 高级功能

### 智能调度

```yaml
scheduler:
  enabled: true
  strategies:
    - name: "business_hours"
      schedule: "0 9-18 * * 1-5"  # 工作日9-18点
      max_concurrent: 3
      
    - name: "off_peak"
      schedule: "0 0-8,19-23 * * *"  # 非高峰时段
      max_concurrent: 5
      
    - name: "weekend"
      schedule: "0 * * * 0,6"  # 周末
      max_concurrent: 8
```

### 内容去重

```yaml
deduplication:
  enabled: true
  method: "semantic"  # exact/semantic/fuzzy
  threshold: 0.95
  check_history: true
  history_retention_days: 30
```

### 智能重试

```yaml
retry:
  enabled: true
  max_attempts: 3
  backoff: "exponential"  # fixed/linear/exponential
  initial_delay: 5
  max_delay: 300
  retry_on:
    - timeout
    - network_error
    - rate_limit
```

## 📚 相关文档

- [SKILL.md](SKILL.md) - 核心功能文档
- [REFERENCE.md](REFERENCE.md) - 详细参考文档
- [examples/](examples/) - 使用示例
- [scripts/knowledge_collector.py](scripts/knowledge_collector.py) - 采集脚本

---

**collect_knowledge_sources** - 专业的知识采集解决方案 📚

**文档版本**: v1.0  
**最后更新**: 2025-11-28