#!/usr/bin/env python3
"""
Skill Manager - 统一入口
提供手动创建、自动分析、模板管理等功能
"""

import argparse
import sys
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent / 'core'))
sys.path.insert(0, str(Path(__file__).parent / 'plugins' / 'workflow_analyzer'))

from skill_creator import SkillCreator
from analyzer import WorkflowAnalyzer


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Skill Manager - 统一Skill管理系统')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='创建新Skill')
    create_parser.add_argument('--name', required=True, help='Skill名称')
    create_parser.add_argument('--description', required=True, help='Skill描述')
    create_parser.add_argument('--type', default='knowledge_processor', 
                              choices=['data_processor', 'api_integrator', 'file_operator', 
                                      'content_creator', 'document_generator', 'workflow'],
                              help='Skill类型')
    create_parser.add_argument('--complexity', default='medium',
                              choices=['simple', 'medium', 'complex'],
                              help='复杂度级别')
    create_parser.add_argument('--audience', default='intermediate',
                              choices=['beginner', 'intermediate', 'expert'],
                              help='目标用户')
    create_parser.add_argument('--no-scripts', action='store_true', help='不包含脚本')
    create_parser.add_argument('--templates', action='store_true', help='包含模板')
    create_parser.add_argument('--requirements', help='自定义需求描述')
    create_parser.add_argument('--commands', nargs='*', help='工作流命令（workflow类型）')
    
    # analyze 命令
    analyze_parser = subparsers.add_parser('analyze', help='分析工作流')
    analyze_parser.add_argument('--log-file', help='操作日志文件路径')
    analyze_parser.add_argument('--config', help='配置文件路径')
    analyze_parser.add_argument('--create-skills', action='store_true', help='基于推荐创建Skill')
    analyze_parser.add_argument('--report', action='store_true', help='生成分析报告')
    analyze_parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'create':
        # 创建Skill
        creator = SkillCreator()
        result = creator.create_skill_from_args(args)
        
        if result.success:
            print(f"✅ {result.message}")
            print(f"📁 路径: {result.path}")
        else:
            print(f"❌ {result.message}")
            for error in result.errors:
                print(f"   - {error}")
            sys.exit(1)
    
    elif args.command == 'analyze':
        # 分析工作流
        analyzer = WorkflowAnalyzer(config_path=args.config)
        
        # 加载操作日志
        operations = analyzer.load_operations_log(args.log_file)
        
        if not operations:
            print("错误: 没有操作日志数据")
            sys.exit(1)
        
        # 过滤操作
        filtered_ops = analyzer.filter_operations(operations)
        
        if not filtered_ops:
            print("错误: 过滤后没有有效操作数据")
            sys.exit(1)
        
        # 分析工作流
        workflows = analyzer.analyze_workflows(filtered_ops)
        
        if not workflows:
            print("未识别出高频工作流")
            return
        
        # 生成推荐
        recommendations = analyzer.generate_skill_recommendations(workflows)
        
        if args.report:
            report = analyzer.generate_report(args.output)
            print(f"报告已生成: {report}")
        
        if args.create_skills:
            created_count = 0
            for rec in recommendations:
                print(f"\n建议创建Skill: {rec['skill_name']}")
                print(f"描述: {rec['description']}")
                response = input("是否创建？(y/N): ").strip().lower()
                
                if response == 'y':
                    if analyzer.create_skill_from_workflow(rec):
                        created_count += 1
                        print(f"✅ 成功创建Skill: {rec['skill_name']}")
                    else:
                        print(f"❌ 创建Skill失败: {rec['skill_name']}")
            
            print(f"\nSkill创建完成: 成功 {created_count}/{len(recommendations)}")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()