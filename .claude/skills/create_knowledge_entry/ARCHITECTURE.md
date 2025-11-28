# create_knowledge_entry - 架构设计

## 📋 系统架构概览

### 整体架构
```
┌─────────────────────────────────────────────────────────────┐
│                    create_knowledge_entry                    │
│                    知识条目创建器（主入口）                   │
└─────────────────────────────────────────────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│  智能推荐引擎 │        │  插件执行引擎 │        │  业务价值评估 │
│  (数据驱动)   │        │  (通用化架构) │        │  (价值导向)   │
└──────────────┘        └──────────────┘        └──────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│ 历史模式匹配 │        │  插件注册表   │        │  多维度评分   │
│  置信度计算  │        │  健康检查    │        │  优化建议     │
└──────────────┘        └──────────────┘        └──────────────┘
```

## 🔧 核心组件

### 1. 插件执行引擎 (`plugin_executor.py`)

#### 职责
- 插件生命周期管理
- 插件健康检查
- 容错执行和降级处理
- 并行执行协调

#### 关键类
```python
class KnowledgeCreationPlugin(ABC):
    """通用插件基类"""
    def __init__(self, name: str, config: Dict[str, Any])
    def is_available(self) -> bool
    def execute(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]
    def get_fallback(self) -> Optional[Any]

class PluginRegistry:
    """插件注册表"""
    def __init__(self, config_path: str)
    def load_plugins(self)
    def register_plugin(self, name: str, config: Dict[str, Any])
    def get_available_plugins(self) -> Dict[str, KnowledgeCreationPlugin]
    def get_plugin_health_status(self) -> Dict[str, Any]

class KnowledgeCreationEngine:
    """主执行引擎"""
    def __init__(self, registry: Optional[PluginRegistry] = None)
    def create_knowledge_entry(self, ...) -> Dict[str, Any]
    def _execute_plugins(self, ...) -> Dict[str, Any]
    def _execute_plugin_with_fallback(self, ...) -> Dict[str, Any]
```

#### 执行流程
```
1. 加载插件配置
2. 验证插件可用性
3. 确定执行插件列表
4. 并行执行插件
5. 容错处理
6. 结果聚合
```

### 2. 智能推荐引擎 (`skill_recommender.py`)

#### 职责
- 历史数据模式匹配
- Skill组合推荐
- 置信度计算
- 数据质量评估

#### 关键类
```python
class SkillRecommender:
    """Skill推荐引擎"""
    def __init__(self, patterns_path: str)
    def recommend_skills(self, content: str, knowledge_type: str) -> Dict[str, Any]
    def _analyze_content_features(self, content: str) -> Dict[str, Any]
    def _find_best_pattern(self, features: Dict[str, Any], knowledge_type: str) -> Optional[Dict[str, Any]]
    def _calculate_pattern_score(self, pattern: Dict[str, Any], features: Dict[str, Any]) -> float
    def record_creation_result(self, ...)
```

#### 推荐算法
```
1. 分析内容特征（长度、结构、关键词）
2. 匹配历史模式
3. 计算匹配分数
4. 生成推荐结果
5. 评估数据质量
6. 记录决策依据
```

### 3. 业务价值评估器 (`business_value_assessor.py`)

#### 职责
- 多维度价值评估
- 综合评分计算
- 优化建议生成
- 批准状态判定

#### 关键类
```python
class BusinessValueAssessor:
    """业务价值评估器"""
    def __init__(self, config_path: str)
    def assess_business_value(self, knowledge_entry: Dict[str, Any]) -> Dict[str, Any]
    def _assess_tag_business_value(self, tags: List[Dict[str, Any]], content: str) -> Dict[str, Any]
    def _assess_faq_utility(self, faqs: List[Dict[str, Any]], target_audience: str) -> Dict[str, Any]
    def _assess_summary_completeness(self, summary: str, content: str) -> Dict[str, Any]
    def _calculate_weighted_score(self, scores: Dict[str, float]) -> float
```

#### 评估维度
```
1. 标签业务价值（权重30%）
   - 高价值标签比例
   - 标签分类合理性
   - 标签覆盖度

2. FAQ实用性（权重25%）
   - FAQ数量和质量
   - 问题覆盖度
   - 答案准确性

3. 摘要完整性（权重25%）
   - 信息保留度
   - 长度适中
   - 关键点覆盖

4. 知识类型价值（权重20%）
   - 政策文档: 0.9
   - 流程指南: 0.85
   - 培训材料: 0.8
   - FAQ: 0.7
```

## 🔄 数据流

### 知识创建流程
```
用户请求
    │
    ▼
输入验证
    │
    ▼
防重复检查 ──► 重复？ ──► 返回更新建议
    │            │
    ▼            ▼
内容分析    继续创建
    │
    ▼
智能推荐 ──► 用户选择模式
    │            │
    ▼            ▼
插件验证    自动/辅助/手动
    │
    ▼
插件执行 ──► 容错处理
    │
    ▼
价值评估
    │
    ▼
结果整合
    │
    ▼
返回结果
```

### 插件执行流程
```
插件列表
    │
    ▼
健康检查 ──► 可用？ ──► 跳过
    │            │
    ▼            ▼
并行执行    记录不可用
    │
    ▼
执行结果 ──► 成功？ ──► 降级方案
    │            │
    ▼            ▼
结果聚合    记录失败
    │
    ▼
返回结果
```

## 🗄️ 数据存储

### 历史模式数据
```json
{
  "patterns": [
    {
      "pattern_id": "pattern_001",
      "knowledge_type": "政策文档",
      "content_length_range": [1000, 10000],
      "recommended_skills": {
        "extract_content_tags": true,
        "generate_faq_from_content": true,
        "generate_knowledge_summary": true
      },
      "historical_data": {
        "sample_size": 120,
        "user_satisfaction": 0.85,
        "avg_processing_time": 3.2
      },
      "confidence": 0.85
    }
  ]
}
```

### 插件配置
```yaml
# config/plugins.yaml
plugins:
  tag_extraction:
    class: "TagExtractionPlugin"
    enabled: true
    config:
      mode: "extraction"
      max_tags: 10
      fallback: "simple_keyword_extraction"
      
  faq_generation:
    class: "FAQGenerationPlugin"
    enabled: true
    config:
      max_questions: 50
      coverage_threshold: 0.85
```

### 治理配置
```yaml
# config/governance.yaml
governance:
  data_driven:
    enabled: true
    min_historical_samples: 50
    
  deduplication:
    enabled: true
    similarity_threshold: 0.8
    
  business_value:
    enabled: true
    min_approval_score: 0.7
```

## 🔒 容错机制

### 插件容错
```python
def execute_plugin_with_fallback(plugin, content, context):
    """执行插件（带容错和降级）"""
    try:
        # 尝试执行插件
        result = plugin.execute(content, context)
        return {
            "status": "completed",
            "result": result,
            "fallback_used": False
        }
    except Exception as e:
        # 使用降级方案
        fallback = plugin.get_fallback()
        if fallback:
            return {
                "status": "completed",
                "result": fallback(content, context),
                "fallback_used": True,
                "original_error": str(e)
            }
        else:
            return {
                "status": "failed",
                "error": str(e),
                "fallback_used": False
            }
```

### 防重复机制
```python
def check_knowledge_duplication(content, knowledge_type):
    """检查知识重复"""
    fingerprint = generate_content_fingerprint(content)
    similar_knowledges = query_by_fingerprint(fingerprint)
    
    duplicates = []
    for knowledge in similar_knowledges:
        similarity = calculate_similarity(fingerprint, knowledge["fingerprint"])
        if similarity > 0.8:
            duplicates.append({
                "knowledge_id": knowledge["id"],
                "similarity": similarity,
                "title": knowledge["title"],
                "recommendation": "update" if similarity > 0.9 else "review"
            })
    
    return {
        "is_duplicate": len(duplicates) > 0,
        "duplicates": duplicates,
        "fingerprint": fingerprint
    }
```

## 📊 性能优化

### 并行执行
```python
with ThreadPoolExecutor() as executor:
    futures = {
        executor.submit(
            execute_plugin_with_fallback,
            plugin,
            content,
            context
        ): plugin_name
        for plugin_name, plugin in plugins_to_execute.items()
    }
    
    for future in as_completed(futures):
        plugin_name = futures[future]
        try:
            results[plugin_name] = future.result()
        except Exception as e:
            results[plugin_name] = {
                "status": "failed",
                "error": str(e)
            }
```

### 缓存机制
- 插件健康状态缓存（5分钟）
- 历史模式数据缓存
- 指纹生成结果缓存

## 🔐 安全考虑

### 输入验证
```python
def _validate_input(self, knowledge_content, knowledge_type, creation_options):
    """验证输入参数"""
    errors = []
    
    if not knowledge_content.get("title"):
        errors.append("知识标题不能为空")
    
    if not knowledge_content.get("content"):
        errors.append("知识内容不能为空")
    
    if not knowledge_type:
        errors.append("知识类型不能为空")
    
    valid_types = ["政策文档", "流程指南", "FAQ", "培训材料"]
    if knowledge_type not in valid_types:
        errors.append(f"无效的知识类型: {knowledge_type}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
```

### 错误处理
- 插件执行异常捕获
- 降级方案自动切换
- 详细错误日志记录
- 用户友好的错误提示

## 🚀 扩展性

### 添加新插件
```python
class NewPlugin(KnowledgeCreationPlugin):
    def __init__(self, name, config):
        super().__init__(name, config)
    
    def is_available(self):
        # 检查依赖
        return True
    
    def execute(self, content, context):
        # 实现功能
        return {"result": "new feature"}
    
    def get_fallback(self):
        return simple_fallback

# 注册插件
registry = PluginRegistry()
registry.register(NewPlugin)
```

### 配置扩展
```yaml
# 在config/plugins.yaml中添加
new_plugin:
  class: "NewPlugin"
  enabled: true
  config:
    param1: "value1"
    param2: "value2"
```

---

**架构设计** - 插件化、数据驱动、高可用的知识创建系统 🏗️