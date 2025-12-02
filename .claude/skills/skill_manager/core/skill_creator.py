#!/usr/bin/env python3
"""
Skill创建器核心
提供统一的Skill创建接口
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import SkillSpec, CreationResult
from core.structure_generator import StructureGenerator
from core.template_manager import TemplateManager


class SkillCreator:
    """Skill创建器"""
    
    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            # 默认为 .claude/skills 目录
            base_path = Path(__file__).parent.parent.parent
        
        self.base_path = Path(base_path)
        self.structure_generator = StructureGenerator(base_path)
        self.template_manager = TemplateManager()
    
    def create_skill(self, spec: SkillSpec) -> CreationResult:
        """创建Skill"""
        try:
            # 1. 验证规格
            if not spec.validate():
                return CreationResult(
                    success=False,
                    skill_name=spec.name,
                    message="Skill规格验证失败",
                    errors=["名称或描述不能为空", "类型或复杂度无效"]
                )
            
            # 2. 检查是否存在
            skill_dir = self.base_path / spec.name
            if skill_dir.exists():
                return CreationResult(
                    success=False,
                    skill_name=spec.name,
                    message=f"Skill '{spec.name}' 已存在",
                    errors=[f"目录已存在: {skill_dir}"]
                )
            
            # 3. 选择模板
            template = self.template_manager.select_template(spec)
            
            # 4. 生成结构配置
            config = self.structure_generator.generate_structure(spec, template)
            
            # 5. 创建结构
            if self.structure_generator.create_structure(config):
                return CreationResult(
                    success=True,
                    skill_name=spec.name,
                    message=f"Skill '{spec.name}' 创建成功",
                    path=str(skill_dir)
                )
            else:
                return CreationResult(
                    success=False,
                    skill_name=spec.name,
                    message="创建目录结构失败"
                )
                
        except Exception as e:
            return CreationResult(
                success=False,
                skill_name=spec.name,
                message=f"创建过程发生错误: {str(e)}",
                errors=[str(e)]
            )
    
    def create_skill_from_args(self, args) -> CreationResult:
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
        return self.create_skill(spec)
    
    def create_skill_from_dict(self, data: dict) -> CreationResult:
        """从字典创建Skill"""
        spec = SkillSpec(**data)
        return self.create_skill(spec)