#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识格式规范化器
统一术语和表达方式，优化内容结构，确保知识格式的一致性和规范性
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple


class KnowledgeFormatNormalizer:
    """知识格式规范化器类"""
    
    def __init__(self, format_standards: Dict[str, Any] = None):
        self.format_standards = format_standards or self._load_default_standards()
        self.changes = []
        
    def _load_default_standards(self) -> Dict[str, Any]:
        """加载默认格式标准"""
        return {
            "terminology": {
                "年假": "年度休假",
                "请假": "申请休假",
                "主管": "直接主管",
                "经理": "部门经理",
                "搞定": "完成",
                "弄好": "完成"
            },
            "document_structure": {
                "title_format": r"^#+\s+.+$",
                "list_format": r"^[-*+]\s+.+$",
                "numbered_list_format": r"^\d+\.\s+.+$"
            },
            "expression_patterns": {
                "passive_to_active": {
                    "被批准": "获得批准",
                    "被要求": "需要",
                    "被通知": "收到通知"
                }
            }
        }
    
    def normalize_content(self, content: str) -> Tuple[str, List[Dict]]:
        """规范化内容"""
        self.changes = []
        normalized = content
        
        # 1. 术语统一
        normalized = self._normalize_terminology(normalized)
        
        # 2. 结构优化
        normalized = self._optimize_structure(normalized)
        
        # 3. 表达优化
        normalized = self._optimize_expressions(normalized)
        
        return normalized, self.changes
    
    def _normalize_terminology(self, content: str) -> str:
        """统一术语"""
        terminology = self.format_standards.get("terminology", {})
        
        for old_term, new_term in terminology.items():
            if old_term in content:
                content = content.replace(old_term, new_term)
                self.changes.append({
                    "change_type": "terminology",
                    "original": old_term,
                    "normalized": new_term,
                    "location": "content"
                })
        
        return content
    
    def _optimize_structure(self, content: str) -> str:
        """优化文档结构"""
        lines = content.split('\n')
        optimized_lines = []
        
        for i, line in enumerate(lines):
            original_line = line
            
            # 优化标题格式
            if line.strip().startswith('#'):
                line = self._optimize_title(line)
            
            # 优化列表格式
            if re.match(r'^\s*[-*+]\s+', line):
                line = self._optimize_list_item(line)
            
            # 优化编号列表
            if re.match(r'^\s*\d+\.\s+', line):
                line = self._optimize_numbered_list(line)
            
            if line != original_line:
                self.changes.append({
                    "change_type": "structure",
                    "original": original_line,
                    "normalized": line,
                    "line_number": i + 1
                })
            
            optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _optimize_title(self, title: str) -> str:
        """优化标题格式"""
        # 确保标题层级正确
        title = title.strip()
        
        # 移除多余的空格
        title = re.sub(r'^(#+)\s+', r'\1 ', title)
        
        # 确保标题末尾没有标点符号
        title = re.sub(r'([。！？,;:!?])$', '', title)
        
        return title
    
    def _optimize_list_item(self, item: str) -> str:
        """优化列表项格式"""
        # 统一使用 '-' 作为列表符号
        item = re.sub(r'^\s*[*+]\s+', '- ', item)
        
        # 确保列表项首字母大写
        match = re.match(r'^(\s*-\s+)(.+)$', item)
        if match:
            prefix = match.group(1)
            content = match.group(2)
            if content and content[0].islower():
                content = content[0].upper() + content[1:]
            item = prefix + content
        
        return item
    
    def _optimize_numbered_list(self, item: str) -> str:
        """优化编号列表格式"""
        # 确保编号后有一个空格
        item = re.sub(r'^(\s*\d+)\.\s+', r'\1. ', item)
        
        # 确保首字母大写
        match = re.match(r'^(\s*\d+\.\s+)(.+)$', item)
        if match:
            prefix = match.group(1)
            content = match.group(2)
            if content and content[0].islower():
                content = content[0].upper() + content[1:]
            item = prefix + content
        
        return item
    
    def _optimize_expressions(self, content: str) -> str:
        """优化表达方式"""
        expression_patterns = self.format_standards.get("expression_patterns", {})
        
        for pattern_type, patterns in expression_patterns.items():
            if pattern_type == "passive_to_active":
                for passive, active in patterns.items():
                    if passive in content:
                        content = content.replace(passive, active)
                        self.changes.append({
                            "change_type": "expression",
                            "original": passive,
                            "normalized": active,
                            "pattern_type": pattern_type
                        })
        
        return content
    
    def generate_report(self, original: str, normalized: str, changes: List[Dict]) -> Dict[str, Any]:
        """生成规范化报告"""
        # 统计变更类型
        change_stats = {}
        for change in changes:
            change_type = change["change_type"]
            change_stats[change_type] = change_stats.get(change_type, 0) + 1
        
        # 计算一致性评分
        total_changes = len(changes)
        content_length = len(original)
        consistency_score = max(0, 1 - (total_changes / max(content_length / 100, 1)))
        
        # 计算术语统一性
        terminology_changes = change_stats.get("terminology", 0)
        terminology_score = 1 - (terminology_changes / max(total_changes, 1) * 0.5)
        
        return {
            "normalization_summary": {
                "consistency_score": round(consistency_score, 2),
                "terminology_score": round(terminology_score, 2),
                "total_changes": total_changes
            },
            "change_statistics": change_stats,
            "detailed_changes": changes,
            "improvement_recommendations": self._generate_recommendations(change_stats)
        }
    
    def _generate_recommendations(self, change_stats: Dict[str, int]) -> List[Dict]:
        """生成改进建议"""
        recommendations = []
        
        terminology_changes = change_stats.get("terminology", 0)
        structure_changes = change_stats.get("structure", 0)
        expression_changes = change_stats.get("expression", 0)
        
        if terminology_changes > 5:
            recommendations.append({
                "priority": "high",
                "recommendation": f"统一了 {terminology_changes} 个术语，建议建立术语词典",
                "estimated_effort": "2小时"
            })
        
        if structure_changes > 3:
            recommendations.append({
                "priority": "medium",
                "recommendation": f"优化了 {structure_changes} 处文档结构",
                "estimated_effort": "1小时"
            })
        
        if expression_changes > 2:
            recommendations.append({
                "priority": "low",
                "recommendation": f"改进了 {expression_changes} 处表达方式",
                "estimated_effort": "0.5小时"
            })
        
        if not recommendations:
            recommendations.append({
                "priority": "low",
                "recommendation": "格式规范性良好，建议定期检查和维护",
                "estimated_effort": "0.5小时/月"
            })
        
        return recommendations


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python format_normalizer.py <知识内容文件路径>")
        sys.exit(1)
    
    content_file = sys.argv[1]
    
    # 检查文件是否存在
    if not Path(content_file).exists():
        print(f"错误: 文件不存在: {content_file}")
        sys.exit(1)
    
    # 读取内容
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)
    
    # 创建规范化器并执行规范化
    normalizer = KnowledgeFormatNormalizer()
    normalized_content, changes = normalizer.normalize_content(content)
    
    # 生成报告
    report = normalizer.generate_report(content, normalized_content, changes)
    
    # 打印报告
    print("\n" + "="*60)
    print("知识格式规范化报告")
    print("="*60)
    
    summary = report["normalization_summary"]
    print(f"\n📊 一致性评分: {summary['consistency_score']}/1.0")
    print(f"📊 术语统一性: {summary['terminology_score']}/1.0")
    print(f"📋 总变更数: {summary['total_changes']}")
    
    print("\n📈 变更统计:")
    for change_type, count in report["change_statistics"].items():
        print(f"  • {change_type}: {count}")
    
    if changes:
        print(f"\n🔍 详细变更 ({len(changes)}个):")
        for i, change in enumerate(changes[:10], 1):  # 只显示前10个
            if change["change_type"] == "terminology":
                print(f"{i}. 术语统一: {change['original']} → {change['normalized']}")
            elif change["change_type"] == "structure":
                print(f"{i}. 结构优化: {change['original'][:30]}...")
            elif change["change_type"] == "expression":
                print(f"{i}. 表达优化: {change['original']} → {change['normalized']}")
    
    print("\n💡 改进建议:")
    for i, rec in enumerate(report["improvement_recommendations"], 1):
        print(f"{i}. [{rec['priority']}] {rec['recommendation']}")
        print(f"   预计工作量: {rec['estimated_effort']}")
    
    # 保存规范化后的内容
    output_file = "normalized_content.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(normalized_content)
    
    print(f"\n📄 规范化后的内容已保存到: {output_file}")
    
    # 保存详细报告
    report_file = "format_normalization_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📊 详细报告已保存到: {report_file}")


if __name__ == "__main__":
    main()