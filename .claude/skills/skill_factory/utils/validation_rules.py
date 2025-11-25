"""验证规则工具函数"""

import re
import yaml
from typing import Any, Dict, List
from pathlib import Path


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_skill_name(name: str) -> bool:
    """验证Skill名称格式（小写下划线）"""
    pattern = r'^[a-z][a-z0-9_]*(_[a-z0-9]+)*$'
    return bool(re.match(pattern, name))


def validate_yaml_content(yaml_content: str) -> Tuple[bool, str]:
    """验证YAML内容格式"""
    try:
        data = yaml.safe_load(yaml_content)
        return True, "YAML格式正确"
    except yaml.YAMLError as e:
        return False, f"YAML格式错误: {e}"


def validate_file_path(file_path: str) -> Tuple[bool, str]:
    """验证文件路径安全性"""
    try:
        path = Path(file_path)

        # 检查路径遍历攻击
        if '..' in str(path):
            return False, "路径包含非法字符 '..'"

        # 检查绝对路径是否在允许范围内
        if path.is_absolute():
            allowed_paths = [
                Path('.claude'),
                Path('/tmp'),
                Path('/var/tmp')
            ]

            if not any(path.is_relative_to(allowed) for allowed in allowed_paths):
                return False, "路径不在允许范围内"

        return True, "路径验证通过"
    except Exception as e:
        return False, f"路径验证失败: {e}"


def validate_python_syntax(code: str) -> Tuple[bool, str]:
    """验证Python语法"""
    try:
        compile(code, '<string>', 'exec')
        return True, "Python语法正确"
    except SyntaxError as e:
        return False, f"Python语法错误: {e}"


def validate_url(url: str) -> bool:
    """验证URL格式"""
    pattern = r'^https?://[\w\-\.]+(:\d+)?(/[\w\-\./?%&=]*)?$'
    return bool(re.match(pattern, url))


def validate_json_content(json_content: str) -> Tuple[bool, str]:
    """验证JSON内容格式"""
    try:
        import json
        json.loads(json_content)
        return True, "JSON格式正确"
    except json.JSONDecodeError as e:
        return False, f"JSON格式错误: {e}"


def validate_required_fields(data: Dict, required_fields: List[str]) -> Tuple[bool, List[str]]:
    """验证必需字段是否存在"""
    missing_fields = []

    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)

    return len(missing_fields) == 0, missing_fields


def validate_field_length(field_value: str, max_length: int, field_name: str = "字段") -> Tuple[bool, str]:
    """验证字段长度"""
    if len(field_value) > max_length:
        return False, f"{field_name}长度超过{max_length}字符限制"
    return True, f"{field_name}长度验证通过"


def validate_skill_yaml_header(skill_content: str) -> Tuple[bool, List[str]]:
    """验证Skill YAML头部规范"""
    errors = []

    # 检查YAML头部是否存在
    yaml_pattern = r'^---\n(.+?)\n---'
    match = re.search(yaml_pattern, skill_content, re.DOTALL)

    if not match:
        errors.append("缺少YAML头部")
        return False, errors

    try:
        yaml_content = match.group(1)
        data = yaml.safe_load(yaml_content)

        # 验证必需字段
        required_fields = ["name", "description"]
        has_all_fields, missing_fields = validate_required_fields(data, required_fields)

        if not has_all_fields:
            errors.extend([f"缺少必需字段: {field}" for field in missing_fields])

        # 验证字段长度
        if "name" in data:
            is_valid, message = validate_field_length(data["name"], 64, "name字段")
            if not is_valid:
                errors.append(message)

        if "description" in data:
            is_valid, message = validate_field_length(data["description"], 1024, "description字段")
            if not is_valid:
                errors.append(message)

        return len(errors) == 0, errors

    except yaml.YAMLError as e:
        errors.append(f"YAML解析错误: {e}")
        return False, errors


def validate_file_extension(file_path: str, allowed_extensions: List[str]) -> bool:
    """验证文件扩展名"""
    file_ext = Path(file_path).suffix.lower()
    return file_ext in allowed_extensions