---
name: api_integrator_template
description: API集成类型Skill的标准模板，适用于REST API调用、数据获取、服务集成等场景
tools: [WebFetch, Read, Write, Bash]
---

# API集成Skill模板

## 🎯 模板概述

这是一个标准的API集成Skill模板，适用于各种Web服务集成场景。基于此模板创建Skill可以确保符合API集成的最佳实践和安全要求。

## 📋 模板特性

### 核心功能组件
- **API客户端**: 标准化的HTTP请求处理
- **认证管理**: 多种认证方式支持
- **错误处理**: 完善的异常处理机制
- **缓存策略**: 性能优化和限流控制
- **数据解析**: 响应数据标准化处理

### 技术架构
- **模块化设计**: 清晰的职责分离
- **安全第一**: 输入验证和错误处理
- **性能优化**: 连接池和缓存机制
- **可扩展性**: 易于添加新的API端点

## 🏗️ 推荐文件结构

```
api_integrator_skill/
├── SKILL.md                      # 主技能文件
├── README.md                     # 使用说明
├── scripts/
│   ├── api_client.py             # API客户端核心
│   ├── auth_manager.py           # 认证管理
│   ├── response_parser.py        # 响应解析器
│   ├── cache_manager.py          # 缓存管理
│   ├── rate_limiter.py           # 限流控制
│   └── error_handler.py          # 错误处理
├── templates/
│   └── api_documentation.md      # API文档模板
├── examples/
│   ├── basic_api_call/           # 基础API调用示例
│   ├── authenticated_call/       # 认证调用示例
│   └── advanced_integration/     # 高级集成示例
└── utils/
    ├── http_helpers.py           # HTTP工具
    ├── validation_rules.py       # 验证规则
    └── logging_utils.py          # 日志工具
```

## 📝 SKILL.md 模板内容

```yaml
---
name: your_api_integrator
description: [在此填写具体的API集成功能描述]
tools: [WebFetch, Read, Write, Bash]
---

# [Skill名称]

## 🎯 概述

[详细描述Skill的API集成功能]

## 🚀 快速开始

### 基本使用
```
使用 [skill_name] 调用API服务
```

### 认证配置
- **API密钥**: 简单的密钥认证
- **OAuth 2.0**: 标准的OAuth流程
- **Basic认证**: 用户名密码认证
- **Token认证**: Bearer token认证

### 支持的API功能
- [API功能1描述]
- [API功能2描述]
- [API功能3描述]

## 🔌 API集成架构

### 1. 请求构建
- URL和参数验证
- 头信息设置
- 请求体格式化

### 2. 认证处理
- 自动令牌刷新
- 安全的凭据存储
- 多认证方式支持

### 3. 请求发送
- 超时和重试机制
- 连接池管理
- SSL/TLS安全

### 4. 响应处理
- 状态码验证
- 数据解析和转换
- 错误信息提取

### 5. 缓存和限流
- 响应缓存策略
- 请求频率控制
- 配额管理

## 🎪 使用示例

### 示例1: 基础API调用
```
使用 api_integrator 获取天气信息
API端点: /weather/current
参数: city=Beijing
```

### 示例2: 认证API调用
```
使用 api_integrator 获取用户数据
认证方式: OAuth 2.0
权限范围: user.read
```

### 示例3: 批量数据处理
```
使用 api_integrator 批量更新数据
数据量: 1000条记录
并发控制: 10个并行请求
```

## 🔧 配置选项

### API配置
```yaml
api:
  base_url: https://api.example.com
  timeout: 30
  retry_attempts: 3
  retry_delay: 1
```

### 认证配置
```yaml
auth:
  type: api_key  # api_key, oauth, basic, token
  api_key: ${API_KEY}
  token_url: https://api.example.com/oauth/token
  client_id: ${CLIENT_ID}
  client_secret: ${CLIENT_SECRET}
```

### 缓存配置
```yaml
cache:
  enabled: true
  ttl: 300  # 5分钟
  max_size: 1000
```

### 限流配置
```yaml
rate_limit:
  enabled: true
  requests_per_minute: 60
  burst_capacity: 10
```

## ⚠️ 注意事项

### 安全考虑
- 妥善保管API密钥和令牌
- 使用HTTPS加密通信
- 验证API响应完整性
- 防止注入攻击

### 性能优化
- 实现连接复用
- 使用响应缓存
- 控制请求频率
- 监控API性能

### 错误处理
- 详细的错误分类
- 优雅的降级策略
- 用户友好的错误信息
- 自动重试机制

---

**基于此模板创建专业的API集成Skill！** 🌐
```

## 🐍 Python脚本模板

### API客户端核心模板
```python
#!/usr/bin/env python3
"""
API客户端核心模块 - 标准化的HTTP请求处理
"""

import requests
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class APIResponse:
    """API响应数据类"""
    status_code: int
    data: Any
    headers: Dict[str, str]
    elapsed: float


class APIClient:
    """API客户端"""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

        # 设置通用头信息
        self.session.headers.update({
            'User-Agent': 'Claude-Agent-Skill/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def get(self, endpoint: str, params: Optional[Dict] = None) -> APIResponse:
        """GET请求"""
        return self._request('GET', endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None) -> APIResponse:
        """POST请求"""
        return self._request('POST', endpoint, json=data)

    def _request(self, method: str, endpoint: str, **kwargs) -> APIResponse:
        """执行HTTP请求"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        start_time = time.time()

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )

            elapsed = time.time() - start_time

            # 验证响应
            if response.status_code >= 400:
                self._handle_error_response(response)

            # 解析响应数据
            data = self._parse_response(response)

            return APIResponse(
                status_code=response.status_code,
                data=data,
                headers=dict(response.headers),
                elapsed=elapsed
            )

        except requests.exceptions.Timeout:
            raise APITimeoutError(f"请求超时: {url}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"请求失败: {e}")

    def _parse_response(self, response) -> Any:
        """解析响应数据"""
        content_type = response.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            return response.json()
        elif 'text/' in content_type:
            return response.text
        else:
            return response.content

    def _handle_error_response(self, response):
        """处理错误响应"""
        error_messages = {
            400: "请求参数错误",
            401: "认证失败",
            403: "权限不足",
            404: "资源未找到",
            429: "请求频率过高",
            500: "服务器内部错误"
        }

        message = error_messages.get(response.status_code, "未知错误")

        try:
            error_data = response.json()
            detail = error_data.get('error', error_data.get('message', message))
        except:
            detail = response.text or message

        raise APIError(f"API错误 ({response.status_code}): {detail}")
```

### 认证管理器模板
```python
#!/usr/bin/env python3
"""
认证管理模块 - 多种认证方式支持
"""

import os
from typing import Optional
from requests.auth import AuthBase


class BearerTokenAuth(AuthBase):
    """Bearer Token认证"""

    def __init__(self, token: str):
        self.token = token

    def __call__(self, request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        return request


class AuthManager:
    """认证管理器"""

    def __init__(self):
        self.token_cache = {}

    def setup_api_key_auth(self, api_key: str) -> dict:
        """设置API密钥认证"""
        return {
            'headers': {
                'X-API-Key': api_key,
                'Authorization': f'Bearer {api_key}'
            }
        }

    def setup_bearer_token_auth(self, token: str) -> BearerTokenAuth:
        """设置Bearer Token认证"""
        return BearerTokenAuth(token)

    def get_token_from_env(self, env_var: str = 'API_TOKEN') -> Optional[str]:
        """从环境变量获取令牌"""
        return os.getenv(env_var)

    def validate_token(self, token: str) -> bool:
        """验证令牌格式"""
        if not token or len(token) < 10:
            return False

        # 简单的格式验证
        if ' ' in token or '\n' in token:
            return False

        return True
```

## 🔄 缓存和限流模板

### 缓存管理器模板
```python
#!/usr/bin/env python3
"""
缓存管理模块 - 响应缓存策略
"""

import time
from typing import Any
from functools import wraps


class APICache:
    """API缓存管理器"""

    def __init__(self, ttl: int = 300):  # 默认5分钟
        self.cache = {}
        self.ttl = ttl

    def get(self, key: str) -> Any:
        """获取缓存"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                # 清理过期缓存
                del self.cache[key]
        return None

    def set(self, key: str, data: Any):
        """设置缓存"""
        self.cache[key] = (data, time.time())

    def clear(self):
        """清空缓存"""
        self.cache.clear()


def cached(ttl: int = 300):
    """缓存装饰器"""
    cache = APICache(ttl)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # 检查缓存
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # 执行函数
            result = func(*args, **kwargs)

            # 缓存结果
            cache.set(cache_key, result)

            return result

        return wrapper
    return decorator
```

## 🔧 自定义扩展指南

### 添加新的API端点
1. 在APIClient类中添加专用的方法
2. 更新API文档和示例
3. 添加相应的测试用例

### 支持新的认证方式
1. 在AuthManager类中添加新的认证方法
2. 更新认证配置选项
3. 验证认证流程安全性

### 性能优化建议
1. 实现连接池配置
2. 添加响应压缩支持
3. 实现异步请求处理

---

**使用此模板，快速构建专业的API集成Skill！** 🚀