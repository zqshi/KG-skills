#!/usr/bin/env python3
"""
Validate Knowledge Quality - Entry Point
Wraps scripts/knowledge_quality_validator.py to provide a standard CLI interface.
"""

import argparse
import sys
import json
import logging
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

try:
    from knowledge_quality_validator import KnowledgeQualityValidator
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"Failed to import script: {e}"}))
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Validate knowledge quality')
    parser.add_argument('--content', required=True, help='Knowledge content')
    parser.add_argument('--metadata', help='JSON string of metadata')
    parser.add_argument('--criteria', help='JSON string of validation criteria')
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    metadata = {}
    if args.metadata:
        try:
            metadata = json.loads(args.metadata)
        except json.JSONDecodeError:
            print(json.dumps({"status": "error", "message": "Invalid JSON in --metadata"}))
            sys.exit(1)
            
    criteria = {}
    if args.criteria:
        try:
            criteria = json.loads(args.criteria)
        except json.JSONDecodeError:
            print(json.dumps({"status": "error", "message": "Invalid JSON in --criteria"}))
            sys.exit(1)
            
    try:
        validator = KnowledgeQualityValidator()
        result = validator.validate(
            content=args.content,
            metadata=metadata,
            criteria=criteria
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
