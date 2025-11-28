#!/usr/bin/env python3
"""
Skill验证器
验证Skill目录结构、YAML头部、Markdown结构等
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import yaml

# 添加utils到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))

from skill_manager.utils.file_helpers import FileHelper
from skill_manager.utils.logging_utils import setup_logger, get_skill_logger
from skill_manager.utils.validation_rules import (
    validate_skill_name, validate_yaml_header, ValidationResult
)


class SkillValidator:
    """Skill验证器类"""
    
    def __init__(self, skills_dir: Optional[Path] = None, verbose: bool = False):
        """
        初始化验证器
        
        Args:
            skills_dir: Skills根目录
            verbose: 是否显示详细信息
        """
        self.skills_dir = skills_dir or Path(__file__).parent.parent.parent
        self.verbose = verbose
        self.logger = setup_logger("skill_validator", 
                                   level=logging.DEBUG if verbose else logging.INFO)
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_skill(self, skill_name: str) -> ValidationResult:
        """
        验证单个Skill
        
        Args:
            skill_name: Skill名称
            
        Returns:
            验证结果
        """
        self.logger.info(f"开始验证Skill: {skill_name}")
        self.errors.clear()
        self.warnings.clear()
        
        skill_dir = self.skills_dir / skill_name
        
        # 1. 验证目录存在
        if not self._validate_directory_exists(skill_dir, skill_name):
            return ValidationResult(False, f"Skill目录不存在: {skill_name}", self.errors)
        
        # 2. 验证SKILL.md存在
        skill_file = skill_dir / "SKILL.md"
        if not self._validate_file_exists(skill_file, "SKILL.md"):
            return ValidationResult(False, f"SKILL.md不存在: {skill_name}", self.errors)
        
        # 3. 验证YAML头部
        if not self._validate_yaml_header(skill_file):
            pass  # 错误已在方法内添加
        
        # 4. 验证Markdown结构
        if not self._validate_markdown_structure(skill_file):
            pass  # 错误已在方法内添加
        
        # 5. 验证scripts目录（如果存在）
        scripts_dir = skill_dir / "scripts"
        if scripts_dir.exists():
            if not self._validate_scripts_directory(scripts_dir):
                pass  # 错误已在方法内添加
        
        # 6. 验证examples目录（如果存在）
        examples_dir = skill_dir / "examples"
        if examples_dir.exists():
            if not self._validate_examples_directory(examples_dir):
                pass  # 错误已在方法内添加
        
        # 返回结果
        if self.errors:
            return ValidationResult(False, f"Skill验证失败: {skill_name}", self.errors)
        elif self.warnings:
            return ValidationResult(True, f"Skill验证通过（有警告）: {skill_name}", self.warnings)
        else:
            return ValidationResult(True, f"Skill验证通过: {skill_name}")
    
    def _validate_directory_exists(self, directory: Path, name: str) -> bool:
        """验证目录存在"""
        if not directory.exists():
            error = f"目录不存在: {directory}"
            self.errors.append(error)
            self.logger.error(error)
            return False
        
        if not directory.is_dir():
            error = f"路径存在但不是目录: {directory}"
            self.errors.append(error)
            self.logger.error(error)
            return False
        
        self.logger.debug(f"✓ 目录存在: {directory}")
        return True
    
    def _validate_file_exists(self, file_path: Path, name: str) -> bool:
        """验证文件存在"""
        if not file_path.exists():
            error = f"文件不存在: {file_path}"
            self.errors.append(error)
            self.logger.error(error)
            return False
        
        if not file_path.is_file():
            error = f"路径存在但不是文件: {file_path}"
            self.errors.append(error)
            self.logger.error(error)
            return False
        
        self.logger.debug(f"✓ 文件存在: {file_path}")
        return True
    
    def _validate_yaml_header(self, skill_file: Path) -> bool:
        """验证YAML头部"""
        try:
            frontmatter, _ = FileHelper.read_markdown_with_frontmatter(skill_file)
            
            if not frontmatter:
                error = "YAML front matter不存在或格式错误"
                self.errors.append(error)
                self.logger.error(error)
                return False
            
            # 验证必需字段
            required_fields = ['name', 'description']
            for field in required_fields:
                if field not in frontmatter:
                    error = f"YAML头部缺少必需字段: {field}"
                    self.errors.append(error)
                    self.logger.error(error)
                    return False
            
            # 验证name字段
            name_result = validate_skill_name(frontmatter['name'])
            if not name_result:
                self.errors.extend(name_result.errors)
                self.logger.error(f"Skill名称验证失败: {name_result}")
            
            self.logger.debug("✓ YAML头部验证通过")
            return True
            
        except Exception as e:
            error = f"YAML头部验证失败: {str(e)}"
            self.errors.append(error)
            self.logger.error(error)
            return False
    
    def _validate_markdown_structure(self, skill_file: Path) -> bool:
        """验证Markdown结构"""
        try:
            _, content = FileHelper.read_markdown_with_frontmatter(skill_file)
            
            # 检查必需章节
            required_sections = [
                '核心功能',
                '工作流SOP',
                '输入规范',
                '输出内容'
            ]
            
            for section in required_sections:
                if section not in content:
                    warning = f"缺少推荐章节: {section}"
                    self.warnings.append(warning)
                    self.logger.warning(warning)
            
            self.logger.debug("✓ Markdown结构验证通过")
            return True
            
        except Exception as e:
            error = f"Markdown结构验证失败: {str(e)}"
            self.errors.append(error)
            self.logger.error(error)
            return False
    
    def _validate_scripts_directory(self, scripts_dir: Path) -> bool:
        """验证scripts目录"""
        try:
            python_files = list(scripts_dir.glob("*.py"))
            
            if not python_files:
                warning = f"scripts目录存在但没有Python文件: {scripts_dir}"
                self.warnings.append(warning)
                self.logger.warning(warning)
                return True
            
            # 验证Python文件语法
            for py_file in python_files:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        compile(f.read(), str(py_file), 'exec')
                    self.logger.debug(f"✓ Python文件语法正确: {py_file.name}")
                except SyntaxError as e:
                    error = f"Python文件语法错误 {py_file.name}: {str(e)}"
                    self.errors.append(error)
                    self.logger.error(error)
            
            return True
            
        except Exception as e:
            error = f"scripts目录验证失败: {str(e)}"
            self.errors.append(error)
            self.logger.error(error)
            return False
    
    def _validate_examples_directory(self, examples_dir: Path) -> bool:
        """验证examples目录"""
        try:
            if not any(examples_dir.iterdir()):
                warning = f"examples目录为空: {examples_dir}"
                self.warnings.append(warning)
                self.logger.warning(warning)
            
            self.logger.debug("✓ examples目录验证通过")
            return True
            
        except Exception as e:
            error = f"examples目录验证失败: {str(e)}"
            self.errors.append(error)
            self.logger.error(error)
            return False
    
    def validate_all_skills(self) -> Dict[str, ValidationResult]:
        """
        验证所有Skills
        
        Returns:
            验证结果字典，key为Skill名称，value为验证结果
        """
        self.logger.info(f"开始验证所有Skills，目录: {self.skills_dir}")
        
        results = {}
        skill_dirs = [d for d in self.skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
        
        self.logger.info(f"发现 {len(skill_dirs)} 个Skills")
        
        for skill_dir in skill_dirs:
            skill_name = skill_dir.name
            result = self.validate_skill(skill_name)
            results[skill_name] = result
            
            if result.is_valid:
                if result.errors:  # 有警告
                    self.logger.warning(f"⚠️  {skill_name}: {result}")
                else:
                    self.logger.info(f"✅ {skill_name}: {result}")
            else:
                self.logger.error(f"❌ {skill_name}: {result}")
        
        return results
    
    def generate_report(self, results: Dict[str, ValidationResult], 
                        output_file: Optional[Path] = None) -> str:
        """
        生成验证报告
        
        Args:
            results: 验证结果字典
            output_file: 输出文件路径（可选）
            
        Returns:
            报告内容
        """
        total = len(results)
        valid = sum(1 for r in results.values() if r.is_valid and not r.errors)
        valid_with_warnings = sum(1 for r in results.values() if r.is_valid and r.errors)
        invalid = sum(1 for r in results.values() if not r.is_valid)
        
        report_lines = [
            "# Skills验证报告",
            "",
            f"**验证时间**: {Path().stat().st_mtime}",
            f"**总Skill数**: {total}",
            f"**验证通过**: {valid}",
            f"**通过（有警告）**: {valid_with_warnings}",
            f"**验证失败**: {invalid}",
            "",
            "## 详细结果",
            ""
        ]
        
        for skill_name, result in sorted(results.items()):
            status = "✅" if result.is_valid else "❌"
            if result.is_valid and result.errors:
                status = "⚠️"
            
            report_lines.append(f"### {status} {skill_name}")
            report_lines.append(f"{result}")
            report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        if output_file:
            FileHelper.write_file(output_file, report_content)
            self.logger.info(f"报告已保存: {output_file}")
        
        return report_content


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Skill验证器')
    parser.add_argument('skill', nargs='?', help='要验证的Skill名称（不指定则验证所有）')
    parser.add_argument('--all', action='store_true', help='验证所有Skills')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出结果')
    parser.add_argument('--report', help='生成报告文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    # 创建验证器
    validator = SkillValidator(verbose=args.verbose)
    
    # 验证单个Skill或所有Skills
    if args.skill and not args.all:
        result = validator.validate_skill(args.skill)
        results = {args.skill: result}
    else:
        results = validator.validate_all_skills()
    
    # 输出结果
    if args.json:
        # JSON格式输出
        json_results = {
            name: {
                "is_valid": result.is_valid,
                "message": result.message,
                "errors": result.errors
            }
            for name, result in results.items()
        }
        print(json.dumps(json_results, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出
        for skill_name, result in results.items():
            status = "✅" if result.is_valid else "❌"
            if result.is_valid and result.errors:
                status = "⚠️"
            print(f"{status} {skill_name}: {result}")
    
    # 生成报告
    if args.report:
        report_path = Path(args.report)
        validator.generate_report(results, report_path)
    
    # 返回退出码
    if any(not result.is_valid for result in results.values()):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    import logging
    main()