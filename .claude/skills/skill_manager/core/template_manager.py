#!/usr/bin/env python3
"""
模板管理器
基于Skill类型和复杂度选择、生成模板
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from ..models import SkillSpec, TemplateConfig


class TemplateManager:
    """模板管理器类"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / 'templates'
        
        self.templates_dir = Path(templates_dir)
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict[str, TemplateConfig]]:
        """加载预定义模板"""
        return {
            'data_processor': {
                'simple': self._data_processor_simple(),
                'medium': self._data_processor_medium(),
                'complex': self._data_processor_complex()
            },
            'api_integrator': {
                'simple': self._api_integrator_simple(),
                'medium': self._api_integrator_medium(),
                'complex': self._api_integrator_complex()
            },
            'file_operator': {
                'simple': self._file_operator_simple(),
                'medium': self._file_operator_medium(),
                'complex': self._file_operator_complex()
            },
            'content_creator': {
                'simple': self._content_creator_simple(),
                'medium': self._content_creator_medium(),
                'complex': self._content_creator_complex()
            },
            'document_generator': {
                'simple': self._document_generator_simple(),
                'medium': self._document_generator_medium(),
                'complex': self._document_generator_complex()
            },
            'workflow': {
                'simple': self._workflow_simple(),
                'medium': self._workflow_medium(),
                'complex': self._workflow_complex()
            }
        }
    
    def select_template(self, spec: SkillSpec) -> TemplateConfig:
        """基于规格选择最合适的模板"""
        # 获取基础模板
        type_templates = self.templates.get(spec.skill_type, {})
        base_template = type_templates.get(spec.complexity, self._default_template())
        
        # 根据目标用户调整
        template = self._adjust_for_audience(base_template, spec.target_audience)
        
        # 添加自定义需求
        if spec.custom_requirements:
            template = self._add_custom_requirements(template, spec.custom_requirements)
        
        return template
    
    def _adjust_for_audience(self, template: TemplateConfig, audience: str) -> TemplateConfig:
        """根据目标用户调整模板"""
        adjusted = TemplateConfig(**template.__dict__)
        
        if audience == 'beginner':
            adjusted.documentation_level = 'detailed'
        elif audience == 'expert':
            adjusted.documentation_level = 'technical'
        
        return adjusted
    
    def _add_custom_requirements(self, template: TemplateConfig, custom_req: str) -> TemplateConfig:
        """添加自定义需求到模板"""
        adjusted = TemplateConfig(**template.__dict__)
        
        if 'api' in custom_req.lower():
            adjusted.authentication = 'oauth'
        if 'batch' in custom_req.lower():
            adjusted.batch_operations = True
        
        return adjusted
    
    def _data_processor_simple(self) -> TemplateConfig:
        """简单数据处理模板"""
        return TemplateConfig(
            skill_type='data_processor',
            description='基础数据处理功能',
            required_tools=['Read', 'Write', 'Edit'],
            scripts=['data_cleaner.py'],
            examples=['basic_data_processing'],
            documentation_level='basic'
        )
    
    def _data_processor_medium(self) -> TemplateConfig:
        """中等复杂度数据处理模板"""
        return TemplateConfig(
            skill_type='data_processor',
            description='高级数据处理和分析',
            required_tools=['Read', 'Write', 'Edit', 'Bash'],
            scripts=['data_processor.py', 'analysis_tool.py'],
            examples=['data_analysis', 'report_generation'],
            documentation_level='intermediate',
            include_validation=True
        )
    
    def _data_processor_complex(self) -> TemplateConfig:
        """复杂数据处理模板"""
        return TemplateConfig(
            skill_type='data_processor',
            description='企业级数据处理流水线',
            required_tools=['Read', 'Write', 'Edit', 'Bash', 'Task'],
            scripts=['pipeline_manager.py', 'quality_checker.py', 'report_generator.py'],
            examples=['data_pipeline', 'quality_assurance'],
            documentation_level='advanced',
            include_validation=True,
            error_handling='comprehensive'
        )
    
    def _api_integrator_simple(self) -> TemplateConfig:
        """简单API集成模板"""
        return TemplateConfig(
            skill_type='api_integrator',
            description='基础API调用功能',
            required_tools=['WebFetch', 'Read'],
            scripts=['api_client.py'],
            examples=['basic_api_call'],
            documentation_level='basic',
            authentication='simple'
        )
    
    def _api_integrator_medium(self) -> TemplateConfig:
        """中等复杂度API集成模板"""
        return TemplateConfig(
            skill_type='api_integrator',
            description='高级API集成和管理',
            required_tools=['WebFetch', 'Read', 'Write', 'Bash'],
            scripts=['api_manager.py', 'response_parser.py'],
            examples=['api_integration', 'data_sync'],
            documentation_level='intermediate',
            authentication='oauth',
            rate_limiting=True
        )
    
    def _api_integrator_complex(self) -> TemplateConfig:
        """复杂API集成模板"""
        return TemplateConfig(
            skill_type='api_integrator',
            description='企业级API生态系统',
            required_tools=['WebFetch', 'Read', 'Write', 'Bash', 'Task'],
            scripts=['ecosystem_manager.py', 'monitoring_tool.py', 'cache_manager.py'],
            examples=['api_ecosystem', 'performance_monitoring'],
            documentation_level='advanced',
            authentication='multi-factor',
            rate_limiting=True,
            caching=True,
            monitoring=True
        )
    
    def _file_operator_simple(self) -> TemplateConfig:
        """简单文件操作模板"""
        return TemplateConfig(
            skill_type='file_operator',
            description='基础文件管理功能',
            required_tools=['Read', 'Write', 'Glob'],
            scripts=['file_manager.py'],
            examples=['file_operations'],
            documentation_level='basic'
        )
    
    def _file_operator_medium(self) -> TemplateConfig:
        """中等复杂度文件操作模板"""
        return TemplateConfig(
            skill_type='file_operator',
            description='高级文件处理和转换',
            required_tools=['Read', 'Write', 'Glob', 'Bash'],
            scripts=['batch_processor.py', 'converter.py'],
            examples=['batch_processing', 'format_conversion'],
            documentation_level='intermediate',
            batch_operations=True
        )
    
    def _file_operator_complex(self) -> TemplateConfig:
        """复杂文件操作模板"""
        return TemplateConfig(
            skill_type='file_operator',
            description='企业级文件管理系统',
            required_tools=['Read', 'Write', 'Glob', 'Bash', 'Task'],
            scripts=['system_manager.py', 'backup_tool.py', 'sync_engine.py'],
            examples=['file_system', 'backup_management'],
            documentation_level='advanced',
            batch_operations=True,
            backup=True,
            synchronization=True
        )
    
    def _content_creator_simple(self) -> TemplateConfig:
        """简单内容创作模板"""
        return TemplateConfig(
            skill_type='content_creator',
            description='基础内容生成功能',
            required_tools=['Read', 'Write'],
            scripts=['content_generator.py'],
            examples=['content_creation'],
            documentation_level='basic'
        )
    
    def _content_creator_medium(self) -> TemplateConfig:
        """中等复杂度内容创作模板"""
        return TemplateConfig(
            skill_type='content_creator',
            description='高级内容创作和优化',
            required_tools=['Read', 'Write', 'Edit'],
            scripts=['content_optimizer.py', 'style_checker.py'],
            examples=['content_optimization', 'style_analysis'],
            documentation_level='intermediate',
            quality_check=True
        )
    
    def _content_creator_complex(self) -> TemplateConfig:
        """复杂内容创作模板"""
        return TemplateConfig(
            skill_type='content_creator',
            description='企业级内容管理系统',
            required_tools=['Read', 'Write', 'Edit', 'Bash'],
            scripts=['content_manager.py', 'seo_analyzer.py', 'publishing_tool.py'],
            examples=['content_workflow', 'seo_optimization'],
            documentation_level='advanced',
            quality_check=True,
            seo_analysis=True,
            publishing=True
        )
    
    def _document_generator_simple(self) -> TemplateConfig:
        """简单文档生成模板"""
        return TemplateConfig(
            skill_type='document_generator',
            description='基础文档创建功能',
            required_tools=['Read', 'Write'],
            scripts=['template_engine.py'],
            examples=['basic_document'],
            documentation_level='basic'
        )
    
    def _document_generator_medium(self) -> TemplateConfig:
        """中等复杂度文档生成模板"""
        return TemplateConfig(
            skill_type='document_generator',
            description='高级文档生成和格式化',
            required_tools=['Read', 'Write', 'Edit'],
            scripts=['document_builder.py', 'formatter.py'],
            examples=['report_generation', 'template_processing'],
            documentation_level='intermediate',
            templates=True
        )
    
    def _document_generator_complex(self) -> TemplateConfig:
        """复杂文档生成模板"""
        return TemplateConfig(
            skill_type='document_generator',
            description='企业级文档管理系统',
            required_tools=['Read', 'Write', 'Edit', 'Bash'],
            scripts=['document_manager.py', 'version_controller.py', 'publisher.py'],
            examples=['document_workflow', 'version_management'],
            documentation_level='advanced',
            templates=True,
            versioning=True,
            publishing=True
        )
    
    def _workflow_simple(self) -> TemplateConfig:
        """简单工作流模板"""
        return TemplateConfig(
            skill_type='workflow',
            description='基础工作流自动化',
            required_tools=['Bash', 'Read'],
            scripts=['workflow_executor.py'],
            examples=['basic_workflow'],
            documentation_level='basic'
        )
    
    def _workflow_medium(self) -> TemplateConfig:
        """中等复杂度工作流模板"""
        return TemplateConfig(
            skill_type='workflow',
            description='高级工作流管理和执行',
            required_tools=['Bash', 'Read', 'Write', 'Task'],
            scripts=['workflow_manager.py', 'error_handler.py'],
            examples=['workflow_management', 'error_recovery'],
            documentation_level='intermediate',
            error_handling='comprehensive'
        )
    
    def _workflow_complex(self) -> TemplateConfig:
        """复杂工作流模板"""
        return TemplateConfig(
            skill_type='workflow',
            description='企业级工作流编排系统',
            required_tools=['Bash', 'Read', 'Write', 'Task', 'Edit'],
            scripts=['orchestrator.py', 'monitoring.py', 'scheduler.py'],
            examples=['workflow_orchestration', 'performance_monitoring'],
            documentation_level='advanced',
            error_handling='comprehensive',
            monitoring=True
        )
    
    def _default_template(self) -> TemplateConfig:
        """默认模板"""
        return TemplateConfig(
            skill_type='general',
            description='通用功能Skill',
            required_tools=['Read', 'Write'],
            scripts=[],
            examples=['basic_usage'],
            documentation_level='basic'
        )