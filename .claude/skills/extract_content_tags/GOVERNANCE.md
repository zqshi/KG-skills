# extract_content_tags Skill 标签治理规范

## 📌 文档定位

**本文档范畴**：extract_content_tags Skill 内部治理规范

**适用范围**：本规范专门针对 `extract_content_tags` 技能的标签提取、管理和质量控制流程，是该skill的专属治理文档。

**与跨skill治理框架的关系**：
- 本文档是 [.claude/TAG_GOVERNANCE.md](../TAG_GOVERNANCE.md) 的具体实现和补充
- 跨skill治理框架提供通用原则和标准，本文档提供skill级别的详细实施规范
- 当两者冲突时，以跨skill治理框架为准

---

## 📋 目录

1. [标签生命周期概述](#标签生命周期概述)
2. [标签创建规范](#标签创建规范)
3. [标签使用规范](#标签使用规范)
4. [标签维护规范](#标签维护规范)
5. [标签归档与淘汰](#标签归档与淘汰)
6. [质量监控与评估](#质量监控与评估)
7. [角色与职责](#角色与职责)
8. [工具与自动化](#工具与自动化)

---

## 🔄 标签生命周期概述

标签在其生命周期中会经历以下阶段：

```
创建 → 审核 → 发布 → 使用 → 监控 → 维护 → 归档/淘汰
```

### 生命周期阶段说明

| 阶段 | 状态 | 主要活动 | 负责角色 |
|------|------|---------|---------|
| **创建** | 草稿 | 标签定义、元数据配置、业务价值评估 | 标签创建者 |
| **审核** | 待审核 | 质量检查、重复检测、业务价值确认 | 标签审核员 |
| **发布** | 已发布 | 加入标签体系、通知相关方、文档更新 | 标签管理员 |
| **使用** | 活跃 | 标签应用、效果监控、反馈收集 | 所有用户 |
| **维护** | 活跃 | 定期评估、优化调整、问题修复 | 标签管理员 |
| **归档** | 已归档 | 停止使用、历史数据保留、文档标记 | 标签管理员 |
| **淘汰** | 已淘汰 | 彻底删除、数据清理、影响评估 | 系统管理员 |

---

## 📝 标签创建规范

### 创建前提条件

**必须满足以下条件才能创建新标签**：
- [ ] 现有标签体系无法覆盖该概念
- [ ] 标签具有明确的业务价值
- [ ] 标签名称清晰、无歧义
- [ ] 已完成重复性检查（相似度<0.8）
- [ ] 已获得相关方认可

### 标签元数据要求

每个标签必须包含以下元数据：

```json
{
  "name": "标签名称",
  "aliases": ["别名1", "别名2"],
  "category": "所属分类",
  "business_value": "高/中/低",
  "description": "标签的详细描述",
  "use_cases": ["适用场景1", "适用场景2"],
  "created_by": "创建人",
  "created_at": "2025-11-26T10:00:00Z",
  "status": "draft",
  "review_status": "pending"
}
```

### 业务价值评估标准

**高业务价值标签**：
- 高频使用（每月使用>100次）
- 核心业务概念
- 支持关键业务流程
- 用户检索需求强烈

**中业务价值标签**：
- 中等频率使用（每月使用10-100次）
- 重要业务概念
- 支持一般业务流程
- 有一定检索需求

**低业务价值标签**：
- 低频使用（每月使用<10次）
- 辅助性概念
- 特定场景使用
- 检索需求较弱

### 创建流程

```python
def create_tag_workflow():
    """
    标签创建标准流程
    """
    # 步骤1：需求分析
    if not analyze_tagging_need():
        return {"status": "rejected", "reason": "无创建必要"}
    
    # 步骤2：重复性检查
    duplicate_check = check_duplicate_tags()
    if duplicate_check["is_duplicate"]:
        return {
            "status": "rejected",
            "reason": "与现有标签重复",
            "suggestion": f"使用现有标签: {duplicate_check['existing_tag']}"
        }
    
    # 步骤3：业务价值评估
    value_eval = evaluate_business_value()
    if value_eval["level"] == "低":
        return {
            "status": "rejected",
            "reason": "业务价值不足",
            "details": value_eval["analysis"]
        }
    
    # 步骤4：元数据准备
    metadata = prepare_tag_metadata()
    
    # 步骤5：提交审核
    submit_for_review(metadata)
    
    return {
        "status": "submitted",
        "message": "标签已提交审核",
        "tag_id": metadata["id"]
    }
```

---

## 🔍 标签使用规范

### 使用原则

1. **一致性原则**：相同概念使用相同标签
2. **最小化原则**：使用最少数量标签表达核心概念
3. **准确性原则**：标签必须准确反映内容主题
4. **价值导向原则**：优先使用高业务价值标签

### 标签选择指南

**选择优先级**：
1. **精确匹配**：优先选择直接描述内容的标签
2. **高业务价值**：在多个候选标签中选择业务价值高的
3. **标准化标签**：优先使用已发布的标准标签
4. **用户友好**：选择用户容易理解和检索的标签

**避免使用**：
- ❌ 未经审核的草稿标签
- ❌ 已归档或淘汰的标签
- ❌ 业务价值为"低"的标签（除非特殊情况）
- ❌ 含义模糊或有歧义的标签

### 标签数量控制

**推荐数量**：
- **简短文档**（<1000字）：3-5个标签
- **中等文档**（1000-5000字）：5-10个标签
- **长篇文档**（>5000字）：10-15个标签

**最大限制**：单个文档不超过20个标签

### 标签组合策略

**推荐组合**：
- 1-2个业务领域标签
- 2-4个内容标签
- 1-2个适用人群标签
- 0-1个办公地点标签
- 0-1个文档类型标签

**示例**：
```json
{
  "document": "工作居住证办理流程",
  "tags": [
    {"name": "工作居住证", "category": "业务领域"},
    {"name": "操作流程", "category": "内容标签"},
    {"name": "申请材料", "category": "内容标签"},
    {"name": "审核要求", "category": "内容标签"},
    {"name": "全体员工", "category": "适用人群"},
    {"name": "北京", "category": "办公地点"}
  ]
}
```

---

## 🔧 标签维护规范

### 定期评估机制

**评估周期**：
- **高业务价值标签**：每月评估
- **中业务价值标签**：每季度评估
- **低业务价值标签**：每半年评估

**评估内容**：
- [ ] 使用频率统计
- [ ] 用户反馈收集
- [ ] 标签准确性评估
- [ ] 业务价值变化分析
- [ ] 重复和冗余检查

### 标签优化策略

**合并策略**：
当两个标签相似度>0.9且业务价值相当时，考虑合并

```python
def merge_tags(tag1: Dict, tag2: Dict) -> Dict:
    """
    合并两个相似标签
    """
    # 保留业务价值高的
    if tag1["business_value"] >= tag2["business_value"]:
        primary = tag1
        secondary = tag2
    else:
        primary = tag2
        secondary = tag1
    
    # 合并别名
    primary["aliases"] = list(set(
        primary.get("aliases", []) + 
        [secondary["name"]] + 
        secondary.get("aliases", [])
    ))
    
    # 更新使用统计
    primary["usage_count"] = primary.get("usage_count", 0) + \
                             secondary.get("usage_count", 0)
    
    # 记录合并历史
    primary["merged_from"] = primary.get("merged_from", []) + \
                             [secondary["id"]]
    
    return primary
```

**拆分策略**：
当一个标签涵盖范围过广时，考虑拆分为更具体的标签

**示例**：
```
原标签: "材料" (过于宽泛)
拆分为:
- "申请材料" (办理业务所需材料)
- "证明材料" (用于证明的材料)
- "附件材料" (作为附件的材料)
```

### 标签更新流程

```python
def update_tag_workflow(tag_id: str, updates: Dict) -> Dict:
    """
    标签更新标准流程
    """
    # 步骤1：验证更新内容
    validation = validate_tag_updates(updates)
    if not validation["valid"]:
        return {"status": "rejected", "errors": validation["errors"]}
    
    # 步骤2：影响评估
    impact = assess_update_impact(tag_id, updates)
    if impact["severity"] == "high":
        # 重大变更需要审批
        submit_for_approval(updates, impact)
        return {"status": "pending_approval"}
    
    # 步骤3：执行更新
    updated_tag = apply_updates(tag_id, updates)
    
    # 步骤4：通知相关方
    notify_stakeholders(updated_tag, impact)
    
    # 步骤5：更新文档
    update_documentation(updated_tag)
    
    return {
        "status": "updated",
        "tag": updated_tag,
        "impact": impact
    }
```

---

## 📦 标签归档与淘汰

### 归档条件

**满足以下任一条件即考虑归档**：
- [ ] 连续6个月零使用
- [ ] 业务价值降级为"低"且持续3个月
- [ ] 被更优标签替代（相似度>0.9，业务价值更高）
- [ ] 相关业务已停止或变更
- [ ] 标签概念过时或不再适用

### 归档流程

```python
def archive_tag_workflow(tag_id: str, reason: str) -> Dict:
    """
    标签归档标准流程
    """
    # 步骤1：使用检查
    usage_stats = get_tag_usage_stats(tag_id)
    if usage_stats["recent_usage"] > 0:
        return {
            "status": "rejected",
            "reason": "标签仍在使用，无法归档"
        }
    
    # 步骤2：影响评估
    impact = assess_archive_impact(tag_id)
    
    # 步骤3：创建归档记录
    archive_record = {
        "tag_id": tag_id,
        "archived_at": datetime.now().isoformat(),
        "reason": reason,
        "usage_history": usage_stats,
        "impact": impact
    }
    
    # 步骤4：更新标签状态
    update_tag_status(tag_id, "archived")
    
    # 步骤5：迁移历史数据
    if impact["has_historical_data"]:
        migrate_historical_data(tag_id)
    
    # 步骤6：通知相关方
    notify_archive(tag_id, archive_record)
    
    return {
        "status": "archived",
        "archive_record": archive_record
    }
```

### 淘汰条件

**满足以下所有条件方可淘汰**：
- [ ] 标签已归档超过12个月
- [ ] 无历史数据需要保留
- [ ] 无依赖关系
- [ ] 获得管理层批准
- [ ] 已完成数据备份

### 淘汰流程

```python
def retire_tag_workflow(tag_id: str) -> Dict:
    """
    标签淘汰标准流程
    """
    # 步骤1：验证淘汰条件
    validation = validate_retirement_conditions(tag_id)
    if not validation["eligible"]:
        return {
            "status": "rejected",
            "reason": "不满足淘汰条件",
            "details": validation["failures"]
        }
    
    # 步骤2：数据备份
    backup_data = backup_tag_data(tag_id)
    
    # 步骤3：清理关联数据
    cleanup_related_data(tag_id)
    
    # 步骤4：物理删除
    permanently_delete_tag(tag_id)
    
    # 步骤5：记录淘汰日志
    retirement_log = {
        "tag_id": tag_id,
        "retired_at": datetime.now().isoformat(),
        "backup_location": backup_data["location"],
        "cleanup_summary": cleanup_related_data.summary()
    }
    
    return {
        "status": "retired",
        "log": retirement_log
    }
```

---

## 📊 质量监控与评估

### 监控指标体系

**核心指标**：
| 指标 | 定义 | 目标值 | 监控频率 |
|------|------|--------|---------|
| **标签准确率** | 正确标签数 / 总标签数 | ≥90% | 实时 |
| **标签覆盖率** | 覆盖概念数 / 总概念数 | ≥85% | 每日 |
| **标签复用率** | 复用标签数 / 总使用标签数 | ≥80% | 每日 |
| **标签一致性** | 一致使用标签数 / 总标签数 | ≥95% | 实时 |
| **业务价值达标率** | 高价值标签数 / 总标签数 | ≥70% | 每周 |
| **标签新鲜度** | 新标签数 / 总标签数 | 5-15% | 每月 |

### 质量评估流程

```python
def quality_assessment_workflow():
    """
    质量评估标准流程
    """
    # 步骤1：数据收集
    metrics = collect_quality_metrics()
    
    # 步骤2：指标计算
    scores = calculate_quality_scores(metrics)
    
    # 步骤3：问题识别
    issues = identify_quality_issues(scores, metrics)
    
    # 步骤4：根因分析
    root_causes = analyze_root_causes(issues)
    
    # 步骤5：改进建议
    recommendations = generate_recommendations(root_causes)
    
    # 步骤6：报告生成
    report = {
        "assessment_date": datetime.now().isoformat(),
        "scores": scores,
        "issues": issues,
        "root_causes": root_causes,
        "recommendations": recommendations
    }
    
    return report
```

### 预警机制

**自动预警条件**：
- 标签准确率连续3天<85%
- 标签覆盖率连续7天<80%
- 标签复用率连续7天<75%
- 新增标签失败率>20%
- 标签使用异常波动（±50%）

**预警流程**：
```python
def quality_alert_system():
    """
    质量预警系统
    """
    # 检查指标
    metrics = get_current_metrics()
    
    alerts = []
    
    # 准确率预警
    if metrics["accuracy"] < 0.85:
        alerts.append({
            "level": "warning",
            "metric": "accuracy",
            "value": metrics["accuracy"],
            "threshold": 0.85,
            "message": "标签准确率低于阈值"
        })
    
    # 覆盖率预警
    if metrics["coverage"] < 0.80:
        alerts.append({
            "level": "warning",
            "metric": "coverage",
            "value": metrics["coverage"],
            "threshold": 0.80,
            "message": "标签覆盖率低于阈值"
        })
    
    # 严重问题预警
    if metrics["accuracy"] < 0.70 or metrics["coverage"] < 0.70:
        alerts.append({
            "level": "critical",
            "message": "标签质量严重下降，需要立即干预"
        })
    
    # 发送预警
    if alerts:
        send_quality_alerts(alerts)
    
    return alerts
```

---

## 👥 角色与职责

### 标签创建者
**职责**：
- 识别标签需求
- 准备标签元数据
- 提交标签创建申请
- 配合审核和优化

**权限**：
- 创建草稿标签
- 查看标签体系
- 提交审核申请

### 标签审核员
**职责**：
- 审核新标签质量
- 评估业务价值
- 检查重复性
- 批准或拒绝标签

**权限**：
- 审核标签
- 要求修改
- 批准发布
- 查看使用统计

### 标签管理员
**职责**：
- 管理标签体系
- 监控标签质量
- 执行维护操作
- 处理用户反馈

**权限**：
- 发布标签
- 更新标签
- 归档标签
- 查看完整统计
- 生成报告

### 系统管理员
**职责**：
- 系统配置管理
- 性能监控优化
- 数据备份恢复
- 安全管理

**权限**：
- 系统配置
- 数据管理
- 淘汰标签
- 系统维护

---

## 🛠️ 工具与自动化

### 自动化脚本

**标签健康检查脚本**：
```python
#!/usr/bin/env python3
"""
标签健康检查脚本
自动检查标签体系健康状况
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

class TagHealthChecker:
    def __init__(self, taxonomy_path: str):
        self.taxonomy_path = taxonomy_path
        self.taxonomy = self._load_taxonomy()
        self.metrics = {}
    
    def _load_taxonomy(self) -> Dict[str, Any]:
        """加载标签体系"""
        with open(self.taxonomy_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def check_health(self) -> Dict[str, Any]:
        """
        执行健康检查
        """
        # 检查1：重复标签检测
        duplicates = self._check_duplicates()
        
        # 检查2：低价值标签识别
        low_value_tags = self._identify_low_value_tags()
        
        # 检查3：未使用标签识别
        unused_tags = self._identify_unused_tags()
        
        # 检查4：元数据完整性检查
        metadata_issues = self._check_metadata_completeness()
        
        # 检查5：标签分布均衡性
        distribution = self._analyze_distribution()
        
        # 生成报告
        report = {
            "check_date": datetime.now().isoformat(),
            "total_tags": self._get_total_tags(),
            "issues": {
                "duplicates": duplicates,
                "low_value_tags": low_value_tags,
                "unused_tags": unused_tags,
                "metadata_issues": metadata_issues
            },
            "distribution": distribution,
            "health_score": self._calculate_health_score()
        }
        
        return report
    
    def _check_duplicates(self) -> List[Dict[str, Any]]:
        """检查重复标签"""
        duplicates = []
        tag_names = {}
        
        for category_name, category in self.taxonomy["categories"].items():
            for tag in category["tags"]:
                name = tag["name"]
                if name in tag_names:
                    duplicates.append({
                        "tag_name": name,
                        "categories": [tag_names[name], category_name],
                        "severity": "high"
                    })
                else:
                    tag_names[name] = category_name
        
        return duplicates
    
    def _identify_low_value_tags(self) -> List[Dict[str, Any]]:
        """识别低价值标签"""
        low_value_tags = []
        
        for category_name, category in self.taxonomy["categories"].items():
            for tag in category["tags"]:
                if tag.get("business_value") == "低":
                    low_value_tags.append({
                        "tag_name": tag["name"],
                        "category": category_name,
                        "reason": "业务价值评估为低"
                    })
        
        return low_value_tags
    
    def _identify_unused_tags(self) -> List[Dict[str, Any]]:
        """识别未使用标签（需要集成使用数据）"""
        # 实际应用中需要查询标签使用数据
        return []
    
    def _check_metadata_completeness(self) -> List[Dict[str, Any]]:
        """检查元数据完整性"""
        issues = []
        
        for category_name, category in self.taxonomy["categories"].items():
            for tag in category["tags"]:
                # 检查必需字段
                required_fields = ["name", "business_value", "description"]
                for field in required_fields:
                    if field not in tag or not tag[field]:
                        issues.append({
                            "tag_name": tag["name"],
                            "category": category_name,
                            "missing_field": field,
                            "severity": "medium"
                        })
                
                # 检查高价值标签是否有别名
                if tag.get("business_value") == "高":
                    aliases = tag.get("aliases", [])
                    if not aliases or len(aliases) < 2:
                        issues.append({
                            "tag_name": tag["name"],
                            "category": category_name,
                            "issue": "高价值标签别名不足",
                            "severity": "low"
                        })
        
        return issues
    
    def _analyze_distribution(self) -> Dict[str, Any]:
        """分析标签分布"""
        distribution = {}
        total_tags = 0
        
        for category_name, category in self.taxonomy["categories"].items():
            count = len(category["tags"])
            total_tags += count
            distribution[category_name] = {
                "count": count,
                "percentage": 0
            }
        
        # 计算百分比
        for cat_name, stats in distribution.items():
            stats["percentage"] = round(stats["count"] / total_tags * 100, 2)
        
        return distribution
    
    def _get_total_tags(self) -> int:
        """获取标签总数"""
        return sum(
            len(category["tags"])
            for category in self.taxonomy["categories"].values()
        )
    
    def _calculate_health_score(self) -> float:
        """计算健康分数"""
        # 基于问题数量和严重程度计算
        # 实际实现需要更复杂的算法
        return 0.85  # 示例值


def main():
    """主函数"""
    checker = TagHealthChecker("config/tag_taxonomy.json")
    report = checker.check_health()
    
    print("标签健康检查报告")
    print("=" * 80)
    print(f"检查时间: {report['check_date']}")
    print(f"标签总数: {report['total_tags']}")
    print(f"健康分数: {report['health_score']:.2f}")
    print()
    
    # 显示问题
    issues = report["issues"]
    
    if issues["duplicates"]:
        print("⚠️  发现重复标签:")
        for dup in issues["duplicates"]:
            print(f"   - {dup['tag_name']}: 出现在分类 {dup['categories']}")
        print()
    
    if issues["low_value_tags"]:
        print("⚠️  发现低价值标签:")
        for tag in issues["low_value_tags"]:
            print(f"   - {tag['tag_name']} ({tag['category']})")
        print()
    
    if issues["metadata_issues"]:
        print("⚠️  发现元数据问题:")
        for issue in issues["metadata_issues"]:
            print(f"   - {issue['tag_name']}: {issue['issue']}")
        print()
    
    # 显示分布
    print("标签分布:")
    for category, stats in report["distribution"].items():
        print(f"   - {category}: {stats['count']} 个 ({stats['percentage']}%)")
    
    # 保存报告
    import json
    with open("output/tag_health_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细报告已保存到: output/tag_health_report.json")


if __name__ == "__main__":
    main()
```

### 集成到CI/CD

**GitHub Actions 示例**：
```yaml
name: Tag Governance Check

on:
  push:
    paths:
      - 'config/tag_taxonomy.json'
  schedule:
    - cron: '0 0 * * 0'  # 每周日执行

jobs:
  tag-health-check:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Run tag health check
        run: |
          python .claude/skills/extract_content_tags/scripts/tag_health_check.py
      
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: tag-health-report
          path: output/tag_health_report.json
      
      - name: Check health score
        run: |
          score=$(jq '.health_score' output/tag_health_report.json)
          if (( $(echo "$score < 0.7" | bc -l) )); then
            echo "健康分数过低: $score"
            exit 1
          fi
```

---

## 📈 持续改进

### 改进循环

```python
def continuous_improvement_cycle():
    """
    持续改进循环
    """
    while True:
        # 1. 监控和度量
        metrics = collect_metrics()
        
        # 2. 分析和评估
        issues = analyze_issues(metrics)
        
        # 3. 规划和决策
        improvements = plan_improvements(issues)
        
        # 4. 实施和执行
        results = execute_improvements(improvements)
        
        # 5. 验证和反馈
        validation = validate_results(results)
        
        # 6. 知识沉淀
        document_lessons_learned(validation)
        
        # 等待下一个周期
        time.sleep(7 * 24 * 3600)  # 每周执行一次
```

### 反馈收集机制

**用户反馈渠道**：
- 标签使用反馈表单
- 定期用户调研
- 标签质量评分
- 问题报告系统

**反馈处理流程**：
```python
def process_user_feedback(feedback: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理用户反馈
    """
    # 分类反馈
    category = classify_feedback(feedback)
    
    if category == "tag_accuracy":
        return handle_accuracy_feedback(feedback)
    elif category == "missing_tag":
        return handle_missing_tag_feedback(feedback)
    elif category == "tag_redundancy":
        return handle_redundancy_feedback(feedback)
    else:
        return handle_general_feedback(feedback)
```

---

## 📋 附录

### 标签状态转换图

```
草稿 (draft) → 待审核 (pending_review) → 已发布 (published) 
    ↑                                              ↓
    └───────────── 更新 (update) ←────────── 活跃 (active)
                                                    ↓
                                              已归档 (archived) → 已淘汰 (retired)
```

### 标签质量检查清单

**创建阶段**：
- [ ] 标签名称清晰无歧义
- [ ] 业务价值评估完成
- [ ] 别名设置合理
- [ ] 描述信息完整
- [ ] 重复性检查通过
- [ ] 分类归属正确

**发布阶段**：
- [ ] 审核通过
- [ ] 相关方确认
- [ ] 文档已更新
- [ ] 通知已发送
- [ ] 培训已完成（如需要）

**使用阶段**：
- [ ] 使用频率监控
- [ ] 用户反馈收集
- [ ] 准确性验证
- [ ] 定期评估

**维护阶段**：
- [ ] 定期健康检查
- [ ] 问题及时修复
- [ ] 性能持续优化
- [ ] 知识沉淀

### 术语表

| 术语 | 定义 |
|------|------|
| **标签（Tag）** | 用于描述和分类知识内容的元数据 |
| **业务价值（Business Value）** | 标签对业务的支持程度（高/中/低） |
| **分类（Category）** | 标签所属的逻辑分组 |
| **别名（Alias）** | 标签的同义词或相关表达 |
| **置信度（Confidence）** | 标签与内容匹配的可信程度 |
| **正确性检测（Correctness Check）** | 验证标签与内容匹配度的过程 |
| **防重复（Deduplication）** | 避免创建相似或重复标签的机制 |
| **生命周期（Lifecycle）** | 标签从创建到淘汰的完整过程 |

---

**extract_content_tags Skill 标签治理规范 v2.0** - 建立健康、可持续的标签体系 🏷️

*本文档是 extract_content_tags skill 的专属治理规范，为该skill的标签提取和管理提供详细的实施指南。*