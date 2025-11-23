#!/bin/bash
# Installation script for GitHub Contribution Analyzer

set -e  # Exit on error

echo "🚀 GitHub Contribution Analyzer - Installation"
echo "=============================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "   Please install Python 3.7 or higher first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Virtual environment created"
echo ""
echo "📥 Installing dependencies..."

# Activate and install
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r scripts/requirements.txt

echo "✓ Dependencies installed successfully!"
echo ""
echo "=============================================="
echo "✅ Installation complete!"
echo ""
echo "To get started:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Set your GitHub token:"
echo "     export GITHUB_TOKEN=your_token_here"
echo ""
echo "  3. Run the analyzer:"
echo "     python3 analyzers/monthly_productivity_analysis.py -u your_username"
echo ""
echo "For more information, see docs/README.md"
echo "=============================================="

