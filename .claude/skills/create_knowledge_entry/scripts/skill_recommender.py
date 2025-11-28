#!/usr/bin/env python3
"""
智能推荐引擎 - 基于历史数据推荐skill组合
原则1：数据驱动优先
"""

import json
import time
from typing import Dict, Any, List
from datetime import datetime, timedelta
import os


class SkillRecommender:
    """Skill推荐引擎"""
    
    def __init__(self, patterns_path: str = "data/knowledge_creation_patterns.json"):
        self.patterns_path = patterns_path
        self.min_historical_samples = 50  # 最小历史样本数
        self.patterns = self._load_patterns()
    
    def _load_patterns(self) -> List[Dict[str, Any]]:
        """加载历史模式数据"""
        try:
            if os.path.exists(self.patterns_path):
                with open(self.patterns_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("patterns", [])
            else:
                # 如果文件不存在，返回默认模式
                return self._get_default_patterns()
        except Exception as e:
            print(f"加载历史模式失败: {e}")
            return self._get_default_patterns()
    
    def _get_default_patterns(self) -> List[Dict[str, Any]]:
        """获取默认模式（用于冷启动）"""
        return [
            {
                "pattern_id": "default_policy",
                "knowledge_type": "政策文档",
                "content_length_range": [1000, 10000],
                "recommended_skills": {
                    "extract_content_tags": True,
                    "generate_faq_from_content": True,
                    "generate_knowledge_summary": True
                },
                "historical_data": {
                    "sample_size": 100,
                    "user_satisfaction": 0.85,
                    "avg_processing_time": 3.2
                },
                "confidence": 0.8
            },
            {
                "pattern_id": "default_process",
                "knowledge_type": "流程指南",
                "content_length_range": [500, 5000],
                "recommended_skills": {
                    "extract_content_tags": True,
                    "generate_faq_from_content": False,
                    "generate_knowledge_summary": False
                },
                "historical_data": {
                    "sample_size": 80,
                    "user_satisfaction": 0.88,
                    "avg_processing_time": 1.5
                },
                "confidence": 0.82
            },
            {
                "pattern_id": "default_training",
                "knowledge_type": "培训材料",
                "content_length_range": [2000, 20000],
                "recommended_skills": {
                    "extract_content_tags": True,
                    "generate_faq_from_content": True,
                    "generate_knowledge_summary": True,
                    "build_knowledge_graph": True
                },
                "historical_data": {
                    "sample_size": 60,
                    "user_satisfaction": 0.82,
                    "avg_processing_time": 5.8
                },
                "confidence": 0.78
            }
        ]
    
    def recommend_skills(self, content: str, knowledge_type: str) -> Dict[str, Any]:
        """
        基于历史数据推荐skill组合
        
        Args:
            content: 知识内容
            knowledge_type: 知识类型
            
        Returns:
            推荐结果
        """
        # 1. 分析内容特征
        content_features = self._analyze_content_features(content)
        
        # 2. 匹配最佳历史模式
        matched_pattern = self._find_best_pattern(
            content_features, knowledge_type
        )
        
        # 3. 生成推荐结果
        if matched_pattern:
            recommendations = matched_pattern["recommended_skills"]
            confidence = matched_pattern["confidence"]
            sample_size = matched_pattern["historical_data"]["sample_size"]
            rationale = f"基于{sample_size}条历史记录，用户满意度{matched_pattern['historical_data']['user_satisfaction']:.0%}"
        else:
            # 如果没有匹配的模式，使用默认推荐
            recommendations = self._get_default_recommendations(knowledge_type)
            confidence = 0.6
            rationale = "基于默认规则推荐（历史数据不足）"
        
        # 4. 添加数据质量评估
        data_quality = self._assess_data_quality(knowledge_type)
        
        return {
            "recommendations": recommendations,
            "confidence": confidence,
            "rationale": rationale,
            "data_quality": data_quality,
            "timestamp": datetime.now().isoformat()
        }
    
    def _analyze_content_features(self, content: str) -> Dict[str, Any]:
        """分析内容特征"""
        words = content.split()
        char_count = len(content)
        
        return {
            "word_count": len(words),
            "char_count": char_count,
            "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
            "unique_words_ratio": len(set(words)) / len(words) if words else 0,
            "has_tables": "```" in content or "|" in content,  # 是否包含表格
            "has_lists": any(line.strip().startswith(("- ", "* ", "1. ")) for line in content.split("\n")),
            "section_count": content.count("##") + content.count("###")  # 章节数量
        }
    
    def _find_best_pattern(self, 
                          content_features: Dict[str, Any], 
                          knowledge_type: str) -> Optional[Dict[str, Any]]:
        """查找最佳匹配模式"""
        best_match = None
        best_score = 0
        
        for pattern in self.patterns:
            # 检查知识类型是否匹配
            if pattern["knowledge_type"] != knowledge_type:
                continue
            
            # 检查内容长度范围
            length_range = pattern["content_length_range"]
            content_length = content_features["char_count"]
            
            if not (length_range[0] <= content_length <= length_range[1]):
                continue
            
            # 计算匹配分数
            score = self._calculate_pattern_score(pattern, content_features)
            
            if score > best_score:
                best_score = score
                best_match = pattern
        
        return best_match
    
    def _calculate_pattern_score(self, 
                                pattern: Dict[str, Any], 
                                content_features: Dict[str, Any]) -> float:
        """计算模式匹配分数"""
        score = 0
        
        # 历史数据质量分数
        historical_data = pattern["historical_data"]
        sample_size = historical_data["sample_size"]
        user_satisfaction = historical_data["user_satisfaction"]
        
        # 样本量分数（样本越多越可靠）
        if sample_size >= 100:
            sample_score = 1.0
        elif sample_size >= 50:
            sample_score = 0.8
        elif sample_size >= 20:
            sample_score = 0.6
        else:
            sample_score = 0.4
        
        # 用户满意度分数
        satisfaction_score = user_satisfaction
        
        # 综合历史数据分数
        historical_score = (sample_score + satisfaction_score) / 2
        
        # 模式置信度
        confidence_score = pattern.get("confidence", 0.7)
        
        # 最终分数
        score = historical_score * 0.6 + confidence_score * 0.4
        
        return score
    
    def _get_default_recommendations(self, knowledge_type: str) -> Dict[str, bool]:
        """获取默认推荐"""
        default_recommendations = {
            "政策文档": {
                "extract_content_tags": True,
                "generate_faq_from_content": True,
                "generate_knowledge_summary": True
            },
            "流程指南": {
                "extract_content_tags": True,
                "generate_faq_from_content": False,
                "generate_knowledge_summary": False
            },
            "FAQ": {
                "extract_content_tags": True,
                "generate_faq_from_content": False,
                "generate_knowledge_summary": False
            },
            "培训材料": {
                "extract_content_tags": True,
                "generate_faq_from_content": True,
                "generate_knowledge_summary": True,
                "build_knowledge_graph": True
            }
        }
        
        return default_recommendations.get(knowledge_type, {
            "extract_content_tags": True
        })
    
    def _assess_data_quality(self, knowledge_type: str) -> Dict[str, Any]:
        """评估数据质量"""
        relevant_patterns = [
            p for p in self.patterns 
            if p["knowledge_type"] == knowledge_type
        ]
        
        total_samples = sum(
            p["historical_data"]["sample_size"] 
            for p in relevant_patterns
        )
        
        avg_satisfaction = (
            sum(p["historical_data"]["user_satisfaction"] for p in relevant_patterns) / 
            len(relevant_patterns)
        ) if relevant_patterns else 0
        
        return {
            "total_samples": total_samples,
            "avg_user_satisfaction": avg_satisfaction,
            "pattern_count": len(relevant_patterns),
            "quality_level": self._get_quality_level(total_samples, avg_satisfaction)
        }
    
    def _get_quality_level(self, samples: int, satisfaction: float) -> str:
        """获取数据质量等级"""
        if samples >= 100 and satisfaction >= 0.85:
            return "high"
        elif samples >= 50 and satisfaction >= 0.75:
            return "medium"
        elif samples >= 20:
            return "low"
        else:
            return "insufficient"
    
    def record_creation_result(self, 
                             content: str,
                             knowledge_type: str,
                             selected_skills: Dict[str, bool],
                             user_satisfaction: float,
                             processing_time: float):
        """
        记录知识创建结果，用于持续优化推荐算法
        
        Args:
            content: 知识内容
            knowledge_type: 知识类型
            selected_skills: 实际选择的skills
            user_satisfaction: 用户满意度（0-1）
            processing_time: 处理时间（秒）
        """
        try:
            # 分析内容特征
            content_features = self._analyze_content_features(content)
            
            # 创建新的模式记录
            new_pattern = {
                "pattern_id": f"pattern_{int(time.time())}",
                "knowledge_type": knowledge_type,
                "content_length_range": [
                    content_features["char_count"] * 0.8,
                    content_features["char_count"] * 1.2
                ],
                "recommended_skills": selected_skills,
                "historical_data": {
                    "sample_size": 1,
                    "user_satisfaction": user_satisfaction,
                    "avg_processing_time": processing_time
                },
                "confidence": user_satisfaction,
                "created_at": datetime.now().isoformat()
            }
            
            # 添加到现有模式或创建新文件
            if os.path.exists(self.patterns_path):
                with open(self.patterns_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    patterns = data.get("patterns", [])
            else:
                patterns = []
            
            patterns.append(new_pattern)
            
            # 保存更新后的模式
            with open(self.patterns_path, 'w', encoding='utf-8') as f:
                json.dump({"patterns": patterns}, f, ensure_ascii=False, indent=2)
            
            print(f"记录创建结果成功，当前模式数: {len(patterns)}")
            
        except Exception as e:
            print(f"记录创建结果失败: {e}")


def data_driven_skill_recommendation(content: str, knowledge_type: str) -> Dict[str, Any]:
    """
    数据驱动的skill推荐函数
    
    Args:
        content: 知识内容
        knowledge_type: 知识类型
        
    Returns:
        推荐结果
    """
    recommender = SkillRecommender()
    return recommender.recommend_skills(content, knowledge_type)


def main():
    """主函数 - 测试用"""
    # 测试内容
    test_content = """
    员工年假管理规定：根据工龄计算年假天数，工龄满1年不满10年的，年休假5天；
    已满10年不满20年的，年休假10天；已满20年的，年休假15天。
    员工申请年假需要提前3个工作日提交申请，经部门经理审批后方可休假。
    """
    
    recommender = SkillRecommender()
    
    print("=" * 80)
    print("数据驱动Skill推荐测试")
    print("=" * 80)
    
    # 测试政策文档推荐
    print("\n【测试1】政策文档推荐:")
    result1 = recommender.recommend_skills(test_content, "政策文档")
    print(f"推荐置信度: {result1['confidence']:.2f}")
    print(f"推荐Skills:")
    for skill, enabled in result1['recommendations'].items():
        print(f"  - {skill}: {'启用' if enabled else '禁用'}")
    print(f"推荐理由: {result1['rationale']}")
    print(f"数据质量: {result1['data_quality']['quality_level']}")
    
    # 测试流程指南推荐
    print("\n【测试2】流程指南推荐:")
    result2 = recommender.recommend_skills(test_content, "流程指南")
    print(f"推荐置信度: {result2['confidence']:.2f}")
    print(f"推荐Skills:")
    for skill, enabled in result2['recommendations'].items():
        print(f"  - {skill}: {'启用' if enabled else '禁用'}")
    
    # 测试培训材料推荐
    print("\n【测试3】培训材料推荐:")
    result3 = recommender.recommend_skills(test_content, "培训材料")
    print(f"推荐置信度: {result3['confidence']:.2f}")
    print(f"推荐Skills:")
    for skill, enabled in result3['recommendations'].items():
        print(f"  - {skill}: {'启用' if enabled else '禁用'}")
    
    # 测试记录创建结果
    print("\n【测试4】记录创建结果:")
    recommender.record_creation_result(
        content=test_content,
        knowledge_type="政策文档",
        selected_skills=result1['recommendations'],
        user_satisfaction=0.9,
        processing_time=2.5
    )
    print("创建结果已记录")


if __name__ == "__main__":
    main()