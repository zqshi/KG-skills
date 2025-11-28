#!/usr/bin/env python3
"""
日志源管理器
自动检测并使用系统日志，如果没有则自行记录
遵循5W1H原则，记录8个核心字段
"""

import os
import sys
import json
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import subprocess
import re

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models import OperationRecord


class LogSourceManager:
    """日志源管理器 - 自动选择最佳日志源"""
    
    def __init__(self, preferred_source: str = 'auto'):
        """
        初始化日志源管理器
        
        Args:
            preferred_source: 首选日志源 ('auto', 'system', 'application', 'self')
        """
        self.preferred_source = preferred_source
        self.active_source = None
        self.sources = {
            'system': SystemLogSource(),
            'application': ApplicationLogSource(),
            'self': SelfLogSource()
        }
        
        # 自动检测并选择最佳日志源
        self._detect_and_select_source()
    
    def _detect_and_select_source(self):
        """检测并选择最佳日志源"""
        print("🔍 检测可用的日志源...")
        
        # 按优先级检测
        detection_order = ['system', 'application', 'self']
        
        for source_name in detection_order:
            source = self.sources[source_name]
            if source.is_available():
                self.active_source = source
                print(f"✅ 使用日志源: {source_name} ({source.get_description()})")
                return
        
        # 如果都没有，使用自记录作为fallback
        self.active_source = self.sources['self']
        print("⚠️  未检测到系统日志源，使用自记录模式")
    
    def get_operations(self, hours: int = 24) -> List[OperationRecord]:
        """
        获取操作记录
        
        Args:
            hours: 获取最近多少小时的记录
            
        Returns:
            操作记录列表
        """
        if not self.active_source:
            return []
        
        return self.active_source.get_operations(hours)
    
    def record_operation(self, operation: OperationRecord) -> bool:
        """
        记录单个操作（仅在自记录模式下有效）
        
        Args:
            operation: 操作记录
            
        Returns:
            是否成功记录
        """
        if not self.active_source or not hasattr(self.active_source, 'record_operation'):
            return False
        
        return self.active_source.record_operation(operation)
    
    def get_source_info(self) -> Dict[str, Any]:
        """获取当前日志源信息"""
        if not self.active_source:
            return {}
        
        return {
            'source_type': self.active_source.__class__.__name__,
            'description': self.active_source.get_description(),
            'is_available': self.active_source.is_available(),
            'capabilities': self.active_source.get_capabilities()
        }


class BaseLogSource:
    """日志源基类"""
    
    def is_available(self) -> bool:
        """检查日志源是否可用"""
        raise NotImplementedError
    
    def get_description(self) -> str:
        """获取日志源描述"""
        raise NotImplementedError
    
    def get_capabilities(self) -> List[str]:
        """获取日志源能力"""
        raise NotImplementedError
    
    def get_operations(self, hours: int = 24) -> List[OperationRecord]:
        """获取操作记录"""
        raise NotImplementedError


class SystemLogSource(BaseLogSource):
    """系统日志源 - 使用Linux auditd或systemd journal"""
    
    def is_available(self) -> bool:
        """检测系统日志是否可用"""
        try:
            # 检测auditd
            result = subprocess.run(['which', 'ausearch'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return True
            
            # 检测systemd journal
            result = subprocess.run(['which', 'journalctl'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return True
            
            return False
        except:
            return False
    
    def get_description(self) -> str:
        return "系统日志 (auditd/systemd journal)"
    
    def get_capabilities(self) -> List[str]:
        return ['who', 'what', 'when', 'where', 'how']
    
    def get_operations(self, hours: int = 24) -> List[OperationRecord]:
        """从系统日志提取操作记录"""
        operations = []
        
        try:
            # 尝试使用auditd
            if self._has_auditd():
                operations.extend(self._get_from_auditd(hours))
            
            # 尝试使用systemd journal
            if self._has_journal():
                operations.extend(self._get_from_journal(hours))
            
        except Exception as e:
            print(f"读取系统日志失败: {e}")
        
        return operations
    
    def _has_auditd(self) -> bool:
        """检查是否有auditd"""
        try:
            result = subprocess.run(['which', 'ausearch'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _has_journal(self) -> bool:
        """检查是否有systemd journal"""
        try:
            result = subprocess.run(['which', 'journalctl'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _get_from_auditd(self, hours: int) -> List[OperationRecord]:
        """从auditd提取"""
        operations = []
        
        try:
            # 使用ausearch查询最近的记录
            since_time = datetime.now() - timedelta(hours=hours)
            since_str = since_time.strftime('%m/%d/%Y %H:%M:%S')
            
            cmd = f'ausearch -ts {since_str} -i'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                operations.extend(self._parse_auditd_output(result.stdout))
            
        except Exception as e:
            print(f"读取auditd日志失败: {e}")
        
        return operations
    
    def _get_from_journal(self, hours: int) -> List[OperationRecord]:
        """从systemd journal提取"""
        operations = []
        
        try:
            # 使用journalctl查询
            cmd = f'journalctl --since "{hours} hours ago" -o json'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                operations.extend(self._parse_journal_output(result.stdout))
            
        except Exception as e:
            print(f"读取systemd journal失败: {e}")
        
        return operations
    
    def _parse_auditd_output(self, output: str) -> List[OperationRecord]:
        """解析auditd输出"""
        operations = []
        
        # auditd输出格式解析
        # 示例: type=EXECVE msg=audit(1234567890.123:45): pid=1234 uid=1000 ...
        
        for line in output.split('\n'):
            if 'type=EXECVE' in line:
                record = self._parse_auditd_execve(line)
                if record:
                    operations.append(record)
        
        return operations
    
    def _parse_auditd_execve(self, line: str) -> Optional[OperationRecord]:
        """解析auditd的EXECVE记录"""
        try:
            # 提取关键信息
            timestamp_match = re.search(r'audit\((\d+\.\d+):\d+\)', line)
            if not timestamp_match:
                return None
            
            timestamp = float(timestamp_match.group(1))
            
            # 提取命令
            cmd_match = re.search(r'cmd=([^ ]+)', line)
            if not cmd_match:
                return None
            
            command = cmd_match.group(1)
            
            # 提取用户
            uid_match = re.search(r'uid=(\d+)', line)
            user = uid_match.group(1) if uid_match else 'unknown'
            
            return OperationRecord(
                timestamp=datetime.fromtimestamp(timestamp).isoformat(),
                user=user,
                session_id=f"audit_{timestamp}",
                command=command,
                exit_code=0,  # auditd不记录退出码
                duration_seconds=0,
                working_directory='',
                hostname=platform.node(),
                source_ip='',
                action_type='execute',
                purpose='system',
                target_object='',
                object_type='command'
            )
            
        except Exception as e:
            print(f"解析auditd记录失败: {e}")
            return None
    
    def _parse_journal_output(self, output: str) -> List[OperationRecord]:
        """解析journalctl输出"""
        operations = []
        
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            try:
                entry = json.loads(line)
                record = self._parse_journal_entry(entry)
                if record:
                    operations.append(record)
            except json.JSONDecodeError:
                continue
        
        return operations
    
    def _parse_journal_entry(self, entry: Dict[str, Any]) -> Optional[OperationRecord]:
        """解析journalctl条目"""
        try:
            # 提取EXECVE类型的记录
            if entry.get('MESSAGE', '').startswith('EXECVE'):
                return OperationRecord(
                    timestamp=datetime.fromtimestamp(
                        entry.get('__REALTIME_TIMESTAMP', 0) / 1000000
                    ).isoformat(),
                    user=entry.get('_UID', 'unknown'),
                    session_id=entry.get('_PID', 'unknown'),
                    command=entry.get('MESSAGE', ''),
                    exit_code=0,
                    duration_seconds=0,
                    working_directory=entry.get('_PWD', ''),
                    hostname=entry.get('_HOSTNAME', platform.node()),
                    source_ip='',
                    action_type='execute',
                    purpose='system',
                    target_object='',
                    object_type='command'
                )
            
        except Exception as e:
            print(f"解析journal条目失败: {e}")
        
        return None


class ApplicationLogSource(BaseLogSource):
    """应用日志源 - 使用应用自身的审计日志"""
    
    def is_available(self) -> bool:
        """检测应用日志是否可用"""
        # 检查常见的应用日志位置
        log_paths = [
            '/var/log/app/audit.log',
            '/var/log/application/audit.json',
            Path.home() / '.app' / 'audit.log',
            Path.cwd() / 'logs' / 'audit.json'
        ]
        
        for log_path in log_paths:
            if Path(log_path).exists():
                return True
        
        return False
    
    def get_description(self) -> str:
        return "应用审计日志"
    
    def get_capabilities(self) -> List[str]:
        return ['who', 'what', 'when', 'where', 'why', 'how']
    
    def get_operations(self, hours: int = 24) -> List[OperationRecord]:
        """从应用日志提取操作记录"""
        operations = []
        
        # 检查所有可能的应用日志位置
        log_paths = [
            '/var/log/app/audit.log',
            '/var/log/application/audit.json',
            Path.home() / '.app' / 'audit.log',
            Path.cwd() / 'logs' / 'audit.json'
        ]
        
        for log_path in log_paths:
            if Path(log_path).exists():
                try:
                    ops = self._parse_application_log(log_path, hours)
                    operations.extend(ops)
                except Exception as e:
                    print(f"读取应用日志 {log_path} 失败: {e}")
        
        return operations
    
    def _parse_application_log(self, log_path: Path, hours: int) -> List[OperationRecord]:
        """解析应用日志"""
        operations = []
        
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            with open(log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        entry = json.loads(line)
                        
                        # 检查时间戳
                        op_time = datetime.fromisoformat(entry.get('timestamp', ''))
                        if op_time < cutoff_time:
                            continue
                        
                        # 转换为OperationRecord
                        record = OperationRecord(
                            timestamp=entry.get('timestamp', ''),
                            user=entry.get('user', 'unknown'),
                            session_id=entry.get('session_id', ''),
                            command=entry.get('action', '') + ' ' + entry.get('target', ''),
                            exit_code=entry.get('result', {}).get('code', 0),
                            duration_seconds=entry.get('duration', 0),
                            working_directory=entry.get('location', ''),
                            hostname=entry.get('host', platform.node()),
                            source_ip=entry.get('source_ip', ''),
                            action_type=entry.get('action_type', 'unknown'),
                            purpose=entry.get('purpose', 'unknown'),
                            target_object=entry.get('target', ''),
                            object_type=entry.get('object_type', 'unknown')
                        )
                        
                        operations.append(record)
                        
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
        
        except Exception as e:
            print(f"解析应用日志失败: {e}")
        
        return operations


class SelfLogSource(BaseLogSource):
    """自记录日志源 - 通过脚本记录"""
    
    def __init__(self):
        self.log_file = Path(__file__).parent / 'logs' / 'operations.json'
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def is_available(self) -> bool:
        """自记录总是可用"""
        return True
    
    def get_description(self) -> str:
        return "自记录模式 (Operation Logger)"
    
    def get_capabilities(self) -> List[str]:
        return ['who', 'what', 'when', 'where', 'how']
    
    def get_operations(self, hours: int = 24) -> List[OperationRecord]:
        """从自记录日志提取操作记录"""
        operations = []
        
        if not self.log_file.exists():
            return operations
        
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        entry = json.loads(line)
                        
                        # 检查时间戳
                        op_time = datetime.fromisoformat(entry.get('timestamp', ''))
                        if op_time < cutoff_time:
                            continue
                        
                        # 转换为OperationRecord
                        record = OperationRecord(
                            timestamp=entry.get('timestamp', ''),
                            user=entry.get('user', 'unknown'),
                            session_id=entry.get('session_id', ''),
                            command=entry.get('command', ''),
                            exit_code=entry.get('exit_code', 0),
                            duration_seconds=entry.get('duration_seconds', 0),
                            working_directory=entry.get('working_directory', ''),
                            hostname=entry.get('hostname', platform.node()),
                            source_ip=entry.get('source_ip', ''),
                            action_type=entry.get('action_type', 'execute'),
                            purpose=entry.get('purpose', 'unknown'),
                            target_object=entry.get('target_object', ''),
                            object_type=entry.get('object_type', 'unknown')
                        )
                        
                        operations.append(record)
                        
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
        
        except Exception as e:
            print(f"读取自记录日志失败: {e}")
        
        return operations
    
    def record_operation(self, operation: OperationRecord) -> bool:
        """记录单个操作"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                json.dump(operation.to_dict(), f, ensure_ascii=False)
                f.write('\n')
            return True
        except Exception as e:
            print(f"记录操作失败: {e}")
            return False


# 全局日志源管理器实例
log_source_manager = LogSourceManager()


def get_log_source_manager() -> LogSourceManager:
    """获取日志源管理器实例"""
    return log_source_manager