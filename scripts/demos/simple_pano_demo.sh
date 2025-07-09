#!/usr/bin/env bash
#
# Simple Panorama Demo - Shows git status in all repos
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PANO="$SCRIPT_DIR/../pano"

echo "=== Simple Panorama Demo ==="
echo
echo "Creating tmux session with all repositories..."

# Close any existing session
$PANO close 2>/dev/null || true

# Create new session (this will return immediately since we're not attaching)
$PANO

echo
echo "Running 'gs' (git status) in all repositories..."
$PANO run gs

echo
echo "Session is now active. You can view it in another terminal with:"
echo "  tmux attach -t panorama"
echo
echo "Keeping session open for 15 seconds..."

# Countdown
for i in {15..1}; do
    printf "\rClosing in %2d seconds... (Ctrl+C to keep open)" $i
    sleep 1
done
echo

echo
echo "Closing session..."
$PANO close

echo "Demo complete!"