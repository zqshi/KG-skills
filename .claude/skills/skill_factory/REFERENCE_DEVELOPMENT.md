# Skill开发规范参考

## 📋 概述

本文档详细说明了Claude Agent Skills的开发规范，确保生成的Skill符合官方标准且易于维护。

## 🏗️ 文件结构规范

### 必需文件结构
```
.claude/skills/<skill_name>/
├── SKILL.md              # 主技能文件（必需）
├── README.md             # 使用说明（必需）
├── scripts/              # Python脚本目录（可选）
├── templates/            # 模板文件目录（可选）
├── examples/             # 使用示例目录（可选）
└── utils/                # 工具函数目录（可选）
```

### 文件命名规范

#### Skill目录命名
- **格式**: 小写下划线 (`skill_name`)
- **示例**: `data_processor`, `api_integrator`, `file_operator`
- **禁止**: 大写字母、连字符、空格

#### 文件命名
- **Python脚本**: 小写下划线 (`script_name.py`)
- **参考文档**: 大写格式 (`REFERENCE_NAME.md`)
- **模板文件**: 小写下划线 (`template_name.md`)

## 📝 SKILL.md 规范

### YAML头部格式
```yaml
---
name: skill_name
description: 清晰的功能描述
tools: [Read, Write, Edit]  # 可选：需要的工具列表
---
```

### 字段要求
- **name**: ≤64字符，小写下划线格式
- **description**: ≤1024字符，清晰描述功能
- **tools**: 可选，列出需要的Claude工具

### 内容结构
```markdown
# Skill名称

## 🎯 概述
[功能描述]

## 🚀 快速开始
[使用方法和示例]

## 📋 输入规范
[输入格式和要求]

## 📤 输出内容
[输出格式和内容]

## 🎪 使用示例
[多个使用场景示例]

## ⚠️ 注意事项
[使用限制和注意事项]
```

## 🐍 Python脚本开发规范

### 代码规范
- **编码**: UTF-8
- **缩进**: 4个空格
- **行长度**: ≤100字符
- **文档字符串**: 每个函数都需要

### 安全规范
```python
# ✅ 安全做法
import os
from pathlib import Path

def safe_file_operation(file_path):
    """安全的文件操作"""
    path = Path(file_path)

    # 验证路径安全性
    if not path.is_relative_to('.claude'):
        raise ValueError("路径不在允许范围内")

    # 执行操作
    return path.read_text()

# ❌ 不安全做法
def unsafe_file_operation(file_path):
    """不安全的文件操作"""
    # 直接使用用户输入，存在安全风险
    with open(file_path, 'r') as f:
        return f.read()
```

### 错误处理
```python
def robust_function():
    """健壮的函数实现"""
    try:
        # 主要逻辑
        result = perform_operation()
        return result
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}")
        return None
    except PermissionError as e:
        print(f"❌ 权限错误: {e}")
        return None
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return None
```

## 📚 文档编写规范

### README.md 结构
```markdown
# Skill名称

## 📖 使用说明
[详细使用说明]

## 🏗️ 项目结构
[文件结构说明]

## 🐛 故障排除
[常见问题和解决方案]

## 📄 许可证
[许可证信息]
```

### 示例文档要求
- **真实性**: 提供真实可运行的示例
- **完整性**: 包含输入、输出、步骤说明
- **多样性**: 从简单到复杂的多级示例

## 🔧 工具使用规范

### 允许的工具列表
```python
# 文件操作工具
Read, Write, Edit, Glob, Grep

# 系统工具
Bash, Task

# 网络工具
WebFetch, WebSearch

# 其他工具
Skill, SlashCommand
```

### 工具使用最佳实践

#### 文件操作
```python
# ✅ 安全的文件读取
from pathlib import Path

def read_file_safe(file_path):
    """安全读取文件"""
    path = Path(file_path)

    # 验证路径
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 读取文件
    return path.read_text(encoding='utf-8')
```

#### Bash命令执行
```python
# ✅ 安全的Bash命令执行
import subprocess

def run_command_safe(command):
    """安全执行命令"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  # 设置超时
        )
        return result
    except subprocess.TimeoutExpired:
        print("❌ 命令执行超时")
        return None
```

## 🛡️ 安全规范

### 输入验证
```python
def validate_user_input(input_data):
    """验证用户输入"""
    # 检查类型
    if not isinstance(input_data, str):
        raise TypeError("输入必须是字符串")

    # 检查长度
    if len(input_data) > 1000:
        raise ValueError("输入过长")

    # 检查内容
    if any(char in input_data for char in ['<', '>', '..']):
        raise ValueError("输入包含非法字符")

    return input_data
```

### 路径安全
- **禁止**: 绝对路径（除非在允许范围内）
- **禁止**: 路径遍历（`../`）
- **限制**: 只能在 `.claude` 目录下操作

## 🧪 测试规范

### 单元测试要求
```python
# tests/test_skill.py
import unittest
from skill_module import SkillFunction

class TestSkill(unittest.TestCase):

    def test_basic_functionality(self):
        """测试基本功能"""
        result = SkillFunction("test_input")
        self.assertEqual(result, "expected_output")

    def test_error_handling(self):
        """测试错误处理"""
        with self.assertRaises(ValueError):
            SkillFunction("invalid_input")
```

### 集成测试
- 验证Skill与Claude的集成
- 测试各种输入场景
- 验证错误处理机制

## 📈 性能规范

### 响应时间
- **简单操作**: ≤5秒
- **复杂操作**: ≤30秒
- **超时处理**: 必须设置超时机制

### 资源使用
- **内存**: 合理使用，避免内存泄漏
- **CPU**: 避免长时间占用CPU
- **文件**: 及时释放文件句柄

## 🔄 版本管理

### 版本号规范
- **格式**: `主版本.次版本.修订版本`
- **示例**: `1.0.0`, `1.1.0`, `1.1.1`

### 变更日志
```markdown
# 变更日志

## [1.1.0] - 2024-01-01
### 新增
- 新增功能A
- 新增功能B

### 修复
- 修复问题C

## [1.0.0] - 2023-12-01
### 初始版本
- 基础功能实现
```

## 🎯 最佳实践总结

### 设计原则
1. **单一职责**: 每个Skill专注于一个功能
2. **开箱即用**: 无需复杂配置即可使用
3. **错误容忍**: 优雅处理各种异常情况
4. **文档完整**: 提供详细的说明和示例

### 开发流程
1. **需求分析**: 明确功能需求和目标用户
2. **结构设计**: 设计合理的文件结构
3. **代码实现**: 遵循编码规范和安全要求
4. **测试验证**: 全面测试功能和边界情况
5. **文档编写**: 编写完整的使用文档
6. **质量审查**: 检查是否符合所有规范

---

**遵循这些规范，确保您的Skill高质量、安全且易于使用！** 🚀