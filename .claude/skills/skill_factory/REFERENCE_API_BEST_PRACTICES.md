# API集成最佳实践

## 📋 概述

本文档提供API集成Skill的开发最佳实践，确保API调用安全、可靠且高效。

## 🏗️ API集成架构

### 标准架构模式
```python
class APIIntegration:
    """API集成基类"""

    def __init__(self, base_url, auth_config=None):
        self.base_url = base_url
        self.auth_config = auth_config
        self.session = self._create_session()

    def _create_session(self):
        """创建HTTP会话"""
        session = requests.Session()

        # 设置通用头信息
        session.headers.update({
            'User-Agent': 'Claude-Agent-Skill/1.0',
            'Content-Type': 'application/json'
        })

        # 设置认证
        if self.auth_config:
            self._setup_auth(session, self.auth_config)

        return session

    def make_request(self, endpoint, method='GET', data=None):
        """发起API请求"""
        url = f"{self.base_url}/{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                timeout=30
            )

            # 验证响应
            return self._validate_response(response)

        except requests.exceptions.Timeout:
            raise APITimeoutError(f"API请求超时: {url}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"API请求失败: {e}")
```

## 🔐 认证和授权

### 认证方式支持

#### API密钥认证
```python
def setup_api_key_auth(session, api_key):
    """设置API密钥认证"""
    session.headers.update({
        'Authorization': f'Bearer {api_key}',
        'X-API-Key': api_key
    })
```

#### OAuth 2.0认证
```python
def setup_oauth_auth(session, client_id, client_secret, token_url):
    """设置OAuth 2.0认证"""
    # 获取访问令牌
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = session.post(token_url, data=token_data)
    token_info = response.json()

    # 设置认证头
    session.headers.update({
        'Authorization': f'Bearer {token_info["access_token"]}'
    })
```

#### Basic认证
```python
def setup_basic_auth(session, username, password):
    """设置Basic认证"""
    from requests.auth import HTTPBasicAuth
    session.auth = HTTPBasicAuth(username, password)
```

### 安全最佳实践

#### 凭据管理
```python
# ✅ 安全的凭据管理
import os
from getpass import getpass

class SecureCredentialManager:
    """安全凭据管理器"""

    @staticmethod
    def get_api_key():
        """安全获取API密钥"""
        # 优先从环境变量获取
        api_key = os.getenv('API_KEY')

        if not api_key:
            # 交互式输入
            api_key = getpass("请输入API密钥: ")

        return api_key

    @staticmethod
    def validate_key_format(api_key):
        """验证API密钥格式"""
        if not api_key or len(api_key) < 10:
            raise ValueError("API密钥格式无效")

        # 检查是否包含敏感信息
        sensitive_patterns = ['password', 'secret', 'key']
        if any(pattern in api_key.lower() for pattern in sensitive_patterns):
            raise ValueError("API密钥可能包含敏感信息")
```

## 🔄 请求处理

### 请求构建
```python
def build_api_request(endpoint, params=None, headers=None):
    """构建API请求"""
    # 基础URL
    url = f"{self.base_url}/{endpoint}"

    # 参数处理
    if params:
        # 验证参数类型
        validated_params = self._validate_parameters(params)
        url += "?" + "&".join([f"{k}={v}" for k, v in validated_params.items()])

    # 头信息处理
    request_headers = self.session.headers.copy()
    if headers:
        request_headers.update(headers)

    return url, request_headers


def _validate_parameters(params):
    """验证请求参数"""
    validated = {}

    for key, value in params.items():
        # 检查参数名安全性
        if not re.match(r'^[a-zA-Z0-9_-]+$', key):
            raise ValueError(f"参数名无效: {key}")

        # 检查参数值安全性
        if isinstance(value, str) and len(value) > 1000:
            raise ValueError(f"参数值过长: {key}")

        validated[key] = value

    return validated
```

### 响应处理
```python
def _validate_response(response):
    """验证API响应"""
    # 检查HTTP状态码
    if response.status_code >= 400:
        self._handle_error_response(response)

    # 检查内容类型
    content_type = response.headers.get('Content-Type', '')
    if 'application/json' not in content_type:
        raise APIError(f"意外的内容类型: {content_type}")

    # 解析JSON
    try:
        data = response.json()
    except ValueError as e:
        raise APIError(f"JSON解析失败: {e}")

    return data


def _handle_error_response(response):
    """处理错误响应"""
    error_messages = {
        400: "请求参数错误",
        401: "认证失败",
        403: "权限不足",
        404: "资源未找到",
        429: "请求频率过高",
        500: "服务器内部错误",
        502: "网关错误",
        503: "服务不可用"
    }

    message = error_messages.get(response.status_code, "未知错误")

    # 尝试获取详细错误信息
    try:
        error_data = response.json()
        detail = error_data.get('error', message)
    except:
        detail = message

    raise APIError(f"API错误 ({response.status_code}): {detail}")
```

## ⚡ 性能优化

### 缓存策略
```python
import time
from functools import wraps

class APICache:
    """API缓存管理器"""

    def __init__(self, ttl=300):  # 5分钟TTL
        self.cache = {}
        self.ttl = ttl

    def get(self, key):
        """获取缓存"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]  # 过期清理
        return None

    def set(self, key, data):
        """设置缓存"""
        self.cache[key] = (data, time.time())


def cached_api_call(ttl=300):
    """API调用缓存装饰器"""
    def decorator(func):
        cache = APICache(ttl)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # 检查缓存
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # 调用API
            result = func(*args, **kwargs)

            # 缓存结果
            cache.set(cache_key, result)

            return result

        return wrapper
    return decorator
```

### 限流控制
```python
import time
from threading import Lock

class RateLimiter:
    """API限流器"""

    def __init__(self, calls_per_minute=60):
        self.calls_per_minute = calls_per_minute
        self.calls = []
        self.lock = Lock()

    def acquire(self):
        """获取执行权限"""
        with self.lock:
            now = time.time()

            # 清理过期记录
            self.calls = [call_time for call_time in self.calls
                         if now - call_time < 60]

            # 检查是否超过限制
            if len(self.calls) >= self.calls_per_minute:
                # 计算等待时间
                wait_time = 60 - (now - self.calls[0])
                time.sleep(wait_time)
                # 重新清理
                self.calls = [call_time for call_time in self.calls
                             if now + wait_time - call_time < 60]

            # 记录本次调用
            self.calls.append(now)


def rate_limited(calls_per_minute=60):
    """限流装饰器"""
    limiter = RateLimiter(calls_per_minute)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter.acquire()
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 🧪 测试策略

### 单元测试
```python
import unittest
from unittest.mock import Mock, patch

class TestAPIIntegration(unittest.TestCase):

    @patch('requests.Session')
    def test_successful_api_call(self, mock_session):
        """测试成功的API调用"""
        # 模拟响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_session.return_value.request.return_value = mock_response

        # 测试调用
        api = APIIntegration('https://api.example.com')
        result = api.make_request('test')

        self.assertEqual(result, {'data': 'test'})

    @patch('requests.Session')
    def test_api_error_handling(self, mock_session):
        """测试API错误处理"""
        # 模拟错误响应
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = 'Not Found'
        mock_session.return_value.request.return_value = mock_response

        # 测试错误处理
        api = APIIntegration('https://api.example.com')

        with self.assertRaises(APIError):
            api.make_request('test')
```

### 集成测试
```python
def test_real_api_integration():
    """真实API集成测试"""
    # 使用测试环境API
    api = APIIntegration('https://api-test.example.com')

    try:
        result = api.make_request('health')
        assert 'status' in result
        assert result['status'] == 'ok'
    except APIError as e:
        # 记录测试失败原因
        print(f"集成测试失败: {e}")
        raise
```

## 📊 监控和日志

### 详细日志记录
```python
import logging

class APILogger:
    """API日志记录器"""

    def __init__(self):
        self.logger = logging.getLogger('api_integration')

    def log_request(self, method, url, params=None):
        """记录请求日志"""
        self.logger.info(f"API请求: {method} {url}")
        if params:
            self.logger.debug(f"请求参数: {params}")

    def log_response(self, status_code, response_time):
        """记录响应日志"""
        self.logger.info(f"API响应: {status_code} ({response_time:.2f}s)")

    def log_error(self, error, context=None):
        """记录错误日志"""
        self.logger.error(f"API错误: {error}")
        if context:
            self.logger.debug(f"错误上下文: {context}")
```

### 性能监控
```python
import time
from contextlib import contextmanager

@contextmanager
def api_timing(operation_name):
    """API操作计时上下文管理器"""
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        duration = end_time - start_time

        # 记录性能指标
        if duration > 5:  # 超过5秒警告
            logging.warning(f"{operation_name} 耗时过长: {duration:.2f}s")
        else:
            logging.info(f"{operation_name} 完成: {duration:.2f}s")
```

## 🔧 配置管理

### 环境配置
```python
import os
from dataclasses import dataclass

@dataclass
class APIConfig:
    """API配置类"""
    base_url: str
    api_key: str = None
    timeout: int = 30
    retry_attempts: int = 3
    cache_ttl: int = 300

    @classmethod
    def from_env(cls):
        """从环境变量加载配置"""
        return cls(
            base_url=os.getenv('API_BASE_URL'),
            api_key=os.getenv('API_KEY'),
            timeout=int(os.getenv('API_TIMEOUT', '30')),
            retry_attempts=int(os.getenv('API_RETRY_ATTEMPTS', '3')),
            cache_ttl=int(os.getenv('API_CACHE_TTL', '300'))
        )
```

## 🎯 最佳实践总结

### 安全第一
1. **验证所有输入**: 参数、URL、响应数据
2. **安全存储凭据**: 使用环境变量或安全存储
3. **限制权限**: 使用最小权限原则
4. **监控异常**: 记录所有错误和异常

### 性能优化
1. **实现缓存**: 减少重复API调用
2. **控制频率**: 避免API限流
3. **异步处理**: 长时间操作使用异步
4. **连接复用**: 使用会话保持连接

### 可靠性保障
1. **错误处理**: 优雅处理各种错误场景
2. **重试机制**: 实现智能重试逻辑
3. **超时设置**: 避免长时间等待
4. **降级策略**: 主服务不可用时使用备用方案

---

**遵循这些最佳实践，构建安全、高效、可靠的API集成Skill！** 🚀