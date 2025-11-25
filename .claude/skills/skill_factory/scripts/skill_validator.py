#!/usr/bin/env python3
"""
Skill结构验证脚本
用于验证生成的Skill包是否符合Claude Agent Skills规范
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple


class SkillValidator:
    """Skill验证器类"""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.errors = []
        self.warnings = []

    def validate_structure(self) -> bool:
        """验证Skill结构完整性"""
        print("🔍 开始验证Skill结构...")

        # 检查必需文件
        required_files = ["SKILL.md", "README.md"]
        for file in required_files:
            if not (self.skill_path / file).exists():
                self.errors.append(f"缺失必需文件: {file}")

        # 检查目录结构
        expected_dirs = ["scripts", "templates", "examples", "utils"]
        for dir_name in expected_dirs:
            dir_path = self.skill_path / dir_name
            if dir_path.exists() and not dir_path.is_dir():
                self.errors.append(f"{dir_name} 应该是一个目录")

        return len(self.errors) == 0

    def validate_yaml_header(self) -> bool:
        """验证SKILL.md的YAML头部"""
        print("📝 验证YAML头部规范...")

        skill_file = self.skill_path / "SKILL.md"
        if not skill_file.exists():
            self.errors.append("SKILL.md文件不存在")
            return False

        content = skill_file.read_text(encoding='utf-8')

        # 检查YAML头部格式
        yaml_pattern = r'^---\n(.+?)\n---'
        match = re.search(yaml_pattern, content, re.DOTALL)

        if not match:
            self.errors.append("SKILL.md缺少YAML头部")
            return False

        try:
            yaml_content = match.group(1)
            data = yaml.safe_load(yaml_content)

            # 检查必需字段
            required_fields = ["name", "description"]
            for field in required_fields:
                if field not in data:
                    self.errors.append(f"YAML头部缺少必需字段: {field}")

            # 验证字段长度限制
            if "name" in data and len(data["name"]) > 64:
                self.errors.append("name字段长度超过64字符限制")

            if "description" in data and len(data["description"]) > 1024:
                self.errors.append("description字段长度超过1024字符限制")

        except yaml.YAMLError as e:
            self.errors.append(f"YAML解析错误: {e}")
            return False

        return len(self.errors) == 0

    def validate_naming_convention(self) -> bool:
        """验证命名规范"""
        print("📛 验证命名规范...")

        # 检查Skill名称格式（小写下划线）
        skill_name = self.skill_path.name
        if not re.match(r'^[a-z][a-z0-9_]*(_[a-z0-9]+)*$', skill_name):
            self.errors.append(f"Skill名称不符合小写下划线规范: {skill_name}")

        # 检查文件命名规范
        for file_path in self.skill_path.rglob("*"):
            if file_path.is_file():
                filename = file_path.name

                # Python文件应该使用小写下划线
                if file_path.suffix == '.py':
                    if not re.match(r'^[a-z][a-z0-9_]*(_[a-z0-9]+)*\.py$', filename):
                        self.warnings.append(f"Python文件命名不规范: {filename}")

                # 参考文档应该使用大写格式
                if filename.startswith('REFERENCE_') and not filename.endswith('.md'):
                    self.errors.append(f"参考文档应该以.md结尾: {filename}")

        return len(self.errors) == 0

    def validate_scripts(self) -> bool:
        """验证Python脚本"""
        print("🐍 验证Python脚本...")

        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return True  # 没有脚本目录是允许的

        for script_file in scripts_dir.glob("*.py"):
            try:
                # 检查Python语法
                with open(script_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    compile(content, str(script_file), 'exec')

                # 检查是否有文档字符串
                if not re.search(r'""".*?"""', content, re.DOTALL):
                    self.warnings.append(f"脚本缺少文档字符串: {script_file.name}")

            except SyntaxError as e:
                self.errors.append(f"Python语法错误 ({script_file.name}): {e}")

        return len(self.errors) == 0

    def validate_templates(self) -> bool:
        """验证模板文件"""
        print("📋 验证模板文件...")

        templates_dir = self.skill_path / "templates"
        if not templates_dir.exists():
            return True  # 没有模板目录是允许的

        # 检查标准模板目录结构
        expected_templates = [
            "data_processor", "api_integrator", "document_generator",
            "file_operator", "content_creator"
        ]

        for template_dir in templates_dir.iterdir():
            if template_dir.is_dir():
                template_name = template_dir.name
                if template_name not in expected_templates:
                    self.warnings.append(f"非标准模板目录: {template_name}")

                # 检查模板目录是否包含SKILL.md
                skill_file = template_dir / "SKILL.md"
                if not skill_file.exists():
                    self.errors.append(f"模板目录缺少SKILL.md: {template_name}")

        return len(self.errors) == 0

    def run_all_checks(self) -> Tuple[bool, List[str], List[str]]:
        """运行所有验证检查"""
        validations = [
            self.validate_structure,
            self.validate_yaml_header,
            self.validate_naming_convention,
            self.validate_scripts,
            self.validate_templates
        ]

        all_passed = True
        for validation in validations:
            if not validation():
                all_passed = False

        return all_passed, self.errors, self.warnings


def main():
    """主函数"""
    import sys

    if len(sys.argv) != 2:
        print("用法: python skill_validator.py <skill_path>")
        sys.exit(1)

    skill_path = sys.argv[1]
    validator = SkillValidator(skill_path)

    passed, errors, warnings = validator.run_all_checks()

    # 输出结果
    print("\n" + "="*50)
    print("📊 验证结果")
    print("="*50)

    if passed:
        print("✅ Skill验证通过！")
    else:
        print("❌ Skill验证失败")

    if warnings:
        print("\n⚠️  警告:")
        for warning in warnings:
            print(f"   • {warning}")

    if errors:
        print("\n❌ 错误:")
        for error in errors:
            print(f"   • {error}")

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()