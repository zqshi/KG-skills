#!/usr/bin/env python3
"""
结构生成器
生成Skill的目录结构和文件内容
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from models import StructureConfig, SkillSpec, TemplateConfig


class StructureGenerator:
    """结构生成器类"""
    
    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = Path(base_path)
    
    def generate_structure(self, spec: SkillSpec, template: TemplateConfig) -> StructureConfig:
        """基于规格和模板生成结构配置"""
        directories = []
        scripts = template.scripts
        templates = []
        examples = template.examples
        
        # 添加脚本目录
        if spec.include_scripts and scripts:
            directories.append('scripts')
        
        # 添加模板目录
        if spec.include_templates:
            directories.append('templates')
            templates = [f"{spec.skill_type}_template"]
        
        # 添加示例目录
        if examples:
            directories.append('examples')
        
        # 添加工具目录（中等复杂度以上）
        if spec.complexity in ['medium', 'complex']:
            directories.append('utils')
        
        return StructureConfig(
            name=spec.name,
            description=spec.description,
            skill_type=spec.skill_type,
            complexity=spec.complexity,
            directories=directories,
            scripts=scripts,
            templates=templates,
            examples=examples
        )
    
    def create_structure(self, config: StructureConfig) -> bool:
        """创建完整的Skill结构"""
        skill_dir = self.base_path / config.name
        
        try:
            # 处理已存在的目录
            if skill_dir.exists():
                return False
            
            # 创建主目录
            skill_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建必需文件
            self._create_required_files(skill_dir, config)
            
            # 创建目录结构
            self._create_directories(skill_dir, config.directories)
            
            # 创建脚本文件
            if config.scripts:
                self._create_script_files(skill_dir, config.scripts, config.skill_type)
            
            # 创建模板文件
            if config.templates:
                self._create_template_files(skill_dir, config.templates, config.skill_type)
            
            # 创建示例文件
            if config.examples:
                self._create_example_files(skill_dir, config.examples, config.skill_type)
            
            # 创建工具文件
            if 'utils' in config.directories:
                self._create_utils_files(skill_dir)
            
            return True
            
        except Exception as e:
            # 清理已创建的目录
            if skill_dir.exists():
                shutil.rmtree(skill_dir)
            raise e
    
    def _create_required_files(self, skill_dir: Path, config: StructureConfig):
        """创建必需文件"""
        # SKILL.md
        skill_content = self._generate_skill_md(config)
        (skill_dir / "SKILL.md").write_text(skill_content, encoding='utf-8')
        
        # README.md
        readme_content = self._generate_readme_md(config)
        (skill_dir / "README.md").write_text(readme_content, encoding='utf-8')
    
    def _create_directories(self, skill_dir: Path, directories: list):
        """创建目录结构"""
        for dir_name in directories:
            dir_path = skill_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            
            # 添加.gitkeep
            (dir_path / ".gitkeep").write_text("", encoding='utf-8')
    
    def _create_script_files(self, skill_dir: Path, scripts: list, skill_type: str):
        """创建脚本文件"""
        scripts_dir = skill_dir / "scripts"
        
        for script_name in scripts:
            script_path = scripts_dir / script_name
            script_content = self._generate_script_template(script_name, skill_type)
            script_path.write_text(script_content, encoding='utf-8')
            script_path.chmod(0o755)
    
    def _create_template_files(self, skill_dir: Path, templates: list, skill_type: str):
        """创建模板文件"""
        templates_dir = skill_dir / "templates"
        
        for template_name in templates:
            template_dir = templates_dir / template_name
            template_dir.mkdir(parents=True, exist_ok=True)
            
            template_content = self._generate_template_skill_md(template_name, skill_type)
            (template_dir / "SKILL.md").write_text(template_content, encoding='utf-8')
    
    def _create_example_files(self, skill_dir: Path, examples: list, skill_type: str):
        """创建示例文件"""
        examples_dir = skill_dir / "examples"
        
        for example_name in examples:
            example_dir = examples_dir / example_name
            example_dir.mkdir(parents=True, exist_ok=True)
            
            example_content = self._generate_example_readme(example_name, skill_type)
            (example_dir / "README.md").write_text(example_content, encoding='utf-8')
            (example_dir / ".gitkeep").write_text("", encoding='utf-8')
    
    def _create_utils_files(self, skill_dir: Path):
        """创建工具文件"""
        utils_dir = skill_dir / "utils"
        
        # __init__.py
        (utils_dir / "__init__.py").write_text("# Utility functions\n", encoding='utf-8')
        
        # 常用工具文件
        common_utils = ["file_helpers.py", "validation_rules.py", "logging_utils.py"]
        
        for util_file in common_utils:
            util_content = self._generate_util_template(util_file)
            (utils_dir / util_file).write_text(util_content, encoding='utf-8')
    
    def _generate_skill_md(self, config: StructureConfig) -> str:
        """生成SKILL.md内容"""
        return f"""---
name: {config.name}
description: {config.description}
---

# {config.name.replace('_', ' ').title()}

## 🎯 概述

{config.description}

## 🚀 快速开始

### 使用方法

```
使用 {config.name} 执行相关操作
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

**{config.name.replace('_', ' ').title()}** - 让工作更高效！ 🚀
"""
    
    def _generate_readme_md(self, config: StructureConfig) -> str:
        """生成README.md内容"""
        return f"""# {config.name.replace('_', ' ').title()}

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
{config.name}/
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

### 技术支持

如果遇到问题，请检查：
1. Skill配置是否正确
2. 输入格式是否符合要求
3. 依赖库是否已安装

## 📄 许可证

[许可证信息]
"""
    
    def _generate_script_template(self, script_name: str, skill_type: str) -> str:
        """生成脚本模板"""
        return f"""#!/usr/bin/env python3
\"\"\"
{script_name} - [功能描述]
\"\"\"

import os
import sys
from pathlib import Path


def main():
    \"\"\"主函数\"\"\"
    print(f"🚀 {{script_name}} 开始执行...")
    
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
        """生成工具模板"""
        if util_file == "file_helpers.py":
            return '''"""文件操作工具函数"""

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
'''
        elif util_file == "validation_rules.py":
            return '''"""验证规则工具函数"""

import re
from typing import Any


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_skill_name(name: str) -> bool:
    """验证Skill名称格式"""
    pattern = r'^[a-z][a-z0-9_]*(_[a-z0-9]+)*$'
    return bool(re.match(pattern, name))
'''
        else:
            return '''"""通用工具函数"""

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
'''