#!/usr/bin/env python3
"""
插件执行引擎 - 实现通用化架构和容错机制
原则3：通用化而非定制化
"""

import json
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, Optional, List
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeCreationPlugin(ABC):
    """通用知识创建插件基类"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.enabled = config.get("enabled", True)
        self.fallback_enabled = config.get("fallback_enabled", True)
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查插件是否可用"""
        pass
    
    @abstractmethod
    def execute(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行插件功能"""
        pass
    
    def get_fallback(self) -> Optional[Any]:
        """获取降级方案"""
        return None
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            available = self.is_available()
            return {
                "status": "healthy" if available else "unavailable",
                "name": self.name,
                "enabled": self.enabled,
                "last_check": time.time()
            }
        except Exception as e:
            return {
                "status": "error",
                "name": self.name,
                "error": str(e),
                "last_check": time.time()
            }


class PluginRegistry:
    """插件注册表 - 动态发现和管理插件"""
    
    def __init__(self, config_path: str = "config/plugins.yaml"):
        self.config_path = config_path
        self.plugins: Dict[str, KnowledgeCreationPlugin] = {}
        self.load_plugins()
    
    def load_plugins(self):
        """加载插件配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            for plugin_name, plugin_config in config.get("plugins", {}).items():
                if plugin_config.get("enabled", True):
                    self.register_plugin(plugin_name, plugin_config)
        except FileNotFoundError:
            logger.warning(f"插件配置文件未找到: {self.config_path}")
        except Exception as e:
            logger.error(f"加载插件配置失败: {e}")
    
    def register_plugin(self, name: str, config: Dict[str, Any]):
        """注册插件"""
        try:
            plugin_class = self._load_plugin_class(config["class"])
            plugin = plugin_class(name, config.get("config", {}))
            self.plugins[name] = plugin
            logger.info(f"插件注册成功: {name}")
        except Exception as e:
            logger.error(f"插件注册失败 {name}: {e}")
    
    def _load_plugin_class(self, class_path: str):
        """动态加载插件类"""
        # 简化实现，实际项目中可以使用importlib
        if "TagExtraction" in class_path:
            from .tag_extraction_plugin import TagExtractionPlugin
            return TagExtractionPlugin
        elif "FAQGeneration" in class_path:
            from .faq_generation_plugin import FAQGenerationPlugin
            return FAQGenerationPlugin
        elif "SummaryGeneration" in class_path:
            from .summary_generation_plugin import SummaryGenerationPlugin
            return SummaryGenerationPlugin
        else:
            raise ValueError(f"未知的插件类: {class_path}")
    
    def get_available_plugins(self) -> Dict[str, KnowledgeCreationPlugin]:
        """获取可用插件"""
        available = {}
        for name, plugin in self.plugins.items():
            try:
                if plugin.is_available():
                    available[name] = plugin
            except Exception as e:
                logger.warning(f"插件健康检查失败 {name}: {e}")
        return available
    
    def get_plugin_health_status(self) -> Dict[str, Any]:
        """获取所有插件的健康状态"""
        status = {
            "total_plugins": len(self.plugins),
            "healthy_plugins": 0,
            "unavailable_plugins": 0,
            "error_plugins": 0,
            "details": {}
        }
        
        for name, plugin in self.plugins.items():
            health = plugin.health_check()
            status["details"][name] = health
            
            if health["status"] == "healthy":
                status["healthy_plugins"] += 1
            elif health["status"] == "unavailable":
                status["unavailable_plugins"] += 1
            else:
                status["error_plugins"] += 1
        
        return status


class KnowledgeCreationEngine:
    """知识创建执行引擎"""
    
    def __init__(self, registry: Optional[PluginRegistry] = None):
        self.registry = registry or PluginRegistry()
        self.execution_history: List[Dict[str, Any]] = []
    
    def create_knowledge_entry(self, 
                             knowledge_content: Dict[str, str],
                             knowledge_type: str,
                             creation_options: Dict[str, Any],
                             selection_mode: str = "assisted") -> Dict[str, Any]:
        """创建知识条目主方法"""
        
        start_time = time.time()
        
        # 1. 验证输入
        validation_result = self._validate_input(
            knowledge_content, knowledge_type, creation_options
        )
        if not validation_result["valid"]:
            return {
                "status": "failed",
                "error": validation_result["errors"],
                "processing_time": time.time() - start_time
            }
        
        # 2. 防重复检查
        from .duplicate_checker import check_knowledge_duplication
        duplicate_check = check_knowledge_duplication(
            knowledge_content["content"], 
            knowledge_type
        )
        
        if duplicate_check["is_duplicate"]:
            return {
                "status": "duplicate_detected",
                "duplicates": duplicate_check["duplicates"],
                "recommendation": "update_existing",
                "processing_time": time.time() - start_time
            }
        
        # 3. 智能推荐skill（数据驱动）
        if selection_mode in ["auto", "assisted"]:
            from .skill_recommender import data_driven_skill_recommendation
            recommendations = data_driven_skill_recommendation(
                knowledge_content["content"], knowledge_type
            )
        else:
            recommendations = {"recommendations": {}, "confidence": 1.0}
        
        # 4. 确定需要执行的插件
        plugins_to_execute = self._determine_plugins(
            creation_options, recommendations, selection_mode
        )
        
        # 5. 执行插件（容错模式）
        plugin_results = self._execute_plugins(
            plugins_to_execute, 
            knowledge_content["content"],
            {"knowledge_type": knowledge_type}
        )
        
        # 6. 业务价值评估
        from .business_value_assessor import assess_business_value
        knowledge_entry = {
            "title": knowledge_content["title"],
            "content": knowledge_content["content"],
            "knowledge_type": knowledge_type,
            "tags": plugin_results.get("tag_extraction", {}).get("result", []),
            "faqs": plugin_results.get("faq_generation", {}).get("result", []),
            "summary": plugin_results.get("summary_generation", {}).get("result", "")
        }
        
        value_assessment = assess_business_value(knowledge_entry)
        
        # 7. 生成唯一标识
        knowledge_id = self._generate_knowledge_id()
        
        # 8. 整合结果
        result = {
            "knowledge_id": knowledge_id,
            "structured_content": {
                "title": knowledge_content["title"],
                "content": knowledge_content["content"],
                "knowledge_type": knowledge_type,
                "created_at": time.time(),
                "version": "1.0"
            },
            "creation_results": plugin_results,
            "value_assessment": value_assessment,
            "creation_status": {
                "overall_status": "success",
                "total_processing_time": time.time() - start_time,
                "selection_mode": selection_mode,
                "recommendations": recommendations,
                "plugins_executed": list(plugins_to_execute.keys())
            }
        }
        
        # 9. 记录执行历史
        self.execution_history.append({
            "knowledge_id": knowledge_id,
            "timestamp": time.time(),
            "result": result
        })
        
        return result
    
    def _validate_input(self, 
                       knowledge_content: Dict[str, str],
                       knowledge_type: str,
                       creation_options: Dict[str, Any]) -> Dict[str, Any]:
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
    
    def _determine_plugins(self,
                          creation_options: Dict[str, Any],
                          recommendations: Dict[str, Any],
                          selection_mode: str) -> Dict[str, KnowledgeCreationPlugin]:
        """确定需要执行的插件"""
        available_plugins = self.registry.get_available_plugins()
        plugins_to_execute = {}
        
        # 基于选项和推荐确定插件
        for plugin_name, plugin in available_plugins.items():
            # 检查是否在creation_options中启用
            if creation_options.get(plugin_name, False):
                plugins_to_execute[plugin_name] = plugin
            
            # 检查系统推荐
            elif (selection_mode in ["auto", "assisted"] and 
                  plugin_name in recommendations.get("recommendations", {})):
                plugins_to_execute[plugin_name] = plugin
        
        return plugins_to_execute
    
    def _execute_plugins(self,
                        plugins: Dict[str, KnowledgeCreationPlugin],
                        content: str,
                        context: Dict[str, Any]) -> Dict[str, Any]:
        """执行插件（容错模式）"""
        results = {}
        
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(
                    self._execute_plugin_with_fallback,
                    plugin,
                    content,
                    context
                ): plugin_name
                for plugin_name, plugin in plugins.items()
            }
            
            for future in as_completed(futures):
                plugin_name = futures[future]
                try:
                    results[plugin_name] = future.result()
                except Exception as e:
                    logger.error(f"插件执行失败 {plugin_name}: {e}")
                    results[plugin_name] = {
                        "status": "failed",
                        "error": str(e),
                        "processing_time": 0
                    }
        
        return results
    
    def _execute_plugin_with_fallback(self,
                                    plugin: KnowledgeCreationPlugin,
                                    content: str,
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """执行插件（带容错和降级）"""
        start_time = time.time()
        
        try:
            # 尝试执行插件
            result = plugin.execute(content, context)
            return {
                "status": "completed",
                "result": result,
                "fallback_used": False,
                "processing_time": time.time() - start_time
            }
        except Exception as e:
            logger.warning(f"插件执行失败，尝试降级方案: {plugin.name}")
            
            # 使用降级方案
            fallback = plugin.get_fallback()
            if fallback and plugin.fallback_enabled:
                try:
                    fallback_result = fallback(content, context)
                    return {
                        "status": "completed",
                        "result": fallback_result,
                        "fallback_used": True,
                        "original_error": str(e),
                        "processing_time": time.time() - start_time
                    }
                except Exception as fallback_error:
                    logger.error(f"降级方案也失败: {fallback_error}")
            
            return {
                "status": "failed",
                "error": str(e),
                "fallback_used": False,
                "processing_time": time.time() - start_time
            }
    
    def _generate_knowledge_id(self) -> str:
        """生成知识条目唯一ID"""
        import uuid
        return f"knl_{uuid.uuid4().hex[:8]}"
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """获取执行历史"""
        return self.execution_history


def main():
    """主函数 - 用于测试"""
    # 创建引擎
    engine = KnowledgeCreationEngine()
    
    # 检查插件健康状态
    health_status = engine.registry.get_plugin_health_status()
    print("插件健康状态:")
    print(json.dumps(health_status, indent=2, ensure_ascii=False))
    
    # 示例：创建知识条目
    sample_content = {
        "title": "测试知识条目",
        "content": "这是一个测试知识条目的内容，用于验证插件执行引擎的功能。"
    }
    
    result = engine.create_knowledge_entry(
        knowledge_content=sample_content,
        knowledge_type="流程指南",
        creation_options={
            "extract_tags": True,
            "generate_faq": True,
            "generate_summary": True
        },
        selection_mode="auto"
    )
    
    print("\n创建结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()