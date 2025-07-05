#!/usr/bin/env python3
"""
Simple test script for panorama collector.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path so we can import collect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collect import PanoramaCollector


def test_collector():
    """Test the panorama collector functionality."""
    print("Testing Panorama Collector...")
    
    # Test with default config
    collector = PanoramaCollector("config/repos.yaml", "test_output")
    
    # Test loading repos.yaml
    repos_data = collector.repos_data
    assert 'repos' in repos_data, "repos.yaml should contain 'repos' key"
    
    repos = repos_data['repos']
    assert len(repos) > 0, "Should have at least one repository defined"
    
    print(f"✓ Loaded {len(repos)} repositories from config")
    
    # Test path expansion
    test_path = "~/dev/jazzydog-labs/foundry/foundry-bootstrap"
    expanded = collector._expand_path(test_path)
    assert expanded.exists(), f"Expanded path should exist: {expanded}"
    print(f"✓ Path expansion works: {test_path} -> {expanded}")
    
    # Test file reading
    readme_path = expanded / "README.md"
    content = collector._read_file_content(readme_path)
    assert content is not None, "Should be able to read README.md"
    assert len(content) > 0, "README.md should not be empty"
    print(f"✓ File reading works: {readme_path}")
    
    # Test collection (just the first repo to keep it fast)
    print("Testing collection...")
    first_repo = repos[0]
    repo_section = collector._collect_repo_files(first_repo)
    assert len(repo_section) > 0, "Repository section should not be empty"
    assert first_repo['name'] in repo_section, "Repository name should be in section"
    print(f"✓ Collection works for {first_repo['name']}")
    
    # Clean up test output
    test_output_dir = Path("test_output")
    if test_output_dir.exists():
        import shutil
        shutil.rmtree(test_output_dir)
    
    print("✓ All tests passed!")


if __name__ == "__main__":
    test_collector() 