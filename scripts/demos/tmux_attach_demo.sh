#!/usr/bin/env bash
#
# Tmux Attach Demo - Creates panorama session, runs gs, and attaches to show results
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PANO_SCRIPT="$SCRIPT_DIR/../pano"

echo "=== Panorama Tmux Attach Demo ==="
echo
echo "This demo will:"
echo "1. Create a panorama tmux session"
echo "2. Run 'gs' (git status) in all repositories"
echo "3. Attach you to the session to see the results"
echo "4. Auto-close after 10 seconds (or detach with Ctrl+b d)"
echo

# Check if we're already in tmux
if [[ -n "$TMUX" ]]; then
    echo "⚠️  You're already in a tmux session!"
    echo "   The demo will create a new window instead of attaching."
    echo
fi

read -p "Press Enter to start the demo..."

# Clean up any existing session
echo -e "\n1. Cleaning up any existing session..."
"$PANO_SCRIPT" close 2>/dev/null || true
sleep 1

# Create the session
echo -e "\n2. Creating panorama session..."
"$PANO_SCRIPT" >/dev/null 2>&1 &
sleep 3

# Run gs command
echo -e "\n3. Running 'gs' in all repositories..."
"$PANO_SCRIPT" run gs

# Add a delayed close command
echo -e "\n4. Setting auto-close timer (10 seconds)..."
(sleep 10 && "$PANO_SCRIPT" close >/dev/null 2>&1) &
TIMER_PID=$!

echo -e "\n5. Attaching to session..."
echo "   (Use Ctrl+b d to detach and keep the session running)"
echo "   (Session will auto-close in 10 seconds)"
sleep 2

# Attach to the session
if [[ -n "$TMUX" ]]; then
    # If already in tmux, switch to the panorama session
    tmux switch-client -t panorama 2>/dev/null || tmux new-window -t panorama
else
    # If not in tmux, attach normally
    tmux attach -t panorama
fi

# If we get here, user detached
kill $TIMER_PID 2>/dev/null || true
echo
echo "You've detached from the session."
echo "The panorama session is still running."
echo "Use 'pano' to reattach or 'pano close' to close it."