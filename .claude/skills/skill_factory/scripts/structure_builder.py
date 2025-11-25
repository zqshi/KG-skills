#!/usr/bin/env python3
"""
目录结构构建器脚本
自动创建Skill的标准文件目录结构
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class SkillStructure:
    """Skill结构定义"""
    name: str
    description: str
    skill_type: str
    complexity: str
    directories: List[str]
    scripts: List[str]
    templates: List[str]
    examples: List[str]


class StructureBuilder:
    """结构构建器类"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def create_skill_structure(self, structure: SkillStructure) -> bool:
        """创建完整的Skill结构"""
        print(f"🏗️ 开始创建Skill结构: {structure.name}")

        # 创建Skill主目录
        skill_dir = self.base_path / structure.name

        try:
            # 如果目录已存在，询问是否覆盖
            if skill_dir.exists():
                print(f"⚠️  目录已存在: {skill_dir}")
                response = input("是否覆盖？(y/N): ").strip().lower()
                if response != 'y':
                    print("❌ 操作取消")
                    return False
                shutil.rmtree(skill_dir)

            skill_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ 创建主目录: {skill_dir}")

            # 创建必需文件
            self._create_required_files(skill_dir, structure)

            # 创建目录结构
            self._create_directories(skill_dir, structure.directories)

            # 创建脚本文件（如果有）
            if structure.scripts:
                self._create_script_files(skill_dir, structure.scripts)

            # 创建模板文件（如果有）
            if structure.templates:
                self._create_template_files(skill_dir, structure.templates, structure.skill_type)

            # 创建示例文件（如果有）
            if structure.examples:
                self._create_example_files(skill_dir, structure.examples, structure.skill_type)

            # 创建工具函数（如果需要）
            if 'utils' in structure.directories:
                self._create_utils_files(skill_dir)

            print(f"\n🎉 Skill结构创建完成: {skill_dir}")
            self._print_structure_summary(skill_dir)
            return True

        except Exception as e:
            print(f"❌ 创建结构失败: {e}")
            return False

    def _create_required_files(self, skill_dir: Path, structure: SkillStructure):
        """创建必需文件"""
        # 创建SKILL.md模板
        skill_md_content = self._generate_skill_md(structure)
        (skill_dir / "SKILL.md").write_text(skill_md_content, encoding='utf-8')
        print("✅ 创建 SKILL.md")

        # 创建README.md模板
        readme_content = self._generate_readme_md(structure)
        (skill_dir / "README.md").write_text(readme_content, encoding='utf-8')
        print("✅ 创建 README.md")

    def _create_directories(self, skill_dir: Path, directories: List[str]):
        """创建目录结构"""
        for dir_name in directories:
            dir_path = skill_dir / dir_name
            dir_path.mkdir(exist_ok=True)

            # 在每个目录中创建.gitkeep文件
            (dir_path / ".gitkeep").write_text("", encoding='utf-8')
            print(f"✅ 创建目录: {dir_name}")

    def _create_script_files(self, skill_dir: Path, scripts: List[str]):
        """创建脚本文件模板"""
        scripts_dir = skill_dir / "scripts"

        for script_name in scripts:
            script_path = scripts_dir / script_name
            script_content = self._generate_script_template(script_name)
            script_path.write_text(script_content, encoding='utf-8')

            # 设置执行权限
            script_path.chmod(0o755)
            print(f"✅ 创建脚本: {script_name}")

    def _create_template_files(self, skill_dir: Path, templates: List[str], skill_type: str):
        """创建模板文件"""
        templates_dir = skill_dir / "templates"

        for template_name in templates:
            template_dir = templates_dir / template_name
            template_dir.mkdir(parents=True, exist_ok=True)

            # 创建模板SKILL.md
            template_content = self._generate_template_skill_md(template_name, skill_type)
            (template_dir / "SKILL.md").write_text(template_content, encoding='utf-8')

            print(f"✅ 创建模板: {template_name}")

    def _create_example_files(self, skill_dir: Path, examples: List[str], skill_type: str):
        """创建示例文件"""
        examples_dir = skill_dir / "examples"

        for example_name in examples:
            example_dir = examples_dir / example_name
            example_dir.mkdir(parents=True, exist_ok=True)

            # 创建示例说明文件
            example_content = self._generate_example_readme(example_name, skill_type)
            (example_dir / "README.md").write_text(example_content, encoding='utf-8')

            # 创建.gitkeep
            (example_dir / ".gitkeep").write_text("", encoding='utf-8')
            print(f"✅ 创建示例: {example_name}")

    def _create_utils_files(self, skill_dir: Path):
        """创建工具函数文件"""
        utils_dir = skill_dir / "utils"

        # 创建__init__.py
        (utils_dir / "__init__.py").write_text("# Utility functions\n", encoding='utf-8')

        # 创建常用工具文件
        common_utils = ["file_helpers.py", "validation_rules.py", "logging_utils.py"]

        for util_file in common_utils:
            util_content = self._generate_util_template(util_file)
            (utils_dir / util_file).write_text(util_content, encoding='utf-8')
            print(f"✅ 创建工具: {util_file}")

    def _generate_skill_md(self, structure: SkillStructure) -> str:
        """生成SKILL.md模板内容"""
        return f"""---
name: {structure.name}
description: {structure.description}
---

# {structure.name.replace('_', ' ').title()}

## 🎯 概述

{structure.description}

## 🚀 快速开始

### 使用方法

```
使用 {structure.name} 执行相关操作
```

### 输入格式

- **必需参数**: [描述]
- **可选参数**: [描述]

### 输出内容

[描述输出内容和格式]

## 📋 功能特性

- [功能点1]
- [功能点2]
- [功能点3]

## 🎪 使用示例

### 示例1: 基础使用

```
[示例命令]
```

### 示例2: 高级使用

```
[示例命令]
```

## 🔧 配置选项

[配置参数说明]

## ⚠️ 注意事项

[使用注意事项]

---

**{structure.name.replace('_', ' ').title()}** - 让工作更高效！ 🚀
"""

    def _generate_readme_md(self, structure: SkillStructure) -> str:
        """生成README.md模板内容"""
        return f"""# {structure.name.replace('_', ' ').title()}

## 📖 使用说明

### 安装

本Skill是Claude Agent Skill，无需额外安装。

### 使用方法

1. 确保Skill已正确配置
2. 使用标准命令格式调用
3. 按照提示提供必要的输入

### 配置

[配置说明]

## 🏗️ 项目结构

```
{structure.name}/
├── SKILL.md              # 主技能文件
├── README.md             # 使用说明
├── scripts/              # Python脚本
├── templates/            # 模板文件
├── examples/             # 使用示例
└── utils/                # 工具函数
```

## 🐛 故障排除

### 常见问题

**Q: [问题描述]**
A: [解决方案]

**Q: [问题描述]**
A: [解决方案]

### 技术支持

如果遇到问题，请检查：
1. Skill配置是否正确
2. 输入格式是否符合要求
3. 依赖库是否已安装

## 📄 许可证

[许可证信息]
"""

    def _generate_script_template(self, script_name: str) -> str:
        """生成脚本文件模板"""
        return f"""#!/usr/bin/env python3
"""
{script_name} - [功能描述]
"""

import os
import sys
from pathlib import Path


def main():
    """主函数"""
    print("🚀 {script_name} 开始执行...")

    # 主要逻辑
    try:
        # TODO: 实现主要功能
        pass
    except Exception as e:
        print(f"❌ 执行出错: {{e}}")
        sys.exit(1)

    print("✅ 执行完成")


if __name__ == "__main__":
    main()
"""

    def _generate_template_skill_md(self, template_name: str, skill_type: str) -> str:
        """生成模板SKILL.md"""
        return f"""---
name: {template_name}
description: {skill_type}类型Skill模板
---

# {template_name.replace('_', ' ').title()} 模板

这是{skill_type}类型Skill的标准化模板。

## 使用说明

1. 复制此模板
2. 修改相关内容
3. 测试功能

## 模板特性

- 标准化结构
- 最佳实践示例
- 可扩展设计
"""

    def _generate_example_readme(self, example_name: str, skill_type: str) -> str:
        """生成示例README"""
        return f"""# {example_name.replace('_', ' ').title()} 示例

## 示例描述

这个示例展示了如何使用{skill_type}类型的Skill。

## 使用方法

1. [步骤1]
2. [步骤2]
3. [步骤3]

## 预期结果

[描述预期输出]
"""

    def _generate_util_template(self, util_file: str) -> str:
        """生成工具函数模板"""
        if util_file == "file_helpers.py":
            return """"""文件操作工具函数"""

import os
import shutil
from pathlib import Path
from typing import List


def ensure_dir_exists(path: str) -> bool:
    """确保目录存在"""
    Path(path).mkdir(parents=True, exist_ok=True)
    return True


def safe_delete(path: str) -> bool:
    """安全删除文件或目录"""
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        return True
    except Exception:
        return False
"""
        elif util_file == "validation_rules.py":
            return """"""验证规则工具函数"""

import re
from typing import Any


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_skill_name(name: str) -> bool:
    """验证Skill名称格式"""
    pattern = r'^[a-z][a-z0-9_]*(_[a-z0-9]+)*$'
    return bool(re.match(pattern, name))
"""
        else:
            return """"""通用工具函数"""

import logging
from datetime import datetime


def setup_logging(level=logging.INFO):
    """设置日志配置"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_timestamp() -> str:
    """获取时间戳"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')
"""

    def _print_structure_summary(self, skill_dir: Path):
        """打印结构摘要"""
        print("\n📊 创建的结构摘要:")
        print("="*40)

        for root, dirs, files in os.walk(skill_dir):
            level = root.replace(str(skill_dir), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")

            sub_indent = ' ' * 2 * (level + 1)
            for file in files:
                if file != ".gitkeep":
                    print(f"{sub_indent}{file}")


def main():
    """主函数 - 示例用法"""
    # 示例结构定义
    structure = SkillStructure(
        name="example_skill",
        description="示例Skill功能描述",
        skill_type="data",
        complexity="medium",
        directories=["scripts", "templates", "examples", "utils"],
        scripts=["main_processor.py", "helper_tool.py"],
        templates=["data_template"],
        examples=["basic_usage", "advanced_usage"]
    )

    builder = StructureBuilder(".claude/skills")
    success = builder.create_skill_structure(structure)

    if success:
        print("\n🎊 Skill结构创建成功！")
    else:
        print("\n💥 Skill结构创建失败")


if __name__ == "__main__":
    main()