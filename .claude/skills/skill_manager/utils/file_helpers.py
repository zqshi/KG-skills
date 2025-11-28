#!/usr/bin/env python3
"""
文件操作工具库
提供统一的文件读写接口和常用文件操作
"""

import os
import json
import yaml
from pathlib import Path
from typing import Any, Dict, List, Union, Optional
import shutil


class FileHelper:
    """文件操作助手类"""
    
    @staticmethod
    def read_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        读取文件内容
        
        Args:
            file_path: 文件路径
            encoding: 文件编码
            
        Returns:
            文件内容字符串
            
        Raises:
            FileNotFoundError: 文件不存在
            IOError: 读取失败
        """
        try:
            path = Path(file_path)
            return path.read_text(encoding=encoding)
        except Exception as e:
            raise IOError(f"读取文件失败 {file_path}: {str(e)}")
    
    @staticmethod
    def write_file(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
        """
        写入文件内容
        
        Args:
            file_path: 文件路径
            content: 写入内容
            encoding: 文件编码
            
        Raises:
            IOError: 写入失败
        """
        try:
            path = Path(file_path)
            # 确保目录存在
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)
        except Exception as e:
            raise IOError(f"写入文件失败 {file_path}: {str(e)}")
    
    @staticmethod
    def read_json(file_path: Union[str, Path], encoding: str = 'utf-8') -> Dict[str, Any]:
        """
        读取JSON文件
        
        Args:
            file_path: JSON文件路径
            encoding: 文件编码
            
        Returns:
            JSON解析后的字典
            
        Raises:
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON解析失败
        """
        try:
            content = FileHelper.read_file(file_path, encoding)
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"JSON解析失败 {file_path}: {str(e)}", e.doc, e.pos)
    
    @staticmethod
    def write_json(file_path: Union[str, Path], data: Dict[str, Any], 
                   encoding: str = 'utf-8', indent: int = 2) -> None:
        """
        写入JSON文件
        
        Args:
            file_path: JSON文件路径
            data: 要写入的数据
            encoding: 文件编码
            indent: 缩进空格数
            
        Raises:
            IOError: 写入失败
        """
        try:
            content = json.dumps(data, ensure_ascii=False, indent=indent)
            FileHelper.write_file(file_path, content, encoding)
        except Exception as e:
            raise IOError(f"写入JSON文件失败 {file_path}: {str(e)}")
    
    @staticmethod
    def read_yaml(file_path: Union[str, Path], encoding: str = 'utf-8') -> Dict[str, Any]:
        """
        读取YAML文件
        
        Args:
            file_path: YAML文件路径
            encoding: 文件编码
            
        Returns:
            YAML解析后的字典
            
        Raises:
            FileNotFoundError: 文件不存在
            yaml.YAMLError: YAML解析失败
        """
        try:
            content = FileHelper.read_file(file_path, encoding)
            return yaml.safe_load(content) or {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML解析失败 {file_path}: {str(e)}")
    
    @staticmethod
    def write_yaml(file_path: Union[str, Path], data: Dict[str, Any], 
                   encoding: str = 'utf-8') -> None:
        """
        写入YAML文件
        
        Args:
            file_path: YAML文件路径
            data: 要写入的数据
            encoding: 文件编码
            
        Raises:
            IOError: 写入失败
        """
        try:
            content = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
            FileHelper.write_file(file_path, content, encoding)
        except Exception as e:
            raise IOError(f"写入YAML文件失败 {file_path}: {str(e)}")
    
    @staticmethod
    def read_markdown_with_frontmatter(file_path: Union[str, Path], 
                                       encoding: str = 'utf-8') -> tuple[Dict[str, Any], str]:
        """
        读取带YAML front matter的Markdown文件
        
        Args:
            file_path: Markdown文件路径
            encoding: 文件编码
            
        Returns:
            (front_matter, content) 元组
            
        Raises:
            FileNotFoundError: 文件不存在
            yaml.YAMLError: YAML解析失败
        """
        try:
            content = FileHelper.read_file(file_path, encoding)
            
            # 检查是否有YAML front matter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter_yaml = parts[1].strip()
                    markdown_content = parts[2].strip()
                    frontmatter = yaml.safe_load(frontmatter_yaml) or {}
                    return frontmatter, markdown_content
            
            # 没有front matter
            return {}, content.strip()
            
        except Exception as e:
            raise IOError(f"读取Markdown文件失败 {file_path}: {str(e)}")
    
    @staticmethod
    def write_markdown_with_frontmatter(file_path: Union[str, Path], 
                                        frontmatter: Dict[str, Any], 
                                        content: str,
                                        encoding: str = 'utf-8') -> None:
        """
        写入带YAML front matter的Markdown文件
        
        Args:
            file_path: Markdown文件路径
            frontmatter: YAML front matter数据
            content: Markdown内容
            encoding: 文件编码
            
        Raises:
            IOError: 写入失败
        """
        try:
            if frontmatter:
                yaml_content = yaml.dump(frontmatter, allow_unicode=True, 
                                       default_flow_style=False, sort_keys=False)
                full_content = f"---\n{yaml_content}---\n\n{content}"
            else:
                full_content = content
            
            FileHelper.write_file(file_path, full_content, encoding)
        except Exception as e:
            raise IOError(f"写入Markdown文件失败 {file_path}: {str(e)}")
    
    @staticmethod
    def file_exists(file_path: Union[str, Path]) -> bool:
        """检查文件是否存在"""
        return Path(file_path).exists()
    
    @staticmethod
    def is_file(file_path: Union[str, Path]) -> bool:
        """检查路径是否为文件"""
        return Path(file_path).is_file()
    
    @staticmethod
    def is_directory(path: Union[str, Path]) -> bool:
        """检查路径是否为目录"""
        return Path(path).is_dir()
    
    @staticmethod
    def get_file_size(file_path: Union[str, Path]) -> int:
        """
        获取文件大小（字节）
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件大小（字节）
            
        Raises:
            FileNotFoundError: 文件不存在
        """
        return Path(file_path).stat().st_size
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """
        格式化文件大小为易读格式
        
        Args:
            size_bytes: 文件大小（字节）
            
        Returns:
            格式化后的文件大小字符串
        """
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        size = size_bytes
        
        while size >= 1024 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f}{size_names[i]}"
    
    @staticmethod
    def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        获取文件详细信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息字典
        """
        path = Path(file_path)
        stat = path.stat()
        
        return {
            "name": path.name,
            "path": str(path.absolute()),
            "size": stat.st_size,
            "size_formatted": FileHelper.format_file_size(stat.st_size),
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
            "extension": path.suffix,
            "parent": str(path.parent)
        }
    
    @staticmethod
    def copy_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
        """
        复制文件
        
        Args:
            src: 源文件路径
            dst: 目标文件路径
            
        Raises:
            FileNotFoundError: 源文件不存在
            IOError: 复制失败
        """
        try:
            shutil.copy2(src, dst)
        except Exception as e:
            raise IOError(f"复制文件失败 {src} -> {dst}: {str(e)}")
    
    @staticmethod
    def move_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
        """
        移动文件
        
        Args:
            src: 源文件路径
            dst: 目标文件路径
            
        Raises:
            FileNotFoundError: 源文件不存在
            IOError: 移动失败
        """
        try:
            shutil.move(str(src), str(dst))
        except Exception as e:
            raise IOError(f"移动文件失败 {src} -> {dst}: {str(e)}")
    
    @staticmethod
    def delete_file(file_path: Union[str, Path]) -> None:
        """
        删除文件
        
        Args:
            file_path: 文件路径
            
        Raises:
            FileNotFoundError: 文件不存在
            IOError: 删除失败
        """
        try:
            path = Path(file_path)
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
        except Exception as e:
            raise IOError(f"删除文件失败 {file_path}: {str(e)}")
    
    @staticmethod
    def list_files(directory: Union[str, Path], 
                   pattern: str = "*",
                   recursive: bool = False) -> List[Path]:
        """
        列出目录中的文件
        
        Args:
            directory: 目录路径
            pattern: 文件匹配模式（glob）
            recursive: 是否递归子目录
            
        Returns:
            文件路径列表
        """
        path = Path(directory)
        
        if recursive:
            return list(path.rglob(pattern))
        else:
            return list(path.glob(pattern))
    
    @staticmethod
    def ensure_directory(directory: Union[str, Path]) -> Path:
        """
        确保目录存在，不存在则创建
        
        Args:
            directory: 目录路径
            
        Returns:
            目录路径对象
        """
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return path


if __name__ == "__main__":
    # 测试文件助手
    print("测试文件操作助手...")
    
    # 测试文件信息获取
    test_file = Path(__file__)
    if test_file.exists():
        info = FileHelper.get_file_info(test_file)
        print(f"文件信息: {info['name']} - {info['size_formatted']}")
    
    # 测试JSON读写
    test_data = {"test": "data", "number": 42}
    test_json_path = "test_temp.json"
    
    try:
        FileHelper.write_json(test_json_path, test_data)
        read_data = FileHelper.read_json(test_json_path)
        print(f"JSON读写测试: {read_data}")
        FileHelper.delete_file(test_json_path)
    except Exception as e:
        print(f"测试失败: {e}")