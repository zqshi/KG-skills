---
name: api_integrator_template
description: API集成Skill模板
---

# API Integrator Template

这是一个API集成Skill的标准化模板，用于与外部API进行交互和数据同步。

## 模板特性

- 支持RESTful API调用
- 认证和授权处理（API Key, OAuth, JWT）
- 请求限流和重试机制
- 响应数据解析和错误处理
- 缓存策略支持

## 使用说明

1. 复制此模板到新的Skill目录
2. 配置API端点和认证信息
3. 实现请求和响应处理逻辑
4. 添加错误处理和重试机制
5. 测试API集成

## 快速开始

```bash
# 使用模板创建新Skill
cp -r api_integrator_template my_api_integration

# 配置API信息
cd my_api_integration
# 编辑 scripts/api_client.py 配置API端点和认证

# 测试
python scripts/api_client.py --endpoint https://api.example.com/data
```

## 配置选项

- `api_endpoint`: API基础URL
- `auth_type`: 认证类型 (api_key, oauth, jwt, basic)
- `rate_limit`: 请求限流 (请求/秒)
- `timeout`: 请求超时时间 (秒)
- `retry_attempts`: 重试次数
- `cache_enabled`: 是否启用缓存

## 支持的认证方式

1. **API Key**: 在请求头或参数中包含API密钥
2. **OAuth 2.0**: 支持授权码流程和客户端凭证流程
3. **JWT**: JSON Web Token认证
4. **Basic Auth**: HTTP基本认证

## 错误处理

- 网络错误自动重试
- HTTP状态码检查
- 响应数据验证
- 详细的错误日志

## 最佳实践

- 使用环境变量存储敏感信息（API密钥等）
- 实现请求限流避免触发API限制
- 对频繁请求的数据实现缓存
- 记录详细的日志便于调试