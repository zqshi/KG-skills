#!/usr/bin/env python3
"""
操作日志记录器
记录用户操作，为工作流分析提供数据源
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import subprocess
import signal
import atexit

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models import OperationRecord
from log_source_manager import get_log_source_manager


class OperationLogger:
    """操作日志记录器类"""
    
    def __init__(self, log_dir: Optional[str] = None):
        if log_dir is None:
            log_dir = Path(__file__).parent / 'logs'
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = self.log_dir / 'operations.json'
        self.session_id = self._generate_session_id()
        self.recording = False
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        atexit.register(self._cleanup)
        
        print(f"操作日志记录器初始化，会话ID: {self.session_id}")
    
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.getpid()}"
    
    def _signal_handler(self, signum, frame):
        """信号处理"""
        print(f"收到信号 {signum}，停止记录")
        self.stop()
        sys.exit(0)
    
    def _cleanup(self):
        """清理资源"""
        if self.recording:
            self.stop()
    
    def start(self):
        """开始记录操作"""
        if self.recording:
            print("记录器已在运行中")
            return
        
        self.recording = True
        print("开始记录操作日志")
        
        # 记录启动事件
        self._log_event('session_start', {
            'session_id': self.session_id,
            'pid': os.getpid(),
            'user': os.getenv('USER', 'unknown')
        })
    
    def stop(self):
        """停止记录操作"""
        if not self.recording:
            return
        
        self.recording = False
        
        # 记录停止事件
        self._log_event('session_end', {
            'session_id': self.session_id
        })
        
        print("停止记录操作日志")
    
    def record_command(self, command: str, exit_code: int = 0, 
                      duration: float = 0.0, output: Optional[str] = None):
        """记录命令执行"""
        if not self.recording:
            return
        
        try:
            operation = {
                'timestamp': datetime.now().isoformat(),
                'session_id': self.session_id,
                'command': command,
                'exit_code': exit_code,
                'duration_seconds': duration,
                'working_directory': str(Path.cwd()),
                'user': os.getenv('USER', 'unknown'),
                'hostname': os.getenv('HOSTNAME', 'unknown')
            }
            
            if output:
                operation['output'] = output[:1000]  # 限制输出长度
            
            self._write_log_entry(operation)
            
        except Exception as e:
            print(f"记录命令失败: {e}")
    
    def _log_event(self, event_type: str, data: Dict[str, Any]):
        """记录事件"""
        try:
            event = {
                'timestamp': datetime.now().isoformat(),
                'session_id': self.session_id,
                'event_type': event_type,
                'data': data
            }
            
            self._write_log_entry(event)
            
        except Exception as e:
            print(f"记录事件失败: {e}")
    
    def _write_log_entry(self, entry: Dict[str, Any]):
        """写入日志条目"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                json.dump(entry, f, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            print(f"写入日志文件失败: {e}")
    
    def wrap_shell_command(self, command: str) -> tuple:
        """包装shell命令，记录执行信息"""
        if not self.recording:
            return None, None
        
        start_time = datetime.now()
        
        try:
            # 执行命令
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # 记录命令
            self.record_command(
                command=command,
                exit_code=result.returncode,
                duration=duration,
                output=result.stdout if result.returncode == 0 else result.stderr
            )
            
            return result.returncode, result.stdout if result.returncode == 0 else result.stderr
            
        except subprocess.TimeoutExpired:
            duration = (datetime.now() - start_time).total_seconds()
            self.record_command(
                command=command,
                exit_code=-1,
                duration=duration,
                output="Command timed out"
            )
            return -1, "Command timed out"
        
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self.record_command(
                command=command,
                exit_code=-1,
                duration=duration,
                output=str(e)
            )
            return -1, str(e)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """获取会话统计"""
        try:
            if not self.log_file.exists():
                return {}
            
            operations = []
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            op = json.loads(line)
                            if op.get('session_id') == self.session_id:
                                operations.append(op)
                        except json.JSONDecodeError:
                            continue
            
            commands = [op for op in operations if 'command' in op]
            events = [op for op in operations if 'event_type' in op]
            
            return {
                'session_id': self.session_id,
                'total_commands': len(commands),
                'total_events': len(events),
                'start_time': min((op['timestamp'] for op in operations), default=None),
                'end_time': max((op['timestamp'] for op in operations), default=None),
                'success_rate': len([c for c in commands if c.get('exit_code') == 0]) / len(commands) if commands else 0
            }
            
        except Exception as e:
            print(f"获取会话统计失败: {e}")
            return {}
    
    def rotate_log_file(self):
        """轮转日志文件"""
        try:
            if not self.log_file.exists():
                return
            
            # 检查文件大小
            file_size = self.log_file.stat().st_size
            max_size = 10 * 1024 * 1024  # 10MB
            
            if file_size < max_size:
                return
            
            # 轮转日志
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            rotated_file = self.log_dir / f'operations_{timestamp}.json'
            
            self.log_file.rename(rotated_file)
            print(f"日志文件已轮转: {rotated_file}")
            
        except Exception as e:
            print(f"日志轮转失败: {e}")


class ShellWrapper:
    """Shell包装器类"""
    
    def __init__(self, logger: OperationLogger):
        self.logger = logger
        self.original_commands = []
    
    def wrap_interactive_shell(self):
        """包装交互式shell"""
        import readline
        
        print("📝 操作日志记录模式已启用")
        print("输入 'exit' 或按 Ctrl+D 退出")
        print("=" * 50)
        
        while True:
            try:
                # 读取命令
                command = input(f"{os.getcwd()} $ ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['exit', 'quit']:
                    break
                
                # 记录原始命令
                self.original_commands.append(command)
                
                # 执行并记录
                exit_code, output = self.logger.wrap_shell_command(command)
                
                # 显示输出
                if output:
                    print(output)
                
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\n^C")
                continue
            except Exception as e:
                print(f"错误: {e}")
        
        print("\n操作日志记录结束")
    
    def wrap_command_execution(self, command: str):
        """包装单次命令执行"""
        print(f"📝 执行命令: {command}")
        
        exit_code, output = self.logger.wrap_shell_command(command)
        
        if output:
            print(output)
        
        return exit_code


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='操作日志记录器')
    parser.add_argument('mode', choices=['interactive', 'wrap', 'daemon'], 
                       help='运行模式')
    parser.add_argument('--command', '-c', help='要包装的命令（wrap模式）')
    parser.add_argument('--log-dir', help='日志目录')
    
    args = parser.parse_args()
    
    # 创建记录器
    logger = OperationLogger(log_dir=args.log_dir)
    
    if args.mode == 'interactive':
        # 交互式模式
        logger.start()
        
        try:
            wrapper = ShellWrapper(logger)
            wrapper.wrap_interactive_shell()
        finally:
            logger.stop()
        
        # 显示统计
        stats = logger.get_session_stats()
        if stats:
            print(f"\n会话统计:")
            print(f"  命令数: {stats['total_commands']}")
            print(f"  成功率: {stats['success_rate']:.1%}")
    
    elif args.mode == 'wrap':
        # 包装单次命令
        if not args.command:
            print("错误: wrap模式需要 --command 参数")
            sys.exit(1)
        
        logger.start()
        
        try:
            wrapper = ShellWrapper(logger)
            exit_code = wrapper.wrap_command_execution(args.command)
            sys.exit(exit_code)
        finally:
            logger.stop()
    
    elif args.mode == 'daemon':
        # 守护进程模式（监听系统命令）
        print("守护进程模式未实现，敬请期待")
        sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()