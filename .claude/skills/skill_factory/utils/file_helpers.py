"""文件操作工具函数"""

import os
import shutil
from pathlib import Path
from typing import List, Union


def ensure_dir_exists(path: Union[str, Path]) -> bool:
    """确保目录存在，如果不存在则创建"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"❌ 创建目录失败 {path}: {e}")
        return False


def safe_delete(path: Union[str, Path]) -> bool:
    """安全删除文件或目录"""
    try:
        path_obj = Path(path)
        if path_obj.is_file():
            path_obj.unlink()
        elif path_obj.is_dir():
            shutil.rmtree(path)
        return True
    except Exception as e:
        print(f"❌ 删除失败 {path}: {e}")
        return False


def copy_file_safe(source: Union[str, Path], destination: Union[str, Path]) -> bool:
    """安全复制文件"""
    try:
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        print(f"❌ 复制文件失败 {source} -> {destination}: {e}")
        return False


def find_files_by_pattern(directory: Union[str, Path], pattern: str) -> List[Path]:
    """根据模式查找文件"""
    try:
        return list(Path(directory).rglob(pattern))
    except Exception as e:
        print(f"❌ 查找文件失败 {directory}/{pattern}: {e}")
        return []


def read_file_content(file_path: Union[str, Path]) -> str:
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ 读取文件失败 {file_path}: {e}")
        return ""


def write_file_content(file_path: Union[str, Path], content: str) -> bool:
    """写入文件内容"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ 写入文件失败 {file_path}: {e}")
        return False


def get_file_size(file_path: Union[str, Path]) -> int:
    """获取文件大小（字节）"""
    try:
        return Path(file_path).stat().st_size
    except Exception as e:
        print(f"❌ 获取文件大小失败 {file_path}: {e}")
        return 0


def is_valid_file_path(file_path: Union[str, Path]) -> bool:
    """验证文件路径是否有效"""
    try:
        path = Path(file_path)
        # 检查路径是否包含非法字符
        illegal_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in str(path) for char in illegal_chars):
            return False

        # 检查路径是否在允许的范围内
        allowed_prefixes = ['.claude', '/tmp', '/var/tmp']
        if not any(str(path).startswith(prefix) for prefix in allowed_prefixes):
            return False

        return True
    except Exception:
        return False