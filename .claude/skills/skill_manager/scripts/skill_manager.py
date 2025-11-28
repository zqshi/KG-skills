#!/usr/bin/env python3
"""
Skill管理器
统一的Skill管理入口，提供创建、验证、部署等功能
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))

from skill_manager.utils.file_helpers import FileHelper
from skill_manager.utils.logging_utils import setup_logger, get_skill_logger
from skill_manager.utils.validation_rules import validate_skill_name, ValidationResult
from skill_validator import SkillValidator


class SkillManager:
    """Skill管理器类"""
    
    def __init__(self, skills_dir: Optional[Path] = None, verbose: bool = False):
        """
        初始化管理器
        
        Args:
            skills_dir: Skills根目录
            verbose: 是否显示详细信息
        """
        self.skills_dir = skills_dir or Path(__file__).parent.parent.parent
        self.verbose = verbose
        self.logger = setup_logger("skill_manager", 
                                   level=logging.DEBUG if verbose else logging.INFO)
        self.validator = SkillValidator(self.skills_dir, verbose)
    
    def list_skills(self, detailed: bool = False) -> List[Dict[str, Any]]:
        """
        列出所有Skills
        
        Args:
            detailed: 是否显示详细信息
            
        Returns:
            Skill信息列表
        """
        self.logger.info("列出所有Skills...")
        
        skills = []
        skill_dirs = [d for d in self.skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
        
        for skill_dir in skill_dirs:
            skill_name = skill_dir.name
            
            # 读取YAML头部
            skill_file = skill_dir / "SKILL.md"
            try:
                frontmatter, _ = FileHelper.read_markdown_with_frontmatter(skill_file)
                
                skill_info = {
                    "name": skill_name,
                    "description": frontmatter.get("description", ""),
                    "has_scripts": (skill_dir / "scripts").exists(),
                    "has_examples": (skill_dir / "examples").exists(),
                    "file_size": FileHelper.get_file_size(skill_file)
                }
                
                if detailed:
                    skill_info.update({
                        "tools": frontmatter.get("tools", []),
                        "path": str(skill_dir)
                    })
                
                skills.append(skill_info)
                
            except Exception as e:
                self.logger.warning(f"读取Skill信息失败 {skill_name}: {str(e)}")
        
        # 按名称排序
        skills.sort(key=lambda x: x["name"])
        
        self.logger.info(f"发现 {len(skills)} 个Skills")
        return skills
    
    def create_skill(self, name: str, description: str, 
                     template: Optional[str] = None) -> ValidationResult:
        """
        创建新Skill
        
        Args:
            name: Skill名称
            description: Skill描述
            template: 模板名称（可选）
            
        Returns:
            创建结果
        """
        self.logger.info(f"创建新Skill: {name}")
        
        # 验证名称
        name_result = validate_skill_name(name)
        if not name_result:
            return name_result
        
        # 检查是否已存在
        skill_dir = self.skills_dir / name
        if skill_dir.exists():
            return ValidationResult(False, f"Skill已存在: {name}")
        
        try:
            # 创建目录
            skill_dir.mkdir(parents=True)
            
            # 创建YAML头部
            frontmatter = {
                "name": name,
                "description": description,
                "tools": ["Read", "Write"]
            }
            
            # 创建基础内容
            content = f"""# {name}

## 🎯 核心功能

{description}

## 📋 工作流SOP

**工作流SOP**：
```
1. 接收输入
2. 处理数据
3. 返回结果
```

### 详细流程说明

**步骤1：接收输入**
- 验证输入参数
- 解析输入数据

**步骤2：处理数据**
- 执行核心逻辑
- 处理异常情况

**步骤3：返回结果**
- 格式化输出
- 返回处理结果

## 📋 输入规范

### 必需输入
```json
{{
  "input_data": "输入数据"
}}
```

### 可选输入
```json
{{
  "options": {{}}
}}
```

## 📤 输出内容

### 标准输出
```json
{{
  "result": "处理结果",
  "status": "success"
}}
```

### 错误输出
```json
{{
  "status": "error",
  "message": "错误信息"
}}
```

## 🎪 使用示例

### 示例1: 基本使用
```
使用 {name} 处理数据
输入：示例数据
```

## ⚠️ 注意事项

### 安全考虑
- 验证输入数据
- 处理敏感信息

### 性能优化
- 合理使用资源
- 避免重复计算

## 📊 质量指标

- **成功率**: ≥95%
- **准确率**: ≥90%

---

**{name}** - 让数据处理变得简单！ 🚀
"""
            
            # 写入文件
            skill_file = skill_dir / "SKILL.md"
            FileHelper.write_markdown_with_frontmatter(skill_file, frontmatter, content)
            
            # 创建scripts目录
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
            # 创建__init__.py
            init_file = scripts_dir / "__init__.py"
            init_file.write_text("# Skill scripts\n")
            
            # 创建examples目录
            examples_dir = skill_dir / "examples"
            examples_dir.mkdir()
            
            # 创建基础示例
            example_file = examples_dir / "basic_usage" / "README.md"
            example_file.parent.mkdir()
            example_file.write_text(f"""# {name} 基础使用示例

## 示例说明

这是一个 {name} 的基础使用示例。

## 使用步骤

1. 准备输入数据
2. 调用Skill
3. 查看输出结果

## 示例输入

```json
{{
  "input_data": "示例数据"
}}
```

## 预期输出

```json
{{
  "result": "处理结果",
  "status": "success"
}}
```
""")
            
            self.logger.info(f"✅ Skill创建成功: {name}")
            return ValidationResult(True, f"Skill创建成功: {name}", 
                                   [f"路径: {skill_dir}"])
            
        except Exception as e:
            error_msg = f"创建Skill失败: {str(e)}"
            self.logger.error(error_msg)
            return ValidationResult(False, error_msg)
    
    def validate_skill(self, name: str) -> ValidationResult:
        """
        验证Skill
        
        Args:
            name: Skill名称
            
        Returns:
            验证结果
        """
        return self.validator.validate_skill(name)
    
    def validate_all_skills(self) -> Dict[str, ValidationResult]:
        """
        验证所有Skills
        
        Returns:
            验证结果字典
        """
        return self.validator.validate_all_skills()
    
    def deploy_skill(self, name: str, target_dir: Path) -> ValidationResult:
        """
        部署Skill到目标目录
        
        Args:
            name: Skill名称
            target_dir: 目标目录
            
        Returns:
            部署结果
        """
        self.logger.info(f"部署Skill: {name} -> {target_dir}")
        
        # 验证Skill存在
        skill_dir = self.skills_dir / name
        if not skill_dir.exists():
            return ValidationResult(False, f"Skill不存在: {name}")
        
        try:
            # 确保目标目录存在
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # 复制Skill目录
            import shutil
            target_skill_dir = target_dir / name
            
            if target_skill_dir.exists():
                # 备份已存在的目录
                backup_dir = target_dir / f"{name}_backup"
                if backup_dir.exists():
                    shutil.rmtree(backup_dir)
                target_skill_dir.rename(backup_dir)
                self.logger.warning(f"已备份现有Skill: {backup_dir}")
            
            # 复制
            shutil.copytree(skill_dir, target_skill_dir)
            
            self.logger.info(f"✅ Skill部署成功: {name}")
            return ValidationResult(True, f"Skill部署成功: {name}",
                                   [f"源路径: {skill_dir}", f"目标路径: {target_skill_dir}"])
            
        except Exception as e:
            error_msg = f"部署Skill失败: {str(e)}"
            self.logger.error(error_msg)
            return ValidationResult(False, error_msg)
    
    def get_skill_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        获取Skill详细信息
        
        Args:
            name: Skill名称
            
        Returns:
            Skill信息字典，不存在返回None
        """
        skill_dir = self.skills_dir / name
        if not skill_dir.exists():
            return None
        
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            return None
        
        try:
            frontmatter, content = FileHelper.read_markdown_with_frontmatter(skill_file)
            
            return {
                "name": name,
                "description": frontmatter.get("description", ""),
                "tools": frontmatter.get("tools", []),
                "path": str(skill_dir),
                "has_scripts": (skill_dir / "scripts").exists(),
                "has_examples": (skill_dir / "examples").exists(),
                "file_size": FileHelper.get_file_size(skill_file),
                "content_preview": content[:200] + "..." if len(content) > 200 else content
            }
            
        except Exception as e:
            self.logger.error(f"读取Skill信息失败 {name}: {str(e)}")
            return None
    
    def generate_project_report(self, output_file: Optional[Path] = None) -> str:
        """
        生成项目报告
        
        Args:
            output_file: 输出文件路径（可选）
            
        Returns:
            报告内容
        """
        self.logger.info("生成项目报告...")
        
        # 获取所有Skills
        skills = self.list_skills(detailed=True)
        
        # 统计信息
        total = len(skills)
        has_scripts = sum(1 for s in skills if s["has_scripts"])
        has_examples = sum(1 for s in skills if s["has_examples"])
        total_size = sum(s["file_size"] for s in skills)
        
        # 验证所有Skills
        validation_results = self.validate_all_skills()
        valid_count = sum(1 for r in validation_results.values() if r.is_valid and not r.errors)
        warning_count = sum(1 for r in validation_results.values() if r.is_valid and r.errors)
        invalid_count = sum(1 for r in validation_results.values() if not r.is_valid)
        
        # 生成报告
        report_lines = [
            "# Skills项目报告",
            "",
            f"**生成时间**: {Path().stat().st_mtime}",
            f"**总Skill数**: {total}",
            f"**包含scripts**: {has_scripts}",
            f"**包含examples**: {has_examples}",
            f"**总大小**: {self._format_size(total_size)}",
            "",
            "## 验证结果",
            f"- **验证通过**: {valid_count}",
            f"- **通过（有警告）**: {warning_count}",
            f"- **验证失败**: {invalid_count}",
            "",
            "## Skills列表",
            ""
        ]
        
        for skill in skills:
            status = "✅"
            if skill["name"] in validation_results:
                result = validation_results[skill["name"]]
                if not result.is_valid:
                    status = "❌"
                elif result.errors:
                    status = "⚠️"
            
            report_lines.append(f"### {status} {skill['name']}")
            report_lines.append(f"**描述**: {skill['description']}")
            report_lines.append(f"**工具**: {', '.join(skill['tools'])}")
            report_lines.append(f"**scripts**: {'✅' if skill['has_scripts'] else '❌'}")
            report_lines.append(f"**examples**: {'✅' if skill['has_examples'] else '❌'}")
            report_lines.append(f"**大小**: {self._format_size(skill['file_size'])}")
            report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        if output_file:
            FileHelper.write_file(output_file, report_content)
            self.logger.info(f"报告已保存: {output_file}")
        
        return report_content
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        size = size_bytes
        
        while size >= 1024 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f}{size_names[i]}"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Skill管理器')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出所有Skills')
    list_parser.add_argument('--detailed', '-d', action='store_true', help='显示详细信息')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='创建新Skill')
    create_parser.add_argument('--name', required=True, help='Skill名称')
    create_parser.add_argument('--description', required=True, help='Skill描述')
    create_parser.add_argument('--template', help='模板名称')
    
    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='验证Skill')
    validate_parser.add_argument('--name', help='Skill名称（不指定则验证所有）')
    validate_parser.add_argument('--all', action='store_true', help='验证所有Skills')
    validate_parser.add_argument('--json', action='store_true', help='JSON格式输出')
    
    # deploy 命令
    deploy_parser = subparsers.add_parser('deploy', help='部署Skill')
    deploy_parser.add_argument('--name', required=True, help='Skill名称')
    deploy_parser.add_argument('--target', required=True, help='目标目录')
    
    # info 命令
    info_parser = subparsers.add_parser('info', help='显示Skill详细信息')
    info_parser.add_argument('--name', required=True, help='Skill名称')
    
    # report 命令
    report_parser = subparsers.add_parser('report', help='生成项目报告')
    report_parser.add_argument('--output', '-o', help='输出文件路径')
    
    # 全局选项
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 创建管理器
    manager = SkillManager(verbose=args.verbose)
    
    if args.command == 'list':
        # 列出Skills
        skills = manager.list_skills(detailed=args.detailed)
        
        if args.detailed:
            for skill in skills:
                print(f"{'='*60}")
                print(f"名称: {skill['name']}")
                print(f"描述: {skill['description']}")
                print(f"工具: {', '.join(skill['tools'])}")
                print(f"路径: {skill['path']}")
                print(f"scripts: {'✅' if skill['has_scripts'] else '❌'}")
                print(f"examples: {'✅' if skill['has_examples'] else '❌'}")
                print(f"大小: {manager._format_size(skill['file_size'])}")
        else:
            print(f"{'名称':<30} {'描述':<40} {'scripts':<8} {'examples'}")
            print("-" * 80)
            for skill in skills:
                print(f"{skill['name']:<30} {skill['description']:<40} "
                      f"{'✅' if skill['has_scripts'] else '❌':<8} "
                      f"{'✅' if skill['has_examples'] else '❌'}")
    
    elif args.command == 'create':
        # 创建Skill
        result = manager.create_skill(args.name, args.description, args.template)
        print(f"{'✅' if result else '❌'} {result}")
        if result.errors:
            for error in result.errors:
                print(f"  - {error}")
    
    elif args.command == 'validate':
        # 验证Skill
        if args.name and not args.all:
            result = manager.validate_skill(args.name)
            results = {args.name: result}
        else:
            results = manager.validate_all_skills()
        
        if args.json:
            import json
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
            for name, result in results.items():
                status = "✅" if result.is_valid else "❌"
                if result.is_valid and result.errors:
                    status = "⚠️"
                print(f"{status} {name}: {result}")
    
    elif args.command == 'deploy':
        # 部署Skill
        target_dir = Path(args.target)
        result = manager.deploy_skill(args.name, target_dir)
        print(f"{'✅' if result else '❌'} {result}")
        if result.errors:
            for error in result.errors:
                print(f"  - {error}")
    
    elif args.command == 'info':
        # 显示Skill信息
        info = manager.get_skill_info(args.name)
        if info:
            print(f"{'='*60}")
            print(f"名称: {info['name']}")
            print(f"描述: {info['description']}")
            print(f"工具: {', '.join(info['tools'])}")
            print(f"路径: {info['path']}")
            print(f"scripts: {'✅' if info['has_scripts'] else '❌'}")
            print(f"examples: {'✅' if info['has_examples'] else '❌'}")
            print(f"大小: {manager._format_size(info['file_size'])}")
            print(f"{'='*60}")
            print("内容预览:")
            print(info['content_preview'])
        else:
            print(f"❌ Skill不存在: {args.name}")
    
    elif args.command == 'report':
        # 生成报告
        output_file = Path(args.output) if args.output else None
        report = manager.generate_project_report(output_file)
        if not args.output:
            print(report)
        else:
            print(f"✅ 报告已生成: {args.output}")


if __name__ == "__main__":
    import logging
    main()