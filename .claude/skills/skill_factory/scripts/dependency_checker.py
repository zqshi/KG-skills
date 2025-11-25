#!/usr/bin/env python3
"""
依赖检查器脚本
检查Skill中Python脚本的依赖库可用性
"""

import sys
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Tuple


class DependencyChecker:
    """依赖检查器类"""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.missing_dependencies = []
        self.available_dependencies = []

    def extract_dependencies(self, script_path: Path) -> List[str]:
        """从Python脚本中提取导入的依赖库"""
        dependencies = []

        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 匹配import语句
            import_patterns = [
                r'^import\s+([a-zA-Z_][a-zA-Z0-9_]*)',  # import module
                r'^from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import',  # from module import
                r'^import\s+([a-zA-Z_][a-zA-Z0-9_]*)\.',  # import module.submodule
            ]

            for line in content.split('\n'):
                line = line.strip()

                # 跳过注释和空行
                if line.startswith('#') or not line:
                    continue

                for pattern in import_patterns:
                    match = re.match(pattern, line)
                    if match:
                        dependency = match.group(1)
                        # 跳过标准库和内置模块
                        if not self._is_stdlib_module(dependency):
                            dependencies.append(dependency)

        except Exception as e:
            print(f"❌ 读取脚本文件失败 {script_path}: {e}")

        return list(set(dependencies))  # 去重

    def _is_stdlib_module(self, module_name: str) -> bool:
        """检查是否为Python标准库模块"""
        stdlib_modules = {
            'os', 'sys', 're', 'json', 'csv', 'datetime', 'time', 'math',
            'pathlib', 'shutil', 'glob', 'subprocess', 'threading', 'multiprocessing',
            'collections', 'itertools', 'functools', 'argparse', 'logging',
            'tempfile', 'urllib', 'http', 'socket', 'ssl', 'hashlib', 'base64'
        }
        return module_name in stdlib_modules

    def check_dependency_availability(self, dependency: str) -> bool:
        """检查单个依赖库是否可用"""
        try:
            # 尝试导入模块
            __import__(dependency)
            return True
        except ImportError:
            return False

    def get_dependency_info(self, dependency: str) -> Dict:
        """获取依赖库的详细信息"""
        try:
            # 尝试获取版本信息
            result = subprocess.run(
                [sys.executable, '-c', f'import {dependency}; print(getattr({dependency}, "__version__", "unknown"))'],
                capture_output=True, text=True, timeout=10
            )
            version = result.stdout.strip() if result.returncode == 0 else "unknown"
        except:
            version = "unknown"

        return {
            'name': dependency,
            'available': self.check_dependency_availability(dependency),
            'version': version,
            'pip_name': self._get_pip_name(dependency)
        }

    def _get_pip_name(self, dependency: str) -> str:
        """获取pip安装包名称"""
        # 常见模块名和包名映射
        name_mapping = {
            'PIL': 'Pillow',
            'sklearn': 'scikit-learn',
            'cv2': 'opencv-python',
            'yaml': 'PyYAML',
            'dateutil': 'python-dateutil',
            'bs4': 'beautifulsoup4'
        }
        return name_mapping.get(dependency, dependency)

    def check_skill_dependencies(self) -> Tuple[bool, List[Dict]]:
        """检查Skill中所有脚本的依赖"""
        print("🔍 检查Skill依赖...")

        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            print("✅ 没有脚本目录，无需检查依赖")
            return True, []

        # 收集所有依赖
        all_dependencies = set()

        for script_file in scripts_dir.glob("*.py"):
            print(f"📄 分析脚本: {script_file.name}")
            deps = self.extract_dependencies(script_file)
            all_dependencies.update(deps)

        if not all_dependencies:
            print("✅ 没有检测到外部依赖")
            return True, []

        # 检查每个依赖
        dependency_info = []
        all_available = True

        for dep in sorted(all_dependencies):
            info = self.get_dependency_info(dep)
            dependency_info.append(info)

            if info['available']:
                self.available_dependencies.append(dep)
                print(f"✅ {dep} - 可用 (版本: {info['version']})")
            else:
                self.missing_dependencies.append(dep)
                all_available = False
                print(f"❌ {dep} - 缺失")

        return all_available, dependency_info

    def generate_requirements_file(self) -> str:
        """生成requirements.txt文件内容"""
        requirements = []

        for dep in self.available_dependencies + self.missing_dependencies:
            pip_name = self._get_pip_name(dep)
            requirements.append(f"{pip_name}")

        return '\n'.join(sorted(requirements))

    def generate_installation_guide(self) -> str:
        """生成安装指南"""
        if not self.missing_dependencies:
            return "✅ 所有依赖都已安装，无需额外操作"

        guide = "# 依赖安装指南\n\n"
        guide += "以下依赖库需要安装：\n\n"

        for dep in self.missing_dependencies:
            pip_name = self._get_pip_name(dep)
            guide += f"## {dep}\n"
            guide += f"```bash\npip install {pip_name}\n```\n\n"

        guide += "或者一次性安装所有依赖：\n\n"
        guide += "```bash\npip install "
        guide += ' '.join([self._get_pip_name(dep) for dep in self.missing_dependencies])
        guide += "\n```"

        return guide


def main():
    """主函数"""
    import sys

    if len(sys.argv) != 2:
        print("用法: python dependency_checker.py <skill_path>")
        sys.exit(1)

    skill_path = sys.argv[1]
    checker = DependencyChecker(skill_path)

    all_available, dependencies = checker.check_skill_dependencies()

    print("\n" + "="*50)
    print("📊 依赖检查结果")
    print("="*50)

    if all_available:
        print("✅ 所有依赖都可用！")
    else:
        print("❌ 发现缺失的依赖")
        print("\n缺失的依赖：")
        for dep in checker.missing_dependencies:
            print(f"  • {dep}")

    # 生成requirements.txt
    requirements_content = checker.generate_requirements_file()
    if requirements_content:
        print("\n📋 建议的requirements.txt内容：")
        print(requirements_content)

    # 生成安装指南
    if checker.missing_dependencies:
        print("\n📖 安装指南：")
        print(checker.generate_installation_guide())

    sys.exit(0 if all_available else 1)


if __name__ == "__main__":
    main()