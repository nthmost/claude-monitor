#!/bin/bash
# Wrapper script to run the monitor with dependency management

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/.venv"

# Create or rebuild virtual environment if missing or broken (e.g. after Python upgrade)
if [ ! -d "$VENV_DIR" ] || [ ! -x "$VENV_DIR/bin/python3" ] || ! "$VENV_DIR/bin/python3" -c "" 2>/dev/null; then
    echo "Creating virtual environment..."
    rm -rf "$VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Check if rich is installed, install if needed
if ! python3 -c "import rich" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Run the monitor
python3 monitor.py "$@"
