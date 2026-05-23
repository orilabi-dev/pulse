#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

set -e
set -u
set -o pipefail

colors_dir="$SCRIPT_DIR/colors.sh"

source $colors_dir

info "Setting up your pulse repo...."

# Check Python3 is available
if ! command -v python3 &> /dev/null; then
    error "Python 3 is not installed or not on your PATH"
fi

success "Python 3 found: $(python3 --version)"

# Check uv is available
if ! command -v uv &> /dev/null; then
    error "uv is not installed. Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

success "uv found: $(uv --version)"

# Create virtual environment
if [[ ! -d ".venv" ]]; then
    uv venv .venv
    success "Virtual environment created"
fi

# Setup .env
if [[ ! -f ".env" ]]; then
    info ".env not found — copying from .env.example..."
    cp .env.example .env
    success ".env created. Open it and fill in your API keys before running anything"
else
    info ".env already exists"
fi

info ""
success "Setup complete. To activate your environment run:"
success "  source .venv/bin/activate"