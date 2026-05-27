#!/usr/bin/env bash
#
# Domainization Pre-Commit Hook Installation Script
#
# This script OPTIONALLY installs the domainization pre-commit hook.
# The hook is NON-BLOCKING and provides observability only.
#
# Usage:
#   ./install_hook.sh          # Install hook
#   ./install_hook.sh uninstall # Uninstall hook
#

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo -e "${RED}✗ Error: Not in a git repository${NC}"
    exit 1
fi

DOMAINIZATION_DIR="$REPO_ROOT/.domainization"
HOOK_SOURCE="$DOMAINIZATION_DIR/hooks/pre-commit"
GIT_HOOKS_DIR="$REPO_ROOT/.git/hooks"
HOOK_DEST="$GIT_HOOKS_DIR/pre-commit"
HOOK_BACKUP="$GIT_HOOKS_DIR/pre-commit.backup"

# Function to display header
display_header() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}Domainization Pre-Commit Hook Installation${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Function to display important information
display_info() {
    echo -e "${BLUE}ℹ IMPORTANT INFORMATION:${NC}"
    echo ""
    echo -e "  ${YELLOW}•${NC} This hook is ${GREEN}OPTIONAL${NC}"
    echo -e "  ${YELLOW}•${NC} This hook is ${GREEN}NON-BLOCKING${NC} (never prevents commits)"
    echo -e "  ${YELLOW}•${NC} This hook provides ${CYAN}OBSERVABILITY${NC} (warnings and suggestions only)"
    echo -e "  ${YELLOW}•${NC} You can bypass it with ${CYAN}--no-verify${NC} (no audit needed)"
    echo -e "  ${YELLOW}•${NC} It helps you understand domainization governance"
    echo ""
}

# Function to install hook
install_hook() {
    display_header
    display_info
    
    # Check if domainization system exists
    if [ ! -d "$DOMAINIZATION_DIR" ]; then
        echo -e "${RED}✗ Error: Domainization system not found at $DOMAINIZATION_DIR${NC}"
        exit 1
    fi
    
    # Check if hook source exists
    if [ ! -f "$HOOK_SOURCE" ]; then
        echo -e "${RED}✗ Error: Hook source not found at $HOOK_SOURCE${NC}"
        exit 1
    fi
    
    # Create git hooks directory if it doesn't exist
    mkdir -p "$GIT_HOOKS_DIR"
    
    # Check if hook already exists
    if [ -f "$HOOK_DEST" ]; then
        echo -e "${YELLOW}⚠ Existing pre-commit hook found${NC}"
        echo ""
        echo "Current hook:"
        echo "  $HOOK_DEST"
        echo ""
        
        # Check if it's already our hook
        if grep -q "Domainization Pre-Commit Hook" "$HOOK_DEST" 2>/dev/null; then
            echo -e "${GREEN}✓ Domainization hook is already installed${NC}"
            echo ""
            return 0
        fi
        
        # Ask user if they want to backup and replace
        echo -e "${CYAN}Do you want to backup the existing hook and install the domainization hook?${NC}"
        echo -e "  ${YELLOW}y${NC} - Yes, backup existing hook and install"
        echo -e "  ${YELLOW}n${NC} - No, cancel installation"
        echo ""
        read -p "Choice [y/N]: " -n 1 -r
        echo ""
        
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}✗ Installation cancelled${NC}"
            echo ""
            return 1
        fi
        
        # Backup existing hook
        echo -e "${BLUE}Creating backup...${NC}"
        cp "$HOOK_DEST" "$HOOK_BACKUP"
        echo -e "${GREEN}✓ Existing hook backed up to: $HOOK_BACKUP${NC}"
        echo ""
    fi
    
    # Install hook
    echo -e "${BLUE}Installing domainization pre-commit hook...${NC}"
    cp "$HOOK_SOURCE" "$HOOK_DEST"
    chmod +x "$HOOK_DEST"
    echo -e "${GREEN}✓ Hook installed successfully${NC}"
    echo ""
    
    # Display usage information
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Installation Complete!${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}What happens now:${NC}"
    echo ""
    echo -e "  ${YELLOW}•${NC} The hook will run automatically on ${CYAN}git commit${NC}"
    echo -e "  ${YELLOW}•${NC} It will display warnings about governance violations"
    echo -e "  ${YELLOW}•${NC} Your commit will ${GREEN}ALWAYS proceed${NC} (never blocked)"
    echo -e "  ${YELLOW}•${NC} Use ${CYAN}git commit --no-verify${NC} to skip the hook entirely"
    echo ""
    echo -e "${BLUE}To uninstall:${NC}"
    echo ""
    echo -e "  ${CYAN}$0 uninstall${NC}"
    echo ""
}

# Function to uninstall hook
uninstall_hook() {
    display_header
    
    echo -e "${BLUE}Uninstalling domainization pre-commit hook...${NC}"
    echo ""
    
    # Check if hook exists
    if [ ! -f "$HOOK_DEST" ]; then
        echo -e "${YELLOW}⚠ No pre-commit hook found${NC}"
        echo ""
        return 0
    fi
    
    # Check if it's our hook
    if ! grep -q "Domainization Pre-Commit Hook" "$HOOK_DEST" 2>/dev/null; then
        echo -e "${YELLOW}⚠ Existing hook is not a domainization hook${NC}"
        echo -e "${YELLOW}  Not removing it to avoid breaking your setup${NC}"
        echo ""
        return 1
    fi
    
    # Remove hook
    rm "$HOOK_DEST"
    echo -e "${GREEN}✓ Hook removed${NC}"
    echo ""
    
    # Check if backup exists
    if [ -f "$HOOK_BACKUP" ]; then
        echo -e "${CYAN}A backup of your previous hook exists:${NC}"
        echo -e "  $HOOK_BACKUP"
        echo ""
        echo -e "${CYAN}Do you want to restore it?${NC}"
        echo -e "  ${YELLOW}y${NC} - Yes, restore previous hook"
        echo -e "  ${YELLOW}n${NC} - No, leave it as backup"
        echo ""
        read -p "Choice [y/N]: " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            mv "$HOOK_BACKUP" "$HOOK_DEST"
            chmod +x "$HOOK_DEST"
            echo -e "${GREEN}✓ Previous hook restored${NC}"
            echo ""
        fi
    fi
    
    echo -e "${GREEN}✓ Uninstallation complete${NC}"
    echo ""
}

# Function to display status
display_status() {
    display_header
    
    echo -e "${BLUE}Hook Status:${NC}"
    echo ""
    
    if [ -f "$HOOK_DEST" ]; then
        if grep -q "Domainization Pre-Commit Hook" "$HOOK_DEST" 2>/dev/null; then
            echo -e "  ${GREEN}✓ Domainization hook is installed${NC}"
            echo -e "    Location: $HOOK_DEST"
        else
            echo -e "  ${YELLOW}⚠ A different pre-commit hook is installed${NC}"
            echo -e "    Location: $HOOK_DEST"
        fi
    else
        echo -e "  ${YELLOW}✗ No pre-commit hook installed${NC}"
    fi
    echo ""
    
    if [ -f "$HOOK_BACKUP" ]; then
        echo -e "  ${BLUE}ℹ Backup exists: $HOOK_BACKUP${NC}"
        echo ""
    fi
}

# Main script logic
case "${1:-}" in
    uninstall)
        uninstall_hook
        ;;
    status)
        display_status
        ;;
    install|"")
        install_hook
        ;;
    *)
        echo -e "${RED}✗ Error: Unknown command '$1'${NC}"
        echo ""
        echo "Usage:"
        echo "  $0              # Install hook"
        echo "  $0 install      # Install hook"
        echo "  $0 uninstall    # Uninstall hook"
        echo "  $0 status       # Show hook status"
        echo ""
        exit 1
        ;;
esac
