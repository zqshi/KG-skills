#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识质量验证器
验证知识库条目的准确性、完整性和时效性
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime


class KnowledgeQualityValidator:
    """知识质量验证器类"""
    
    def __init__(self, knowledge_data: Dict[str, Any]):
        self.knowledge_data = knowledge_data
        self.validation_results = {}
        
    def validate_completeness(self) -> Tuple[float, List[Dict]]:
        """验证内容完整性"""
        issues = []
        score = 100
        
        required_fields = ['title', 'content', 'category', 'tags']
        for field in required_fields:
            if field not in self.knowledge_data or not self.knowledge_data[field]:
                issues.append({
                    "type": "missing_field",
                    "field": field,
                    "severity": "high",
                    "description": f"缺少必需字段: {field}"
                })
                score -= 20
        
        # 检查内容长度
        content = self.knowledge_data.get('content', '')
        if len(content) < 100:
            issues.append({
                "type": "insufficient_content",
                "severity": "medium",
                "description": f"内容长度不足: {len(content)} 字符"
            })
            score -= 10
        
        return max(0, score / 100), issues
    
    def validate_accuracy(self) -> Tuple[float, List[Dict]]:
        """验证内容准确性"""
        issues = []
        score = 100
        
        content = self.knowledge_data.get('content', '')
        
        # 检查是否有明显的逻辑错误
        if len(content) > 0:
            # 简单的准确性检查：检查是否有矛盾表述
            contradiction_patterns = [
                r'既[^\n]{0,20}又[^\n]{0,20}不',
                r'虽然[^\n]{0,20}但是[^\n]{0,20}不'
            ]
            
            for pattern in contradiction_patterns:
                if re.search(pattern, content):
                    issues.append({
                        "type": "logical_contradiction",
                        "severity": "high",
                        "description": "可能存在逻辑矛盾"
                    })
                    score -= 30
        
        return max(0, score / 100), issues
    
    def validate_timeliness(self) -> Tuple[float, List[Dict]]:
        """验证内容时效性"""
        issues = []
        score = 100
        
        # 检查创建时间
        create_time = self.knowledge_data.get('create_time', '')
        if create_time:
            try:
                create_date = datetime.fromisoformat(create_time.replace('Z', '+00:00'))
                days_old = (datetime.now(create_date.tzinfo) - create_date).days
                
                if days_old > 365:
                    issues.append({
                        "type": "outdated_content",
                        "severity": "medium",
                        "description": f"内容创建时间超过1年（{days_old}天前）"
                    })
                    score -= 20
                elif days_old > 180:
                    issues.append({
                        "type": "aging_content",
                        "severity": "low",
                        "description": f"内容创建时间超过半年（{days_old}天前）"
                    })
                    score -= 10
            except:
                issues.append({
                    "type": "invalid_timestamp",
                    "severity": "low",
                    "description": "创建时间格式无效"
                })
                score -= 5
        
        return max(0, score / 100), issues
    
    def validate_consistency(self) -> Tuple[float, List[Dict]]:
        """验证内容一致性"""
        issues = []
        score = 100
        
        # 检查标签一致性
        tags = self.knowledge_data.get('tags', [])
        category = self.knowledge_data.get('category', '')
        
        if tags and category:
            # 简单的标签-分类一致性检查
            category_keywords = {
                'policy': ['政策', '规定', '制度'],
                'process': ['流程', '步骤', '操作'],
                'faq': ['常见', '问题', 'FAQ']
            }
            
            category_matched = False
            if category in category_keywords:
                keywords = category_keywords[category]
                for tag in tags:
                    if any(keyword in tag for keyword in keywords):
                        category_matched = True
                        break
            
            if not category_matched:
                issues.append({
                    "type": "tag_category_mismatch",
                    "severity": "low",
                    "description": "标签与分类可能不匹配"
                })
                score -= 10
        
        return max(0, score / 100), issues
    
    def generate_report(self) -> Dict[str, Any]:
        """生成完整的质量验证报告"""
        print("开始验证内容完整性...")
        completeness, completeness_issues = self.validate_completeness()
        
        print("开始验证内容准确性...")
        accuracy, accuracy_issues = self.validate_accuracy()
        
        print("开始验证内容时效性...")
        timeliness, timeliness_issues = self.validate_timeliness()
        
        print("开始验证内容一致性...")
        consistency, consistency_issues = self.validate_consistency()
        
        # 计算综合评分
        overall_score = (completeness * 0.3 + accuracy * 0.3 + timeliness * 0.2 + consistency * 0.2) * 100
        
        all_issues = completeness_issues + accuracy_issues + timeliness_issues + consistency_issues
        
        report = {
            "quality_score": round(overall_score, 1),
            "dimension_scores": {
                "completeness": round(completeness * 100, 1),
                "accuracy": round(accuracy * 100, 1),
                "timeliness": round(timeliness * 100, 1),
                "consistency": round(consistency * 100, 1)
            },
            "issues_found": all_issues,
            "improvement_suggestions": self._generate_suggestions(all_issues)
        }
        
        return report
    
    def _generate_suggestions(self, issues: List[Dict]) -> List[Dict]:
        """生成改进建议"""
        suggestions = []
        
        # 按严重程度分组
        high_priority = [i for i in issues if i['severity'] == 'high']
        medium_priority = [i for i in issues if i['severity'] == 'medium']
        low_priority = [i for i in issues if i['severity'] == 'low']
        
        if high_priority:
            suggestions.append({
                "priority": "high",
                "suggestion": f"解决 {len(high_priority)} 个高优先级问题",
                "estimated_effort": f"{len(high_priority) * 0.5} 小时"
            })
        
        if medium_priority:
            suggestions.append({
                "priority": "medium",
                "suggestion": f"处理 {len(medium_priority)} 个中优先级问题",
                "estimated_effort": f"{len(medium_priority) * 0.3} 小时"
            })
        
        if low_priority:
            suggestions.append({
                "priority": "low",
                "suggestion": f"优化 {len(low_priority)} 个低优先级问题",
                "estimated_effort": f"{len(low_priority) * 0.2} 小时"
            })
        
        if not suggestions:
            suggestions.append({
                "priority": "low",
                "suggestion": "知识质量良好，建议定期审核更新",
                "estimated_effort": "0.5 小时/月"
            })
        
        return suggestions


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python knowledge_quality_validator.py <知识数据JSON文件路径>")
        sys.exit(1)
    
    knowledge_file = sys.argv[1]
    
    # 检查文件是否存在
    if not Path(knowledge_file).exists():
        print(f"错误: 文件不存在: {knowledge_file}")
        sys.exit(1)
    
    # 加载知识数据
    try:
        with open(knowledge_file, 'r', encoding='utf-8') as f:
            knowledge_data = json.load(f)
    except Exception as e:
        print(f"加载知识数据失败: {e}")
        sys.exit(1)
    
    # 创建验证器并执行验证
    validator = KnowledgeQualityValidator(knowledge_data)
    
    # 生成报告
    report = validator.generate_report()
    
    # 打印报告
    print("\n" + "="*60)
    print("知识质量验证报告")
    print("="*60)
    
    print(f"\n📊 综合质量评分: {report['quality_score']}/100")
    
    print("\n📈 各维度评分:")
    for dimension, score in report["dimension_scores"].items():
        print(f"  • {dimension}: {score}/100")
    
    if report["issues_found"]:
        print(f"\n🔍 发现的问题 ({len(report['issues_found'])}个):")
        for issue in report["issues_found"][:5]:  # 只显示前5个
            print(f"  • [{issue['severity']}] {issue['description']}")
    
    print("\n💡 改进建议:")
    for i, suggestion in enumerate(report["improvement_suggestions"], 1):
        print(f"{i}. [{suggestion['priority']}] {suggestion['suggestion']}")
        print(f"   预计工作量: {suggestion['estimated_effort']}")
    
    # 保存详细报告到文件
    report_file = "knowledge_quality_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细报告已保存到: {report_file}")


if __name__ == "__main__":
    main()