#!/usr/bin/env python3
"""
Skill优化器
基于结构分析结果，自动优化Skill的各个方面
"""

import os
import sys
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from self_optimization.skill_analyzer import SkillStructureAnalysis
from models import SkillSpec


@dataclass
class OptimizationResult:
    """优化结果"""
    skill_name: str
    optimization_type: str  # structure, documentation, script, input, output, workflow
    success: bool
    changes_made: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'skill_name': self.skill_name,
            'optimization_type': self.optimization_type,
            'success': self.success,
            'changes_made': self.changes_made,
            'warnings': self.warnings,
            'errors': self.errors
        }


class SkillOptimizer:
    """Skill优化器"""
    
    def __init__(self, backup_dir: Optional[Path] = None):
        self.backup_dir = backup_dir or Path('.claude/skills/skill_manager/backups')
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def optimize_skill(self, analysis: SkillStructureAnalysis, 
                      optimization_types: Optional[List[str]] = None) -> List[OptimizationResult]:
        """优化Skill"""
        if optimization_types is None:
            optimization_types = ['structure', 'documentation', 'script', 'input', 'output', 'workflow']
        
        results = []
        
        # 备份原始文件
        self._backup_skill(analysis.skill_path)
        
        for opt_type in optimization_types:
            try:
                if opt_type == 'structure':
                    result = self._optimize_structure(analysis)
                elif opt_type == 'documentation':
                    result = self._optimize_documentation(analysis)
                elif opt_type == 'script':
                    result = self._optimize_scripts(analysis)
                elif opt_type == 'input':
                    result = self._optimize_inputs(analysis)
                elif opt_type == 'output':
                    result = self._optimize_outputs(analysis)
                elif opt_type == 'workflow':
                    result = self._optimize_workflows(analysis)
                else:
                    continue
                
                results.append(result)
                
            except Exception as e:
                results.append(OptimizationResult(
                    skill_name=analysis.skill_name,
                    optimization_type=opt_type,
                    success=False,
                    errors=[str(e)]
                ))
        
        return results
    
    def _backup_skill(self, skill_path: Path):
        """备份Skill"""
        backup_path = self.backup_dir / f"{skill_path.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            import shutil
            shutil.copytree(skill_path, backup_path)
            print(f"备份Skill到: {backup_path}")
        except Exception as e:
            print(f"备份失败: {e}")
    
    def _optimize_structure(self, analysis: SkillStructureAnalysis) -> OptimizationResult:
        """优化文件结构"""
        result = OptimizationResult(
            skill_name=analysis.skill_name,
            optimization_type='structure',
            success=True
        )
        
        skill_path = analysis.skill_path
        
        # 创建缺失的目录
        if not analysis.has_examples:
            examples_dir = skill_path / 'examples'
            examples_dir.mkdir(exist_ok=True)
            (examples_dir / 'basic_usage').mkdir(exist_ok=True)
            result.changes_made.append("创建examples/basic_usage目录")
        
        if not analysis.has_utils and analysis.has_scripts:
            utils_dir = skill_path / 'utils'
            utils_dir.mkdir(exist_ok=True)
            (utils_dir / '__init__.py').touch()
            result.changes_made.append("创建utils目录")
        
        # 创建README.md（如果不存在）
        if not analysis.has_readme:
            self._create_readme(skill_path)
            result.changes_made.append("创建README.md")
        
        return result
    
    def _create_readme(self, skill_path: Path):
        """创建README.md"""
        skill_name = skill_path.name
        
        readme_content = f"""# {skill_name}

## 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 基本使用
```bash
# 使用{skill_name} Skill
python scripts/main.py --help
```

### 示例
```bash
# 示例1: 基本用法
python scripts/main.py [参数]

# 示例2: 高级用法
python scripts/main.py --advanced [参数]
```

## 项目结构
```
{skill_name}/
├── SKILL.md          # Skill定义文件
├── README.md         # 说明文档
├── scripts/          # Python脚本
├── examples/         # 使用示例
└── utils/           # 工具函数
```

## 配置
参考 `config/` 目录下的配置文件。

## 支持
如有问题，请查看SKILL.md中的详细文档。
"""
        
        with open(skill_path / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def _optimize_documentation(self, analysis: SkillStructureAnalysis) -> OptimizationResult:
        """优化文档"""
        result = OptimizationResult(
            skill_name=analysis.skill_name,
            optimization_type='documentation',
            success=True
        )
        
        skill_path = analysis.skill_path
        skill_md_path = skill_path / 'SKILL.md'
        
        if not skill_md_path.exists():
            result.success = False
            result.errors.append("SKILL.md不存在")
            return result
        
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 确保元数据部分完整
            content = self._ensure_metadata(content, analysis)
            
            # 确保各个章节存在
            content = self._ensure_sections(content)
            
            # 更新文件
            with open(skill_md_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            result.changes_made.append("优化文档结构")
            
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
        
        return result
    
    def _ensure_metadata(self, content: str, analysis: SkillStructureAnalysis) -> str:
        """确保元数据完整"""
        metadata_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        metadata_match = re.match(metadata_pattern, content, re.S)
        
        if metadata_match:
            try:
                metadata = yaml.safe_load(metadata_match.group(1))
            except:
                metadata = {}
        else:
            metadata = {}
        
        # 确保基本字段
        if 'name' not in metadata:
            metadata['name'] = analysis.skill_name
        
        if 'description' not in metadata:
            metadata['description'] = f"{analysis.skill_name} Skill"
        
        if 'tools' not in metadata:
            metadata['tools'] = ['Read', 'Write']
        
        # 重新构建元数据部分
        metadata_yaml = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)
        new_metadata = f"---\n{metadata_yaml}---\n"
        
        if metadata_match:
            return re.sub(metadata_pattern, new_metadata, content, count=1)
        else:
            return new_metadata + content
    
    def _ensure_sections(self, content: str) -> str:
        """确保各个章节存在"""
        sections = [
            ('## 🎯 核心功能', '## 🎯 核心功能\n\n描述Skill的核心功能和用途。\n'),
            ('## 📋 工作流SOP', '## 📋 工作流SOP\n\n```\n1. 接收输入\n2. 处理数据\n3. 生成结果\n4. 返回输出\n```\n'),
            ('## 🚀 快速开始', '## 🚀 快速开始\n\n### 基本使用\n```\n使用 {skill_name} 处理数据\n```\n'),
            ('## 📋 输入规范', '## 📋 输入规范\n\n### 必需输入\n```json\n{\n  "input_data": "输入数据"\n}\n```\n'),
            ('## 📤 输出内容', '## 📤 输出内容\n\n### 标准输出\n```json\n{\n  "result": "处理结果"\n}\n```\n'),
            ('## 🎪 使用示例', '## 🎪 使用示例\n\n### 示例1: 基本用法\n```\n使用 {skill_name} 处理示例数据\n```\n'),
            ('## 📊 质量指标', '## 📊 质量指标\n\n- **准确率**: ≥90%（目标值）\n- **处理效率**: ≤5秒/条（目标值）\n')
        ]
        
        for header, default_content in sections:
            if header not in content:
                content += f"\n{default_content}\n"
        
        return content
    
    def _optimize_scripts(self, analysis: SkillStructureAnalysis) -> OptimizationResult:
        """优化脚本"""
        result = OptimizationResult(
            skill_name=analysis.skill_name,
            optimization_type='script',
            success=True
        )
        
        if not analysis.has_scripts:
            result.success = False
            result.errors.append("没有脚本文件")
            return result
        
        scripts_dir = analysis.skill_path / 'scripts'
        
        try:
            for script_file in scripts_dir.glob('*.py'):
                if script_file.name == '__init__.py':
                    continue
                
                with open(script_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 优化导入语句
                content = self._optimize_imports(content)
                
                # 添加错误处理（如果没有）
                content = self._add_error_handling(content)
                
                # 添加日志记录（如果没有）
                content = self._add_logging(content)
                
                # 添加文档字符串（如果没有）
                content = self._add_docstrings(content)
                
                # 保存优化后的脚本
                with open(script_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                result.changes_made.append(f"优化脚本: {script_file.name}")
            
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
        
        return result
    
    def _optimize_imports(self, content: str) -> str:
        """优化导入语句"""
        # 确保标准导入在文件开头
        if 'import sys' not in content and 'sys.' in content:
            content = 'import sys\n' + content
        
        if 'import os' not in content and 'os.' in content:
            content = 'import os\n' + content
        
        if 'import json' not in content and ('json.' in content or 'json.loads' in content):
            content = 'import json\n' + content
        
        return content
    
    def _add_error_handling(self, content: str) -> str:
        """添加错误处理"""
        # 简单的错误处理添加逻辑
        if 'try:' not in content and 'def main' in content:
            # 找到main函数并添加try-except
            main_pattern = r'(def main\(.*?\):.*?\n)(.*?)(?=\nif __name__|\Z)'
            def add_try_except(match):
                indent = '    '
                return f"{match.group(1)}{indent}try:\n{indent}{match.group(2).replace(chr(10), chr(10)+indent*2)}\n{indent}except Exception as e:\n{indent}    print(f'执行出错: {{e}}')\n{indent}    return False\n"
            
            content = re.sub(main_pattern, add_try_except, content, flags=re.S)
        
        return content
    
    def _add_logging(self, content: str) -> str:
        """添加日志记录"""
        if 'import logging' not in content:
            # 在文件开头添加logging导入
            content = 'import logging\n\n' + content
            
            # 在main函数中添加基本配置
            if 'def main' in content:
                content = content.replace(
                    'def main',
                    'logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")\n\ndef main',
                    1
                )
        
        return content
    
    def _add_docstrings(self, content: str) -> str:
        """添加文档字符串"""
        # 为没有文档字符串的函数添加简单docstring
        func_pattern = r'(def\s+\w+\s*\([^)]*\):\s*\n)(?!\s*""")'
        
        def add_docstring(match):
            return f'{match.group(1)}    """处理函数"""\n'
        
        content = re.sub(func_pattern, add_docstring, content)
        return content
    
    def _optimize_inputs(self, analysis: SkillStructureAnalysis) -> OptimizationResult:
        """优化输入规范"""
        result = OptimizationResult(
            skill_name=analysis.skill_name,
            optimization_type='input',
            success=True
        )
        
        skill_path = analysis.skill_path
        skill_md_path = skill_path / 'SKILL.md'
        
        if not skill_md_path.exists():
            result.success = False
            result.errors.append("SKILL.md不存在")
            return result
        
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 确保输入规范章节存在且完整
            if '## 📋 输入规范' not in content:
                input_section = '''## 📋 输入规范

### 必需输入
```json
{
  "input_data": "输入数据（根据实际Skill需求定义）"
}
```

### 可选输入
```json
{
  "config_file": "配置文件路径（可选）",
  "output_format": "输出格式（可选，默认：json）"
}
```
'''
                content += f"\n{input_section}\n"
                result.changes_made.append("添加输入规范章节")
            
            # 保存更新
            with open(skill_md_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
        
        return result
    
    def _optimize_outputs(self, analysis: SkillStructureAnalysis) -> OptimizationResult:
        """优化输出格式"""
        result = OptimizationResult(
            skill_name=analysis.skill_name,
            optimization_type='output',
            success=True
        )
        
        skill_path = analysis.skill_path
        skill_md_path = skill_path / 'SKILL.md'
        
        if not skill_md_path.exists():
            result.success = False
            result.errors.append("SKILL.md不存在")
            return result
        
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 确保输出内容章节存在且完整
            if '## 📤 输出内容' not in content:
                output_section = '''## 📤 输出内容

### 标准输出
```json
{
  "status": "success",
  "result": "处理结果",
  "metadata": {
    "processing_time": 1.5,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### 错误输出
```json
{
  "status": "error",
  "error_type": "processing_error",
  "message": "处理过程中发生错误",
  "details": "详细错误信息"
}
```
'''
                content += f"\n{output_section}\n"
                result.changes_made.append("添加输出格式章节")
            
            # 保存更新
            with open(skill_md_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
        
        return result
    
    def _optimize_workflows(self, analysis: SkillStructureAnalysis) -> OptimizationResult:
        """优化工作流"""
        result = OptimizationResult(
            skill_name=analysis.skill_name,
            optimization_type='workflow',
            success=True
        )
        
        skill_path = analysis.skill_path
        skill_md_path = skill_path / 'SKILL.md'
        
        if not skill_md_path.exists():
            result.success = False
            result.errors.append("SKILL.md不存在")
            return result
        
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 确保工作流SOP章节存在且详细
            if '## 📋 工作流SOP' not in content:
                workflow_section = '''## 📋 工作流SOP

```
1. 接收输入参数
2. 验证输入数据完整性
3. 执行核心处理逻辑
4. 生成处理结果
5. 格式化输出
6. 记录执行日志
```

### 详细流程说明

**步骤1：接收输入参数**
- 验证必需参数是否存在
- 解析可选参数
- 加载配置文件（如需要）

**步骤2：验证输入数据完整性**
- 检查数据格式
- 验证数据有效性
- 处理缺失值

**步骤3：执行核心处理逻辑**
- 调用主处理函数
- 执行具体业务逻辑
- 处理异常情况

**步骤4：生成处理结果**
- 整理处理结果
- 格式化输出数据
- 准备元数据

**步骤5：格式化输出**
- 按指定格式生成输出
- 包含状态信息和结果
- 添加时间戳等元数据

**步骤6：记录执行日志**
- 记录执行参数
- 记录处理结果
- 记录异常信息（如有）
'''
                content += f"\n{workflow_section}\n"
                result.changes_made.append("添加详细工作流SOP")
            
            # 保存更新
            with open(skill_md_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
        
        return result


# 全局优化器实例
skill_optimizer = SkillOptimizer()


def get_skill_optimizer() -> SkillOptimizer:
    """获取Skill优化器实例"""
    return skill_optimizer


if __name__ == '__main__':
    # 测试优化器
    from skill_analyzer import get_skill_analyzer
    
    analyzer = get_skill_analyzer()
    optimizer = get_skill_optimizer()
    
    # 分析所有Skill
    analysis_results = analyzer.analyze_all_skills()
    
    # 优化需要改进的Skill
    for skill_name, analysis in analysis_results.items():
        if analysis.overall_score < 70:
            print(f"优化Skill: {skill_name} (评分: {analysis.overall_score:.1f})")
            results = optimizer.optimize_skill(analysis)
            
            for result in results:
                print(f"  {result.optimization_type}: {'成功' if result.success else '失败'}")
                if result.changes_made:
                    for change in result.changes_made:
                        print(f"    - {change}")