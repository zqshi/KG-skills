#!/usr/bin/env python3
"""
工作流分析器
分析操作日志，识别高频工作流
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any, Tuple, Optional
import re

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models import SkillSpec
from core.skill_creator import SkillCreator


class WorkflowAnalyzer:
    """工作流分析器类"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.operations_log: List[Dict[str, Any]] = []
        self.workflows: List[Dict[str, Any]] = []
        self.skill_creator = SkillCreator()
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            'analysis': {
                'cycle_days': 30,
                'frequency_threshold': 5,
                'min_sequence_length': 3,
                'similarity_threshold': 0.8
            },
            'monitoring': {
                'enabled': True,
                'log_retention_days': 90,
                'ignore_patterns': [
                    "^cd\\s+",
                    "^ls\\s+",
                    "^pwd$",
                    "^echo\\s+",
                    "^cat\\s+",
                    "^vim?",
                    "^nano\\s+",
                    "^git\\s+status"
                ]
            },
            'skill_generation': {
                'auto_create': False,
                'require_confirmation': True,
                'default_skill_type': 'workflow',
                'complexity_mapping': {
                    'simple': 'simple',
                    'medium': 'medium',
                    'complex': 'complex'
                }
            },
            'template_selection': {
                'operation_type_mapping': {
                    'data_processing': 'data_processor',
                    'api_integration': 'api_integrator',
                    'file_operation': 'file_operator',
                    'content_creation': 'content_creator',
                    'documentation': 'document_generator'
                }
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_content = yaml.safe_load(f) or {}
                # 合并配置
                self._merge_config(default_config, config_content)
            except Exception as e:
                print(f"配置文件加载失败，使用默认配置: {e}")
        
        return default_config
    
    def _merge_config(self, base: Dict, override: Dict):
        """递归合并配置字典"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def load_operations_log(self, log_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """加载操作日志"""
        if log_path is None:
            log_path = Path(__file__).parent / 'logs' / 'operations.json'
        
        log_file = Path(log_path)
        if not log_file.exists():
            print(f"操作日志文件不存在: {log_path}")
            return []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                operations = []
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            operation = json.loads(line)
                            operations.append(operation)
                        except json.JSONDecodeError:
                            continue
            
            self.operations_log = operations
            print(f"加载 {len(operations)} 条操作记录")
            return operations
        
        except Exception as e:
            print(f"加载操作日志失败: {e}")
            return []
    
    def filter_operations(self, operations: List[Dict[str, Any]], 
                         days: Optional[int] = None) -> List[Dict[str, Any]]:
        """过滤操作记录（按时间）"""
        if days is None:
            days = self.config['analysis']['cycle_days']
        
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered = []
        
        for op in operations:
            try:
                op_time = datetime.fromisoformat(op['timestamp'].replace('Z', '+00:00'))
                if op_time >= cutoff_date:
                    if not self._should_ignore_operation(op['command']):
                        filtered.append(op)
            except (KeyError, ValueError):
                continue
        
        print(f"过滤后剩余 {len(filtered)} 条操作记录")
        return filtered
    
    def _should_ignore_operation(self, command: str) -> bool:
        """检查是否应该忽略该操作"""
        ignore_patterns = self.config['monitoring']['ignore_patterns']
        
        for pattern in ignore_patterns:
            if re.match(pattern, command):
                return True
        
        return False
    
    def analyze_workflows(self, operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """分析工作流模式"""
        print("开始分析工作流模式...")
        
        operations.sort(key=lambda x: x['timestamp'])
        
        command_sequences = self._extract_command_sequences(operations)
        
        frequent_sequences = self._find_frequent_sequences(command_sequences)
        
        workflows = []
        for seq in frequent_sequences:
            workflow = self._create_workflow_definition(seq)
            if workflow:
                workflows.append(workflow)
        
        self.workflows = workflows
        print(f"识别出 {len(workflows)} 个高频工作流")
        
        return workflows
    
    def _extract_command_sequences(self, operations: List[Dict[str, Any]]) -> List[List[str]]:
        """提取命令序列"""
        sequences = []
        current_sequence = []
        last_time = None
        
        time_window = timedelta(minutes=self.config['analysis'].get('time_window_minutes', 30))
        
        for op in operations:
            try:
                current_time = datetime.fromisoformat(op['timestamp'].replace('Z', '+00:00'))
                
                if last_time and (current_time - last_time) > time_window:
                    if len(current_sequence) >= self.config['analysis']['min_sequence_length']:
                        sequences.append(current_sequence)
                    current_sequence = []
                
                current_sequence.append(op['command'])
                last_time = current_time
                
            except (KeyError, ValueError):
                continue
        
        if len(current_sequence) >= self.config['analysis']['min_sequence_length']:
            sequences.append(current_sequence)
        
        return sequences
    
    def _find_frequent_sequences(self, sequences: List[List[str]]) -> List[Dict[str, Any]]:
        """发现频繁序列"""
        sequence_counts = defaultdict(int)
        
        for seq in sequences:
            for length in range(self.config['analysis']['min_sequence_length'], len(seq) + 1):
                for i in range(len(seq) - length + 1):
                    subseq = tuple(seq[i:i + length])
                    sequence_counts[subseq] += 1
        
        threshold = self.config['analysis']['frequency_threshold']
        frequent_sequences = []
        
        for seq, count in sequence_counts.items():
            if count >= threshold:
                frequent_sequences.append({
                    'sequence': list(seq),
                    'frequency': count,
                    'support': count / len(sequences) if sequences else 0
                })
        
        frequent_sequences.sort(key=lambda x: x['frequency'], reverse=True)
        
        return frequent_sequences
    
    def _create_workflow_definition(self, seq_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """创建工作流定义"""
        sequence = seq_info['sequence']
        
        workflow_type = self._analyze_workflow_type(sequence)
        complexity = self._evaluate_complexity(sequence)
        workflow_name = self._generate_workflow_name(sequence, workflow_type)
        
        return {
            'workflow_id': f"wf_{hash(tuple(sequence)) % 10000:04d}",
            'name': workflow_name,
            'type': workflow_type,
            'complexity': complexity,
            'commands': sequence,
            'frequency': seq_info['frequency'],
            'support': seq_info['support'],
            'description': f"自动识别的工作流: {workflow_name}",
            'recommended_action': 'create_skill'
        }
    
    def _analyze_workflow_type(self, sequence: List[str]) -> str:
        """分析工作流类型"""
        commands_str = ' '.join(sequence).lower()
        
        if any(keyword in commands_str for keyword in ['data', 'csv', 'json', 'pandas', 'numpy']):
            return 'data_processing'
        elif any(keyword in commands_str for keyword in ['api', 'http', 'curl', 'request']):
            return 'api_integration'
        elif any(keyword in commands_str for keyword in ['file', 'mv', 'cp', 'rm', 'glob']):
            return 'file_operation'
        elif any(keyword in commands_str for keyword in ['doc', 'markdown', 'pdf', 'content']):
            return 'content_creation'
        else:
            return 'general'
    
    def _evaluate_complexity(self, sequence: List[str]) -> str:
        """评估复杂度"""
        if len(sequence) <= 3:
            return 'simple'
        elif len(sequence) <= 5:
            return 'medium'
        else:
            return 'complex'
    
    def _generate_workflow_name(self, sequence: List[str], workflow_type: str) -> str:
        """生成工作流名称"""
        if workflow_type == 'data_processing':
            return 'data_processing_pipeline'
        elif workflow_type == 'api_integration':
            return 'api_integration_workflow'
        elif workflow_type == 'file_operation':
            return 'file_management_workflow'
        elif workflow_type == 'content_creation':
            return 'content_generation_workflow'
        else:
            first_cmd = sequence[0].split()[0]
            return f"{first_cmd}_workflow"
    
    def generate_skill_recommendations(self, workflows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """生成Skill创建建议"""
        recommendations = []
        
        for workflow in workflows:
            if workflow['frequency'] >= self.config['analysis']['frequency_threshold']:
                recommendation = {
                    'workflow_id': workflow['workflow_id'],
                    'skill_name': self._suggest_skill_name(workflow),
                    'description': workflow['description'],
                    'skill_type': self._map_to_skill_type(workflow['type']),
                    'complexity': self.config['skill_generation']['complexity_mapping'][workflow['complexity']],
                    'frequency': workflow['frequency'],
                    'estimated_time_saved': self._calculate_time_saved(workflow),
                    'confidence': workflow['support'],
                    'recommended_action': workflow['recommended_action'],
                    'commands': workflow['commands']
                }
                recommendations.append(recommendation)
        
        return recommendations
    
    def _suggest_skill_name(self, workflow: Dict[str, Any]) -> str:
        """建议Skill名称"""
        base_name = workflow['name']
        skill_name = base_name.replace('-', '_').replace(' ', '_').lower()
        
        if skill_name and not skill_name[0].isalpha():
            skill_name = 'skill_' + skill_name
        
        return skill_name
    
    def _map_to_skill_type(self, workflow_type: str) -> str:
        """映射到Skill类型"""
        mapping = self.config['template_selection']['operation_type_mapping']
        return mapping.get(workflow_type, 'knowledge_processor')
    
    def _calculate_time_saved(self, workflow: Dict[str, Any]) -> int:
        """估算节省时间"""
        base_time_per_run = len(workflow['commands']) * 2
        return base_time_per_run * workflow['frequency']
    
    def create_skill_from_workflow(self, recommendation: Dict[str, Any]) -> bool:
        """基于工作流推荐创建Skill"""
        try:
            # 创建规格
            spec = SkillSpec(
                name=recommendation['skill_name'],
                description=recommendation['description'],
                skill_type=recommendation['skill_type'],
                complexity=recommendation['complexity'],
                target_audience='intermediate',
                include_scripts=True,
                include_templates=False,
                custom_requirements=f"自动从工作流生成: {'; '.join(recommendation['commands'][:3])}",
                commands=recommendation['commands']
            )
            
            # 使用skill_creator创建
            result = self.skill_creator.create_skill(spec)
            
            return result.success
            
        except Exception as e:
            print(f"创建工作流Skill时出错: {e}")
            return False
    
    def generate_report(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """生成分析报告"""
        if not self.workflows:
            print("没有工作流数据可生成报告")
            return {}
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'analysis_period_days': self.config['analysis']['cycle_days'],
            'total_workflows_identified': len(self.workflows),
            'high_frequency_workflows': [
                wf for wf in self.workflows 
                if wf['frequency'] >= self.config['analysis']['frequency_threshold']
            ],
            'summary': {
                'total_commands_analyzed': len(self.operations_log),
                'unique_commands': len(set(op.get('command', '') for op in self.operations_log)),
                'skills_recommended': len([wf for wf in self.workflows if wf['frequency'] >= self.config['analysis']['frequency_threshold']]),
                'estimated_total_time_saved_minutes': sum(
                    self._calculate_time_saved(wf) for wf in self.workflows
                    if wf['frequency'] >= self.config['analysis']['frequency_threshold']
                )
            }
        }
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"报告已保存: {output_file}")
        
        return report