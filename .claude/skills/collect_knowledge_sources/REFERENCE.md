# collect_knowledge_sources - 参考文档

## 📋 输入验证详细说明

### 必需字段检查
- `source_urls`: 必需，需提供有效的URL或文件路径
- `content_types`: 必需，需与source_urls一一对应
- 如果缺少必需输入，将返回错误并提示补全信息

### 格式验证
- 检查URL格式和文件路径有效性
- 验证content_types与来源的匹配性
- 缺失处理：发现缺失时返回明确的补全建议

## 🔧 高级配置选项

### 采集策略配置
```yaml
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
  
source:
  web:
    user_agent: "KnowledgeCollector/1.0"
    timeout: 30
    follow_redirects: true
    verify_ssl: true
    
  file:
    supported_formats: ["pdf", "docx", "xlsx", "txt", "md"]
    max_file_size: 10485760  # 10MB
    
  api:
    default_timeout: 30
    retry_on_error: true
    rate_limit: 100  # 请求/分钟
```

### 错误处理配置
```yaml
error_handling:
  continue_on_error: true    # 遇到错误时继续采集
  error_log_level: "warning"  # 错误日志级别
  notify_on_failure: true    # 失败时通知
  failure_threshold: 0.2     # 失败率阈值
```

## 🎪 高级使用示例

### 示例1: 带质量要求的采集
```
使用 collect_knowledge_sources 采集高质量政策文档

配置：
- 最小内容长度：200字
- 必需字段：标题、内容、来源、作者
- 编码验证：UTF-8
- 并发数：3（避免服务器压力）
```

### 示例2: 增量采集
```
使用 collect_knowledge_sources 增量采集更新内容

策略：
- 只采集最近7天修改的内容
- 对比已有内容，跳过重复
- 更新已有条目的变更部分
```

### 示例3: 错误恢复采集
```
使用 collect_knowledge_sources 采集（带错误恢复）

错误处理：
- 单个来源失败时继续采集其他来源
- 记录失败原因和重试建议
- 失败率超过20%时停止并报警
```

## 📊 质量指标详细说明

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

## 🔍 故障排除

### 常见问题

**问题1：采集超时**
- **原因**：网络延迟、来源响应慢、文件过大
- **解决方案**：增加timeout值、减少并发数、分批采集

**问题2：编码错误**
- **原因**：来源编码不标准、特殊字符处理
- **解决方案**：启用编码验证、使用chardet检测编码、手动指定编码

**问题3：权限不足**
- **原因**：API密钥无效、文件访问权限不足
- **解决方案**：检查认证信息、验证文件权限、联系管理员

**问题4：内容不完整**
- **原因**：来源内容缺失、动态加载内容
- **解决方案**：检查必需字段、使用浏览器自动化、联系内容提供方

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

## 📚 相关文档

- [SKILL.md](SKILL.md) - 核心功能文档
- [README.md](README.md) - 用户指南
- [examples/](examples/) - 使用示例

---

**collect_knowledge_sources** - 专业的知识采集解决方案 📚