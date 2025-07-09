#!/usr/bin/env python3
"""
Demo script for Panorama Tmux Session Management.

This demo shows how the pano command works to create and manage
a tmux session displaying all foundry repositories.
"""

import subprocess
import sys
import time
from pathlib import Path


def run_command(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}", file=sys.stderr)
    
    if check and result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(1)
    
    return result


def main():
    print("=== Panorama Tmux Session Management Demo ===\n")
    
    # Check if pano is in PATH
    pano_script = Path(__file__).parent.parent / "pano"
    if not pano_script.exists():
        print("Error: pano script not found")
        sys.exit(1)
    
    # Use the local pano script for demo
    pano = str(pano_script)
    
    print("1. Checking tmux installation...")
    result = run_command("which tmux", check=False)
    if result.returncode != 0:
        print("   ❌ tmux is not installed. Please install it first:")
        print("      macOS: brew install tmux")
        print("      Linux: sudo apt-get install tmux")
        sys.exit(1)
    print("   ✓ tmux is installed\n")
    
    print("2. Checking current session status...")
    run_command(f"{pano} status", check=False)
    print()
    
    print("3. Creating panorama session...")
    result = run_command(f"{pano} close", check=False)  # Clean up any existing session
    time.sleep(1)
    
    # Create the session (but don't attach since we're in a demo)
    print(f"$ {pano}")
    # Run synchronously to ensure it completes
    result = subprocess.run([sys.executable, pano], 
                          capture_output=True, 
                          text=True)
    if result.stdout:
        print(result.stdout)
    time.sleep(2)  # Give tmux time to stabilize
    
    print("\n4. Checking session status after creation...")
    run_command(f"{pano} status")
    
    print("\n5. Listing tmux sessions...")
    run_command("tmux ls | grep panorama || echo 'No panorama session found'", check=False)
    
    print("\n6. Showing session layout...")
    result = run_command("tmux list-windows -t panorama 2>/dev/null || echo 'Session not found'", check=False)
    
    print("\n7. Demonstrating refresh command...")
    print("   This would reload the session with any updated repository list")
    run_command(f"{pano} refresh", check=False)
    time.sleep(2)
    
    # Check if session exists after refresh
    result = run_command(f"{pano} status", check=False)
    if "No panorama session found" in result.stdout:
        print("\n   Creating session again...")
        # Create the session synchronously
        result = subprocess.run([sys.executable, pano], 
                              capture_output=True, 
                              text=True)
        if result.stdout:
            print(result.stdout)
        time.sleep(2)
    
    print("\n8. Running 'gs' (git status) in all repositories...")
    print("   Note: gs is aliased to 'git status --short --branch --show-stash'")
    run_command(f"{pano} run gs", check=False)
    
    print("\n9. Session is now running with git status displayed in each pane.")
    print("   To view the session, run: tmux attach -t panorama")
    print("   Or use: pano")
    print()
    print("   Waiting 10 seconds before closing...")
    
    # Show countdown
    for i in range(10, 0, -1):
        print(f"   {i}...", end='', flush=True)
        time.sleep(1)
    print()
    
    print("\n10. Cleaning up - closing the session...")
    run_command(f"{pano} close")
    
    print("\n=== Demo Complete ===")
    print("\nTo use pano in your terminal:")
    print("  1. Install it: ./scripts/install_pano.sh")
    print("  2. Run 'pano' to open the multi-repo view")
    print("  3. Use standard tmux commands to navigate:")
    print("     - Ctrl+b then arrow keys to move between panes")
    print("     - Ctrl+b then z to zoom a pane")
    print("     - Ctrl+b then d to detach from session")
    print("  4. Run 'pano close' to end the session")


if __name__ == "__main__":
    main()