# Skill Factory 使用示例

## 📋 概述

本文档提供 `skill_factory` 的完整使用示例，展示如何通过结构化对话创建不同类型的Skill。

## 🚀 快速开始示例

### 示例1：创建数据处理Skill

**用户请求**:
```
请帮我创建一个处理Excel数据的Skill
```

**Skill Factory 交互流程**:

**步骤1: 基本信息收集**
```
Skill Factory: 🎯 开始创建数据处理Skill

请提供以下信息：
1. Skill名称（建议小写下划线格式）：excel_data_processor
2. 功能描述：处理Excel文件的数据清洗和格式转换
3. 目标用户技术水平：intermediate
```

**步骤2: 功能细节深化**
```
Skill Factory: 📊 请描述具体功能需求：

1. 处理哪些Excel格式？（xlsx/csv/tsv）
   → xlsx, csv

2. 需要哪些数据处理功能？
   → 数据清洗、格式转换、简单计算

3. 输出格式要求？
   → 处理后的Excel文件、数据报告
```

**步骤3: 技术需求确认**
```
Skill Factory: 🔧 技术配置：

1. 是否需要Python脚本？
   → 是

2. 是否需要模板文件？
   → 是，提供标准数据处理模板

3. 复杂度级别？
   → medium（中等复杂度）
```

**生成结果**:
```
✅ Skill创建完成！

📁 生成的文件结构：
.claude/skills/excel_data_processor/
├── SKILL.md
├── README.md
├── scripts/
│   ├── data_cleaner.py
│   └── report_generator.py
├── templates/
│   └── data_processor/SKILL.md
└── examples/
    └── basic_usage/README.md
```

### 示例2：创建API集成Skill

**用户请求**:
```
需要集成天气预报API
```

**Skill Factory 交互流程**:

**步骤1: 基本信息收集**
```
Skill Factory: 🌤️ 开始创建天气预报API集成Skill

请提供：
1. Skill名称：weather_api_integrator
2. 功能描述：获取和展示天气预报信息
3. 目标用户：beginner
```

**步骤2: API细节配置**
```
Skill Factory: 🔌 API配置：

1. API端点URL？
   → https://api.weather.com/forecast

2. 认证方式？
   → API密钥认证

3. 数据格式？
   → JSON

4. 需要哪些天气信息？
   → 温度、湿度、风速、天气预报
```

**步骤3: 高级功能**
```
Skill Factory: ⚡ 高级功能：

1. 是否需要缓存？
   → 是，缓存1小时

2. 是否需要错误重试？
   → 是，重试3次

3. 是否需要地理位置支持？
   → 是，支持城市名称和坐标
```

**生成结果**:
```
✅ Weather API集成Skill创建完成！

📁 生成的文件结构：
.claude/skills/weather_api_integrator/
├── SKILL.md
├── README.md
├── scripts/
│   ├── api_client.py
│   ├── cache_manager.py
│   └── location_parser.py
├── templates/
│   └── api_integrator/SKILL.md
└── examples/
    ├── basic_usage/
    └── advanced_usage/
```

## 🎯 不同复杂度示例

### 简单Skill示例：文件重命名工具

**需求**: 批量重命名文件

**生成内容**:
```yaml
# SKILL.md 头部
---
name: file_renamer
description: 批量重命名文件的简单工具
---

# 功能特性
- 支持通配符匹配
- 预览重命名结果
- 安全撤销功能
```

**脚本示例**:
```python
# scripts/file_renamer.py
import os
from pathlib import Path

def batch_rename(pattern, new_name):
    """批量重命名文件"""
    files = list(Path('.').glob(pattern))

    # 预览更改
    for file in files:
        new_file = file.parent / new_name.format(
            index=files.index(file) + 1,
            original=file.stem
        )
        print(f"{file.name} -> {new_file.name}")

    # 确认后执行
    if input("确认重命名？(y/N): ").lower() == 'y':
        for file in files:
            # 执行重命名
            pass
```

### 中等复杂度示例：数据报告生成器

**需求**: 从多个数据源生成综合报告

**生成内容**:
```yaml
# SKILL.md 头部
---
name: report_generator
description: 从多个数据源生成格式化报告
tools: [Read, Write, Edit, Bash]
---
```

**脚本结构**:
```
scripts/
├── data_collector.py    # 数据收集
├── report_builder.py    # 报告构建
├── formatter.py         # 格式处理
└── validator.py         # 数据验证
```

### 复杂Skill示例：内容管理系统

**需求**: 企业级内容创作和管理

**生成内容**:
```yaml
# SKILL.md 头部
---
name: content_management_system
description: 企业级内容创作、优化和发布系统
tools: [Read, Write, Edit, Bash, Task, WebFetch]
---
```

**完整结构**:
```
.claude/skills/content_management_system/
├── SKILL.md
├── README.md
├── scripts/
│   ├── content_creator.py
│   ├── seo_optimizer.py
│   ├── quality_checker.py
│   ├── publishing_tool.py
│   └── analytics.py
├── templates/
│   ├── blog_post/
│   ├── product_page/
│   └── newsletter/
├── examples/
│   ├── blog_workflow/
│   ├── seo_optimization/
│   └── analytics_dashboard/
└── utils/
    ├── file_helpers.py
    ├── validation_rules.py
    └── logging_utils.py
```

## 🔧 模板使用示例

### 数据处理模板应用

**模板选择**: `data_processor`

**生成内容示例**:
```python
# 自动生成的SKILL.md模板内容
---
name: customer_data_analyzer
description: 客户数据分析工具
---

## 功能特性
- 数据导入和清洗
- 统计分析
- 可视化报告
- 数据导出

## 输入格式
- CSV文件
- Excel文件
- 数据库连接
```

### API集成模板应用

**模板选择**: `api_integrator`

**生成内容示例**:
```python
# 自动生成的API客户端代码
class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def make_request(self, endpoint, method='GET', data=None):
        # 标准API请求逻辑
        pass
```

## 🎪 实际应用场景

### 场景1：营销团队内容创作

**需求背景**:
- 营销团队需要快速创建社交媒体内容
- 需要SEO优化和格式标准化

**生成的Skill**: `social_media_manager`

**功能特性**:
- 内容模板管理
- SEO关键词优化
- 多平台格式适配
- 发布计划管理

### 场景2：数据分析师工作流

**需求背景**:
- 数据分析师需要处理多种数据格式
- 需要自动化报告生成

**生成的Skill**: `data_analysis_workflow`

**功能特性**:
- 数据清洗和转换
- 统计分析计算
- 可视化图表生成
- 报告自动导出

### 场景3：开发者工具集成

**需求背景**:
- 开发团队需要集成多个开发工具
- 需要自动化代码质量检查

**生成的Skill**: `developer_toolkit`

**功能特性**:
- 代码质量检查
- 依赖管理
- 自动化测试
- 部署流水线

## 📊 性能优化示例

### 缓存策略实现

**问题**: API调用频繁，需要降低延迟

**解决方案**:
```python
# 自动生成的缓存管理器
from functools import wraps
import time

class CacheManager:
    def __init__(self, ttl=3600):  # 1小时TTL
        self.cache = {}
        self.ttl = ttl

    def get(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
        return None

    def set(self, key, data):
        self.cache[key] = (data, time.time())

def cached(ttl=3600):
    """缓存装饰器"""
    cache = CacheManager(ttl)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            cached_result = cache.get(cache_key)

            if cached_result is not None:
                return cached_result

            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            return result

        return wrapper
    return decorator
```

### 错误处理优化

**问题**: 网络不稳定导致API调用失败

**解决方案**:
```python
# 自动生成的错误处理和重试逻辑
import time
from functools import wraps

def retry(max_attempts=3, delay=1, backoff=2):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay

            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e

                    print(f"尝试 {attempts}/{max_attempts} 失败，{current_delay}秒后重试...")
                    time.sleep(current_delay)
                    current_delay *= backoff

            return None

        return wrapper
    return decorator
```

## 🔄 迭代优化示例

### 基于用户反馈优化

**原始Skill**: `basic_file_organizer`

**用户反馈**:
- 需要更多文件类型支持
- 希望有预览功能
- 需要批量操作支持

**优化后的Skill**: `advanced_file_manager`

**新增功能**:
- 支持100+文件格式
- 实时预览界面
- 批量操作队列
- 撤销/重做功能

### 性能优化案例

**问题Skill**: `slow_data_processor`
- 处理大型文件时内存占用高
- 执行时间过长

**优化措施**:
1. 实现流式处理
2. 添加内存监控
3. 优化算法复杂度

**优化后**: `efficient_data_processor`
- 内存使用减少80%
- 处理速度提升3倍

---

**通过这些示例，您可以看到 `skill_factory` 如何根据不同的需求和场景，生成专业化、标准化的Skill解决方案。** 🚀