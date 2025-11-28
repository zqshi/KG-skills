#!/usr/bin/env python3
"""
自优化调度器
周期性执行Skill性能分析和自动优化
"""

import os
import sys
import time
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import schedule
import threading

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from self_optimization.optimization_engine import (
    SkillOptimizationEngine, SkillPerformanceMetrics, OptimizationRecommendation
)
from plugins.workflow_analyzer.scheduler import WorkflowScheduler


class SelfOptimizationScheduler:
    """自优化调度器类"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.optimization_engine = SkillOptimizationEngine(self.config.get('optimization', {}))
        self.workflow_scheduler = WorkflowScheduler(config_path)
        self.running = False
        self.scheduler_thread = None
        self.daily_thread = None
        self.weekly_thread = None
        self.monthly_thread = None
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent / 'config' / 'self_optimization.yaml'
        
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
            'self_optimization': {
                'enabled': True,
                'schedules': {
                    'daily': {
                        'enabled': True,
                        'execution_time': '01:00',
                        'tasks': ['health_check', 'metrics_collection']
                    },
                    'weekly': {
                        'enabled': True,
                        'day_of_week': 0,  # 周一
                        'execution_time': '02:00',
                        'tasks': ['performance_analysis', 'trend_analysis']
                    },
                    'monthly': {
                        'enabled': True,
                        'day_of_month': 1,  # 每月1号
                        'execution_time': '03:00',
                        'tasks': ['deep_optimization', 'template_update', 'documentation_review']
                    }
                },
                'optimization': {
                    'auto_apply': False,
                    'require_confirmation': True,
                    'min_health_score': 60,
                    'min_confidence': 0.7,
                    'max_optimizations_per_run': 5
                },
                'monitoring': {
                    'log_retention_days': 90,
                    'metrics_history_days': 365,
                    'alert_thresholds': {
                        'health_score_drop': 10,  # 健康度下降超过10分告警
                        'error_rate_spike': 0.05,  # 错误率上升超过5%告警
                        'satisfaction_drop': 0.5   # 满意度下降超过0.5告警
                    }
                }
            },
            'workflow_analysis': {
                'enabled': True,
                'interval_days': 7,  # 每周执行一次
                'execution_time': '02:30'
            }
        }
    
    def start(self):
        """启动自优化调度器"""
        if self.running:
            print("自优化调度器已在运行中")
            return
        
        if not self.config.get('self_optimization', {}).get('enabled', False):
            print("自优化功能未启用")
            return
        
        print("🚀 启动Skill自优化调度器")
        
        # 配置调度任务
        self._schedule_tasks()
        
        self.running = True
        
        # 启动调度器线程
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        # 启动工作流调度器（如果启用）
        if self.config.get('workflow_analysis', {}).get('enabled', False):
            self.workflow_scheduler.start()
            print("工作流分析调度器已启动")
        
        print("✅ 自优化调度器启动成功")
        print(f"📊 日常健康检查: {self.config['self_optimization']['schedules']['daily']['execution_time']}")
        print(f"📈 周度性能分析: 每周一 {self.config['self_optimization']['schedules']['weekly']['execution_time']}")
        print(f"🎯 月度深度优化: 每月1号 {self.config['self_optimization']['schedules']['monthly']['execution_time']}")
    
    def _schedule_tasks(self):
        """配置调度任务"""
        schedules = self.config['self_optimization']['schedules']
        
        # 日常任务
        if schedules['daily']['enabled']:
            daily_time = schedules['daily']['execution_time']
            hour, minute = map(int, daily_time.split(':'))
            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(self._execute_daily_tasks)
            print(f"📅 日常任务已调度: 每天 {daily_time}")
        
        # 周度任务
        if schedules['weekly']['enabled']:
            weekly_config = schedules['weekly']
            weekly_time = weekly_config['execution_time']
            hour, minute = map(int, weekly_time.split(':'))
            day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            day_name = day_names[weekly_config['day_of_week']]
            getattr(schedule.every(), day_name).at(f"{hour:02d}:{minute:02d}").do(self._execute_weekly_tasks)
            print(f"📅 周度任务已调度: 每周{day_name} {weekly_time}")
        
        # 月度任务
        if schedules['monthly']['enabled']:
            monthly_time = schedules['monthly']['execution_time']
            hour, minute = map(int, monthly_time.split(':'))
            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(self._execute_monthly_tasks)
            print(f"📅 月度任务已调度: 每月1号 {monthly_time}")
    
    def _run_scheduler(self):
        """运行调度器主循环"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
            except Exception as e:
                print(f"调度器执行出错: {e}")
                time.sleep(300)  # 出错后等待5分钟继续
    
    def _execute_daily_tasks(self):
        """执行日常任务"""
        try:
            print("开始执行日常健康检查任务")
            start_time = datetime.now()
            
            # 收集性能指标
            metrics_list = self.optimization_engine.tracker.collect_metrics(days=1)
            
            if not metrics_list:
                print("没有Skill使用数据")
                return
            
            # 健康检查
            health_issues = self._check_health(metrics_list)
            
            # 告警（如果有严重问题）
            if health_issues:
                self._send_alerts(health_issues)
            
            # 记录日志
            self._log_daily_check(metrics_list, health_issues)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"日常健康检查完成，耗时 {duration:.2f} 秒")
            
        except Exception as e:
            print(f"执行日常任务失败: {e}")
    
    def _execute_weekly_tasks(self):
        """执行周度任务"""
        try:
            print("开始执行周度性能分析任务")
            start_time = datetime.now()
            
            # 分析Skill性能
            metrics_list, recommendations = self.optimization_engine.analyze_skill_performance(days=7)
            
            if not metrics_list:
                print("没有Skill性能数据")
                return
            
            # 生成报告
            report_file = self._get_report_path('weekly')
            report = self.optimization_engine.generate_optimization_report(
                metrics_list, recommendations, str(report_file)
            )
            
            # 趋势分析
            trends = self._analyze_trends(metrics_list)
            
            # 自动优化（如果启用）
            if self.config['self_optimization']['optimization'].get('auto_apply', False):
                self._auto_optimize(recommendations)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"周度性能分析完成，耗时 {duration:.2f} 秒")
            print(f"报告已保存: {report_file}")
            
        except Exception as e:
            print(f"执行周度任务失败: {e}")
    
    def _execute_monthly_tasks(self):
        """执行月度任务"""
        # 检查是否是每月1号
        if datetime.now().day != 1:
            return
        
        try:
            print("开始执行月度深度优化任务")
            start_time = datetime.now()
            
            # 深度性能分析
            metrics_list, recommendations = self.optimization_engine.analyze_skill_performance(days=30)
            
            if not metrics_list:
                print("没有Skill性能数据")
                return
            
            # 生成深度报告
            report_file = self._get_report_path('monthly')
            report = self.optimization_engine.generate_optimization_report(
                metrics_list, recommendations, str(report_file)
            )
            
            # 模板更新
            self._update_templates(metrics_list)
            
            # 文档审查和更新
            self._review_documentation(recommendations)
            
            # 清理旧数据
            self._cleanup_old_data()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"月度深度优化完成，耗时 {duration:.2f} 秒")
            print(f"报告已保存: {report_file}")
            
        except Exception as e:
            print(f"执行月度任务失败: {e}")
    
    def _check_health(self, metrics_list: List[SkillPerformanceMetrics]) -> List[Dict[str, Any]]:
        """健康检查"""
        health_issues = []
        thresholds = self.config['self_optimization']['monitoring']['alert_thresholds']
        
        for metrics in metrics_list:
            issues = []
            
            # 健康度过低
            if metrics.health_score < self.config['self_optimization']['optimization']['min_health_score']:
                issues.append({
                    'type': 'low_health',
                    'severity': 'high',
                    'value': metrics.health_score
                })
            
            # 错误率过高
            if metrics.error_rate > 0.1:
                issues.append({
                    'type': 'high_error_rate',
                    'severity': 'high',
                    'value': metrics.error_rate
                })
            
            if issues:
                health_issues.append({
                    'skill_name': metrics.skill_name,
                    'issues': issues
                })
        
        return health_issues
    
    def _send_alerts(self, health_issues: List[Dict[str, Any]]):
        """发送告警"""
        print("🚨 发现健康度问题:")
        for issue in health_issues:
            print(f"  - Skill: {issue['skill_name']}")
            for problem in issue['issues']:
                print(f"    {problem['type']}: {problem['value']}")
        
        # 这里可以集成邮件、Slack等告警通知
        alert_file = Path(__file__).parent / 'alerts' / f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        alert_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(alert_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'issues': health_issues
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存告警失败: {e}")
    
    def _log_daily_check(self, metrics_list: List[SkillPerformanceMetrics], 
                        health_issues: List[Dict[str, Any]]):
        """记录日常检查日志"""
        log_file = Path(__file__).parent / 'logs' / 'daily_check.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'total_skills': len(metrics_list),
            'average_health': sum(m.health_score for m in metrics_list) / len(metrics_list) if metrics_list else 0,
            'health_issues': len(health_issues),
            'details': [m.to_dict() for m in metrics_list]
        }
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"记录日常检查日志失败: {e}")
    
    def _analyze_trends(self, metrics_list: List[SkillPerformanceMetrics]) -> List[Dict[str, Any]]:
        """分析趋势"""
        # 这里可以实现趋势分析逻辑
        print("分析Skill性能趋势...")
        return []
    
    def _auto_optimize(self, recommendations: List[OptimizationRecommendation]):
        """自动优化"""
        print("开始自动优化...")
        
        max_optimizations = self.config['self_optimization']['optimization'].get('max_optimizations_per_run', 5)
        applied_count = 0
        
        for rec in recommendations[:max_optimizations]:
            if rec.priority == 'high':
                print(f"应用高优先级优化: {rec.skill_name}")
                if self.optimization_engine.apply_optimization(rec):
                    applied_count += 1
        
        print(f"自动优化完成: 应用 {applied_count} 个优化")
    
    def _update_templates(self, metrics_list: List[SkillPerformanceMetrics]):
        """更新模板"""
        print("更新Skill模板...")
        # 这里可以实现模板更新逻辑
    
    def _review_documentation(self, recommendations: List[OptimizationRecommendation]):
        """审查文档"""
        print("审查和更新文档...")
        # 这里可以实现文档审查逻辑
    
    def _cleanup_old_data(self):
        """清理旧数据"""
        print("清理旧数据...")
        
        retention_days = self.config['self_optimization']['monitoring']['log_retention_days']
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # 清理日志文件
        logs_dir = Path(__file__).parent / 'logs'
        if logs_dir.exists():
            for log_file in logs_dir.glob('*.log'):
                try:
                    if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff_date:
                        log_file.unlink()
                        print(f"删除旧日志: {log_file.name}")
                except Exception as e:
                    print(f"删除日志失败: {e}")
    
    def _get_report_path(self, report_type: str) -> Path:
        """获取报告路径"""
        report_dir = Path(__file__).parent / 'reports' / report_type
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return report_dir / f"{report_type}_report_{timestamp}.json"
    
    def stop(self):
        """停止调度器"""
        if not self.running:
            print("自优化调度器未在运行")
            return
        
        self.running = False
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        # 停止工作流调度器
        self.workflow_scheduler.stop()
        
        print("自优化调度器已停止")
    
    def run_once(self, task_type: str = 'weekly'):
        """立即执行一次任务"""
        print(f"执行单次{task_type}任务")
        
        if task_type == 'daily':
            self._execute_daily_tasks()
        elif task_type == 'weekly':
            self._execute_weekly_tasks()
        elif task_type == 'monthly':
            self._execute_monthly_tasks()
        else:
            print(f"未知的任务类型: {task_type}")
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        status = {
            'running': self.running,
            'next_runs': {}
        }
        
        if self.running:
            try:
                # 获取下一个日常任务
                next_run = schedule.next_run()
                if next_run:
                    status['next_runs']['daily'] = next_run.isoformat()
            except:
                pass
        
        return status


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Skill自优化调度器')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status', 'run-once', 'health-check'], 
                       help='操作命令')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--task-type', choices=['daily', 'weekly', 'monthly'], 
                       default='weekly', help='任务类型（run-once时使用）')
    
    args = parser.parse_args()
    
    # 创建调度器
    scheduler = SelfOptimizationScheduler(config_path=args.config)
    
    if args.action == 'start':
        scheduler.start()
        
        try:
            print("自优化调度器已启动，按 Ctrl+C 停止...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n收到停止信号...")
            scheduler.stop()
    
    elif args.action == 'stop':
        print("停止命令已发送（需要手动停止进程）")
    
    elif args.action == 'restart':
        print("重启自优化调度器...")
        scheduler.stop()
        time.sleep(2)
        scheduler.start()
        
        try:
            print("自优化调度器已重启，按 Ctrl+C 停止...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n收到停止信号...")
            scheduler.stop()
    
    elif args.action == 'status':
        status = scheduler.get_status()
        if status['running']:
            print("自优化调度器运行中")
            if status['next_runs']:
                for task_type, next_run in status['next_runs'].items():
                    print(f"下次{task_type}任务: {next_run}")
        else:
            print("自优化调度器未运行")
    
    elif args.action == 'run-once':
        scheduler.run_once(args.task_type)
    
    elif args.action == 'health-check':
        # 执行健康检查
        metrics_list = scheduler.optimization_engine.tracker.collect_metrics(days=1)
        health_issues = scheduler._check_health(metrics_list)
        
        if health_issues:
            print(f"发现 {len(health_issues)} 个健康度问题")
            for issue in health_issues:
                print(f"  - {issue['skill_name']}: {len(issue['issues'])} 个问题")
        else:
            print("所有Skill健康度正常")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()