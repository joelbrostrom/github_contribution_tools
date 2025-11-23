#!/bin/bash
# Convenience script to activate the virtual environment
#
# Usage: source ./activate_venv.sh
# or:    . ./activate_venv.sh

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: ./scripts/install.sh"
    return 1 2>/dev/null || exit 1
fi

source venv/bin/activate
echo "✅ Virtual environment activated!"
echo "   (venv) indicator should appear in your prompt"
echo ""
echo "To deactivate, run: deactivate"

