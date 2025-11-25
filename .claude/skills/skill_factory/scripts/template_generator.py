#!/usr/bin/env python3
"""
模板生成器脚本
基于Skill类型和复杂度自动生成合适的模板内容
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SkillRequirements:
    """Skill需求数据类"""
    name: str
    description: str
    skill_type: str  # 'data', 'api', 'doc', 'file', 'content'
    complexity: str  # 'simple', 'medium', 'complex'
    target_audience: str  # 'beginner', 'intermediate', 'expert'
    include_scripts: bool = False
    include_templates: bool = False
    custom_requirements: Optional[str] = None


class TemplateGenerator:
    """模板生成器类"""

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """加载预定义模板"""
        return {
            'data': {
                'simple': self._simple_data_template(),
                'medium': self._medium_data_template(),
                'complex': self._complex_data_template()
            },
            'api': {
                'simple': self._simple_api_template(),
                'medium': self._medium_api_template(),
                'complex': self._complex_api_template()
            },
            'doc': {
                'simple': self._simple_doc_template(),
                'medium': self._medium_doc_template(),
                'complex': self._complex_doc_template()
            },
            'file': {
                'simple': self._simple_file_template(),
                'medium': self._medium_file_template(),
                'complex': self._complex_file_template()
            },
            'content': {
                'simple': self._simple_content_template(),
                'medium': self._medium_content_template(),
                'complex': self._complex_content_template()
            }
        }

    def select_template(self, requirements: SkillRequirements) -> Dict:
        """基于需求选择最合适的模板"""
        print(f"🎯 为 {requirements.skill_type} 类型选择模板 (复杂度: {requirements.complexity})")

        # 获取基础模板
        base_template = self.templates.get(requirements.skill_type, {}).get(
            requirements.complexity, self._default_template()
        )

        # 根据目标用户调整模板
        template = self._adjust_for_audience(base_template, requirements.target_audience)

        # 添加自定义需求
        if requirements.custom_requirements:
            template = self._add_custom_requirements(template, requirements.custom_requirements)

        return template

    def _adjust_for_audience(self, template: Dict, audience: str) -> Dict:
        """根据目标用户调整模板"""
        adjusted = template.copy()

        if audience == 'beginner':
            # 为初学者添加更多指导和示例
            adjusted['documentation_level'] = 'detailed'
            adjusted['include_basic_examples'] = True
            adjusted['step_by_step_guide'] = True

        elif audience == 'expert':
            # 为专家简化文档，增加技术细节
            adjusted['documentation_level'] = 'technical'
            adjusted['include_advanced_features'] = True
            adjusted['api_reference'] = True

        return adjusted

    def _add_custom_requirements(self, template: Dict, custom_req: str) -> Dict:
        """添加自定义需求到模板"""
        template['custom_requirements'] = custom_req

        # 根据自定义需求调整模板内容
        if 'api' in custom_req.lower():
            template['include_api_integration'] = True
        if 'data' in custom_req.lower():
            template['data_processing'] = True
        if 'file' in custom_req.lower():
            template['file_operations'] = True

        return template

    def _simple_data_template(self) -> Dict:
        """简单数据处理模板"""
        return {
            'skill_type': 'data_processor',
            'description': '基础数据处理功能',
            'required_tools': ['Read', 'Write', 'Edit'],
            'scripts': ['data_cleaner.py'],
            'examples': ['basic_data_processing'],
            'documentation_level': 'basic'
        }

    def _medium_data_template(self) -> Dict:
        """中等复杂度数据处理模板"""
        return {
            'skill_type': 'data_processor',
            'description': '高级数据处理和分析',
            'required_tools': ['Read', 'Write', 'Edit', 'Bash'],
            'scripts': ['data_processor.py', 'analysis_tool.py'],
            'examples': ['data_analysis', 'report_generation'],
            'documentation_level': 'intermediate',
            'include_validation': True
        }

    def _complex_data_template(self) -> Dict:
        """复杂数据处理模板"""
        return {
            'skill_type': 'data_processor',
            'description': '企业级数据处理流水线',
            'required_tools': ['Read', 'Write', 'Edit', 'Bash', 'Task'],
            'scripts': ['pipeline_manager.py', 'quality_checker.py', 'report_generator.py'],
            'examples': ['data_pipeline', 'quality_assurance'],
            'documentation_level': 'advanced',
            'include_validation': True,
            'error_handling': 'comprehensive'
        }

    def _simple_api_template(self) -> Dict:
        """简单API集成模板"""
        return {
            'skill_type': 'api_integrator',
            'description': '基础API调用功能',
            'required_tools': ['WebFetch', 'Read'],
            'scripts': ['api_client.py'],
            'examples': ['basic_api_call'],
            'documentation_level': 'basic',
            'authentication': 'simple'
        }

    def _medium_api_template(self) -> Dict:
        """中等复杂度API集成模板"""
        return {
            'skill_type': 'api_integrator',
            'description': '高级API集成和管理',
            'required_tools': ['WebFetch', 'Read', 'Write', 'Bash'],
            'scripts': ['api_manager.py', 'response_parser.py'],
            'examples': ['api_integration', 'data_sync'],
            'documentation_level': 'intermediate',
            'authentication': 'oauth',
            'rate_limiting': True
        }

    def _complex_api_template(self) -> Dict:
        """复杂API集成模板"""
        return {
            'skill_type': 'api_integrator',
            'description': '企业级API生态系统',
            'required_tools': ['WebFetch', 'Read', 'Write', 'Bash', 'Task'],
            'scripts': ['ecosystem_manager.py', 'monitoring_tool.py', 'cache_manager.py'],
            'examples': ['api_ecosystem', 'performance_monitoring'],
            'documentation_level': 'advanced',
            'authentication': 'multi-factor',
            'rate_limiting': True,
            'caching': True,
            'monitoring': True
        }

    def _simple_doc_template(self) -> Dict:
        """简单文档生成模板"""
        return {
            'skill_type': 'document_generator',
            'description': '基础文档创建功能',
            'required_tools': ['Read', 'Write'],
            'scripts': ['template_engine.py'],
            'examples': ['basic_document'],
            'documentation_level': 'basic'
        }

    def _medium_doc_template(self) -> Dict:
        """中等复杂度文档生成模板"""
        return {
            'skill_type': 'document_generator',
            'description': '高级文档生成和格式化',
            'required_tools': ['Read', 'Write', 'Edit'],
            'scripts': ['document_builder.py', 'formatter.py'],
            'examples': ['report_generation', 'template_processing'],
            'documentation_level': 'intermediate',
            'templates': True
        }

    def _complex_doc_template(self) -> Dict:
        """复杂文档生成模板"""
        return {
            'skill_type': 'document_generator',
            'description': '企业级文档管理系统',
            'required_tools': ['Read', 'Write', 'Edit', 'Bash'],
            'scripts': ['document_manager.py', 'version_controller.py', 'publisher.py'],
            'examples': ['document_workflow', 'version_management'],
            'documentation_level': 'advanced',
            'templates': True,
            'versioning': True,
            'publishing': True
        }

    def _simple_file_template(self) -> Dict:
        """简单文件操作模板"""
        return {
            'skill_type': 'file_operator',
            'description': '基础文件管理功能',
            'required_tools': ['Read', 'Write', 'Glob'],
            'scripts': ['file_manager.py'],
            'examples': ['file_operations'],
            'documentation_level': 'basic'
        }

    def _medium_file_template(self) -> Dict:
        """中等复杂度文件操作模板"""
        return {
            'skill_type': 'file_operator',
            'description': '高级文件处理和转换',
            'required_tools': ['Read', 'Write', 'Glob', 'Bash'],
            'scripts': ['batch_processor.py', 'converter.py'],
            'examples': ['batch_processing', 'format_conversion'],
            'documentation_level': 'intermediate',
            'batch_operations': True
        }

    def _complex_file_template(self) -> Dict:
        """复杂文件操作模板"""
        return {
            'skill_type': 'file_operator',
            'description': '企业级文件管理系统',
            'required_tools': ['Read', 'Write', 'Glob', 'Bash', 'Task'],
            'scripts': ['system_manager.py', 'backup_tool.py', 'sync_engine.py'],
            'examples': ['file_system', 'backup_management'],
            'documentation_level': 'advanced',
            'batch_operations': True,
            'backup': True,
            'synchronization': True
        }

    def _simple_content_template(self) -> Dict:
        """简单内容创作模板"""
        return {
            'skill_type': 'content_creator',
            'description': '基础内容生成功能',
            'required_tools': ['Read', 'Write'],
            'scripts': ['content_generator.py'],
            'examples': ['content_creation'],
            'documentation_level': 'basic'
        }

    def _medium_content_template(self) -> Dict:
        """中等复杂度内容创作模板"""
        return {
            'skill_type': 'content_creator',
            'description': '高级内容创作和优化',
            'required_tools': ['Read', 'Write', 'Edit'],
            'scripts': ['content_optimizer.py', 'style_checker.py'],
            'examples': ['content_optimization', 'style_analysis'],
            'documentation_level': 'intermediate',
            'quality_check': True
        }

    def _complex_content_template(self) -> Dict:
        """复杂内容创作模板"""
        return {
            'skill_type': 'content_creator',
            'description': '企业级内容管理系统',
            'required_tools': ['Read', 'Write', 'Edit', 'Bash'],
            'scripts': ['content_manager.py', 'seo_analyzer.py', 'publishing_tool.py'],
            'examples': ['content_workflow', 'seo_optimization'],
            'documentation_level': 'advanced',
            'quality_check': True,
            'seo_analysis': True,
            'publishing': True
        }

    def _default_template(self) -> Dict:
        """默认模板"""
        return {
            'skill_type': 'general',
            'description': '通用功能Skill',
            'required_tools': ['Read', 'Write'],
            'scripts': [],
            'examples': ['basic_usage'],
            'documentation_level': 'basic'
        }

    def generate_skill_structure(self, requirements: SkillRequirements, template: Dict) -> Dict:
        """基于模板生成Skill结构"""
        structure = {
            'skill_name': requirements.name,
            'description': requirements.description,
            'files': {
                'required': ['SKILL.md', 'README.md']
            },
            'directories': [],
            'scripts': [],
            'templates': [],
            'examples': []
        }

        # 添加脚本目录和文件
        if requirements.include_scripts and template.get('scripts'):
            structure['directories'].append('scripts')
            structure['scripts'] = template['scripts']

        # 添加模板目录
        if requirements.include_templates:
            structure['directories'].append('templates')
            structure['templates'] = [f"{requirements.skill_type}_template"]

        # 添加示例
        if template.get('examples'):
            structure['directories'].append('examples')
            structure['examples'] = template['examples']

        # 添加工具函数目录
        if requirements.complexity in ['medium', 'complex']:
            structure['directories'].append('utils')

        return structure


def main():
    """主函数 - 示例用法"""
    # 示例需求
    requirements = SkillRequirements(
        name="excel_processor",
        description="Excel数据处理和转换工具",
        skill_type="data",
        complexity="medium",
        target_audience="intermediate",
        include_scripts=True,
        include_templates=False
    )

    generator = TemplateGenerator()
    template = generator.select_template(requirements)
    structure = generator.generate_skill_structure(requirements, template)

    print("🎯 生成的模板:")
    print(template)
    print("\n📁 生成的Skill结构:")
    print(structure)


if __name__ == "__main__":
    main()