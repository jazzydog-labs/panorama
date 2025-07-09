#!/usr/bin/env python3
"""
Basic collection demo for Panorama.

This demo shows how to use the PanoramaCollector to aggregate
documentation from multiple repositories.
"""

import sys
from pathlib import Path

# Add parent directory to path to import collect module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from collect import PanoramaCollector


def main():
    print("=== Panorama Basic Collection Demo ===\n")
    
    # Initialize collector with default config
    print("1. Initializing collector with config/repos.yaml...")
    collector = PanoramaCollector("config/repos.yaml", "demo_output")
    
    # Show loaded repositories
    repos = collector.repos_data.get('repos', [])
    print(f"\n2. Loaded {len(repos)} repositories:")
    for repo in repos[:3]:  # Show first 3
        print(f"   - {repo['name']}: {repo.get('description', 'No description')}")
    if len(repos) > 3:
        print(f"   ... and {len(repos) - 3} more\n")
    
    # Run collection
    print("3. Running collection (this may take a moment)...")
    content = collector.collect_all()
    collector.write_output(content)
    
    # Show results
    output_file = Path("demo_output/context.md")
    if output_file.exists():
        file_size = output_file.stat().st_size / 1024  # KB
        with open(output_file, 'r') as f:
            line_count = sum(1 for line in f)
        
        print(f"\n4. Collection complete!")
        print(f"   - Output file: {output_file}")
        print(f"   - File size: {file_size:.1f} KB")
        print(f"   - Line count: {line_count:,}")
        
        # Show a snippet
        print("\n5. First few lines of output:")
        print("   " + "-" * 60)
        with open(output_file, 'r') as f:
            for i, line in enumerate(f):
                if i >= 10:
                    print("   ...")
                    break
                print(f"   {line.rstrip()}")
    else:
        print("\n❌ Error: Output file not created")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()