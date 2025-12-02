#!/usr/bin/env python3
"""
Validate FAQ Quality - Entry Point
Wraps scripts/faq_validator.py to provide a standard CLI interface.
"""

import argparse
import sys
import json
import logging
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

try:
    from faq_validator import FAQValidator
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"Failed to import script: {e}"}))
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Validate FAQ quality')
    parser.add_argument('--question', required=True, help='FAQ Question')
    parser.add_argument('--answer', required=True, help='FAQ Answer')
    parser.add_argument('--context', help='Context or source content')
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        validator = FAQValidator()
        result = validator.validate(
            question=args.question,
            answer=args.answer,
            context=args.context
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
