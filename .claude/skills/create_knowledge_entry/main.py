#!/usr/bin/env python3
"""
Create Knowledge Entry - Entry Point
Wraps scripts/plugin_executor.py to provide a standard CLI interface.
"""

import argparse
import sys
import json
import logging
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

try:
    from plugin_executor import KnowledgeCreationEngine
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"Failed to import script: {e}"}))
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Create structured knowledge entry')
    parser.add_argument('--title', required=True, help='Knowledge title')
    parser.add_argument('--content', required=True, help='Knowledge content')
    parser.add_argument('--type', required=True, help='Knowledge type (e.g., 政策文档, 流程指南)')
    parser.add_argument('--mode', default='assisted', choices=['auto', 'assisted', 'manual'], help='Selection mode')
    parser.add_argument('--options', help='JSON string of creation options')
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Parse options
    creation_options = {
        "extract_tags": True,
        "generate_faq": True,
        "generate_summary": True
    }
    if args.options:
        try:
            creation_options.update(json.loads(args.options))
        except json.JSONDecodeError:
            print(json.dumps({"status": "error", "message": "Invalid JSON in --options"}))
            sys.exit(1)
    
    knowledge_content = {
        "title": args.title,
        "content": args.content
    }
    
    try:
        engine = KnowledgeCreationEngine()
        result = engine.create_knowledge_entry(
            knowledge_content=knowledge_content,
            knowledge_type=args.type,
            creation_options=creation_options,
            selection_mode=args.mode
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({
            "status": "error", 
            "message": str(e),
            "error_type": type(e).__name__
        }, ensure_ascii=False))
        sys.exit(1)

if __name__ == '__main__':
    main()
