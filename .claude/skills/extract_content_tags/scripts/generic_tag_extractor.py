#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用标签提取框架
基于 extract_content_tags skill 实现，支持多种业务场景配置
"""

import json
import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TagConfig:
    """标签配置"""
    name: str
    aliases: List[str] = field(default_factory=list)
    business_value: str = "中"
    description: str = ""
    
    def matches(self, text: str) -> bool:
        """检查标签是否匹配文本"""
        all_names = [self.name] + self.aliases
        return any(name in text for name in all_names)


@dataclass
class CategoryConfig:
    """分类配置"""
    name: str
    description: str
    tags: List[TagConfig] = field(default_factory=list)
    
    def get_tag(self, tag_name: str) -> Optional[TagConfig]:
        """根据名称获取标签配置"""
        for tag in self.tags:
            if tag.name == tag_name or tag_name in tag.aliases:
                return tag
        return None


@dataclass
class ExtractionResult:
    """提取结果"""
    tag_name: str
    category: str
    confidence: float
    relevance: float
    source: str
    business_value: str
    correctness_check: Optional[Dict[str, Any]] = None


class TagDeduplicator:
    """标签去重和归一化处理器"""
    
    def __init__(self, existing_tags: List[Dict[str, Any]]):
        self.existing_tags = existing_tags
        self.tag_index = self._build_index()
    
    def _build_index(self) -> Dict[str, List[Dict[str, Any]]]:
        """构建标签索引"""
        index = {}
        for tag in self.existing_tags:
            name = tag.get("name", "")
            aliases = tag.get("aliases", [])
            
            # 索引主名称
            if name:
                normalized = self._normalize(name)
                if normalized not in index:
                    index[normalized] = []
                index[normalized].append(tag)
            
            # 索引别名
            for alias in aliases:
                normalized = self._normalize(alias)
                if normalized not in index:
                    index[normalized] = []
                index[normalized].append(tag)
        
        return index
    
    def _normalize(self, tag_name: str) -> str:
        """标签名称归一化"""
        # 统一大小写
        normalized = tag_name.lower()
        # 去除特殊字符和空格
        normalized = re.sub(r'[^\w\s]', '', normalized)
        # 去除多余空格
        normalized = re.sub(r'\s+', '', normalized)
        return normalized
    
    def check_duplicate(self, new_tag: str) -> Dict[str, Any]:
        """
        检查新标签是否与现有标签重复或相似
        
        返回: {
            "is_duplicate": bool,
            "similarity": float,
            "existing_tag": dict,
            "action": "use_existing" | "create_new" | "review"
        }
        """
        normalized_new = self._normalize(new_tag)
        
        # 精确匹配检查
        if normalized_new in self.tag_index:
            exact_match = self.tag_index[normalized_new][0]
            return {
                "is_duplicate": True,
                "similarity": 1.0,
                "existing_tag": exact_match,
                "action": "use_existing"
            }
        
        # 相似度检查（简化版）
        # 实际应用中可使用更复杂的语义相似度算法
        max_similarity = 0
        most_similar = None
        
        for existing_normalized, tags in self.tag_index.items():
            # 计算编辑距离相似度
            similarity = self._calculate_similarity(normalized_new, existing_normalized)
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar = tags[0]
        
        if max_similarity >= 0.8:
            return {
                "is_duplicate": False,
                "similarity": max_similarity,
                "existing_tag": most_similar,
                "action": "review"
            }
        
        return {
            "is_duplicate": False,
            "similarity": 0.0,
            "existing_tag": None,
            "action": "create_new"
        }
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """计算字符串相似度（基于编辑距离）"""
        if not str1 or not str2:
            return 0.0
        
        # 转换为集合计算Jaccard相似度
        set1 = set(str1)
        set2 = set(str2)
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        if union == 0:
            return 0.0
        
        return intersection / union


class BusinessValueEvaluator:
    """业务价值评估器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.anti_patterns = [
            re.compile(r"^\d+$"),  # 纯数字
            re.compile(r"^\d{4}年$"),  # 年份
            re.compile(r"^\d+月$"),  # 月份
            re.compile(r"^\d+日$"),  # 日期
            re.compile(r"^\d+个工作日$"),  # 工作日
            re.compile(r"^Q\d$"),  # 季度
            re.compile(r"^\d+-\d+$"),  # 数字范围
        ]
        
        self.value_criteria = {
            "process": {"keywords": ["流程", "步骤", "操作", "办理"], "weight": 1.2},
            "material": {"keywords": ["材料", "证明", "附件", "文件"], "weight": 1.1},
            "requirement": {"keywords": ["要求", "条件", "标准", "资格"], "weight": 1.1},
            "policy": {"keywords": ["政策", "规定", "制度", "办法"], "weight": 1.0},
            "scenario": {"keywords": ["场景", "情况", "情形", "案例"], "weight": 0.9},
        }
    
    def evaluate(self, tag_name: str, document_content: str, 
                 category: str = "") -> Dict[str, Any]:
        """
        评估标签的业务价值
        
        返回: {
            "has_business_value": bool,
            "score": float,
            "reason": str,
            "recommendation": str
        }
        """
        # 检查反模式（无业务价值）
        for pattern in self.anti_patterns:
            if pattern.match(tag_name):
                return {
                    "has_business_value": False,
                    "score": 0.0,
                    "reason": "标签无明确业务含义（纯数字/时间）",
                    "recommendation": "移除该标签"
                }
        
        # 计算业务价值分数
        value_score = self._calculate_value_score(tag_name, category)
        
        # 计算相关性分数
        relevance_score = self._calculate_relevance(tag_name, document_content)
        
        # 综合评估
        final_score = (value_score + relevance_score) / 2
        
        if final_score > 0.6:
            return {
                "has_business_value": True,
                "score": final_score,
                "reason": f"标签具有明确的业务价值（分数: {final_score:.2f}）",
                "recommendation": "保留该标签"
            }
        else:
            return {
                "has_business_value": False,
                "score": final_score,
                "reason": f"标签业务价值较低（分数: {final_score:.2f}）",
                "recommendation": "重新评估或移除"
            }
    
    def _calculate_value_score(self, tag_name: str, category: str) -> float:
        """计算业务价值分数"""
        score = 0.5  # 基础分数
        
        # 根据关键词加分
        for criteria, config in self.value_criteria.items():
            if any(keyword in tag_name for keyword in config["keywords"]):
                score = max(score, 0.7 * config["weight"])
        
        # 根据分类加分
        high_value_categories = ["业务领域", "内容标签"]
        if category in high_value_categories:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_relevance(self, tag_name: str, content: str) -> float:
        """计算标签与文档内容的相关性"""
        if not content:
            return 0.0
        
        # 检查直接匹配
        if tag_name in content:
            return 0.9
        
        # 检查关键词匹配
        keywords = list(tag_name)
        matched = sum(1 for kw in keywords if kw in content and kw.strip())
        
        return min(matched / len(keywords) * 0.8, 0.8)


class GenericTagExtractor:
    """通用标签提取器"""
    
    def __init__(self, taxonomy_path: Optional[str] = None):
        """
        初始化提取器
        
        Args:
            taxonomy_path: 标签体系文件路径，如果为None则使用默认路径
        """
        self.taxonomy_path = Path(taxonomy_path) if taxonomy_path else Path("config/tag_taxonomy.json")
        self.taxonomy = self._load_taxonomy()
        self.document_content = ""
        self.extraction_results: List[ExtractionResult] = []
        
        # 初始化组件
        self.business_evaluator = BusinessValueEvaluator()
        
        logger.info(f"通用标签提取器初始化完成，加载 {self._get_total_tags()} 个标签")
    
    def _load_taxonomy(self) -> Dict[str, CategoryConfig]:
        """加载标签体系"""
        if not self.taxonomy_path.exists():
            raise FileNotFoundError(f"标签体系文件不存在: {self.taxonomy_path}")
        
        with open(self.taxonomy_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        categories = {}
        for cat_name, cat_data in data["categories"].items():
            tags = []
            for tag_data in cat_data["tags"]:
                tag = TagConfig(
                    name=tag_data["name"],
                    aliases=tag_data.get("aliases", []),
                    business_value=tag_data.get("business_value", "中"),
                    description=tag_data.get("description", "")
                )
                tags.append(tag)
            
            category = CategoryConfig(
                name=cat_name,
                description=cat_data["description"],
                tags=tags
            )
            categories[cat_name] = category
        
        return categories
    
    def _get_total_tags(self) -> int:
        """获取标签总数"""
        return sum(len(cat.tags) for cat in self.taxonomy.values())
    
    def set_document_content(self, content: str):
        """设置文档内容"""
        self.document_content = content
        logger.info(f"文档内容已设置，长度: {len(content)} 字符")
    
    def extract_tags(self, mode: str = "extraction", 
                     max_tags: int = 15,
                     min_confidence: float = 0.6) -> List[ExtractionResult]:
        """
        提取标签
        
        Args:
            mode: 提取模式，extraction（基于现有标签体系）或 mining（基于文档内容）
            max_tags: 最大标签数量
            min_confidence: 最小置信度阈值
        
        Returns:
            提取结果列表
        """
        if not self.document_content:
            raise ValueError("文档内容未设置，请先调用 set_document_content()")
        
        logger.info(f"开始提取标签，模式: {mode}, 最大数量: {max_tags}, 最小置信度: {min_confidence}")
        
        if mode == "extraction":
            results = self._extract_based_on_taxonomy(min_confidence)
        elif mode == "mining":
            results = self._extract_based_on_content(min_confidence)
        else:
            raise ValueError(f"不支持的模式: {mode}，请选择 'extraction' 或 'mining'")
        
        # 按置信度排序并限制数量
        results.sort(key=lambda x: x.confidence, reverse=True)
        results = results[:max_tags]
        
        self.extraction_results = results
        
        logger.info(f"标签提取完成，共提取 {len(results)} 个标签")
        return results
    
    def _extract_based_on_taxonomy(self, min_confidence: float) -> List[ExtractionResult]:
        """基于现有标签体系提取"""
        results = []
        
        for category_name, category in self.taxonomy.items():
            for tag in category.tags:
                # 计算置信度
                confidence = self._calculate_tag_confidence(tag, category_name)
                
                if confidence >= min_confidence:
                    # 评估业务价值
                    value_eval = self.business_evaluator.evaluate(
                        tag.name, self.document_content, category_name
                    )
                    
                    if value_eval["has_business_value"]:
                        result = ExtractionResult(
                            tag_name=tag.name,
                            category=category_name,
                            confidence=confidence,
                            relevance=confidence * 0.9,
                            source="existing_taxonomy",
                            business_value=tag.business_value
                        )
                        results.append(result)
        
        return results
    
    def _extract_based_on_content(self, min_confidence: float) -> List[ExtractionResult]:
        """基于文档内容挖掘（简化版）"""
        # 实际应用中可使用NLP技术进行实体识别和关键词提取
        # 这里使用简单的关键词频率统计作为示例
        
        results = []
        
        # 提取高频词作为候选标签
        words = re.findall(r'[\u4e00-\u9fff]{2,8}', self.document_content)
        word_freq = {}
        
        for word in words:
            if len(word) >= 2:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 选择高频词作为候选
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        for word, freq in sorted_words[:50]:  # 取前50个高频词
            confidence = min(0.5 + freq * 0.05, 0.95)
            
            if confidence >= min_confidence:
                # 评估业务价值
                value_eval = self.business_evaluator.evaluate(word, self.document_content)
                
                if value_eval["has_business_value"]:
                    result = ExtractionResult(
                        tag_name=word,
                        category="内容挖掘",
                        confidence=confidence,
                        relevance=confidence * 0.85,
                        source="content_mining",
                        business_value="中"
                    )
                    results.append(result)
        
        return results
    
    def _calculate_tag_confidence(self, tag: TagConfig, category: str) -> float:
        """计算标签置信度"""
        base_confidence = 0.6
        
        # 检查标签名称和别名在文档中的出现情况
        all_names = [tag.name] + tag.aliases
        
        for name in all_names:
            count = self.document_content.count(name)
            if count > 0:
                # 出现次数越多，置信度越高
                confidence_boost = min(count * 0.1, 0.3)
                base_confidence = max(base_confidence, 0.7 + confidence_boost)
                break
        
        # 检查是否在文档开头（标题区域）
        for name in all_names:
            if name in self.document_content[:200]:
                base_confidence += 0.1
                break
        
        # 根据业务价值调整
        if tag.business_value == "高":
            base_confidence += 0.05
        
        return min(base_confidence, 0.98)
    
    def perform_correctness_check(self) -> Dict[str, Any]:
        """执行标签正确性检测"""
        if not self.extraction_results:
            return {"status": "error", "message": "未提取标签"}
        
        passed_results = []
        failed_results = []
        
        for result in self.extraction_results:
            check_result = self._check_tag_correctness(result)
            result.correctness_check = check_result
            
            if check_result["passed"]:
                passed_results.append(result)
            else:
                failed_results.append(result)
        
        overall_accuracy = len(passed_results) / len(self.extraction_results) if self.extraction_results else 0
        
        return {
            "passed_tags": passed_results,
            "failed_tags": failed_results,
            "overall_accuracy": round(overall_accuracy, 2),
            "total_checked": len(self.extraction_results),
            "recommendations": self._generate_recommendations(failed_results)
        }
    
    def _check_tag_correctness(self, result: ExtractionResult) -> Dict[str, Any]:
        """检查单个标签的正确性"""
        tag_name = result.tag_name
        
        # 查找内容证据
        evidence = self._find_content_evidence(tag_name)
        
        if evidence:
            return {
                "passed": True,
                "content_evidence": evidence,
                "confidence": result.confidence
            }
        else:
            return {
                "passed": False,
                "content_evidence": f"在文档中未找到'{tag_name}'相关字样",
                "confidence": 0.0,
                "issue": "标签与文档内容不匹配"
            }
    
    def _find_content_evidence(self, tag_name: str) -> str:
        """查找内容证据"""
        if not self.document_content:
            return ""
        
        # 直接匹配
        if tag_name in self.document_content:
            # 提取上下文
            try:
                idx = self.document_content.index(tag_name)
                start = max(0, idx - 30)
                end = min(len(self.document_content), idx + len(tag_name) + 30)
                context = self.document_content[start:end]
                return f"文档中提到: ...{context}..."
            except ValueError:
                pass
        
        # 检查相关词
        related_terms = self._get_related_terms(tag_name)
        for term in related_terms:
            if term in self.document_content:
                try:
                    idx = self.document_content.index(term)
                    start = max(0, idx - 20)
                    end = min(len(self.document_content), idx + len(term) + 20)
                    context = self.document_content[start:end]
                    return f"文档中提到相关概念: ...{context}..."
                except ValueError:
                    pass
        
        return ""
    
    def _get_related_terms(self, tag_name: str) -> List[str]:
        """获取相关词"""
        # 实际应用中可使用知识图谱或同义词库
        related_map = {
            "工作居住证": ["工作居住证", "居住证", "工居", "证件", "申报"],
            "操作流程": ["流程", "步骤", "操作", "办理", "程序"],
            "申请材料": ["材料", "证明", "附件", "文件", "资料"],
            "审核要求": ["审核", "审批", "要求", "条件", "标准"],
            "注意事项": ["注意", "提醒", "重要", "小心", "当心"],
        }
        return related_map.get(tag_name, [])
    
    def _generate_recommendations(self, failed_results: List[ExtractionResult]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        for result in failed_results:
            recommendations.append(f"建议移除标签: {result.tag_name}（文档中无相关证据）")
        
        if failed_results:
            failed_names = [r.tag_name for r in failed_results]
            recommendations.append(f"建议人工审核以下标签: {', '.join(failed_names)}")
        
        return recommendations
    
    def generate_report(self) -> Dict[str, Any]:
        """生成标签提取报告"""
        if not self.extraction_results:
            return {"status": "error", "message": "未提取标签"}
        
        correctness_result = self.perform_correctness_check()
        
        # 计算覆盖率
        coverage = len(self.extraction_results) / max(len(self.document_content) / 100, 1)
        
        # 统计业务价值分布
        value_distribution = {}
        for result in self.extraction_results:
            value = result.business_value
            value_distribution[value] = value_distribution.get(value, 0) + 1
        
        return {
            "mode": "extraction",
            "assigned_tags": [
                {
                    "tag_name": r.tag_name,
                    "confidence": round(r.confidence, 2),
                    "category": r.category,
                    "relevance": round(r.relevance, 2),
                    "source": r.source,
                    "business_value": r.business_value,
                    "correctness_check": r.correctness_check
                }
                for r in self.extraction_results
            ],
            "tagging_coverage": round(min(coverage, 1.0), 2),
            "processing_stats": {
                "total_candidates": len(self.extraction_results) * 2,
                "selected_tags": len(self.extraction_results),
                "correctness_check_passed": len(correctness_result["passed_tags"]),
                "correctness_check_failed": len(correctness_result["failed_tags"]),
                "business_value_distribution": value_distribution
            },
            "correctness_summary": {
                "overall_accuracy": correctness_result["overall_accuracy"],
                "recommendations": correctness_result["recommendations"]
            },
            "metadata": {
                "document_length": len(self.document_content),
                "extraction_timestamp": datetime.now().isoformat(),
                "taxonomy_version": "2.0",
                "total_taxonomy_tags": self._get_total_tags()
            }
        }


def main():
    """主函数 - 示例用法"""
    
    # 示例文档内容
    document_content = """
    新工居系统新办操作流程
    一、登录个人系统，完善信息
    登录北京国际人才网http://www.bjrcgz.gov.cn/ 【业务办理登录】模块点击【个人入口】，用北京通账号登录。
    按照系统提示及操作手册要求注册、完善基础信息、教育信息、学习经历、工作经历、证件照片等信息并在电子附件栏上传相应证明材料的PDF 彩色扫描件（同办理业务材料）。
    
    二、关联单位
    信息完善后在可办业务列表点击【工作居住证】模块，按照当前劳动合同所属公司输入【单位关联码】发起关联，待单位审核通过后方可关联成功。
    
    三、上传个人附件
    关联成功后找到【附件管理】，上传所需材料的原件扫描件（必须是彩色）
    其中，必须由本人上传的材料有：
    1、学历、学位证书——彩色扫描件
    2、入职本单位至今的应税收入材料
    3、诚信声明
    4、在京合法稳定住所证明
    5、户口本首页及本人页——彩色扫描件
    
    四、个人提交新办申请
    五、单位审核
    六、主管部门审核
    """
    
    try:
        # 创建提取器
        extractor = GenericTagExtractor()
        extractor.set_document_content(document_content)
        
        # 提取标签
        tags = extractor.extract_tags(mode="extraction", max_tags=15)
        
        # 生成报告
        report = extractor.generate_report()
        
        # 输出结果
        print("=" * 80)
        print("通用标签提取框架 - 工作居住证文档示例")
        print("=" * 80)
        print(f"\n提取模式: {report['mode']}")
        print(f"文档长度: {report['metadata']['document_length']} 字符")
        print(f"标签覆盖率: {report['tagging_coverage']:.2%}")
        print(f"正确性检测通过率: {report['correctness_summary']['overall_accuracy']:.2%}")
        
        print("\n提取的标签:")
        print("-" * 80)
        for i, tag in enumerate(report['assigned_tags'], 1):
            correctness = "✓" if tag.get("correctness_check", {}).get("passed", True) else "✗"
            print(f"{i:2d}. {tag['tag_name']:<20} (置信度: {tag['confidence']:.2f}, "
                  f"分类: {tag['category']:<15} 业务价值: {tag['business_value']:<2} 正确性: {correctness})")
        
        print("\n业务价值分布:")
        print("-" * 80)
        for value, count in report['processing_stats']['business_value_distribution'].items():
            print(f"  {value}: {count} 个标签")
        
        print("\n正确性检测结果:")
        print("-" * 80)
        for rec in report['correctness_summary']['recommendations']:
            print(f"- {rec}")
        
        # 保存到文件
        output_file = Path("output/generic_tag_extraction_result.json")
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细报告已保存到: {output_file}")
        
    except Exception as e:
        logger.error(f"标签提取失败: {str(e)}")
        raise


if __name__ == "__main__":
    main()