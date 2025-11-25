#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAQ完整性检查清单
用于验证从文档生成的FAQ是否完整覆盖了关键内容
"""

from typing import Dict, List, Any, Optional
import json
import re
import sys
import argparse
import os
import logging
from dataclasses import dataclass, asdict
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    logger.warning("PyPDF2未安装，PDF文件支持将不可用。请运行: pip install PyPDF2")


class DocumentType(Enum):
    """文档类型枚举"""
    EMPLOYEE_HANDBOOK = "employee_handbook"
    POLICY_DOCUMENT = "policy_document"
    OPERATION_GUIDE = "operation_guide"
    PRODUCT_MANUAL = "product_manual"


@dataclass
class CompletenessCheckResult:
    """完整性检查结果"""
    document_type: str
    total_sections: int
    covered_sections: int
    section_coverage_rate: float
    total_key_points: int
    covered_key_points: int
    key_point_coverage_rate: float
    faq_count: int
    min_faq_count_met: bool
    priority_coverage: Dict[str, bool]
    overall_score: float
    recommendations: List[str]
    covered_section_names: List[str] = None
    uncovered_section_names: List[str] = None
    
    def __post_init__(self):
        if self.covered_section_names is None:
            self.covered_section_names = []
        if self.uncovered_section_names is None:
            self.uncovered_section_names = []


class FAQCompletenessChecker:
    """FAQ完整性检查器"""
    
    def __init__(self):
        self.checklist_templates = self._load_checklist_templates()
        self.stats = {
            "total_faqs": 0,
            "sections_checked": 0,
            "key_points_checked": 0
        }
    
    def _load_checklist_templates(self) -> Dict[str, Any]:
        """加载检查清单模板"""
        return {
            DocumentType.EMPLOYEE_HANDBOOK.value: {
                "name": "员工手册检查清单",
                "sections": [
                    {"name": "公司概况", "priority": "high", "key_points": ["公司介绍", "企业文化", "业务范围"]},
                    {"name": "总则", "priority": "high", "key_points": ["适用范围", "员工定义", "手册效力"]},
                    {"name": "员工聘用", "priority": "high", "key_points": ["聘用原则", "招聘流程", "入职材料"]},
                    {"name": "劳动合同", "priority": "high", "key_points": ["合同类型", "签订要求", "特殊情形"]},
                    {"name": "试用期管理", "priority": "high", "key_points": ["试用期期限", "考核标准", "不符合录用条件"]},
                    {"name": "考勤休假", "priority": "high", "key_points": ["工作时间", "考勤方式", "迟到早退", "旷工", "各类假期"]},
                    {"name": "劳动合同解除", "priority": "medium", "key_points": ["解除条件", "解除流程", "经济补偿"]},
                    {"name": "奖惩管理", "priority": "medium", "key_points": ["奖励类型", "处罚类型", "适用情形"]},
                    {"name": "廉洁承诺", "priority": "high", "key_points": ["行为规范", "禁止行为", "举报方式"]},
                    {"name": "入职指引", "priority": "high", "key_points": ["办理事项", "系统登录", "信息采集"]},
                    {"name": "薪酬福利", "priority": "high", "key_points": ["薪资结构", "五险一金", "商业保险", "薪资发放"]}
                ],
                "min_faq_count": 30,
                "coverage_threshold": 0.8
            },
            DocumentType.POLICY_DOCUMENT.value: {
                "name": "政策文档检查清单",
                "sections": [
                    {"name": "政策目的", "priority": "high", "key_points": ["制定背景", "适用范围", "政策目标"]},
                    {"name": "政策内容", "priority": "high", "key_points": ["核心条款", "执行标准", "例外情况"]},
                    {"name": "执行流程", "priority": "high", "key_points": ["申请流程", "审批流程", "操作流程"]},
                    {"name": "责任分工", "priority": "medium", "key_points": ["部门职责", "岗位职责", "监督责任"]},
                    {"name": "违规处理", "priority": "medium", "key_points": ["违规情形", "处理措施", "申诉渠道"]}
                ],
                "min_faq_count": 15,
                "coverage_threshold": 0.85
            }
        }
    
    def check_completeness(self, document_type: str, faq_data: List[Dict], 
                          source_content: str) -> CompletenessCheckResult:
        """
        检查FAQ完整性
        
        Args:
            document_type: 文档类型
            faq_data: FAQ数据列表
            source_content: 源文档内容
        
        Returns:
            完整性检查结果
        """
        if document_type not in self.checklist_templates:
            raise ValueError(f"不支持的文档类型: {document_type}")
        
        template = self.checklist_templates[document_type]
        
        # 分析章节覆盖情况
        section_coverage = self._check_section_coverage(template["sections"], faq_data, source_content)
        
        # 分析关键点覆盖情况
        key_point_coverage = self._check_key_point_coverage(template["sections"], faq_data, source_content)
        
        # 检查FAQ数量
        faq_count = len(faq_data)
        min_faq_count_met = faq_count >= template["min_faq_count"]
        
        # 计算优先级覆盖
        priority_coverage = self._check_priority_coverage(template["sections"], section_coverage)
        
        # 计算总体得分
        overall_score = self._calculate_overall_score(
            section_coverage["coverage_rate"],
            key_point_coverage["coverage_rate"],
            faq_count,
            template["min_faq_count"],
            priority_coverage
        )
        
        # 生成改进建议
        recommendations = self._generate_recommendations(
            template["sections"],
            section_coverage,
            key_point_coverage,
            faq_count,
            template["min_faq_count"],
            priority_coverage
        )
        
        # 保存详细的覆盖信息用于调试
        self.stats["section_coverage"] = section_coverage
        self.stats["key_point_coverage"] = key_point_coverage
        
        return CompletenessCheckResult(
            document_type=document_type,
            total_sections=len(template["sections"]),
            covered_sections=section_coverage["covered_count"],
            section_coverage_rate=section_coverage["coverage_rate"],
            total_key_points=key_point_coverage["total_count"],
            covered_key_points=key_point_coverage["covered_count"],
            key_point_coverage_rate=key_point_coverage["coverage_rate"],
            faq_count=faq_count,
            min_faq_count_met=min_faq_count_met,
            priority_coverage=priority_coverage,
            overall_score=overall_score,
            recommendations=recommendations,
            covered_section_names=section_coverage.get("covered_sections", []),
            uncovered_section_names=section_coverage.get("uncovered_sections", [])
        )
    
    def _check_section_coverage(self, sections: List[Dict], faq_data: List[Dict], 
                               source_content: str) -> Dict[str, Any]:
        """检查章节覆盖情况"""
        covered_sections = []
        uncovered_sections = []
        
        for section in sections:
            section_name = section["name"]
            # 检查FAQ中是否提及该章节
            section_mentioned = any(
                self._is_section_mentioned(section_name, faq.get("question", "")) or
                self._is_section_mentioned(section_name, faq.get("answer", ""))
                for faq in faq_data
            )
            
            # 检查源文档中是否有相关内容
            content_exists = self._is_section_mentioned(section_name, source_content)
            
            if section_mentioned and content_exists:
                covered_sections.append(section_name)
            elif content_exists:
                uncovered_sections.append(section_name)
        
        return {
            "covered_count": len(covered_sections),
            "uncovered_count": len(uncovered_sections),
            "coverage_rate": len(covered_sections) / len(sections) if sections else 0,
            "covered_sections": covered_sections,
            "uncovered_sections": uncovered_sections
        }
    
    def _check_key_point_coverage(self, sections: List[Dict], faq_data: List[Dict],
                                 source_content: str) -> Dict[str, Any]:
        """检查关键点覆盖情况"""
        total_key_points = 0
        covered_key_points = 0
        coverage_details = []
        
        for section in sections:
            for key_point in section.get("key_points", []):
                total_key_points += 1
                
                # 检查FAQ中是否提及该关键点
                key_point_mentioned = any(
                    self._is_key_point_mentioned(key_point, faq.get("question", "")) or
                    self._is_key_point_mentioned(key_point, faq.get("answer", ""))
                    for faq in faq_data
                )
                
                # 检查源文档中是否有相关内容
                content_exists = self._is_key_point_mentioned(key_point, source_content)
                
                if key_point_mentioned and content_exists:
                    covered_key_points += 1
                    coverage_details.append({"key_point": key_point, "covered": True})
                elif content_exists:
                    coverage_details.append({"key_point": key_point, "covered": False})
        
        return {
            "total_count": total_key_points,
            "covered_count": covered_key_points,
            "coverage_rate": covered_key_points / total_key_points if total_key_points > 0 else 0,
            "details": coverage_details
        }
    
    def _check_priority_coverage(self, sections: List[Dict], 
                                section_coverage: Dict[str, Any]) -> Dict[str, bool]:
        """检查优先级覆盖情况"""
        priority_coverage = {"high": True, "medium": True, "low": True}
        
        for section in sections:
            priority = section.get("priority", "medium")
            section_name = section["name"]
            
            if section_name in section_coverage.get("uncovered_sections", []):
                if priority == "high":
                    priority_coverage["high"] = False
                elif priority == "medium":
                    priority_coverage["medium"] = False
        
        return priority_coverage
    
    def _is_section_mentioned(self, section_name: str, text: str) -> bool:
        """检查章节是否在文本中被提及"""
        if not text or not section_name:
            return False
        
        # 简化的匹配逻辑，实际应用中可以使用更复杂的NLP技术
        keywords = section_name.replace("、", " ").replace("，", " ").replace("：", " ").split()
        keywords = [kw.strip() for kw in keywords if kw.strip()]
        
        if not keywords:
            return False
        
        # 检查是否有任何关键词在文本中出现
        text_lower = text.lower()
        for keyword in keywords:
            if keyword.lower() in text_lower:
                return True
        return False
    
    def _is_section_content_covered(self, section: Dict, faq_data: List[Dict],
                                   source_content: str) -> bool:
        """深度检查：分析FAQ内容是否涉及该章节的知识点"""
        section_name = section["name"]
        key_points = section.get("key_points", [])
        
        # 获取该章节在源文档中的内容
        section_content = self._extract_section_content(section_name, source_content)
        if not section_content:
            return False
        
        # 分析该章节的核心概念和关键词
        section_keywords = self._extract_section_keywords(section_name, section_content)
        
        # 检查是否有FAQ涉及这些核心概念
        for faq in faq_data:
            faq_text = f"{faq.get('question', '')} {faq.get('answer', '')}"
            if self._has_concept_overlap(faq_text, section_keywords):
                return True
        
        return False
    
    def _extract_section_content(self, section_name: str, source_content: str) -> str:
        """从源文档中提取指定章节的内容"""
        # 简化的章节提取逻辑
        # 实际应用中可以使用更复杂的文本分割算法
        lines = source_content.split('\n')
        section_lines = []
        in_section = False
        
        for i, line in enumerate(lines):
            if section_name in line:
                in_section = True
                section_lines.append(line)
            elif in_section and i < len(lines) - 1:
                # 检查下一行是否是新的章节开始
                next_line = lines[i + 1]
                if self._is_new_section_start(next_line):
                    break
                section_lines.append(line)
        
        return '\n'.join(section_lines)
    
    def _is_new_section_start(self, line: str) -> bool:
        """判断一行是否是新章节的开始"""
        # 检查是否匹配章节标题模式，如："一、" "二、" "三、" 或 "1." "2." "3."
        patterns = [
            r'^[一二三四五六七八九十]+、',  # 中文数字章节
            r'^\d+\.\d+\s',  # 数字章节，如 3.1
            r'^[A-Z]\.',  # 字母章节，如 A.
            r'^第[一二三四五六七八九十]+章',  # "第一章"格式
        ]
        
        for pattern in patterns:
            if re.match(pattern, line.strip()):
                return True
        return False
    
    def _extract_section_keywords(self, section_name: str, section_content: str) -> List[str]:
        """提取章节的核心关键词"""
        keywords = []
        
        # 添加章节名称作为关键词
        keywords.extend(section_name.replace("、", " ").split())
        
        # 从内容中提取高频词和关键短语
        words = re.findall(r'\b\w+\b', section_content.lower())
        # 过滤停用词
        stop_words = {'的', '了', '和', '是', '在', '有', '我', '你', '他', '她', '它', '们', '这', '那', '个', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十'}
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 1]
        
        # 统计词频，取前10个高频词
        from collections import Counter
        word_counts = Counter(meaningful_words)
        top_words = [word for word, count in word_counts.most_common(10)]
        
        keywords.extend(top_words)
        
        # 去重
        return list(set(keywords))
    
    def _has_concept_overlap(self, faq_text: str, section_keywords: List[str]) -> bool:
        """检查FAQ文本是否与章节关键词有概念重叠"""
        faq_text_lower = faq_text.lower()
        
        # 检查是否有任何关键词在FAQ中出现
        for keyword in section_keywords:
            if keyword.lower() in faq_text_lower:
                return True
        
        # 检查语义相似性（简化版）
        # 实际应用中可以使用词向量或预训练语言模型
        return False
    
    def _is_key_point_mentioned(self, key_point: str, text: str) -> bool:
        """检查关键点是否在文本中被提及"""
        if not text or not key_point:
            return False
        
        # 扩展匹配逻辑：支持同义词和近义词
        key_point_variants = self._generate_key_point_variants(key_point)
        
        text_lower = text.lower()
        for variant in key_point_variants:
            if variant.lower() in text_lower:
                return True
        
        return False
    
    def _generate_key_point_variants(self, key_point: str) -> List[str]:
        """生成关键点的变体形式（同义词、近义词）"""
        variants = [key_point]
        
        # 添加常见变体
        if "解除" in key_point:
            variants.extend(["辞退", "终止", "结束"])
        if "合同" in key_point:
            variants.extend(["协议", "合约"])
        if "条件" in key_point:
            variants.extend(["要求", "标准"])
        
        return list(set(variants))
    
    def get_detailed_stats(self) -> Dict[str, Any]:
        """获取详细统计信息"""
        return self.stats
    
    def _calculate_overall_score(self, section_coverage_rate: float,
                                key_point_coverage_rate: float,
                                faq_count: int,
                                min_faq_count: int,
                                priority_coverage: Dict[str, bool]) -> float:
        """计算总体得分"""
        # 各维度权重
        weights = {
            "section_coverage": 0.3,
            "key_point_coverage": 0.4,
            "faq_count": 0.2,
            "priority_coverage": 0.1
        }
        
        # 计算各项得分
        section_score = section_coverage_rate * weights["section_coverage"]
        
        key_point_score = key_point_coverage_rate * weights["key_point_coverage"]
        
        faq_count_score = (min(faq_count / min_faq_count, 1.0) * 
                          weights["faq_count"]) if min_faq_count > 0 else 0
        
        priority_score = (1.0 * weights["priority_coverage"] if priority_coverage.get("high") 
                         else 0.5 * weights["priority_coverage"])
        
        return section_score + key_point_score + faq_count_score + priority_score
    
    def _generate_recommendations(self, sections: List[Dict],
                                 section_coverage: Dict[str, Any],
                                 key_point_coverage: Dict[str, Any],
                                 faq_count: int,
                                 min_faq_count: int,
                                 priority_coverage: Dict[str, bool]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 检查章节覆盖
        if section_coverage["coverage_rate"] < 0.8:
            recommendations.append(
                f"章节覆盖率仅为{section_coverage['coverage_rate']:.1%}，建议增加以下章节的FAQ: "
                f"{', '.join(section_coverage['uncovered_sections'][:3])}"
            )
        
        # 检查关键点覆盖
        if key_point_coverage["coverage_rate"] < 0.85:
            uncovered_points = [d["key_point"] for d in key_point_coverage["details"] if not d["covered"]]
            recommendations.append(
                f"关键点覆盖率为{key_point_coverage['coverage_rate']:.1%}，建议补充以下关键点: "
                f"{', '.join(uncovered_points[:5])}"
            )
        
        # 检查FAQ数量
        if faq_count < min_faq_count:
            recommendations.append(
                f"FAQ数量不足，当前{faq_count}个，建议至少{min_faq_count}个"
            )
        
        # 检查高优先级覆盖
        if not priority_coverage.get("high"):
            recommendations.append(
                "存在高优先级章节未覆盖，请优先补充这些章节的FAQ"
            )
        
        return recommendations


def parse_faq_file(faq_file_path: str) -> List[Dict[str, str]]:
    """
    解析FAQ Markdown文件，提取问答对
    
    Args:
        faq_file_path: FAQ文件路径
        
    Returns:
        FAQ数据列表
    """
    if not os.path.exists(faq_file_path):
        logger.error(f"FAQ文件不存在: {faq_file_path}")
        return []
    
    try:
        with open(faq_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content:
            logger.warning(f"FAQ文件为空: {faq_file_path}")
            return []
        
        faq_data = []
        # 匹配FAQ格式：### Qxx: 问题标题
        faq_pattern = r'### Q\d+:\s*(.+?)\n\*\*A:\*\*\s*(.+?)(?=\n\n### Q|\n\n---|\Z)'
        matches = re.findall(faq_pattern, content, re.DOTALL)
        
        logger.info(f"从FAQ文件中提取到 {len(matches)} 个问答对")
        
        for question, answer in matches:
            # 清理多余的空白字符
            question = question.strip()
            answer = answer.strip()
            if question and answer:  # 确保问题和答案都不为空
                faq_data.append({
                    "question": question,
                    "answer": answer
                })
        
        if not faq_data:
            logger.warning(f"未能从文件中提取任何FAQ: {faq_file_path}")
            logger.info("请确保FAQ格式正确：### Q1: 问题标题\\n**A:** 答案内容")
        
        return faq_data
    except UnicodeDecodeError:
        logger.error(f"文件编码问题，请确保文件为UTF-8编码: {faq_file_path}")
        return []
    except Exception as e:
        logger.error(f"读取FAQ文件失败: {e}")
        return []


def parse_pdf_file(pdf_file_path: str) -> str:
    """
    解析PDF文件，提取文本内容
    
    Args:
        pdf_file_path: PDF文件路径
        
    Returns:
        PDF文本内容
    """
    if not PDF_SUPPORT:
        logger.error("PyPDF2未安装，无法读取PDF文件。请运行: pip install PyPDF2")
        return ""
    
    try:
        with open(pdf_file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text_content = []
            
            logger.info(f"PDF文件共有 {len(pdf_reader.pages)} 页")
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                    else:
                        logger.warning(f"第 {page_num + 1} 页未能提取文本")
                except Exception as e:
                    logger.warning(f"提取第 {page_num + 1} 页文本时出错: {e}")
            
            full_text = "\n".join(text_content)
            logger.info(f"成功提取 {len(full_text)} 个字符")
            return full_text
    
    except Exception as e:
        logger.error(f"读取PDF文件失败: {e}")
        return ""


def parse_source_file(source_file_path: str) -> str:
    """
    解析源文档文件（支持PDF和文本格式）
    
    Args:
        source_file_path: 源文档路径
        
    Returns:
        源文档内容
    """
    if not os.path.exists(source_file_path):
        logger.error(f"源文档不存在: {source_file_path}")
        return ""
    
    # 根据文件扩展名选择解析方式
    file_ext = os.path.splitext(source_file_path)[1].lower()
    
    if file_ext == '.pdf':
        logger.info(f"检测到PDF文件，使用PDF解析器: {source_file_path}")
        return parse_pdf_file(source_file_path)
    else:
        # 默认为文本文件
        try:
            with open(source_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content:
                logger.warning(f"源文档为空: {source_file_path}")
            
            logger.info(f"成功读取源文档，共 {len(content)} 个字符")
            return content
        except UnicodeDecodeError:
            logger.error(f"文件编码问题，请确保文件为UTF-8编码: {source_file_path}")
            return ""
        except Exception as e:
            logger.error(f"读取源文档失败: {e}")
            return ""


def main():
    """主函数：命令行用法"""
    parser = argparse.ArgumentParser(
        description='FAQ完整性检查工具 - 验证生成的FAQ是否完整覆盖源文档的关键内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 检查员工手册FAQ完整性
  python faq_completeness_checklist.py 员工手册FAQ.md 员工手册.pdf --type employee_handbook
  
  # 检查政策文档FAQ完整性
  python faq_completeness_checklist.py 政策FAQ.md 政策文档.pdf --type policy_document
  
  # 显示详细信息和调试日志
  python faq_completeness_checklist.py 员工手册FAQ.md 员工手册.pdf --type employee_handbook --verbose
  
  # 显示帮助信息
  python faq_completeness_checklist.py --help
        
依赖说明:
  - 支持Markdown格式的FAQ文件
  - 支持PDF和文本格式的源文档
  - 如需PDF支持，请安装: pip install PyPDF2
        """
    )
    
    parser.add_argument('faq_file', help='FAQ文件路径（Markdown格式）')
    parser.add_argument('source_file', help='源文档路径（PDF或文本格式）')
    parser.add_argument('--type', default='employee_handbook',
                       choices=['employee_handbook', 'policy_document', 'operation_guide', 'product_manual'],
                       help='文档类型（决定检查标准和最低FAQ数量）')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细检查信息和调试日志')
    parser.add_argument('--debug', '-d', action='store_true', help='启用调试模式（显示更多技术细节）')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)
    
    logger.info("=" * 70)
    logger.info("FAQ完整性检查工具启动")
    logger.info("=" * 70)
    
    # 检查文件是否存在
    if not os.path.isfile(args.faq_file):
        logger.error(f"FAQ文件不存在或不是文件: {args.faq_file}")
        print(f"❌ 错误：FAQ文件不存在: {args.faq_file}", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.isfile(args.source_file):
        logger.error(f"源文档不存在或不是文件: {args.source_file}")
        print(f"❌ 错误：源文档不存在: {args.source_file}", file=sys.stderr)
        sys.exit(1)
    
    logger.info(f"FAQ文件: {args.faq_file}")
    logger.info(f"源文档: {args.source_file}")
    logger.info(f"文档类型: {args.type}")
    
    # 解析文件
    logger.info("开始解析FAQ文件...")
    faq_data = parse_faq_file(args.faq_file)
    
    logger.info("开始解析源文档...")
    source_content = parse_source_file(args.source_file)
    
    if not faq_data:
        logger.error("未能读取有效的FAQ数据")
        print("❌ 错误：未能读取有效的FAQ数据", file=sys.stderr)
        sys.exit(1)
    
    if not source_content:
        logger.error("未能读取有效的源文档内容")
        print("❌ 错误：未能读取有效的源文档内容", file=sys.stderr)
        sys.exit(1)
    
    logger.info(f"成功提取 {len(faq_data)} 个FAQ问答对")
    logger.info(f"源文档内容长度: {len(source_content)} 字符")
    
    # 执行完整性检查
    logger.info("开始执行完整性检查...")
    checker = FAQCompletenessChecker()
    result = checker.check_completeness(
        document_type=args.type,
        faq_data=faq_data,
        source_content=source_content
    )
    
    # 输出结果
    print("\n" + "=" * 70)
    print(" " * 20 + "FAQ完整性检查结果")
    print("=" * 70)
    print(f"📄 文档类型: {result.document_type}")
    print(f"📊 总体得分: {result.overall_score:.2f}/1.00")
    print(f"📚 章节覆盖率: {result.section_coverage_rate:.1%} ({result.covered_sections}/{result.total_sections})")
    print(f"🎯 关键点覆盖率: {result.key_point_coverage_rate:.1%} ({result.covered_key_points}/{result.total_key_points})")
    print(f"❓ FAQ数量: {result.faq_count}个")
    
    min_faq = 30 if args.type == 'employee_handbook' else 15
    print(f"📈 最低要求: {min_faq}个")
    
    # 状态指示
    status_emoji = "✅" if result.overall_score >= 0.7 and result.priority_coverage['high'] else "⚠️" if result.overall_score >= 0.5 else "❌"
    print(f"{status_emoji} 数量达标: {'是' if result.min_faq_count_met else '否'}")
    print(f"{status_emoji} 高优先级覆盖: {'是' if result.priority_coverage['high'] else '否'}")
    
    print("-" * 70)
    
    if result.recommendations:
        print("💡 改进建议:")
        for i, rec in enumerate(result.recommendations, 1):
            print(f"   {i}. {rec}")
    else:
        print("🎉 恭喜！FAQ完整性检查通过，无需改进。")
    
    # 详细模式
    if args.verbose or args.debug:
        print("\n" + "-" * 70)
        print("📋 详细信息:")
        print(f"   已覆盖章节: {', '.join(result.covered_section_names) if result.covered_section_names else '无'}")
        print(f"   未覆盖章节: {', '.join(result.uncovered_section_names) if result.uncovered_section_names else '无'}")
    
    print("=" * 70 + "\n")
    
    # 返回码
    success = result.overall_score >= 0.7 and result.priority_coverage['high']
    if success:
        logger.info("完整性检查通过！")
        print("\n🎉 恭喜！FAQ完整性检查通过，达到生产级标准。")
    else:
        logger.warning("完整性检查未通过，需要改进")
        print("\n⚠️  注意：FAQ完整性检查未通过，建议补充缺失内容。")
    
    # 输出JSON格式的详细结果，便于其他程序解析
    if args.debug:
        import json
        result_dict = {
            "document_type": result.document_type,
            "overall_score": round(result.overall_score, 2),
            "section_coverage_rate": round(result.section_coverage_rate, 2),
            "key_point_coverage_rate": round(result.key_point_coverage_rate, 2),
            "faq_count": result.faq_count,
            "min_faq_count_met": result.min_faq_count_met,
            "priority_coverage_high": result.priority_coverage['high'],
            "covered_sections": result.covered_section_names,
            "uncovered_sections": result.uncovered_section_names,
            "recommendations": result.recommendations,
            "passed": success
        }
        print(f"\n📊 JSON结果:\n{json.dumps(result_dict, ensure_ascii=False, indent=2)}")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()