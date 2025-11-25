# 问题排查指南

## 📋 概述

本文档提供Skill开发和使用过程中常见问题的排查方法和解决方案。

## 🔍 问题分类

### 1. 结构验证问题

#### 问题：SKILL.md验证失败
**症状**:
- Skill无法正确加载
- 控制台显示YAML解析错误

**排查步骤**:
1. 检查YAML头部格式
```yaml
---
name: skill_name
description: 功能描述
---
```

2. 验证必需字段是否存在
```bash
# 使用验证脚本检查
python scripts/skill_validator.py .claude/skills/your_skill
```

3. 检查字段长度限制
- name: ≤64字符
- description: ≤1024字符

**解决方案**:
- 修复YAML语法错误
- 确保字段符合长度要求
- 使用验证脚本自动检查

#### 问题：文件结构不正确
**症状**:
- 缺失必需文件
- 目录命名不规范

**排查步骤**:
1. 检查必需文件是否存在
```bash
ls -la .claude/skills/your_skill/
# 应该包含: SKILL.md, README.md
```

2. 验证目录命名
```python
# 正确的命名格式
import re
pattern = r'^[a-z][a-z0-9_]*(_[a-z0-9]+)*$'
assert re.match(pattern, 'skill_name')  # 应该通过
```

**解决方案**:
- 创建缺失的文件
- 重命名不符合规范的目录
- 使用结构构建器重新创建

### 2. Python脚本问题

#### 问题：脚本执行失败
**症状**:
- Python语法错误
- 模块导入失败
- 运行时异常

**排查步骤**:
1. 检查Python语法
```bash
python -m py_compile script.py
```

2. 验证依赖库
```bash
# 检查依赖可用性
python scripts/dependency_checker.py .claude/skills/your_skill
```

3. 调试脚本
```python
# 添加详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

try:
    # 你的代码
    pass
except Exception as e:
    logging.error(f"错误详情: {e}")
    raise
```

**解决方案**:
- 修复语法错误
- 安装缺失的依赖库
- 添加异常处理

#### 问题：权限错误
**症状**:
- 文件操作被拒绝
- 无法创建目录

**排查步骤**:
1. 检查文件权限
```bash
ls -la script.py
# 应该有执行权限: -rwxr-xr-x
```

2. 验证路径安全性
```python
from pathlib import Path

path = Path("your_path")
# 检查是否在允许范围内
assert path.is_relative_to('.claude') or path.is_relative_to('/tmp')
```

**解决方案**:
- 设置正确的文件权限
```bash
chmod +x script.py
```
- 使用安全的路径操作

### 3. API集成问题

#### 问题：API调用失败
**症状**:
- 网络连接错误
- 认证失败
- 响应超时

**排查步骤**:
1. 检查网络连接
```bash
# 测试API端点可达性
curl -I https://api.example.com/health
```

2. 验证认证信息
```python
# 检查API密钥格式
api_key = os.getenv('API_KEY')
assert api_key and len(api_key) > 10
```

3. 测试API调用
```python
import requests

try:
    response = requests.get('https://api.example.com/health', timeout=10)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
```

**解决方案**:
- 检查网络配置
- 更新认证信息
- 调整超时设置

#### 问题：速率限制
**症状**:
- API返回429状态码
- 请求频率过高

**排查步骤**:
1. 检查当前请求频率
```python
# 实现限流监控
from datetime import datetime, timedelta

class RateLimitMonitor:
    def __init__(self):
        self.requests = []

    def record_request(self):
        self.requests.append(datetime.now())
        # 清理1分钟前的记录
        self.requests = [r for r in self.requests
                        if datetime.now() - r < timedelta(minutes=1)]

    def get_current_rate(self):
        return len(self.requests)
```

**解决方案**:
- 实现请求限流
- 使用指数退避重试
- 缓存频繁请求的结果

### 4. 性能问题

#### 问题：响应缓慢
**症状**:
- Skill执行时间过长
- 资源占用过高

**排查步骤**:
1. 性能分析
```python
import time
import cProfile

def profile_function(func):
    """性能分析装饰器"""
    def wrapper(*args, **kwargs):
        start_time = time.time()

        # 使用cProfile进行详细分析
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.print_stats()

        end_time = time.time()
        print(f"执行时间: {end_time - start_time:.2f}秒")

        return result
    return wrapper
```

2. 资源监控
```python
import psutil
import os

def monitor_resources():
    """监控资源使用"""
    process = psutil.Process(os.getpid())

    print(f"内存使用: {process.memory_info().rss / 1024 / 1024:.2f} MB")
    print(f"CPU使用: {process.cpu_percent()}%")
```

**解决方案**:
- 优化算法复杂度
- 实现缓存机制
- 使用异步处理

### 5. 配置问题

#### 问题：环境配置错误
**症状**:
- 环境变量未设置
- 配置文件格式错误

**排查步骤**:
1. 检查环境变量
```python
import os

required_env_vars = ['API_KEY', 'DATABASE_URL']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    print(f"缺失环境变量: {missing_vars}")
```

2. 验证配置文件
```python
import yaml

try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    print("配置文件格式正确")
except yaml.YAMLError as e:
    print(f"配置文件错误: {e}")
```

**解决方案**:
- 设置正确的环境变量
- 修复配置文件格式
- 提供配置模板

## 🛠️ 调试工具

### 内置调试脚本

#### 结构验证工具
```bash
# 验证Skill结构
python scripts/skill_validator.py path/to/skill

# 输出示例:
✅ Skill验证通过！
❌ 发现错误: 缺失SKILL.md文件
```

#### 依赖检查工具
```bash
# 检查依赖库
python scripts/dependency_checker.py path/to/skill

# 输出示例:
✅ 所有依赖都可用！
❌ 缺失依赖: requests, pandas
```

#### 性能分析工具
```python
# 性能分析装饰器
from utils.performance import profile_function

@profile_function
def slow_function():
    # 你的代码
    pass
```

### 日志配置

#### 详细日志设置
```python
import logging

# 配置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

#### 结构化日志
```python
import json
import logging

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def log_event(self, event_type, **kwargs):
        """记录结构化事件"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            **kwargs
        }
        self.logger.info(json.dumps(log_data))
```

## 🚨 紧急处理

### 快速恢复步骤

1. **立即停止问题Skill**
   ```bash
   # 临时禁用Skill
   mv .claude/skills/problem_skill .claude/skills/problem_skill.disabled
   ```

2. **检查系统状态**
   ```bash
   # 检查资源使用
   top
   # 检查磁盘空间
   df -h
   ```

3. **回滚更改**
   ```bash
   # 如果使用版本控制
   git checkout HEAD~1 .claude/skills/problem_skill
   ```

### 问题上报模板

当需要外部帮助时，请提供以下信息：

```markdown
## 问题描述
[详细描述问题现象]

## 环境信息
- 操作系统: [例如: macOS 14.0]
- Python版本: [例如: 3.9.0]
- Skill名称: [skill名称]

## 错误信息
[完整的错误堆栈]

## 重现步骤
1. [步骤1]
2. [步骤2]
3. [步骤3]

## 已尝试的解决方案
- [方案1]
- [方案2]
```

## 📈 预防措施

### 开发阶段预防

1. **代码审查**
   - 使用验证脚本检查代码
   - 进行同行代码审查
   - 测试边界情况

2. **自动化测试**
   ```python
   # 单元测试示例
   def test_edge_cases():
       # 测试边界值
       test_cases = [
           ("", "空输入"),
           ("a" * 1000, "长输入"),
           ("特殊字符!@#", "特殊字符")
       ]
   ```

3. **性能基准测试**
   ```python
   # 性能测试
   def benchmark_performance():
       start_time = time.time()
       # 执行操作
       duration = time.time() - start_time
       assert duration < 5.0, "性能不达标"
   ```

### 运维阶段监控

1. **健康检查**
   ```python
   # 定期健康检查
   def health_check():
       checks = [
           check_disk_space,
           check_memory_usage,
           check_api_availability
       ]

       for check in checks:
           if not check():
               alert_admin(f"健康检查失败: {check.__name__}")
   ```

2. **监控告警**
   - 设置资源使用阈值
   - 监控错误率
   - 跟踪性能指标

---

**记住：预防胜于治疗！建立完善的测试和监控体系是避免问题的关键。** 🔧