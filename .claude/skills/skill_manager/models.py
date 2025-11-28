#!/usr/bin/env python3
"""
数据模型定义
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class OperationRecord:
    """操作记录 - 遵循5W1H原则，包含8个核心字段"""
    
    # Who (谁)
    user: str  # 操作用户
    session_id: str  # 会话/请求ID
    
    # When (何时)
    timestamp: str  # 操作时间 (ISO 8601格式)
    
    # What (什么)
    action_type: str  # 操作类型: login, modify, delete, query, execute等
    command: str  # 具体命令或操作
    
    # Where (何地)
    working_directory: str  # 工作目录
    hostname: str  # 主机名
    source_ip: str  # 来源IP地址
    
    # Why (为何)
    purpose: str  # 操作目的: business, maintenance, investigation, emergency等
    description: str  # 操作说明/原因
    
    # How (如何)
    tool: str  # 使用的工具/接口
    duration_seconds: float  # 执行时长
    exit_code: int  # 退出码
    output: str  # 输出结果
    
    # Object (对象)
    target_object: str  # 操作对象 (文件名、表名等)
    object_type: str  # 对象类型: file, database_table, api_endpoint, directory等
    
    # Result (结果)
    result_code: int  # 结果码
    result_message: str  # 结果消息
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OperationRecord':
        """从字典创建实例"""
        return cls(**data)
    
    def is_successful(self) -> bool:
        """判断操作是否成功"""
        return self.exit_code == 0 and self.result_code == 0


@dataclass
class SkillSpec:
    """Skill规格定义"""
    name: str
    description: str
    skill_type: str  # data_processor, api_integrator, file_operator, content_creator, document_generator, workflow
    complexity: str = 'medium'  # simple, medium, complex
    target_audience: str = 'intermediate'  # beginner, intermediate, expert
    include_scripts: bool = True
    include_templates: bool = False
    custom_requirements: Optional[str] = None
    commands: Optional[List[str]] = None  # 工作流命令（workflow类型用）
    
    def validate(self) -> bool:
        """验证规格有效性"""
        if not self.name or not self.description:
            return False
        
        valid_types = ['data_processor', 'api_integrator', 'file_operator', 
                      'content_creator', 'document_generator', 'workflow']
        if self.skill_type not in valid_types:
            return False
        
        valid_complexity = ['simple', 'medium', 'complex']
        if self.complexity not in valid_complexity:
            return False
        
        return True


@dataclass
class TemplateConfig:
    """模板配置"""
    skill_type: str
    description: str
    required_tools: List[str]
    scripts: List[str]
    examples: List[str]
    documentation_level: str = 'basic'
    include_validation: bool = False
    error_handling: str = 'basic'
    authentication: str = 'none'
    rate_limiting: bool = False
    caching: bool = False
    monitoring: bool = False
    batch_operations: bool = False
    backup: bool = False
    synchronization: bool = False
    quality_check: bool = False
    seo_analysis: bool = False
    publishing: bool = False
    templates: bool = False
    versioning: bool = False
    custom_options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructureConfig:
    """结构配置"""
    name: str
    description: str
    skill_type: str
    complexity: str
    directories: List[str]
    scripts: List[str]
    templates: List[str]
    examples: List[str]
    required_files: List[str] = field(default_factory=lambda: ['SKILL.md', 'README.md'])
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


@dataclass
class WorkflowInfo:
    """工作流信息"""
    workflow_id: str
    name: str
    type: str
    complexity: str
    commands: List[str]
    frequency: int
    support: float
    description: str
    confidence: float
    
    def to_skill_spec(self) -> SkillSpec:
        """转换为Skill规格"""
        return SkillSpec(
            name=self.name,
            description=self.description,
            skill_type='workflow',
            complexity=self.complexity,
            target_audience='intermediate',
            include_scripts=True,
            include_templates=False,
            custom_requirements=f"自动从工作流生成: {'; '.join(self.commands[:3])}",
            commands=self.commands
        )


@dataclass
class CreationResult:
    """创建结果"""
    success: bool
    skill_name: str
    message: str
    path: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)