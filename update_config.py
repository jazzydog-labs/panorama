#!/usr/bin/env python3
"""
Helper script to update panorama config from bill-of-materials.
"""

import shutil
import sys
from pathlib import Path


def update_config():
    """Update panorama config from bill-of-materials."""
    # Paths
    bom_repos_yaml = Path("../bill-of-materials/repos.yaml")
    panorama_repos_yaml = Path("config/repos.yaml")
    
    if not bom_repos_yaml.exists():
        print(f"❌ Error: {bom_repos_yaml} not found")
        print("   Make sure you're running this from the panorama directory")
        sys.exit(1)
    
    try:
        # Copy the file
        shutil.copy2(bom_repos_yaml, panorama_repos_yaml)
        print(f"✅ Updated {panorama_repos_yaml} from {bom_repos_yaml}")
        
        # Show file info
        stat = panorama_repos_yaml.stat()
        print(f"   Size: {stat.st_size} bytes")
        print(f"   Modified: {stat.st_mtime}")
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        sys.exit(1)


if __name__ == "__main__":
    update_config() 