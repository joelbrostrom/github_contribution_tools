#!/bin/bash
# Quick Start Script for GitHub Contribution Analyzer

echo "📊 GitHub Contribution Analyzer - Quick Start"
echo "=============================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "   Running installation first..."
    ./scripts/install.sh
else
    echo "✓ Virtual environment found"
fi

# Activate venv
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Check for token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  GITHUB_TOKEN not set!"
    echo ""
    echo "Please set your GitHub token:"
    echo "  export GITHUB_TOKEN=ghp_your_token_here"
    echo ""
    echo "Get a token at: https://github.com/settings/tokens"
    echo "(Required scope: read:user)"
    echo ""
    exit 1
fi

echo "✓ GitHub token found"
echo ""

# Ask for username
echo "Enter your GitHub username:"
read -p "> " username

if [ -z "$username" ]; then
    echo "❌ Username is required"
    exit 1
fi

echo ""
echo "🚀 Running analysis for @$username..."
echo "=============================================="
echo ""

# Run the analysis
python3 analyzers/monthly_productivity_analysis.py -u "$username"

echo ""
echo "=============================================="
echo "✅ Analysis complete!"
echo ""
echo "To run again:"
echo "  source venv/bin/activate"
echo "  python3 analyzers/monthly_productivity_analysis.py -u $username"
echo ""
echo "For detailed breakdown, add --detailed flag"
echo "=============================================="

