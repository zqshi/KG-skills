#!/usr/bin/env python3
"""
业务价值评估模块 - 多维度评估知识价值
原则5：业务价值评估
"""

import json
from typing import Dict, Any, List
from datetime import datetime


class BusinessValueAssessor:
    """业务价值评估器"""
    
    def __init__(self, config_path: str = "config/business_value.yaml"):
        self.config_path = config_path
        self.min_approval_score = 0.7  # 最低批准分数
        self.review_required_score = 0.5  # 需要审核的分数
        
        # 标签业务价值权重
        self.tag_value_weights = {
            "流程类": 0.9,    # 高价值
            "材料类": 0.8,    # 中高价值
            "要求类": 0.85,   # 高价值
            "政策类": 0.9,    # 高价值
            "指南类": 0.75,   # 中等价值
            "说明类": 0.6,    # 中低价值
            "其他": 0.5       # 低价值
        }
    
    def assess_business_value(self, knowledge_entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        综合评估业务价值
        
        Args:
            knowledge_entry: 知识条目
            
        Returns:
            业务价值评估结果
        """
        # 1. 标签业务价值评估
        tag_value = self._assess_tag_business_value(
            knowledge_entry.get("tags", []),
            knowledge_entry["content"]
        )
        
        # 2. FAQ实用性评估
        faq_utility = self._assess_faq_utility(
            knowledge_entry.get("faqs", []),
            knowledge_entry.get("target_audience", "全体员工")
        )
        
        # 3. 摘要完整性评估
        summary_completeness = self._assess_summary_completeness(
            knowledge_entry.get("summary", ""),
            knowledge_entry["content"]
        )
        
        # 4. 知识类型价值评估
        type_value = self._assess_knowledge_type_value(
            knowledge_entry["knowledge_type"]
        )
        
        # 5. 综合评分
        overall_score = self._calculate_weighted_score({
            "tag_value": tag_value["score"],
            "faq_utility": faq_utility["score"],
            "summary_completeness": summary_completeness["score"],
            "type_value": type_value["score"]
        })
        
        # 6. 生成优化建议
        optimization_suggestions = self._generate_optimization_suggestions(
            tag_value, faq_utility, summary_completeness, type_value
        )
        
        # 7. 确定批准状态
        approval_status = self._determine_approval_status(overall_score)
        
        return {
            "overall_score": overall_score,
            "approval_status": approval_status,
            "dimension_scores": {
                "tag_value": tag_value,
                "faq_utility": faq_utility,
                "summary_completeness": summary_completeness,
                "type_value": type_value
            },
            "optimization_suggestions": optimization_suggestions,
            "assessment_timestamp": datetime.now().isoformat()
        }
    
    def _assess_tag_business_value(self, tags: List[Dict[str, Any]], content: str) -> Dict[str, Any]:
        """评估标签业务价值"""
        if not tags:
            return {
                "score": 0.0,
                "level": "低",
                "details": {
                    "high_value_tags": 0,
                    "medium_value_tags": 0,
                    "low_value_tags": 0,
                    "total_tags": 0
                },
                "issues": ["未提取到标签"]
            }
        
        # 评估每个标签的业务价值
        high_value_count = 0
        medium_value_count = 0
        low_value_count = 0
        
        for tag in tags:
            tag_name = tag.get("tag_name", "")
            category = tag.get("category", "其他")
            
            # 基于分类评估价值
            if category in ["流程类", "政策类", "要求类"]:
                high_value_count += 1
            elif category in ["材料类", "指南类"]:
                medium_value_count += 1
            else:
                low_value_count += 1
        
        # 计算综合分数
        total_tags = len(tags)
        score = (
            high_value_count * 0.9 +
            medium_value_count * 0.7 +
            low_value_count * 0.5
        ) / total_tags if total_tags > 0 else 0
        
        # 确定价值等级
        if score >= 0.8:
            level = "高"
        elif score >= 0.6:
            level = "中"
        else:
            level = "低"
        
        return {
            "score": score,
            "level": level,
            "details": {
                "high_value_tags": high_value_count,
                "medium_value_tags": medium_value_count,
                "low_value_tags": low_value_count,
                "total_tags": total_tags,
                "high_value_ratio": high_value_count / total_tags if total_tags > 0 else 0
            },
            "issues": self._identify_tag_issues(tags, score)
        }
    
    def _identify_tag_issues(self, tags: List[Dict[str, Any]], score: float) -> List[str]:
        """识别标签问题"""
        issues = []
        
        if len(tags) < 3:
            issues.append("标签数量过少，可能无法全面描述知识内容")
        
        if len(tags) > 15:
            issues.append("标签数量过多，建议精简到3-10个核心标签")
        
        high_value_tags = sum(1 for tag in tags if tag.get("category") in ["流程类", "政策类", "要求类"])
        if high_value_tags == 0:
            issues.append("缺少高业务价值标签（流程类、政策类、要求类）")
        
        if score < 0.6:
            issues.append("标签业务价值偏低，建议优化标签体系")
        
        return issues
    
    def _assess_faq_utility(self, faqs: List[Dict[str, Any]], target_audience: str) -> Dict[str, Any]:
        """评估FAQ实用性"""
        if not faqs:
            return {
                "score": 0.0,
                "level": "低",
                "details": {
                    "total_faqs": 0,
                    "avg_confidence": 0,
                    "coverage_score": 0
                },
                "issues": ["未生成FAQ"]
            }
        
        total_faqs = len(faqs)
        avg_confidence = sum(faq.get("confidence", 0) for faq in faqs) / total_faqs
        
        # 评估FAQ覆盖度
        coverage_score = self._assess_faq_coverage(faqs, target_audience)
        
        # 评估问题质量
        question_quality = self._assess_question_quality(faqs)
        
        # 综合评分
        score = (avg_confidence * 0.4 + coverage_score * 0.4 + question_quality * 0.2)
        
        # 确定等级
        if score >= 0.8:
            level = "高"
        elif score >= 0.6:
            level = "中"
        else:
            level = "低"
        
        return {
            "score": score,
            "level": level,
            "details": {
                "total_faqs": total_faqs,
                "avg_confidence": avg_confidence,
                "coverage_score": coverage_score,
                "question_quality": question_quality
            },
            "issues": self._identify_faq_issues(faqs, score)
        }
    
    def _assess_faq_coverage(self, faqs: List[Dict[str, Any]], target_audience: str) -> float:
        """评估FAQ覆盖度"""
        # 简化的覆盖度评估
        # 实际项目中可以基于用户查询日志、业务场景等评估
        
        # 检查是否覆盖常见场景
        questions = [faq.get("question", "").lower() for faq in faqs]
        
        coverage_indicators = {
            "what": any("什么" in q or "what" in q for q in questions),
            "how": any("如何" in q or "怎么" in q or "how" in q for q in questions),
            "when": any("何时" in q or "什么时候" in q or "when" in q for q in questions),
            "who": any("谁" in q or "who" in q for q in questions),
            "why": any("为什么" in q or "为何" in q or "why" in q for q in questions)
        }
        
        covered_scenarios = sum(1 for v in coverage_indicators.values() if v)
        total_scenarios = len(coverage_indicators)
        
        return covered_scenarios / total_scenarios
    
    def _assess_question_quality(self, faqs: List[Dict[str, Any]]) -> float:
        """评估问题质量"""
        quality_scores = []
        
        for faq in faqs:
            question = faq.get("question", "")
            
            # 问题长度适中（10-100个字符）
            length_score = 1.0 if 10 <= len(question) <= 100 else 0.5
            
            # 问题以问号结尾
            punctuation_score = 1.0 if question.endswith("?") or question.endswith("？") else 0.8
            
            # 问题包含关键词
            has_keywords = any(keyword in question.lower() for keyword in 
                             ["如何", "什么", "为什么", "何时", "哪里", "who", "what", "when", "where", "why", "how"])
            keyword_score = 1.0 if has_keywords else 0.6
            
            quality_scores.append((length_score + punctuation_score + keyword_score) / 3)
        
        return sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
    
    def _identify_faq_issues(self, faqs: List[Dict[str, Any]], score: float) -> List[str]:
        """识别FAQ问题"""
        issues = []
        
        if len(faqs) < 5:
            issues.append("FAQ数量过少，可能无法覆盖主要问题")
        
        if len(faqs) > 50:
            issues.append("FAQ数量过多，建议精简到10-30个核心问题")
        
        low_confidence_faqs = sum(1 for faq in faqs if faq.get("confidence", 0) < 0.7)
        if low_confidence_faqs > len(faqs) * 0.3:
            issues.append("过多FAQ置信度偏低，建议人工审核")
        
        if score < 0.6:
            issues.append("FAQ实用性偏低，建议优化问题质量")
        
        return issues
    
    def _assess_summary_completeness(self, summary: str, content: str) -> Dict[str, Any]:
        """评估摘要完整性"""
        if not summary:
            return {
                "score": 0.0,
                "level": "低",
                "details": {
                    "summary_length": 0,
                    "content_coverage": 0,
                    "key_points_coverage": 0
                },
                "issues": ["未生成摘要"]
            }
        
        # 评估摘要长度
        summary_length = len(summary)
        content_length = len(content)
        length_ratio = summary_length / content_length
        
        # 评估内容覆盖度（简化实现）
        # 检查摘要是否包含内容中的关键词
        content_words = set(content.lower().split())
        summary_words = set(summary.lower().split())
        coverage_ratio = len(content_words & summary_words) / len(content_words) if content_words else 0
        
        # 评估关键点覆盖
        key_points = self._extract_key_points(content)
        key_points_in_summary = sum(1 for point in key_points if point.lower() in summary.lower())
        key_points_coverage = key_points_in_summary / len(key_points) if key_points else 0
        
        # 综合评分
        score = (
            min(length_ratio * 10, 1.0) * 0.3 +  # 长度适中（摘要应为原文的5-15%）
            coverage_ratio * 0.4 +
            key_points_coverage * 0.3
        )
        
        # 确定等级
        if score >= 0.8:
            level = "高"
        elif score >= 0.6:
            level = "中"
        else:
            level = "低"
        
        return {
            "score": score,
            "level": level,
            "details": {
                "summary_length": summary_length,
                "content_coverage": coverage_ratio,
                "key_points_coverage": key_points_coverage,
                "length_ratio": length_ratio
            },
            "issues": self._identify_summary_issues(summary, score, length_ratio)
        }
    
    def _extract_key_points(self, content: str) -> List[str]:
        """提取关键点"""
        # 简化的关键点提取
        # 提取包含数字、关键词的句子
        key_points = []
        sentences = content.split("。")
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:
                # 如果句子包含数字或特定关键词，视为关键点
                if any(char.isdigit() for char in sentence) or \
                   any(keyword in sentence for keyword in ["必须", "需要", "应该", "重要", "关键"]):
                    key_points.append(sentence)
        
        return key_points[:10]  # 返回前10个关键点
    
    def _identify_summary_issues(self, summary: str, score: float, length_ratio: float) -> List[str]:
        """识别摘要问题"""
        issues = []
        
        if len(summary) < 50:
            issues.append("摘要过短，可能无法完整概括内容")
        
        if len(summary) > 500:
            issues.append("摘要过长，建议精简到200-300字")
        
        if length_ratio > 0.3:
            issues.append("摘要占比过高，建议压缩到原文的10-20%")
        
        if length_ratio < 0.05:
            issues.append("摘要占比过低，可能遗漏重要信息")
        
        if score < 0.6:
            issues.append("摘要完整性偏低，建议重新生成")
        
        return issues
    
    def _assess_knowledge_type_value(self, knowledge_type: str) -> Dict[str, Any]:
        """评估知识类型价值"""
        # 知识类型价值权重
        type_weights = {
            "政策文档": 0.9,
            "流程指南": 0.85,
            "培训材料": 0.8,
            "FAQ": 0.7
        }
        
        score = type_weights.get(knowledge_type, 0.6)
        
        if score >= 0.85:
            level = "高"
        elif score >= 0.7:
            level = "中"
        else:
            level = "低"
        
        return {
            "score": score,
            "level": level,
            "knowledge_type": knowledge_type,
            "details": {
                "type_weight": score,
                "business_impact": "高" if score >= 0.85 else "中" if score >= 0.7 else "低"
            },
            "issues": []
        }
    
    def _calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        """计算加权分数"""
        # 权重配置
        weights = {
            "tag_value": 0.3,
            "faq_utility": 0.25,
            "summary_completeness": 0.25,
            "type_value": 0.2
        }
        
        weighted_sum = sum(
            scores[dimension] * weights[dimension] 
            for dimension in scores.keys()
        )
        
        return weighted_sum
    
    def _generate_optimization_suggestions(self,
                                         tag_value: Dict[str, Any],
                                         faq_utility: Dict[str, Any],
                                         summary_completeness: Dict[str, Any],
                                         type_value: Dict[str, Any]) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        # 标签优化建议
        if tag_value["score"] < 0.7:
            suggestions.extend(tag_value["issues"])
        
        # FAQ优化建议
        if faq_utility["score"] < 0.7:
            suggestions.extend(faq_utility["issues"])
        
        # 摘要优化建议
        if summary_completeness["score"] < 0.7:
            suggestions.extend(summary_completeness["issues"])
        
        # 通用优化建议
        if not suggestions:
            suggestions.append("知识条目质量良好，建议定期更新以保持时效性")
        
        return suggestions
    
    def _determine_approval_status(self, overall_score: float) -> str:
        """确定批准状态"""
        if overall_score >= self.min_approval_score:
            return "approved"
        elif overall_score >= self.review_required_score:
            return "review_required"
        else:
            return "rejected"


def assess_business_value(knowledge_entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    评估业务价值的便捷函数
    
    Args:
        knowledge_entry: 知识条目
        
    Returns:
        业务价值评估结果
    """
    assessor = BusinessValueAssessor()
    return assessor.assess_business_value(knowledge_entry)


def main():
    """主函数 - 测试用"""
    print("=" * 80)
    print("业务价值评估测试")
    print("=" * 80)
    
    # 测试知识条目1：高质量
    knowledge_entry1 = {
        "title": "员工年假管理规定",
        "content": "员工年假管理规定：根据工龄计算年假天数，工龄满1年不满10年的，年休假5天；已满10年不满20年的，年休假10天；已满20年的，年休假15天。员工申请年假需要提前3个工作日提交申请，经部门经理审批后方可休假。",
        "knowledge_type": "政策文档",
        "tags": [
            {"tag_name": "年假", "category": "政策类", "confidence": 0.95},
            {"tag_name": "工龄计算", "category": "流程类", "confidence": 0.88},
            {"tag_name": "申请流程", "category": "流程类", "confidence": 0.92}
        ],
        "faqs": [
            {"question": "年假天数如何计算？", "answer": "根据工龄计算...", "confidence": 0.9},
            {"question": "如何申请年假？", "answer": "需要提前3个工作日提交申请...", "confidence": 0.85},
            {"question": "年假可以累积吗？", "answer": "年假当年有效，不可累积...", "confidence": 0.8}
        ],
        "summary": "本政策规定了员工年假的天数计算标准、申请流程和审批要求。",
        "target_audience": "全体员工"
    }
    
    # 测试知识条目2：低质量
    knowledge_entry2 = {
        "title": "办公用品管理",
        "content": "办公用品管理说明。",
        "knowledge_type": "流程指南",
        "tags": [
            {"tag_name": "办公用品", "category": "其他", "confidence": 0.6}
        ],
        "faqs": [],
        "summary": "",
        "target_audience": "全体员工"
    }
    
    print("\n【测试1】高质量知识条目评估:")
    result1 = assess_business_value(knowledge_entry1)
    print(f"综合评分: {result1['overall_score']:.2f}")
    print(f"批准状态: {result1['approval_status']}")
    print(f"标签价值: {result1['dimension_scores']['tag_value']['level']} ({result1['dimension_scores']['tag_value']['score']:.2f})")
    print(f"FAQ实用性: {result1['dimension_scores']['faq_utility']['level']} ({result1['dimension_scores']['faq_utility']['score']:.2f})")
    print(f"摘要完整性: {result1['dimension_scores']['summary_completeness']['level']} ({result1['dimension_scores']['summary_completeness']['score']:.2f})")
    print(f"优化建议: {result1['optimization_suggestions']}")
    
    print("\n【测试2】低质量知识条目评估:")
    result2 = assess_business_value(knowledge_entry2)
    print(f"综合评分: {result2['overall_score']:.2f}")
    print(f"批准状态: {result2['approval_status']}")
    print(f"优化建议: {result2['optimization_suggestions']}")


if __name__ == "__main__":
    main()