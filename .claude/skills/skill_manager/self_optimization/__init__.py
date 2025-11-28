#!/usr/bin/env python3
"""
Skill自优化模块
提供Skill性能监控、偏差检测和自动优化功能
"""

from .optimization_engine import (
    SkillOptimizationEngine,
    SkillPerformanceMetrics,
    OptimizationRecommendation,
    SkillPerformanceTracker,
    SkillDeviationDetector
)

from .skill_analyzer import (
    SkillStructureAnalyzer,
    SkillStructureAnalysis
)

from .skill_optimizer import (
    SkillOptimizer,
    OptimizationResult
)

# 可选导入scheduler（需要schedule依赖）
try:
    from .scheduler import SelfOptimizationScheduler
    _has_scheduler = True
except ImportError:
    SelfOptimizationScheduler = None
    _has_scheduler = False

__all__ = [
    'SkillOptimizationEngine',
    'SkillPerformanceMetrics',
    'OptimizationRecommendation',
    'SkillPerformanceTracker',
    'SkillDeviationDetector',
    'SkillStructureAnalyzer',
    'SkillStructureAnalysis',
    'SkillOptimizer',
    'OptimizationResult',
    'SelfOptimizationScheduler'
]