#!/usr/bin/env python3
"""
工作流分析调度器
周期性执行工作流分析和Skill自动创建
"""

import os
import sys
import time
import yaml
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import schedule
import threading

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from plugins.workflow_analyzer.analyzer import WorkflowAnalyzer


class WorkflowScheduler:
    """工作流分析调度器类"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.analyzer = WorkflowAnalyzer(config_path)
        self.running = False
        self.scheduler_thread = None
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent / 'config' / 'workflow_config.yaml'
        
        config_file = Path(config_path)
        if not config_file.exists():
            print(f"配置文件不存在，使用默认配置: {config_path}")
            return self._get_default_config()
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
            print(f"配置文件加载成功: {config_path}")
            return config
        except Exception as e:
            print(f"配置文件加载失败: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            'scheduler': {
                'enabled': True,
                'interval_days': 30,
                'execution_time': '02:00',
                'timezone': 'Asia/Shanghai',
                'work_days': [0, 1, 2, 3, 4]
            },
            'analysis': {
                'cycle_days': 30,
                'frequency_threshold': 5
            },
            'skill_generation': {
                'auto_create': False,
                'require_confirmation': True,
                'min_confidence': 0.6
            }
        }
    
    def start(self):
        """启动调度器"""
        if self.running:
            print("调度器已在运行中")
            return
        
        scheduler_config = self.config.get('scheduler', {})
        
        if not scheduler_config.get('enabled', False):
            print("调度器未启用")
            return
        
        interval_days = scheduler_config.get('interval_days', 30)
        execution_time = scheduler_config.get('execution_time', '02:00')
        
        print(f"启动工作流分析调度器")
        print(f"执行间隔: {interval_days}天")
        print(f"执行时间: {execution_time}")
        
        # 配置调度任务
        self._schedule_task(interval_days, execution_time)
        
        self.running = True
        
        # 启动调度器线程
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        print("调度器启动成功")
    
    def _schedule_task(self, interval_days: int, execution_time: str):
        """配置调度任务"""
        hour, minute = map(int, execution_time.split(':'))
        
        if interval_days == 1:
            # 每天执行
            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(self._execute_analysis)
        elif interval_days == 7:
            # 每周执行
            schedule.every().week.at(f"{hour:02d}:{minute:02d}").do(self._execute_analysis)
        else:
            # 自定义间隔
            schedule.every(interval_days).days.at(f"{hour:02d}:{minute:02d}").do(self._execute_analysis)
        
        print(f"任务已调度: 每{interval_days}天 {execution_time} 执行")
    
    def _run_scheduler(self):
        """运行调度器主循环"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
            except Exception as e:
                print(f"调度器执行出错: {e}")
                time.sleep(300)  # 出错后等待5分钟继续
    
    def _execute_analysis(self):
        """执行工作流分析"""
        try:
            print("开始执行周期性工作流分析")
            
            # 记录开始时间
            start_time = datetime.now()
            
            # 加载操作日志
            operations = self.analyzer.load_operations_log()
            
            if not operations:
                print("没有操作日志数据，跳过分析")
                return
            
            # 过滤操作
            filtered_ops = self.analyzer.filter_operations(operations)
            
            if not filtered_ops:
                print("过滤后没有有效操作数据，跳过分析")
                return
            
            # 分析工作流
            workflows = self.analyzer.analyze_workflows(filtered_ops)
            
            if not workflows:
                print("未识别出高频工作流")
                return
            
            # 生成推荐
            recommendations = self.analyzer.generate_skill_recommendations(workflows)
            
            if not recommendations:
                print("没有Skill创建推荐")
                return
            
            print(f"识别出 {len(recommendations)} 个Skill创建推荐")
            
            # 生成报告
            report_dir = Path(__file__).parent / 'reports'
            report_dir.mkdir(parents=True, exist_ok=True)
            
            report_file = report_dir / f"workflow_report_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
            report = self.analyzer.generate_report(str(report_file))
            
            # 自动创建Skill（如果启用）
            if self.config['skill_generation'].get('auto_create', False):
                self._auto_create_skills(recommendations)
            
            # 记录完成
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"周期性分析完成，耗时 {duration:.2f} 秒")
            print(f"报告已保存: {report_file}")
            
        except Exception as e:
            print(f"执行分析任务失败: {e}")
    
    def _auto_create_skills(self, recommendations: list):
        """自动创建Skill"""
        print("开始自动创建Skill...")
        
        created_count = 0
        skipped_count = 0
        
        for rec in recommendations:
            try:
                # 检查置信度
                if rec['confidence'] < self.config['skill_generation'].get('min_confidence', 0.6):
                    print(f"跳过低置信度推荐: {rec['skill_name']} (置信度: {rec['confidence']:.2%})")
                    skipped_count += 1
                    continue
                
                # 检查是否需要确认
                if self.config['skill_generation'].get('require_confirmation', True):
                    print(f"需要手动确认: {rec['skill_name']}")
                    skipped_count += 1
                    continue
                
                # 创建Skill
                if self.analyzer.create_skill_from_workflow(rec):
                    created_count += 1
                    print(f"自动创建Skill成功: {rec['skill_name']}")
                else:
                    print(f"自动创建Skill失败: {rec['skill_name']}")
                    skipped_count += 1
                    
            except Exception as e:
                print(f"自动创建Skill出错: {rec['skill_name']} - {e}")
                skipped_count += 1
        
        print(f"自动创建完成: 成功 {created_count} 个，跳过 {skipped_count} 个")
    
    def stop(self):
        """停止调度器"""
        if not self.running:
            print("调度器未在运行")
            return
        
        self.running = False
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        print("调度器已停止")
    
    def run_once(self):
        """立即执行一次分析"""
        print("执行单次工作流分析")
        self._execute_analysis()
    
    def get_next_run_time(self) -> Optional[datetime]:
        """获取下次执行时间"""
        if not self.running:
            return None
        
        try:
            # 获取下一个计划任务
            next_run = schedule.next_run()
            if next_run:
                return next_run
        except:
            pass
        
        return None


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='工作流分析调度器')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status', 'run-once'], 
                       help='操作命令')
    parser.add_argument('--config', help='配置文件路径')
    
    args = parser.parse_args()
    
    # 创建调度器
    scheduler = WorkflowScheduler(config_path=args.config)
    
    if args.action == 'start':
        scheduler.start()
        
        try:
            print("调度器已启动，按 Ctrl+C 停止...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n收到停止信号...")
            scheduler.stop()
    
    elif args.action == 'stop':
        print("停止命令已发送（需要手动停止进程）")
    
    elif args.action == 'restart':
        print("重启调度器...")
        scheduler.stop()
        time.sleep(2)
        scheduler.start()
        
        try:
            print("调度器已重启，按 Ctrl+C 停止...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n收到停止信号...")
            scheduler.stop()
    
    elif args.action == 'status':
        if scheduler.running:
            next_run = scheduler.get_next_run_time()
            if next_run:
                print(f"调度器运行中，下次执行: {next_run}")
            else:
                print("调度器运行中，但无计划任务")
        else:
            print("调度器未运行")
    
    elif args.action == 'run-once':
        scheduler.run_once()
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()