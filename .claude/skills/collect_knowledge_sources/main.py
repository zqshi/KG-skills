#!/usr/bin/env python3
"""
Knowledge Collector - Entry Point
Wraps scripts/knowledge_collector.py to provide a standard CLI interface.
"""

import argparse
import sys
import json
import logging
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

try:
    from knowledge_collector import KnowledgeCollector
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"Failed to import script: {e}"}))
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Collect knowledge from various sources')
    parser.add_argument('--sources', required=True, nargs='+', help='List of source URLs or file paths')
    parser.add_argument('--types', nargs='+', help='List of content types (web, pdf, doc, etc.)')
    parser.add_argument('--strategy', default='parallel', choices=['parallel', 'sequential'], help='Collection strategy')
    parser.add_argument('--max-concurrent', type=int, default=5, help='Max concurrent collections')
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Prepare config
    config = {
        'max_concurrent': args.max_concurrent,
        'timeout_seconds': 30
    }
    
    collection_config = {
        'source_urls': args.sources,
        'content_types': args.types if args.types else [],
        'collection_strategy': args.strategy,
        'max_concurrent': args.max_concurrent
    }
    
    try:
        collector = KnowledgeCollector(config)
        result = collector.collect_sources(collection_config)
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
