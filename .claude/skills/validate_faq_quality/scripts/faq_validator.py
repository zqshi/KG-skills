#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAQ质量验证器
验证FAQ集合的质量，包括答案准确性、问题覆盖度、语言质量和实用价值评估
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple


class FAQQualityValidator:
    """FAQ质量验证器类"""
    
    def __init__(self, source_doc_path: str, faq_path: str):
        self.source_doc_path = source_doc_path
        self.faq_path = faq_path
        self.source_content = ""
        self.faq_content = ""
        self.faq_pairs = []
        
    def load_documents(self):
        """加载源文档和FAQ文档"""
        try:
            # 读取源文档 (PDF 文本)
            with open(self.source_doc_path, 'r', encoding='utf-8') as f:
                self.source_content = f.read()
            
            # 读取FAQ文档
            with open(self.faq_path, 'r', encoding='utf-8') as f:
                self.faq_content = f.read()
            
            # 解析FAQ对
            self._parse_faq_pairs()
            
        except Exception as e:
            print(f"加载文档时出错: {e}")
            sys.exit(1)
    
    def _parse_faq_pairs(self):
        """解析FAQ文档中的问答对"""
        # 使用正则表达式匹配Q和A
        q_pattern = r'### Q\d+:\s*(.+?)\n'
        a_pattern = r'\*\*A:\*\*\s*(.+?)(?=\n###|\n##|\Z)'
        
        questions = re.findall(q_pattern, self.faq_content, re.DOTALL)
        answers = re.findall(a_pattern, self.faq_content, re.DOTALL)
        
        self.faq_pairs = list(zip(questions, answers))
        print(f"成功解析 {len(self.faq_pairs)} 个FAQ对")
    
    def validate_accuracy(self) -> Tuple[float, List[Dict]]:
        """
        验证答案准确性
        检查FAQ答案是否与源文档内容一致
        """
        issues = []
        correct_count = 0
        
        for i, (question, answer) in enumerate(self.faq_pairs):
            # 清理答案文本
            clean_answer = self._clean_text(answer)
            
            # 检查关键信息是否在源文档中
            accuracy_score = self._check_accuracy(clean_answer, self.source_content)
            
            if accuracy_score < 0.7:
                issues.append({
                    "question": question.strip(),
                    "issue": f"答案准确性较低 ({accuracy_score:.2f})，可能与源文档不一致",
                    "severity": "high" if accuracy_score < 0.5 else "medium"
                })
            else:
                correct_count += 1
        
        accuracy_rate = correct_count / len(self.faq_pairs) if self.faq_pairs else 0
        return accuracy_rate, issues
    
    def validate_coverage(self) -> Tuple[float, List[Dict]]:
        """
        验证问题覆盖度
        检查FAQ是否覆盖源文档的主要主题
        """
        # 提取源文档的主要主题
        source_topics = self._extract_key_topics(self.source_content)
        
        # 提取FAQ中的主题
        faq_topics = []
        for question, _ in self.faq_pairs:
            faq_topics.extend(self._extract_keywords(question))
        
        # 计算覆盖度
        covered_topics = 0
        missing_topics = []
        
        for topic in source_topics:
            if any(self._topic_match(topic, faq_topic) for faq_topic in faq_topics):
                covered_topics += 1
            else:
                missing_topics.append(topic)
        
        coverage_rate = covered_topics / len(source_topics) if source_topics else 0
        
        issues = []
        for topic in missing_topics[:5]:  # 只显示前5个缺失主题
            issues.append({
                "topic": topic,
                "importance": self._assess_topic_importance(topic, self.source_content)
            })
        
        return coverage_rate, issues
    
    def validate_clarity(self) -> Tuple[float, List[Dict]]:
        """
        验证语言清晰度
        评估问题表述和答案的清晰度
        """
        issues = []
        clear_count = 0
        
        for question, answer in self.faq_pairs:
            # 评估问题清晰度
            q_clarity = self._assess_clarity(question)
            
            # 评估答案清晰度
            a_clarity = self._assess_clarity(answer)
            
            avg_clarity = (q_clarity + a_clarity) / 2
            
            if avg_clarity < 3.0:
                issues.append({
                    "question": question.strip(),
                    "problem": f"清晰度评分较低 ({avg_clarity:.1f}/5.0)",
                    "suggestion": "建议简化表述，使用更清晰的结构"
                })
            else:
                clear_count += 1
        
        clarity_rate = clear_count / len(self.faq_pairs) if self.faq_pairs else 0
        return clarity_rate, issues
    
    def validate_usability(self) -> Tuple[float, List[Dict]]:
        """
        验证实用价值
        评估FAQ的实际使用价值
        """
        issues = []
        usable_count = 0
        
        for question, answer in self.faq_pairs:
            usability_score = self._assess_usability(question, answer)
            
            if usability_score < 3.0:
                issues.append({
                    "question": question.strip(),
                    "issue": f"实用性评分较低 ({usability_score:.1f}/5.0)",
                    "suggestion": "建议增加具体示例或操作步骤"
                })
            else:
                usable_count += 1
        
        usability_rate = usable_count / len(self.faq_pairs) if self.faq_pairs else 0
        return usability_rate, issues
    
    def generate_report(self) -> Dict[str, Any]:
        """生成完整的质量验证报告"""
        print("开始验证答案准确性...")
        accuracy, accuracy_issues = self.validate_accuracy()
        
        print("开始验证问题覆盖度...")
        coverage, coverage_issues = self.validate_coverage()
        
        print("开始验证语言清晰度...")
        clarity, clarity_issues = self.validate_clarity()
        
        print("开始验证实用价值...")
        usability, usability_issues = self.validate_usability()
        
        # 计算综合评分
        overall_score = (accuracy * 0.3 + coverage * 0.3 + clarity * 0.2 + usability * 0.2) * 100
        
        report = {
            "quality_summary": {
                "overall_score": round(overall_score, 1),
                "dimension_scores": {
                    "accuracy": round(accuracy * 100, 1),
                    "coverage": round(coverage * 100, 1),
                    "clarity": round(clarity * 100, 1),
                    "usability": round(usability * 100, 1)
                },
                "total_faqs": len(self.faq_pairs)
            },
            "detailed_analysis": {
                "incorrect_answers": accuracy_issues,
                "missing_questions": coverage_issues,
                "ambiguity_issues": clarity_issues,
                "usability_issues": usability_issues
            },
            "improvement_recommendations": self._generate_recommendations(
                accuracy_issues, coverage_issues, clarity_issues, usability_issues
            )
        }
        
        return report
    
    def _clean_text(self, text: str) -> str:
        """清理文本，移除markdown标记"""
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'\* ', '', text)
        text = re.sub(r'- ', '', text)
        text = re.sub(r'\n+', ' ', text)
        return text.strip()
    
    def _check_accuracy(self, answer: str, source: str) -> float:
        """检查答案准确性"""
        # 提取答案中的关键信息
        answer_keywords = self._extract_keywords(answer)
        
        if not answer_keywords:
            return 0.5
        
        # 检查关键信息在源文档中的匹配程度
        matched_keywords = 0
        for keyword in answer_keywords:
            if keyword in source:
                matched_keywords += 1
        
        return matched_keywords / len(answer_keywords)
    
    def _extract_key_topics(self, content: str) -> List[str]:
        """提取关键主题"""
        # 提取标题和关键词
        titles = re.findall(r'[一二三四五六七八九十]+、(\S+)', content)
        titles.extend(re.findall(r'\d+\.(\S+)', content))
        
        # 提取高频名词
        words = re.findall(r'[\u4e00-\u9fff]{2,4}', content)
        word_freq = {}
        for word in words:
            if len(word) >= 2:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 返回高频词作为主题
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        topics = titles + [word for word, freq in sorted_words[:20] if freq > 3]
        
        return list(set(topics))[:15]  # 去重并限制数量
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 提取2-4个字符的词
        words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        return list(set(words))
    
    def _topic_match(self, topic1: str, topic2: str) -> bool:
        """检查主题是否匹配"""
        return topic1 in topic2 or topic2 in topic1 or topic1[:2] == topic2[:2]
    
    def _assess_topic_importance(self, topic: str, content: str) -> str:
        """评估主题重要性"""
        count = content.count(topic)
        if count > 10:
            return "high"
        elif count > 5:
            return "medium"
        else:
            return "low"
    
    def _assess_clarity(self, text: str) -> float:
        """评估文本清晰度"""
        # 简单的清晰度评估
        score = 5.0
        
        # 检查句子长度
        sentences = re.split(r'[。！？\n]+', text)
        long_sentences = [s for s in sentences if len(s) > 50]
        
        if len(long_sentences) > len(sentences) * 0.5:
            score -= 1.5
        
        # 检查复杂词汇
        complex_words = re.findall(r'[\u4e00-\u9fff]{5,}', text)
        if len(complex_words) > 5:
            score -= 1.0
        
        # 检查列表使用
        if re.search(r'\d+\)|[①②③④⑤]', text):
            score += 0.5
        
        return max(1.0, min(5.0, score))
    
    def _assess_usability(self, question: str, answer: str) -> float:
        """评估实用性"""
        score = 3.0
        
        # 检查是否包含具体操作步骤
        if re.search(r'\d+\.|[①②③④⑤]|步骤|流程|方法', answer):
            score += 1.0
        
        # 检查是否包含示例
        if re.search(r'例如|比如|示例|如：', answer):
            score += 0.5
        
        # 检查问题是否具体
        if len(question) > 10 and re.search(r'[如何怎样哪里什么何时]', question):
            score += 0.5
        
        return max(1.0, min(5.0, score))
    
    def _generate_recommendations(self, accuracy_issues, coverage_issues, clarity_issues, usability_issues) -> List[Dict]:
        """生成改进建议"""
        recommendations = []
        
        if accuracy_issues:
            recommendations.append({
                "priority": "high",
                "recommendation": f"修正 {len(accuracy_issues)} 个答案准确性问题",
                "estimated_effort": f"{len(accuracy_issues) * 0.5} 小时"
            })
        
        if coverage_issues:
            recommendations.append({
                "priority": "high",
                "recommendation": f"补充 {len(coverage_issues)} 个缺失的重要主题",
                "estimated_effort": f"{len(coverage_issues) * 1} 小时"
            })
        
        if clarity_issues:
            recommendations.append({
                "priority": "medium",
                "recommendation": f"优化 {len(clarity_issues)} 个FAQ的语言清晰度",
                "estimated_effort": f"{len(clarity_issues) * 0.3} 小时"
            })
        
        if usability_issues:
            recommendations.append({
                "priority": "medium",
                "recommendation": f"提升 {len(usability_issues)} 个FAQ的实用性，增加具体示例",
                "estimated_effort": f"{len(usability_issues) * 0.5} 小时"
            })
        
        if not recommendations:
            recommendations.append({
                "priority": "low",
                "recommendation": "FAQ质量良好，建议定期更新以保持时效性",
                "estimated_effort": "0.5 小时/月"
            })
        
        return recommendations
    
    def print_report(self, report: Dict[str, Any]):
        """打印验证报告"""
        print("\n" + "="*60)
        print("FAQ质量验证报告")
        print("="*60)
        
        summary = report["quality_summary"]
        print(f"\n📊 综合质量评分: {summary['overall_score']}/100")
        print(f"📋 FAQ总数: {summary['total_faqs']}")
        
        print("\n📈 各维度评分:")
        for dimension, score in summary["dimension_scores"].items():
            print(f"  • {dimension}: {score}/100")
        
        print("\n🔍 详细分析:")
        
        analysis = report["detailed_analysis"]
        
        if analysis["incorrect_answers"]:
            print(f"\n❌ 准确性问题 ({len(analysis['incorrect_answers'])}个):")
            for issue in analysis["incorrect_answers"][:3]:  # 只显示前3个
                print(f"  • {issue['question'][:50]}...")
                print(f"    问题: {issue['issue']}")
        
        if analysis["missing_questions"]:
            print(f"\n⚠️  覆盖度问题 - 缺失主题 ({len(analysis['missing_questions'])}个):")
            for issue in analysis["missing_questions"][:3]:
                print(f"  • {issue['topic']} (重要性: {issue['importance']})")
        
        if analysis["ambiguity_issues"]:
            print(f"\n💬 清晰度问题 ({len(analysis['ambiguity_issues'])}个):")
            for issue in analysis["ambiguity_issues"][:3]:
                print(f"  • {issue['question'][:50]}...")
        
        if analysis["usability_issues"]:
            print(f"\n🛠️  实用性问题 ({len(analysis['usability_issues'])}个):")
            for issue in analysis["usability_issues"][:3]:
                print(f"  • {issue['question'][:50]}...")
        
        print("\n💡 改进建议:")
        for i, rec in enumerate(report["improvement_recommendations"], 1):
            print(f"{i}. [{rec['priority']}] {rec['recommendation']}")
            print(f"   预计工作量: {rec['estimated_effort']}")


def main():
    """主函数"""
    if len(sys.argv) != 3:
        print("使用方法: python faq_validator.py <源文档路径> <FAQ文档路径>")
        sys.exit(1)
    
    source_path = sys.argv[1]
    faq_path = sys.argv[2]
    
    # 检查文件是否存在
    if not Path(source_path).exists():
        print(f"错误: 源文档不存在: {source_path}")
        sys.exit(1)
    
    if not Path(faq_path).exists():
        print(f"错误: FAQ文档不存在: {faq_path}")
        sys.exit(1)
    
    # 创建验证器并执行验证
    validator = FAQQualityValidator(source_path, faq_path)
    validator.load_documents()
    
    # 生成报告
    report = validator.generate_report()
    
    # 打印报告
    validator.print_report(report)
    
    # 保存详细报告到文件
    report_file = "faq_quality_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细报告已保存到: {report_file}")


if __name__ == "__main__":
    main()