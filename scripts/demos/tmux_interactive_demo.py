#!/usr/bin/env python3
"""
Interactive demo script for Panorama Tmux Session Management.

This demo creates a tmux session, runs commands, and allows you to see
the results in real-time before cleaning up.
"""

import subprocess
import sys
import time
from pathlib import Path


def run_command(cmd: str, capture=True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    print(f"$ {cmd}")
    if capture:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout.rstrip())
        if result.stderr:
            print(f"Error: {result.stderr.rstrip()}", file=sys.stderr)
    else:
        # Run without capturing for interactive commands
        result = subprocess.run(cmd, shell=True)
    return result


def main():
    print("=== Panorama Interactive Tmux Demo ===\n")
    
    # Path to pano script
    pano_script = Path(__file__).parent.parent / "pano"
    if not pano_script.exists():
        print("Error: pano script not found")
        sys.exit(1)
    
    pano = str(pano_script)
    
    print("This demo will:")
    print("1. Create a panorama tmux session")
    print("2. Run 'gs' (git status) in all repositories")
    print("3. Keep the session open for 10 seconds so you can see it")
    print("4. Clean up the session\n")
    
    input("Press Enter to start the demo...")
    
    # Clean up any existing session
    print("\n1. Cleaning up any existing session...")
    run_command(f"{pano} close")
    time.sleep(1)
    
    # Create the session
    print("\n2. Creating panorama session with all repositories...")
    # Create in detached mode
    run_command(f"{pano}")
    time.sleep(2)
    
    # Check status
    print("\n3. Checking session status...")
    run_command(f"{pano} status")
    
    # Run gs command
    print("\n4. Running 'gs' (git status) in all repositories...")
    print("   Note: 'gs' is aliased to 'git status --short --branch --show-stash'")
    run_command(f"{pano} run gs")
    time.sleep(1)
    
    print("\n5. The session is now active with git status displayed in each pane.")
    print("\n   *** IMPORTANT: Open a new terminal and run one of these commands to see the session: ***")
    print("   tmux attach -t panorama")
    print("   OR")
    print("   pano\n")
    
    print("   The session will remain open for 15 seconds...")
    print("   (You can detach from tmux with Ctrl+b then d)\n")
    
    # Countdown
    for i in range(15, 0, -1):
        print(f"\r   Closing in {i:2d} seconds... (Ctrl+C to keep session open)", end='', flush=True)
        time.sleep(1)
    print()
    
    # Clean up
    print("\n6. Cleaning up - closing the session...")
    run_command(f"{pano} close")
    
    print("\n=== Demo Complete ===")
    print("\nWhat you should have seen:")
    print("- A tmux session with 12 panes (one for each repository)")
    print("- Each pane showing the git status of its repository")
    print("- The ability to navigate between panes with tmux commands")
    print("\nTo use pano yourself:")
    print("1. Install: ./scripts/install_pano.sh")
    print("2. Run 'pano' to create a session")
    print("3. Run 'pano run <command>' to execute commands in all repos")
    print("4. Run 'pano close' when done")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. The panorama session is still running.")
        print("Use 'pano close' to close it when you're done.")
        sys.exit(0)