#!/usr/bin/env python3
"""
Skill结构分析器
分析Skill的文件结构、代码质量、文档完整性等
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class SkillStructureAnalysis:
    """Skill结构分析结果"""
    skill_name: str
    skill_path: Path

    # 文件结构检查
    has_skill_md: bool = False
    has_readme: bool = False
    has_scripts: bool = False
    has_examples: bool = False
    has_utils: bool = False
    has_config: bool = False
    has_templates: bool = False

    # 文档质量
    has_metadata: bool = False
    has_description: bool = False
    has_input_spec: bool = False
    has_output_spec: bool = False
    has_workflow: bool = False
    has_examples_section: bool = False

    # 脚本质量
    script_count: int = 0
    has_main_script: bool = False
    has_error_handling: bool = False
    has_logging: bool = False
    has_docstrings: bool = False

    # 质量评分
    structure_score: float = 0.0
    documentation_score: float = 0.0
    code_quality_score: float = 0.0
    overall_score: float = 0.0

    # 问题和建议
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    def calculate_scores(self):
        """计算各项评分"""
        # 结构评分 (满分100)
        structure_items = {
            'has_skill_md': 30,
            'has_readme': 10,
            'has_scripts': 20,
            'has_examples': 15,
            'has_utils': 10,
            'has_config': 10,
            'has_templates': 5
        }

        self.structure_score = sum(
            score for item, score in structure_items.items()
            if getattr(self, item, False)
        )

        # 文档评分 (满分100)
        doc_items = {
            'has_metadata': 15,
            'has_description': 20,
            'has_input_spec': 20,
            'has_output_spec': 20,
            'has_workflow': 15,
            'has_examples_section': 10
        }

        self.documentation_score = sum(
            score for item, score in doc_items.items()
            if getattr(self, item, False)
        )

        # 代码质量评分 (满分100)
        code_items = {
            'has_main_script': 30,
            'has_error_handling': 25,
            'has_logging': 20,
            'has_docstrings': 25
        }

        self.code_quality_score = sum(
            score for item, score in code_items.items()
            if getattr(self, item, False)
        )

        # 综合评分 (加权平均)
        self.overall_score = (
            self.structure_score * 0.3 +
            self.documentation_score * 0.4 +
            self.code_quality_score * 0.3
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'skill_name': self.skill_name,
            'skill_path': str(self.skill_path),
            'structure': {
                'has_skill_md': self.has_skill_md,
                'has_readme': self.has_readme,
                'has_scripts': self.has_scripts,
                'has_examples': self.has_examples,
                'has_utils': self.has_utils,
                'has_config': self.has_config,
                'has_templates': self.has_templates
            },
            'documentation': {
                'has_metadata': self.has_metadata,
                'has_description': self.has_description,
                'has_input_spec': self.has_input_spec,
                'has_output_spec': self.has_output_spec,
                'has_workflow': self.has_workflow,
                'has_examples_section': self.has_examples_section
            },
            'code_quality': {
                'script_count': self.script_count,
                'has_main_script': self.has_main_script,
                'has_error_handling': self.has_error_handling,
                'has_logging': self.has_logging,
                'has_docstrings': self.has_docstrings
            },
            'scores': {
                'structure_score': self.structure_score,
                'documentation_score': self.documentation_score,
                'code_quality_score': self.code_quality_score,
                'overall_score': self.overall_score
            },
            'issues': self.issues,
            'suggestions': self.suggestions
        }


class SkillStructureAnalyzer:
    """Skill结构分析器"""

    def __init__(self, skills_dir: Optional[Path] = None):
        if skills_dir is None:
            # 默认为 .claude/skills 目录
            skills_dir = Path.cwd() / '.claude' / 'skills'

        self.skills_dir = Path(skills_dir)

    def analyze_skill(self, skill_name: str) -> SkillStructureAnalysis:
        """分析单个Skill"""
        skill_path = self.skills_dir / skill_name

        if not skill_path.exists():
            raise ValueError(f"Skill不存在: {skill_name}")

        analysis = SkillStructureAnalysis(
            skill_name=skill_name,
            skill_path=skill_path
        )

        # 检查文件结构
        self._check_file_structure(skill_path, analysis)

        # 检查文档质量
        self._check_documentation(skill_path, analysis)

        # 检查脚本质量
        self._check_scripts(skill_path, analysis)

        # 生成问题和建议
        self._generate_issues_and_suggestions(analysis)

        # 计算评分
        analysis.calculate_scores()

        return analysis

    def analyze_all_skills(self) -> Dict[str, SkillStructureAnalysis]:
        """分析所有Skill"""
        if not self.skills_dir.exists():
            print(f"Skills目录不存在: {self.skills_dir}")
            return {}

        results = {}

        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            # 跳过隐藏目录和特殊目录
            if skill_dir.name.startswith('.') or skill_dir.name == '__pycache__':
                continue

            # 检查是否有SKILL.md文件
            if not (skill_dir / 'SKILL.md').exists():
                continue

            try:
                analysis = self.analyze_skill(skill_dir.name)
                results[skill_dir.name] = analysis
            except Exception as e:
                print(f"分析Skill失败 {skill_dir.name}: {e}")

        return results

    def _check_file_structure(self, skill_path: Path, analysis: SkillStructureAnalysis):
        """检查文件结构"""
        analysis.has_skill_md = (skill_path / 'SKILL.md').exists()
        analysis.has_readme = (skill_path / 'README.md').exists()
        analysis.has_scripts = (skill_path / 'scripts').exists() and (skill_path / 'scripts').is_dir()
        analysis.has_examples = (skill_path / 'examples').exists() and (skill_path / 'examples').is_dir()
        analysis.has_utils = (skill_path / 'utils').exists() and (skill_path / 'utils').is_dir()
        analysis.has_config = (skill_path / 'config').exists() and (skill_path / 'config').is_dir()
        analysis.has_templates = (skill_path / 'templates').exists() and (skill_path / 'templates').is_dir()

    def _check_documentation(self, skill_path: Path, analysis: SkillStructureAnalysis):
        """检查文档质量"""
        skill_md_path = skill_path / 'SKILL.md'

        if not skill_md_path.exists():
            return

        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查元数据
            analysis.has_metadata = bool(re.search(r'^---\s*\n.*?\n---\s*\n', content, re.S))

            # 检查描述
            analysis.has_description = bool(re.search(r'##.*?概述|##.*?描述|##.*?功能', content, re.I))

            # 检查输入规范
            analysis.has_input_spec = bool(re.search(r'##.*?输入.*?规范|##.*?Input', content, re.I))

            # 检查输出规范
            analysis.has_output_spec = bool(re.search(r'##.*?输出.*?内容|##.*?Output', content, re.I))

            # 检查工作流
            analysis.has_workflow = bool(re.search(r'##.*?工作流|##.*?Workflow|##.*?SOP', content, re.I))

            # 检查示例
            analysis.has_examples_section = bool(re.search(r'##.*?示例|##.*?Example', content, re.I))

        except Exception as e:
            print(f"读取SKILL.md失败: {e}")

    def _check_scripts(self, skill_path: Path, analysis: SkillStructureAnalysis):
        """检查脚本质量"""
        scripts_dir = skill_path / 'scripts'

        if not scripts_dir.exists():
            return

        # 统计脚本数量
        python_files = list(scripts_dir.glob('*.py'))
        analysis.script_count = len([f for f in python_files if f.name != '__init__.py'])

        # 检查main.py
        main_script = scripts_dir / 'main.py'
        analysis.has_main_script = main_script.exists()

        # 检查代码质量
        for script_file in python_files:
            if script_file.name == '__init__.py':
                continue

            try:
                with open(script_file, 'r', encoding='utf-8') as f:
                    code = f.read()

                # 检查错误处理
                if 'try:' in code and 'except' in code:
                    analysis.has_error_handling = True

                # 检查日志记录
                if 'import logging' in code or 'logging.' in code:
                    analysis.has_logging = True

                # 检查文档字符串
                if '"""' in code or "'''" in code:
                    analysis.has_docstrings = True

            except Exception as e:
                print(f"读取脚本失败 {script_file}: {e}")

    def _generate_issues_and_suggestions(self, analysis: SkillStructureAnalysis):
        """生成问题和建议"""
        # 结构问题
        if not analysis.has_skill_md:
            analysis.issues.append("缺少SKILL.md文件")
            analysis.suggestions.append("创建SKILL.md文件")

        if not analysis.has_readme:
            analysis.suggestions.append("建议添加README.md说明文档")

        if not analysis.has_scripts:
            analysis.suggestions.append("建议添加scripts目录和Python脚本")

        if not analysis.has_examples:
            analysis.suggestions.append("建议添加examples目录和使用示例")

        # 文档问题
        if not analysis.has_metadata:
            analysis.issues.append("SKILL.md缺少元数据部分")
            analysis.suggestions.append("在SKILL.md开头添加元数据(name, description, tools)")

        if not analysis.has_input_spec:
            analysis.issues.append("缺少输入规范说明")
            analysis.suggestions.append("添加输入规范章节，说明必需和可选参数")

        if not analysis.has_output_spec:
            analysis.issues.append("缺少输出格式说明")
            analysis.suggestions.append("添加输出内容章节，说明标准输出和错误输出格式")

        if not analysis.has_workflow:
            analysis.suggestions.append("建议添加工作流SOP章节，详细说明执行步骤")

        # 代码质量问题
        if analysis.has_scripts:
            if not analysis.has_main_script:
                analysis.suggestions.append("建议添加main.py主入口脚本")

            if not analysis.has_error_handling:
                analysis.issues.append("脚本缺少错误处理")
                analysis.suggestions.append("在脚本中添加try-except错误处理")

            if not analysis.has_logging:
                analysis.suggestions.append("建议添加日志记录功能")

            if not analysis.has_docstrings:
                analysis.suggestions.append("建议为函数添加文档字符串")

    def generate_analysis_report(self, results: Dict[str, SkillStructureAnalysis],
                                output_file: Optional[str] = None) -> Dict[str, Any]:
        """生成分析报告"""
        if not results:
            return {
                'generated_at': datetime.now().isoformat(),
                'total_skills': 0,
                'summary': {}
            }

        # 统计信息
        total_skills = len(results)
        avg_overall_score = sum(r.overall_score for r in results.values()) / total_skills

        # 分类统计
        excellent_skills = [name for name, r in results.items() if r.overall_score >= 80]
        good_skills = [name for name, r in results.items() if 60 <= r.overall_score < 80]
        needs_improvement = [name for name, r in results.items() if r.overall_score < 60]

        report = {
            'generated_at': datetime.now().isoformat(),
            'total_skills': total_skills,
            'summary': {
                'average_overall_score': round(avg_overall_score, 2),
                'excellent_count': len(excellent_skills),
                'good_count': len(good_skills),
                'needs_improvement_count': len(needs_improvement)
            },
            'categories': {
                'excellent': excellent_skills,
                'good': good_skills,
                'needs_improvement': needs_improvement
            },
            'detailed_results': {
                name: analysis.to_dict()
                for name, analysis in results.items()
            }
        }

        if output_file:
            import json
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=2)
                print(f"分析报告已保存: {output_file}")
            except Exception as e:
                print(f"保存报告失败: {e}")

        return report


# 全局分析器实例
skill_analyzer = SkillStructureAnalyzer()


def get_skill_analyzer() -> SkillStructureAnalyzer:
    """获取Skill分析器实例"""
    return skill_analyzer


if __name__ == '__main__':
    import json

    # 测试分析器
    analyzer = SkillStructureAnalyzer()

    # 分析所有Skill
    results = analyzer.analyze_all_skills()

    print(f"分析完成: {len(results)} 个Skill")
    print("\n评分汇总:")

    for skill_name, analysis in sorted(results.items(), key=lambda x: x[1].overall_score, reverse=True):
        print(f"\n{skill_name}:")
        print(f"  综合评分: {analysis.overall_score:.1f}")
        print(f"  - 结构: {analysis.structure_score:.1f}")
        print(f"  - 文档: {analysis.documentation_score:.1f}")
        print(f"  - 代码: {analysis.code_quality_score:.1f}")

        if analysis.issues:
            print(f"  问题 ({len(analysis.issues)}):")
            for issue in analysis.issues[:3]:
                print(f"    - {issue}")

    # 生成报告
    report = analyzer.generate_analysis_report(results, 'skill_analysis_report.json')
    print(f"\n报告汇总:")
    print(f"  总计: {report['total_skills']} 个Skill")
    print(f"  平均分: {report['summary']['average_overall_score']}")
    print(f"  优秀: {report['summary']['excellent_count']}")
    print(f"  良好: {report['summary']['good_count']}")
    print(f"  待改进: {report['summary']['needs_improvement_count']}")
