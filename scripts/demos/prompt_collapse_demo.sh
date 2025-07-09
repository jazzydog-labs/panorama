#!/usr/bin/env bash
#
# Prompt Collapse Demo - Shows how to simplify prompts for cleaner viewing
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PANO="$SCRIPT_DIR/../pano"

echo "=== Panorama Prompt Collapse Demo ==="
echo
echo "This demo shows how to simplify prompts in all panes for a cleaner view."
echo

# Close any existing session
$PANO close 2>/dev/null || true

# Create new session
echo "1. Creating panorama session..."
$PANO
echo

# Show initial state
echo "2. By default, each pane has its normal shell prompt (often long and complex)"
echo "   You can view this in another terminal with: tmux attach -t panorama"
echo
sleep 2

# Collapse prompts
echo "3. Collapsing all prompts to simple '>'"
$PANO prompt-collapse
echo

echo "4. Now all panes show a simple '>' prompt, making it easier to see content"
echo "   This is especially useful when running commands across all repos"
echo
sleep 2

# Run a command to show the effect
echo "5. Running 'pwd' to show how clean it looks with collapsed prompts..."
$PANO run pwd
echo

echo "Session is active with collapsed prompts."
echo "View it with: tmux attach -t panorama"
echo
echo "Keeping session open for 10 seconds..."

# Countdown
for i in {10..1}; do
    printf "\rClosing in %2d seconds... (Ctrl+C to keep open)" $i
    sleep 1
done
echo

echo
echo "Closing session..."
$PANO close

echo "Demo complete!"