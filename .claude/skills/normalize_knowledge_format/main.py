#!/usr/bin/env python3
"""
Normalize Knowledge Format - Entry Point
Wraps scripts/format_normalizer.py to provide a standard CLI interface.
"""

import argparse
import sys
import json
import logging
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

try:
    from format_normalizer import FormatNormalizer
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"Failed to import script: {e}"}))
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Normalize knowledge format')
    parser.add_argument('--content', required=True, help='Content to normalize')
    parser.add_argument('--format', default='markdown', choices=['markdown', 'text', 'html'], help='Target format')
    parser.add_argument('--options', help='JSON string of normalization options')
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    options = {}
    if args.options:
        try:
            options = json.loads(args.options)
        except json.JSONDecodeError:
            print(json.dumps({"status": "error", "message": "Invalid JSON in --options"}))
            sys.exit(1)
            
    try:
        normalizer = FormatNormalizer()
        # Assuming normalize method exists
        result = normalizer.normalize(
            content=args.content,
            target_format=args.format,
            options=options
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
