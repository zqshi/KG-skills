#!/usr/bin/env python3
"""
Skill创建器核心
基于skill_builder，提供统一的Skill创建接口
"""

import sys
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'skill_builder'))

from skill_builder import SkillCreator as BaseSkillCreator, SkillSpec, CreationResult


class SkillCreator:
    """Skill创建器包装类"""
    
    def __init__(self):
        self.base_creator = BaseSkillCreator()
    
    def create_skill(self, args) -> CreationResult:
        """从命令行参数创建Skill"""
        # 转换参数
        spec = SkillSpec(
            name=args.name,
            description=args.description,
            skill_type=args.type,
            complexity=args.complexity,
            target_audience=args.audience,
            include_scripts=not args.no_scripts,
            include_templates=args.templates,
            custom_requirements=args.requirements,
            commands=args.commands
        )
        
        # 创建
        return self.base_creator.create_skill(spec)
    
    def create_skill_from_dict(self, data: dict) -> CreationResult:
        """从字典创建Skill"""
        spec = SkillSpec(**data)
        return self.base_creator.create_skill(spec)