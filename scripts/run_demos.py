#!/usr/bin/env python3
"""
Demo runner for Panorama.

Executes all demonstration scripts in the demos directory.
"""

import subprocess
import sys
from pathlib import Path


def run_demo(demo_path: Path) -> bool:
    """Run a single demo script."""
    print(f"\n{'=' * 60}")
    print(f"Running: {demo_path.name}")
    print("=" * 60)

    try:
        result = subprocess.run([sys.executable, str(demo_path)], check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Demo failed: {demo_path.name}")
        print(f"Error: {e}")
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error output:", e.stderr)
        return False


def main():
    """Run all demos in the demos directory."""
    demos_dir = Path(__file__).parent / "demos"

    if not demos_dir.exists():
        print("❌ Demos directory not found!")
        sys.exit(1)

    # Find all Python demo scripts
    demo_scripts = sorted(demos_dir.glob("*.py"))
    demo_scripts = [d for d in demo_scripts if d.name != "__init__.py"]

    if not demo_scripts:
        print("No demo scripts found!")
        sys.exit(0)

    print(f"Found {len(demo_scripts)} demo(s) to run:")
    for demo in demo_scripts:
        print(f"  - {demo.name}")

    # Run each demo
    successful = 0
    failed = 0

    for demo in demo_scripts:
        if run_demo(demo):
            successful += 1
        else:
            failed += 1

    # Summary
    print(f"\n{'=' * 60}")
    print("Demo Summary:")
    print(f"  ✓ Successful: {successful}")
    if failed > 0:
        print(f"  ✗ Failed: {failed}")
    print("=" * 60)

    # Clean up demo output
    demo_output = Path("demo_output")
    if demo_output.exists():
        import shutil

        shutil.rmtree(demo_output)
        print("\nCleaned up demo output directory")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
