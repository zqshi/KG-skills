#!/usr/bin/env python3
"""
日志工具库
提供统一的日志配置和Skill专用日志记录器
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union
import colorama
from colorama import Fore, Back, Style

# 初始化colorama
colorama.init(autoreset=True)


class LogFormatter(logging.Formatter):
    """自定义日志格式化器，支持颜色输出"""
    
    # 颜色映射
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA + Back.WHITE
    }
    
    def __init__(self, use_color: bool = True, show_time: bool = True, show_level: bool = True):
        """
        初始化日志格式化器
        
        Args:
            use_color: 是否使用颜色
            show_time: 是否显示时间
            show_level: 是否显示日志级别
        """
        self.use_color = use_color
        self.show_time = show_time
        self.show_level = show_level
        
        # 构建格式字符串
        format_parts = []
        if show_time:
            format_parts.append('%(asctime)s')
        if show_level:
            format_parts.append('%(levelname)s')
        format_parts.append('%(name)s')
        format_parts.append('%(message)s')
        
        fmt = ' | '.join(format_parts)
        super().__init__(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S')
    
    def format(self, record: logging.LogRecord) -> str:
        """
        格式化日志记录
        
        Args:
            record: 日志记录对象
            
        Returns:
            格式化后的日志字符串
        """
        # 保存原始值
        orig_levelname = record.levelname
        
        # 添加颜色
        if self.use_color and record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{Style.RESET_ALL}"
        
        # 格式化
        result = super().format(record)
        
        # 恢复原始值
        record.levelname = orig_levelname
        
        return result


class SkillLogger:
    """Skill专用日志记录器"""
    
    def __init__(self, name: str, level: int = logging.INFO, log_file: Optional[Union[str, Path]] = None):
        """
        初始化Skill日志记录器
        
        Args:
            name: 日志记录器名称
            level: 日志级别
            log_file: 日志文件路径（可选）
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False  # 防止重复日志
        
        # 清除已有处理器
        self.logger.handlers.clear()
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # 创建格式化器
        console_formatter = LogFormatter(use_color=True, show_time=True, show_level=True)
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(console_handler)
        
        # 创建文件处理器（如果指定了日志文件）
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setLevel(level)
            
            # 文件日志不使用颜色
            file_formatter = LogFormatter(use_color=False, show_time=True, show_level=True)
            file_handler.setFormatter(file_formatter)
            
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, *args, **kwargs):
        """记录DEBUG级别日志"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """记录INFO级别日志"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """记录WARNING级别日志"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """记录ERROR级别日志"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """记录CRITICAL级别日志"""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """记录异常日志"""
        self.logger.exception(message, *args, **kwargs)
    
    def log(self, level: int, message: str, *args, **kwargs):
        """
        记录指定级别的日志
        
        Args:
            level: 日志级别
            message: 日志消息
        """
        self.logger.log(level, message, *args, **kwargs)


# 全局日志配置
def setup_logger(name: str = "skill", level: int = logging.INFO, 
                 log_file: Optional[Union[str, Path]] = None) -> SkillLogger:
    """
    设置并获取日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径（可选）
        
    Returns:
        SkillLogger实例
    """
    return SkillLogger(name, level, log_file)


def get_skill_logger(skill_name: str, level: int = logging.INFO) -> SkillLogger:
    """
    获取Skill专用日志记录器
    
    Args:
        skill_name: Skill名称
        level: 日志级别
        
    Returns:
        SkillLogger实例
    """
    log_file = Path(f".claude/skills/logs/{skill_name}.log")
    return setup_logger(f"skill.{skill_name}", level, log_file)


# 预定义的日志级别
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def parse_log_level(level: Union[str, int]) -> int:
    """
    解析日志级别
    
    Args:
        level: 日志级别（字符串或整数）
        
    Returns:
        日志级别整数
    """
    if isinstance(level, int):
        return level
    
    if isinstance(level, str):
        level_upper = level.upper()
        if level_upper in LOG_LEVELS:
            return LOG_LEVELS[level_upper]
        
        # 尝试转换为整数
        try:
            return int(level)
        except ValueError:
            pass
    
    # 默认返回INFO级别
    return logging.INFO


# 日志装饰器
def log_function_call(logger: Optional[SkillLogger] = None, level: int = logging.DEBUG):
    """
    函数调用日志装饰器
    
    Args:
        logger: 日志记录器
        level: 日志级别
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            
            # 使用默认日志记录器
            log = logger or setup_logger()
            
            log.log(level, f"调用函数: {func_name}")
            log.log(level, f"参数: args={args}, kwargs={kwargs}")
            
            try:
                result = func(*args, **kwargs)
                log.log(level, f"函数 {func_name} 执行成功")
                return result
            except Exception as e:
                log.error(f"函数 {func_name} 执行失败: {str(e)}")
                raise
        
        return wrapper
    return decorator


if __name__ == "__main__":
    # 测试日志工具
    print("测试日志工具库...")
    
    # 测试控制台日志
    logger = setup_logger("test", level=logging.DEBUG)
    
    logger.debug("这是一条DEBUG消息")
    logger.info("这是一条INFO消息")
    logger.warning("这是一条WARNING消息")
    logger.error("这是一条ERROR消息")
    logger.critical("这是一条CRITICAL消息")
    
    # 测试Skill日志记录器
    skill_logger = get_skill_logger("test_skill")
    skill_logger.info("Skill测试消息")
    
    # 测试日志装饰器
    @log_function_call(logger, logging.INFO)
    def test_function(a, b):
        return a + b
    
    result = test_function(1, 2)
    print(f"函数执行结果: {result}")
    
    print("日志测试完成！")