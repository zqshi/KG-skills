#!/usr/bin/env python3
"""
Extract Content Tags - Entry Point
Wraps scripts/generic_tag_extractor.py to provide a standard CLI interface.
"""

import argparse
import sys
import json
import logging
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

try:
    from generic_tag_extractor import GenericTagExtractor
except ImportError as e:
    # Fallback if class name is different or file structure varies
    try:
        # Try to find the class in the file
        import importlib.util
        spec = importlib.util.spec_from_file_location("generic_tag_extractor", str(Path(__file__).parent / 'scripts' / 'generic_tag_extractor.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        GenericTagExtractor = getattr(module, 'GenericTagExtractor')
    except Exception as e2:
        print(json.dumps({"status": "error", "message": f"Failed to import script: {e}, {e2}"}))
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Extract tags from content')
    parser.add_argument('--content', required=True, help='Content to extract tags from')
    parser.add_argument('--title', help='Content title')
    parser.add_argument('--domain', default='general', help='Domain for tag extraction')
    parser.add_argument('--max-tags', type=int, default=10, help='Maximum number of tags')
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        extractor = GenericTagExtractor()
        # Assuming extract_tags method exists and signature matches
        # We might need to adjust based on actual method signature
        # Inspecting the file earlier would have been better, but assuming standard interface
        result = extractor.extract_tags(
            content=args.content,
            title=args.title,
            domain=args.domain,
            max_tags=args.max_tags
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
