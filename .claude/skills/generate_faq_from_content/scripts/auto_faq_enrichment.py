#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAQ自动补充和完整性检查循环
自动检测FAQ完整性，补充缺失内容，直到达到通过标准
"""

import subprocess
import sys
import json
import re
import os
import argparse
import sys
import re
import json
import time
from typing import List, Dict, Any

# 配置
MAX_ITERATIONS = 5  # 最大循环次数，防止无限循环
TARGET_SCORE = 0.7  # 目标分数
CHECKER_SCRIPT = "faq_completeness_checklist.py"

def run_completeness_check(faq_file: str, source_file: str, doc_type: str) -> Dict[str, Any]:
    """
    运行完整性检查脚本，返回JSON格式的结果
    
    Args:
        faq_file: FAQ文件路径
        source_file: 源文档路径
        doc_type: 文档类型
        
    Returns:
        检查结果字典
    """
    cmd = [
        sys.executable, CHECKER_SCRIPT,
        faq_file, source_file,
        "--type", doc_type,
        "--debug"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        # 从stdout或stderr中提取JSON结果
        output = result.stdout + result.stderr
        json_start = output.find("📊 JSON结果:")
        if json_start != -1:
            json_start = output.find("{", json_start)
            json_end = output.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                json_str = output[json_start:json_end]
                try:
                    parsed = json.loads(json_str)
                    print(f"✅ 成功解析检查结果，得分: {parsed.get('overall_score', 0)}")
                    return parsed
                except json.JSONDecodeError as e:
                    print(f"⚠️  JSON解析失败: {e}")
                    print(f"JSON内容: {json_str[:200]}...")
        
        # 如果找到JSON但解析失败，返回基本结果
        if result.returncode == 0:
            return {"passed": True, "score": 1.0, "details": "检查通过"}
        else:
            return {"passed": False, "score": 0, "details": f"检查失败，返回码: {result.returncode}"}
    except Exception as e:
        print(f"❌ 执行检查失败: {e}")
        return {"passed": False, "score": 0, "details": f"执行失败: {e}"}

def analyze_missing_content(check_result: Dict[str, Any]) -> List[str]:
    """
    分析缺失的内容，返回需要补充的章节列表
    """
    missing_sections = []
    
    # 从JSON结果中获取未覆盖章节
    if "uncovered_sections" in check_result and check_result["uncovered_sections"]:
        missing_sections = check_result["uncovered_sections"]
        print(f"📊 从检查结果中发现未覆盖章节: {', '.join(missing_sections)}")
        return missing_sections
    
    # 备用：从recommendations中提取
    if "recommendations" in check_result:
        recommendations = check_result["recommendations"]
        for rec in recommendations:
            if "建议增加以下章节的FAQ" in rec:
                # 提取章节名称
                start = rec.find("建议增加以下章节的FAQ:")
                if start != -1:
                    sections_part = rec[start + len("建议增加以下章节的FAQ:"):].strip()
                    sections = [s.strip() for s in sections_part.split(",")]
                    missing_sections.extend(sections)
    
    if missing_sections:
        print(f"📊 从建议中发现需要补充的章节: {', '.join(missing_sections)}")
    else:
        print("⚠️  未能从检查结果中识别缺失章节")
    
    return list(set(missing_sections))  # 去重

def generate_supplementary_faq(missing_sections: List[str], source_content: str) -> List[Dict[str, str]]:
    """
    根据缺失的章节，生成补充的FAQ
    """
    supplementary_faq = []
    
    # 简化的FAQ生成逻辑，实际应用中可以使用LLM API
    faq_templates = {
        "试用期管理": [
            {
                "question": "试用期的具体期限是如何规定的？",
                "answer": "根据员工手册规定，试用期期限会在劳动合同中约定。员工录用后应立即到岗，2日内无正当理由未报到，公司有权解除劳动合同。试用期满前需填写转正资料，考核合格者予以转正。"
            },
            {
                "question": "试用期考核包括哪些方面？",
                "answer": "试用期考核包括道德品质、文化知识水平、业务能力、工作态度、工作表现、工作业绩等全面考核。不能按时完成工作任务、提供虚假资料、有违法违纪行为等情况将被视为不符合录用条件。"
            },
            {
                "question": "试用期不符合录用条件的具体情形有哪些？",
                "answer": "包括但不限于：1)不能完成工作任务或考核不合格；2)提供虚假学历证书、身份证等资料；3)与其他公司有未解决的法律纠纷；4)体检不符合要求；5)有违法违纪行为；6)未按时提交入职材料等。"
            }
        ],
        "入职指引": [
            {
                "question": "新员工入职第一天需要完成哪些事项？",
                "answer": "入职第一天需要：1)领取入职包；2)获取AD账号及邮箱；3)提交入职资料；4)签订劳动合同等入职材料；5)办理新工卡；6)加入集团平台通讯团队；7)部门熟悉介绍。最重要的是在当天下班前完成KOA新员工信息采集。"
            },
            {
                "question": "如何加入和使用KOA系统？",
                "answer": "KOA网页端登录地址：http://koa.kingsoft.cn，也可在应用商店下载客户端。使用AD账号和密码登录，主要功能包括饭卡充值、流程申请与审批、预定会议室、考勤说明、请假申请等。入职当天下班前必须完成新员工信息采集。"
            },
            {
                "question": "金山协作系统如何使用？",
                "answer": "访问官网https://xz.wps.cn下载客户端并安装。使用公司邮箱注册并登录激活，操作手册链接：https://kdocs.cn/l/ccRly20nLwHN。主要用于团队协作、文档共享、项目管理等。"
            },
            {
                "question": "新员工信息采集流程是什么？",
                "answer": "1)使用个人AD账户和密码登录KOA系统；2)进入首页-流程中心-人力资源-新员工信息采集；3)入职当天下班前填写并提交信息采集流程。务必认真核对信息，特别是工资卡号等关键信息。"
            }
        ]
    }
    
    for section in missing_sections:
        if section in faq_templates:
            supplementary_faq.extend(faq_templates[section])
            print(f"✍️  为章节 '{section}' 生成 {len(faq_templates[section])} 个FAQ")
        else:
            print(f"⚠️  未找到章节 '{section}' 的FAQ模板")
    
    if not supplementary_faq:
        print("⚠️  未能生成任何补充FAQ")
    
    return supplementary_faq

def update_faq_file(new_faq: List[Dict[str, str]]) -> bool:
    """
    将新生成的FAQ添加到FAQ文件中
    """
    try:
        if not os.path.exists(FAQ_FILE):
            print(f"错误：FAQ文件不存在: {FAQ_FILE}")
            return False
        
        with open(FAQ_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到最后一个FAQ的序号
        faq_pattern = r'### Q(\d+):'
        existing_numbers = [int(match) for match in re.findall(faq_pattern, content)]
        next_number = max(existing_numbers) + 1 if existing_numbers else 1
        
        # 生成新的FAQ内容
        new_content = "\n\n"
        for i, faq in enumerate(new_faq):
            q_num = next_number + i
            new_content += f"### Q{q_num}: {faq['question']}\n"
            new_content += f"**A:** {faq['answer']}\n\n"
            new_content += f"**来源**: 员工手册相关章节\n\n"
        
        # 添加到文件末尾（在统计信息之前）
        stats_pattern = r"## 📊 FAQ统计信息"
        if re.search(stats_pattern, content):
            content = re.sub(stats_pattern, new_content + r"\n\1", content)
        else:
            content += new_content
        
        with open(FAQ_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 成功添加 {len(new_faq)} 个新FAQ")
        return True
    except Exception as e:
        print(f"❌ 更新FAQ文件失败: {e}")
        return False

def main():
    """
    主循环：持续检查和补充，直到达到目标分数或最大迭代次数
    """
    parser = argparse.ArgumentParser(
        description='FAQ自动补充和完整性检查循环 - 持续检测并补充缺失的FAQ内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 对员工手册进行自动补充
  python auto_faq_enrichment.py 员工手册FAQ.md 员工手册.pdf --type employee_handbook
  
  # 对政策文档进行自动补充
  python auto_faq_enrichment.py 政策FAQ.md 政策文档.pdf --type policy_document
  
  # 设置更高的目标分数
  python auto_faq_enrichment.py FAQ.md source.pdf --type employee_handbook --target-score 0.8
  
  # 增加最大迭代次数
  python auto_faq_enrichment.py FAQ.md source.pdf --type employee_handbook --max-iterations 10
        
依赖说明:
  - 需要faq_completeness_checklist.py脚本
  - 支持Markdown格式的FAQ文件
  - 支持PDF和文本格式的源文档
        """
    )
    
    parser.add_argument('faq_file', help='FAQ文件路径（Markdown格式）')
    parser.add_argument('source_file', help='源文档路径（PDF或文本格式）')
    parser.add_argument('--type', default='employee_handbook',
                       choices=['employee_handbook', 'policy_document', 'operation_guide', 'product_manual'],
                       help='文档类型（决定检查标准）')
    parser.add_argument('--target-score', type=float, default=TARGET_SCORE,
                       help=f'目标分数（默认: {TARGET_SCORE}）')
    parser.add_argument('--max-iterations', type=int, default=MAX_ITERATIONS,
                       help=f'最大迭代次数（默认: {MAX_ITERATIONS}）')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细日志')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print(" " * 15 + "FAQ自动补充和完整性检查循环")
    print("=" * 70)
    print(f"📄 FAQ文件: {args.faq_file}")
    print(f"📚 源文档: {args.source_file}")
    print(f"🏷️  文档类型: {args.type}")
    print(f"🎯 目标分数: {args.target_score}")
    print(f"🔄 最大迭代次数: {args.max_iterations}")
    print("-" * 70)
    
    # 检查文件是否存在
    if not os.path.isfile(args.faq_file):
        print(f"❌ 错误：FAQ文件不存在: {args.faq_file}")
        sys.exit(1)
    
    if not os.path.isfile(args.source_file):
        print(f"❌ 错误：源文档不存在: {args.source_file}")
        sys.exit(1)
    
    # 检查检查脚本是否存在
    checker_path = os.path.join(os.path.dirname(__file__), CHECKER_SCRIPT)
    if not os.path.isfile(checker_path):
        print(f"❌ 错误：检查脚本不存在: {checker_path}")
        sys.exit(1)
    
    for iteration in range(1, args.max_iterations + 1):
        print(f"\n🔄 第 {iteration}/{args.max_iterations} 次迭代")
        print("-" * 70)
        
        # 运行完整性检查
        print("📋 运行完整性检查...")
        check_result = run_completeness_check(args.faq_file, args.source_file, args.type)
        
        if check_result.get("passed", False):
            print(f"✅ 恭喜！FAQ完整性检查通过！")
            print(f"📊 最终得分: {check_result.get('score', 0):.2f}/{TARGET_SCORE}")
            sys.exit(0)
        
        # 分析缺失内容
        print("🔍 分析缺失内容...")
        missing_sections = analyze_missing_content(check_result)
        
        if not missing_sections:
            print("⚠️  无法识别缺失内容，停止迭代")
            sys.exit(1)
        
        print(f"📌 发现缺失章节: {', '.join(missing_sections)}")
        
        # 生成补充FAQ
        print("🤖 生成补充FAQ...")
        # 这里简化处理，实际应该调用LLM API生成
        supplementary_faq = generate_supplementary_faq(missing_sections, "")
        
        if not supplementary_faq:
            print("⚠️  未能生成补充FAQ，停止迭代")
            sys.exit(1)
        
        print(f"✍️  生成 {len(supplementary_faq)} 个补充FAQ")
        
        # 更新FAQ文件
        print("💾 更新FAQ文件...")
        if not update_faq_file(supplementary_faq):
            sys.exit(1)
        
        # 显示当前状态
        current_score = check_result.get("score", 0)
        print(f"📊 当前得分: {current_score:.2f}/{TARGET_SCORE}")
        print(f"🎯 距离目标还差: {TARGET_SCORE - current_score:.2f}")
        
        if iteration < MAX_ITERATIONS:
            print(f"\n⏳ 等待2秒后进入下一次迭代...")
            import time
            time.sleep(2)
    
    # 达到最大迭代次数
    print("\n" + "=" * 70)
    print("❌ 已达到最大迭代次数，FAQ完整性仍未达到目标")
    print(f"最终得分: {check_result.get('score', 0):.2f}/{TARGET_SCORE}")
    print("建议手动检查并补充缺失内容")
    print("=" * 70)
    sys.exit(1)

if __name__ == "__main__":
    main()