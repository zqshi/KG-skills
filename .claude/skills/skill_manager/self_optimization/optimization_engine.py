#!/usr/bin/env python3
"""
Skill自优化引擎
基于用户行为数据和性能指标，自动优化现有Skill
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import OperationRecord


@dataclass
class SkillPerformanceMetrics:
    """Skill性能指标"""
    skill_name: str
    period_start: datetime
    period_end: datetime
    
    # 使用指标
    total_calls: int = 0
    success_calls: int = 0
    failed_calls: int = 0
    avg_duration: float = 0.0
    total_duration: float = 0.0
    
    # 质量指标
    user_satisfaction: float = 0.0  # 1-5分
    satisfaction_count: int = 0
    error_rate: float = 0.0
    timeout_rate: float = 0.0
    
    # 价值指标
    time_saved: float = 0.0  # 分钟
    user_adoption_rate: float = 0.0  # 采用率
    
    # 健康度
    health_score: float = 0.0  # 0-100分
    
    def calculate_health_score(self) -> float:
        """计算健康度分数"""
        if self.total_calls == 0:
            return 0.0
        
        # 成功率权重 40%
        success_rate = self.success_calls / self.total_calls if self.total_calls > 0 else 0
        success_score = success_rate * 40
        
        # 用户满意度权重 30%
        satisfaction_score = (self.user_satisfaction / 5.0) * 30 if self.user_satisfaction > 0 else 0
        
        # 采用率权重 20%
        adoption_score = self.user_adoption_rate * 20
        
        # 性能权重 10%
        performance_score = max(0, 10 - (self.avg_duration / 10))  # 假设10秒为满分
        
        self.health_score = success_score + satisfaction_score + adoption_score + performance_score
        return self.health_score
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'skill_name': self.skill_name,
            'period_start': self.period_start.isoformat(),
            'period_end': self.period_end.isoformat(),
            'total_calls': self.total_calls,
            'success_calls': self.success_calls,
            'failed_calls': self.failed_calls,
            'avg_duration': self.avg_duration,
            'total_duration': self.total_duration,
            'user_satisfaction': self.user_satisfaction,
            'satisfaction_count': self.satisfaction_count,
            'error_rate': self.error_rate,
            'timeout_rate': self.timeout_rate,
            'time_saved': self.time_saved,
            'user_adoption_rate': self.user_adoption_rate,
            'health_score': self.health_score
        }


@dataclass
class OptimizationRecommendation:
    """优化建议"""
    skill_name: str
    recommendation_type: str  # parameter, template, documentation, enhancement
    priority: str  # high, medium, low
    description: str
    expected_impact: str
    implementation_effort: str  # low, medium, high
    specific_actions: List[str] = field(default_factory=list)
    current_metrics: Optional[Dict[str, Any]] = None
    target_metrics: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'skill_name': self.skill_name,
            'recommendation_type': self.recommendation_type,
            'priority': self.priority,
            'description': self.description,
            'expected_impact': self.expected_impact,
            'implementation_effort': self.implementation_effort,
            'specific_actions': self.specific_actions,
            'current_metrics': self.current_metrics,
            'target_metrics': self.target_metrics
        }


class SkillPerformanceTracker:
    """Skill性能追踪器"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_file = self.data_dir / 'skill_metrics.json'
        self.usage_log_file = self.data_dir / 'skill_usage.log'
    
    def record_skill_usage(self, skill_name: str, operation: OperationRecord, 
                          user_satisfaction: Optional[int] = None):
        """记录Skill使用"""
        usage_data = {
            'timestamp': datetime.now().isoformat(),
            'skill_name': skill_name,
            'operation': operation.to_dict(),
            'user_satisfaction': user_satisfaction,
            'success': operation.is_successful()
        }
        
        try:
            with open(self.usage_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(usage_data, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"记录Skill使用失败: {e}")
    
    def collect_metrics(self, skill_name: Optional[str] = None, 
                       days: int = 30) -> List[SkillPerformanceMetrics]:
        """收集性能指标"""
        if not self.usage_log_file.exists():
            return []
        
        cutoff_time = datetime.now() - timedelta(days=days)
        skill_metrics = {}
        
        try:
            with open(self.usage_log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        usage_data = json.loads(line)
                        op_time = datetime.fromisoformat(usage_data['timestamp'])
                        
                        if op_time < cutoff_time:
                            continue
                        
                        name = usage_data['skill_name']
                        if skill_name and name != skill_name:
                            continue
                        
                        if name not in skill_metrics:
                            skill_metrics[name] = SkillPerformanceMetrics(
                                skill_name=name,
                                period_start=cutoff_time,
                                period_end=datetime.now()
                            )
                        
                        self._update_metrics(skill_metrics[name], usage_data)
                        
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
        
        except Exception as e:
            print(f"收集性能指标失败: {e}")
        
        # 计算健康度
        for metrics in skill_metrics.values():
            metrics.calculate_health_score()
        
        return list(skill_metrics.values())
    
    def _update_metrics(self, metrics: SkillPerformanceMetrics, usage_data: Dict[str, Any]):
        """更新指标"""
        metrics.total_calls += 1
        
        if usage_data.get('success', False):
            metrics.success_calls += 1
        else:
            metrics.failed_calls += 1
        
        operation = usage_data.get('operation', {})
        duration = operation.get('duration_seconds', 0)
        metrics.total_duration += duration
        
        satisfaction = usage_data.get('user_satisfaction')
        if satisfaction:
            metrics.satisfaction_count += 1
            # 计算移动平均
            total_satisfaction = metrics.user_satisfaction * (metrics.satisfaction_count - 1) + satisfaction
            metrics.user_satisfaction = total_satisfaction / metrics.satisfaction_count
        
        # 计算平均时长
        if metrics.total_calls > 0:
            metrics.avg_duration = metrics.total_duration / metrics.total_calls
        
        # 计算错误率
        metrics.error_rate = metrics.failed_calls / metrics.total_calls
        
        # 估算节省时间（简化计算）
        metrics.time_saved = metrics.success_calls * 5  # 假设每次成功节省5分钟


class SkillDeviationDetector:
    """Skill偏差检测器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.thresholds = self.config.get('thresholds', {
            'health_score_min': 70.0,
            'error_rate_max': 0.1,
            'timeout_rate_max': 0.05,
            'satisfaction_min': 3.5,
            'adoption_rate_min': 0.3
        })
    
    def detect_deviations(self, metrics: SkillPerformanceMetrics) -> List[Dict[str, Any]]:
        """检测偏差"""
        deviations = []
        
        # 健康度检查
        if metrics.health_score < self.thresholds['health_score_min']:
            deviations.append({
                'type': 'low_health_score',
                'severity': 'high',
                'current_value': metrics.health_score,
                'threshold': self.thresholds['health_score_min'],
                'description': f"健康度低于阈值: {metrics.health_score:.1f} < {self.thresholds['health_score_min']}"
            })
        
        # 错误率检查
        if metrics.error_rate > self.thresholds['error_rate_max']:
            deviations.append({
                'type': 'high_error_rate',
                'severity': 'high',
                'current_value': metrics.error_rate,
                'threshold': self.thresholds['error_rate_max'],
                'description': f"错误率过高: {metrics.error_rate:.1%} > {self.thresholds['error_rate_max']:.1%}"
            })
        
        # 用户满意度检查
        if metrics.user_satisfaction > 0 and metrics.user_satisfaction < self.thresholds['satisfaction_min']:
            deviations.append({
                'type': 'low_satisfaction',
                'severity': 'medium',
                'current_value': metrics.user_satisfaction,
                'threshold': self.thresholds['satisfaction_min'],
                'description': f"用户满意度较低: {metrics.user_satisfaction:.1f} < {self.thresholds['satisfaction_min']}"
            })
        
        # 采用率检查
        if metrics.user_adoption_rate < self.thresholds['adoption_rate_min']:
            deviations.append({
                'type': 'low_adoption',
                'severity': 'medium',
                'current_value': metrics.user_adoption_rate,
                'threshold': self.thresholds['adoption_rate_min'],
                'description': f"采用率较低: {metrics.user_adoption_rate:.1%} < {self.thresholds['adoption_rate_min']:.1%}"
            })
        
        return deviations
    
    def analyze_trends(self, historical_metrics: List[SkillPerformanceMetrics]) -> List[Dict[str, Any]]:
        """分析趋势"""
        if len(historical_metrics) < 2:
            return []
        
        trends = []
        recent = historical_metrics[-1]
        previous = historical_metrics[-2]
        
        # 健康度趋势
        health_trend = recent.health_score - previous.health_score
        if abs(health_trend) > 5:  # 变化超过5分
            trends.append({
                'type': 'health_trend',
                'direction': 'declining' if health_trend < 0 else 'improving',
                'change': health_trend,
                'description': f"健康度{'下降' if health_trend < 0 else '提升'} {abs(health_trend):.1f} 分"
            })
        
        # 错误率趋势
        error_trend = recent.error_rate - previous.error_rate
        if abs(error_trend) > 0.02:  # 变化超过2%
            trends.append({
                'type': 'error_rate_trend',
                'direction': 'increasing' if error_trend > 0 else 'decreasing',
                'change': error_trend,
                'description': f"错误率{'上升' if error_trend > 0 else '下降'} {abs(error_trend):.1%}"
            })
        
        return trends


class SkillOptimizationEngine:
    """Skill优化引擎"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.tracker = SkillPerformanceTracker()
        self.deviation_detector = SkillDeviationDetector(config)

        # 优化策略配置
        self.optimization_strategies = {
            'parameter': self._optimize_parameters,
            'template': self._optimize_template,
            'documentation': self._optimize_documentation,
            'enhancement': self._enhance_functionality
        }
    
    def analyze_skill_performance(self, skill_name: Optional[str] = None, 
                                 days: int = 30) -> Tuple[List[SkillPerformanceMetrics], List[OptimizationRecommendation]]:
        """分析Skill性能"""
        # 收集指标
        metrics_list = self.tracker.collect_metrics(skill_name, days)
        
        recommendations = []
        
        for metrics in metrics_list:
            # 检测偏差
            deviations = self.deviation_detector.detect_deviations(metrics)
            
            if deviations:
                # 生成优化建议
                recs = self._generate_recommendations(metrics, deviations)
                recommendations.extend(recs)
        
        return metrics_list, recommendations
    
    def _generate_recommendations(self, metrics: SkillPerformanceMetrics, 
                                 deviations: List[Dict[str, Any]]) -> List[OptimizationRecommendation]:
        """生成优化建议"""
        recommendations = []
        
        for deviation in deviations:
            rec = self._create_recommendation(metrics, deviation)
            if rec:
                recommendations.append(rec)
        
        return recommendations
    
    def _create_recommendation(self, metrics: SkillPerformanceMetrics, 
                              deviation: Dict[str, Any]) -> Optional[OptimizationRecommendation]:
        """创建优化建议"""
        deviation_type = deviation['type']
        
        if deviation_type == 'low_health_score':
            return OptimizationRecommendation(
                skill_name=metrics.skill_name,
                recommendation_type='enhancement',
                priority='high',
                description='Skill整体健康度较低，需要全面优化',
                expected_impact='提升健康度20-30分',
                implementation_effort='high',
                specific_actions=[
                    '分析失败原因并修复',
                    '优化核心算法',
                    '改进错误处理',
                    '更新文档和示例'
                ],
                current_metrics=metrics.to_dict(),
                target_metrics={'health_score': 85.0}
            )
        
        elif deviation_type == 'high_error_rate':
            return OptimizationRecommendation(
                skill_name=metrics.skill_name,
                recommendation_type='parameter',
                priority='high',
                description='错误率过高，需要调整参数和错误处理',
                expected_impact='将错误率降低到5%以下',
                implementation_effort='medium',
                specific_actions=[
                    '增加输入验证',
                    '优化错误处理逻辑',
                    '添加重试机制',
                    '改进参数默认值'
                ],
                current_metrics=metrics.to_dict(),
                target_metrics={'error_rate': 0.05}
            )
        
        elif deviation_type == 'low_satisfaction':
            return OptimizationRecommendation(
                skill_name=metrics.skill_name,
                recommendation_type='documentation',
                priority='medium',
                description='用户满意度较低，需要改进文档和用户体验',
                expected_impact='提升用户满意度到4.0以上',
                implementation_effort='low',
                specific_actions=[
                    '简化使用说明',
                    '添加更多示例',
                    '改进输出格式',
                    '增加常见问题解答'
                ],
                current_metrics=metrics.to_dict(),
                target_metrics={'user_satisfaction': 4.0}
            )
        
        elif deviation_type == 'low_adoption':
            return OptimizationRecommendation(
                skill_name=metrics.skill_name,
                recommendation_type='enhancement',
                priority='medium',
                description='采用率较低，需要增加功能和改进推广',
                expected_impact='提升采用率到50%以上',
                implementation_effort='medium',
                specific_actions=[
                    '分析用户需求',
                    '增加缺失功能',
                    '改进推广策略',
                    '收集用户反馈'
                ],
                current_metrics=metrics.to_dict(),
                target_metrics={'user_adoption_rate': 0.5}
            )
        
        return None
    
    def _optimize_parameters(self, skill_name: str, metrics: SkillPerformanceMetrics) -> bool:
        """优化参数"""
        print(f"优化Skill参数: {skill_name}")

        try:
            # 查找Skill路径
            skill_path = Path('.claude/skills') / skill_name
            if not skill_path.exists():
                print(f"Skill路径不存在: {skill_path}")
                return False

            # 读取SKILL.md
            skill_md_path = skill_path / 'SKILL.md'
            if not skill_md_path.exists():
                print(f"SKILL.md不存在")
                return False

            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            changes_made = False

            # 基于错误率优化超时参数
            if metrics.error_rate > 0.1:
                print(f"  - 错误率过高({metrics.error_rate:.1%})，调整超时和重试参数")

                # 检查是否有超时配置
                if 'timeout' in content.lower() or 'retry' in content.lower():
                    # 增加超时时间建议
                    timeout_suggestion = "\n### 参数优化建议\n\n基于性能分析，建议调整以下参数:\n- `timeout`: 建议增加至 60 秒\n- `max_retries`: 建议设置为 3 次\n- `retry_delay`: 建议设置为 2 秒\n"

                    if '## 📋 输入规范' in content and '### 参数优化建议' not in content:
                        content = content.replace('## 📋 输入规范', timeout_suggestion + '\n## 📋 输入规范')
                        changes_made = True

            # 基于性能优化批处理参数
            if metrics.avg_duration > 10:
                print(f"  - 平均执行时间过长({metrics.avg_duration:.2f}秒)，建议启用批处理")

                batch_suggestion = "\n### 性能优化建议\n\n- 启用批处理模式以提升性能\n- `batch_size`: 建议设置为 100\n- `parallel_workers`: 建议设置为 4\n"

                if '## 🔧 高级功能' not in content and changes_made is False:
                    content += f"\n{batch_suggestion}\n"
                    changes_made = True

            # 基于用户反馈优化默认参数
            if metrics.user_satisfaction < 3.5 and metrics.satisfaction_count > 5:
                print(f"  - 用户满意度较低({metrics.user_satisfaction:.1f})，优化默认参数")

                # 添加用户友好的默认值建议
                default_suggestion = "\n### 默认参数优化\n\n基于用户反馈优化:\n- 增加输出详细度\n- 提供更友好的错误提示\n- 添加进度显示\n"

                if changes_made is False:
                    content += f"\n{default_suggestion}\n"
                    changes_made = True

            # 保存更新
            if changes_made:
                with open(skill_md_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ 参数优化建议已添加到文档")
                return True
            else:
                print(f"  ℹ️  当前参数配置良好，无需优化")
                return True

        except Exception as e:
            print(f"参数优化失败: {e}")
            return False
    
    def _optimize_template(self, skill_name: str, metrics: SkillPerformanceMetrics) -> bool:
        """优化模板"""
        print(f"优化Skill模板: {skill_name}")
        return True
    
    def _optimize_documentation(self, skill_name: str, metrics: SkillPerformanceMetrics) -> bool:
        """优化文档"""
        print(f"优化Skill文档: {skill_name}")
        return True
    
    def _enhance_functionality(self, skill_name: str, metrics: SkillPerformanceMetrics) -> bool:
        """增强功能"""
        print(f"增强Skill功能: {skill_name}")

        try:
            # 查找Skill路径
            skill_path = Path('.claude/skills') / skill_name
            if not skill_path.exists():
                print(f"Skill路径不存在: {skill_path}")
                return False

            enhancements = []

            # 基于采用率低，建议增加功能
            if metrics.user_adoption_rate < 0.3:
                print(f"  - 采用率较低({metrics.user_adoption_rate:.1%})，分析缺失功能")

                enhancements.append({
                    'type': 'feature',
                    'priority': 'high',
                    'title': '增加用户需求的功能',
                    'suggestions': [
                        '调研用户实际需求',
                        '增加常用功能快捷方式',
                        '提供更多输出格式选项',
                        '增加批处理模式支持'
                    ]
                })

            # 基于错误率，增加健壮性功能
            if metrics.error_rate > 0.1:
                print(f"  - 错误率过高({metrics.error_rate:.1%})，增强健壮性")

                enhancements.append({
                    'type': 'robustness',
                    'priority': 'high',
                    'title': '增强错误处理和恢复能力',
                    'suggestions': [
                        '添加输入验证机制',
                        '实现自动重试逻辑',
                        '增加错误恢复策略',
                        '提供详细的错误诊断信息',
                        '添加降级处理方案'
                    ]
                })

            # 基于用户满意度，增加用户体验功能
            if metrics.user_satisfaction < 3.5 and metrics.satisfaction_count > 5:
                print(f"  - 用户满意度较低({metrics.user_satisfaction:.1f})，改善用户体验")

                enhancements.append({
                    'type': 'ux',
                    'priority': 'medium',
                    'title': '改善用户体验',
                    'suggestions': [
                        '添加进度条和状态提示',
                        '优化输出格式的可读性',
                        '提供交互式配置向导',
                        '增加使用提示和帮助信息',
                        '简化常用操作流程'
                    ]
                })

            # 基于性能，增加优化功能
            if metrics.avg_duration > 10:
                print(f"  - 平均执行时间过长({metrics.avg_duration:.2f}秒)，增加性能优化功能")

                enhancements.append({
                    'type': 'performance',
                    'priority': 'high',
                    'title': '性能优化增强',
                    'suggestions': [
                        '实现增量处理模式',
                        '添加缓存机制',
                        '支持并行处理',
                        '优化资源使用',
                        '实现懒加载策略'
                    ]
                })

            # 写入增强建议文档
            if enhancements:
                enhancement_doc_path = skill_path / 'ENHANCEMENT_RECOMMENDATIONS.md'

                enhancement_content = f"""# {skill_name} 功能增强建议

> 基于性能分析自动生成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 当前性能指标

- 健康度评分: {metrics.health_score:.1f}/100
- 用户满意度: {metrics.user_satisfaction:.1f}/5.0
- 采用率: {metrics.user_adoption_rate:.1%}
- 错误率: {metrics.error_rate:.1%}
- 平均执行时间: {metrics.avg_duration:.2f}秒

## 🚀 增强建议

"""

                for idx, enhancement in enumerate(enhancements, 1):
                    enhancement_content += f"""
### {idx}. {enhancement['title']} ({enhancement['type'].upper()})

**优先级**: {enhancement['priority'].upper()}

**具体建议**:
"""
                    for suggestion in enhancement['suggestions']:
                        enhancement_content += f"- {suggestion}\n"

                    enhancement_content += "\n"

                enhancement_content += """
## 📋 实施计划

1. **评估阶段** (1-2天)
   - 与用户沟通确认需求
   - 评估实施成本和收益
   - 确定优先级

2. **设计阶段** (2-3天)
   - 设计增强方案
   - 评审技术可行性
   - 准备测试计划

3. **实施阶段** (5-10天)
   - 按优先级实施增强
   - 编写单元测试
   - 更新文档

4. **验证阶段** (2-3天)
   - 功能测试
   - 性能测试
   - 用户验收测试

## ⚠️ 注意事项

- 所有增强需要经过充分测试
- 保持向后兼容性
- 及时更新文档和示例
- 收集用户反馈并迭代
"""

                try:
                    with open(enhancement_doc_path, 'w', encoding='utf-8') as f:
                        f.write(enhancement_content)
                    print(f"  ✅ 功能增强建议已保存到: {enhancement_doc_path}")

                    # 同时在SKILL.md中添加引用
                    skill_md_path = skill_path / 'SKILL.md'
                    if skill_md_path.exists():
                        with open(skill_md_path, 'r', encoding='utf-8') as f:
                            skill_content = f.read()

                        if 'ENHANCEMENT_RECOMMENDATIONS.md' not in skill_content:
                            enhancement_link = f"\n\n> 💡 **功能增强建议**: 查看 [ENHANCEMENT_RECOMMENDATIONS.md](./ENHANCEMENT_RECOMMENDATIONS.md) 了解基于性能分析的改进建议\n"

                            # 在文档末尾添加链接
                            skill_content += enhancement_link

                            with open(skill_md_path, 'w', encoding='utf-8') as f:
                                f.write(skill_content)
                            print(f"  ✅ 已在SKILL.md中添加增强建议链接")

                    return True

                except Exception as e:
                    print(f"保存增强建议失败: {e}")
                    return False

            else:
                print(f"  ℹ️  当前功能满足需求，无需增强")
                return True

        except Exception as e:
            print(f"功能增强失败: {e}")
            return False
    
    def apply_optimization(self, recommendation: OptimizationRecommendation) -> bool:
        """应用优化"""
        strategy = self.optimization_strategies.get(recommendation.recommendation_type)
        if not strategy:
            return False
        
        try:
            # 获取当前指标
            metrics_list = self.tracker.collect_metrics(recommendation.skill_name, 30)
            if not metrics_list:
                return False
            
            metrics = metrics_list[0]
            
            # 应用优化策略
            return strategy(recommendation.skill_name, metrics)
            
        except Exception as e:
            print(f"应用优化失败: {e}")
            return False
    
    def generate_optimization_report(self, metrics_list: List[SkillPerformanceMetrics],
                                    recommendations: List[OptimizationRecommendation],
                                    output_file: Optional[str] = None) -> Dict[str, Any]:
        """生成优化报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'analysis_period_days': 30,
            'total_skills_analyzed': len(metrics_list),
            'skills_needing_optimization': len(recommendations),
            'overall_health': {
                'average_health_score': sum(m.health_score for m in metrics_list) / len(metrics_list) if metrics_list else 0,
                'high_performing_skills': len([m for m in metrics_list if m.health_score >= 80]),
                'underperforming_skills': len([m for m in metrics_list if m.health_score < 60])
            },
            'skill_metrics': [m.to_dict() for m in metrics_list],
            'optimization_recommendations': [r.to_dict() for r in recommendations],
            'priority_summary': {
                'high_priority': len([r for r in recommendations if r.priority == 'high']),
                'medium_priority': len([r for r in recommendations if r.priority == 'medium']),
                'low_priority': len([r for r in recommendations if r.priority == 'low'])
            }
        }
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=2)
                print(f"优化报告已保存: {output_file}")
            except Exception as e:
                print(f"保存报告失败: {e}")
        
        return report


# 全局优化引擎实例
optimization_engine = SkillOptimizationEngine()


def get_optimization_engine() -> SkillOptimizationEngine:
    """获取优化引擎实例"""
    return optimization_engine


if __name__ == '__main__':
    # 测试优化引擎
    engine = SkillOptimizationEngine()
    
    # 分析所有Skill性能
    metrics, recommendations = engine.analyze_skill_performance(days=7)
    
    print(f"分析完成: {len(metrics)} 个Skill，{len(recommendations)} 条优化建议")
    
    # 生成报告
    report = engine.generate_optimization_report(metrics, recommendations)
    print(json.dumps(report, ensure_ascii=False, indent=2))