#!/usr/bin/env bash
#
# Installation script for the pano command
# This script creates a symlink or copies the pano script to a location in PATH
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PANO_SCRIPT="$SCRIPT_DIR/pano"

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Installing pano command..."

# Check if pano script exists
if [[ ! -f "$PANO_SCRIPT" ]]; then
    echo -e "${RED}Error: pano script not found at $PANO_SCRIPT${NC}"
    exit 1
fi

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${YELLOW}Warning: tmux is not installed${NC}"
    echo "Please install tmux first:"
    echo "  macOS: brew install tmux"
    echo "  Linux: sudo apt-get install tmux (or equivalent)"
    exit 1
fi

# Check if PyYAML is installed
if ! python3 -c "import yaml" &> /dev/null; then
    echo -e "${YELLOW}Warning: PyYAML is not installed${NC}"
    echo "Installing PyYAML..."
    pip3 install pyyaml || {
        echo -e "${RED}Failed to install PyYAML. Please install it manually: pip3 install pyyaml${NC}"
        exit 1
    }
fi

# Determine installation directory
if [[ -d "$HOME/.local/bin" ]]; then
    INSTALL_DIR="$HOME/.local/bin"
elif [[ -d "$HOME/bin" ]]; then
    INSTALL_DIR="$HOME/bin"
else
    # Create ~/.local/bin if it doesn't exist
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
    echo -e "${YELLOW}Created $INSTALL_DIR${NC}"
    echo -e "${YELLOW}You may need to add this to your PATH:${NC}"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# Create symlink
PANO_LINK="$INSTALL_DIR/pano"

if [[ -e "$PANO_LINK" ]]; then
    echo -e "${YELLOW}Removing existing pano command at $PANO_LINK${NC}"
    rm -f "$PANO_LINK"
fi

ln -s "$PANO_SCRIPT" "$PANO_LINK"
echo -e "${GREEN}✓ Created symlink: $PANO_LINK -> $PANO_SCRIPT${NC}"

# Check if install directory is in PATH
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    echo -e "${YELLOW}Warning: $INSTALL_DIR is not in your PATH${NC}"
    echo "Add this line to your shell configuration file (~/.bashrc, ~/.zshrc, etc.):"
    echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
    echo
fi

# Test the installation
if command -v pano &> /dev/null; then
    echo -e "${GREEN}✓ Installation successful!${NC}"
    echo
    echo "You can now use the pano command:"
    echo "  pano          - Open panorama view of all repos"
    echo "  pano status   - Check session status"
    echo "  pano close    - Close the session"
    echo "  pano refresh  - Refresh with updated repo list"
else
    echo -e "${YELLOW}Installation complete, but 'pano' command not found in PATH${NC}"
    echo "Please ensure $INSTALL_DIR is in your PATH and restart your shell"
fi