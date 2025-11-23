# 📊 GitHub Contribution Analyzer

Analyze your GitHub contribution history and track your programming productivity over time with beautiful terminal visualizations!

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 📈 **Monthly Productivity Analysis** - Track contributions per active day with trend visualization
- 📊 **Lifetime Statistics** - Year-over-year growth analysis from your account creation
- 📅 **Weekly Patterns** - Understand your contribution patterns by weekday
- 🎨 **Beautiful Terminal Graphs** - No browser needed, everything in your terminal!
- 🔒 **Privacy First** - All analysis runs locally, no data sent anywhere

## 🚀 Quick Start

### 1. Clone or Download

```bash
git clone <repository-url>
cd github_averge_contributions
```

### 2. Run Installation Script

```bash
./scripts/install.sh
```

This will:
- Create a Python virtual environment
- Install all required dependencies
- Set everything up for you!

### 3. Get Your GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name (e.g., "Contribution Analyzer")
4. Select scope: `read:user`
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)

### 4. Set Up Your Token

**Option A: Environment Variable (Recommended)**
```bash
export GITHUB_TOKEN=ghp_your_token_here
```

**Option B: Config File**
```bash
cp config.example.sh config.sh
# Edit config.sh with your token and username
source config.sh
```

### 5. Run the Analyzer! 🎉

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run analysis
python3 monthly_productivity_analysis.py -u your_username
```

## 📖 Usage Guide

### Monthly Productivity Analysis

Analyzes your contribution productivity by month, filtering out vacation/inactive days.

```bash
# Basic usage
python3 analyzers/monthly_productivity_analysis.py -u your_username

# With detailed monthly breakdown
python3 analyzers/monthly_productivity_analysis.py -u your_username --detailed

# Pass token directly (not recommended for scripts)
python3 analyzers/monthly_productivity_analysis.py -u your_username -t ghp_xxxxx
```

**Output includes:**
- Beautiful terminal graph with trend line
- Summary statistics
- Peak productivity months
- Recent trend analysis
- Improvement percentages

### Lifetime Contribution Analysis

Shows year-over-year statistics from account creation.

```bash
export GITHUB_TOKEN=your_token
python3 analyzers/lifetime_contribution_analysis.py
```

**Note:** Currently requires editing the script to set your username (line 22).

**Shows:**
- Contributions by year
- Year-over-year growth
- Breakdown by type (commits, PRs, issues, reviews)
- Historical trends

### Weekly Pattern Analysis

Analyzes contribution patterns by weekday for 2025.

```bash
export GITHUB_TOKEN=your_token
python3 analyzers/fetch_commit_contributions_2025.py
```

**Note:** Currently requires editing the script to set your username (line 22).

**Shows:**
- Contributions per weekday
- Average per day
- Work patterns (weekday vs weekend)

## 📁 Project Structure

```
github-contribution-analyzer/
├── docs/                               # Documentation
│   ├── README.md                      # Main documentation
│   ├── GETTING_STARTED.md             # Beginner's guide
│   ├── PROJECT_STRUCTURE.md           # Project overview
│   └── SUMMARY.md                     # Refactoring summary
├── scripts/                            # Setup & installation
│   ├── install.sh                     # One-command installation
│   ├── quickstart.sh                  # Interactive quick start
│   └── requirements.txt               # Python dependencies
├── config/                             # Configuration
│   └── config.example.sh              # Configuration template
├── analyzers/                          # Analysis scripts
│   ├── monthly_productivity_analysis.py
│   ├── lifetime_contribution_analysis.py
│   └── fetch_commit_contributions_2025.py
├── .gitignore                          # Git ignore rules
├── LICENSE                             # MIT License
├── README.md                           # Symlink to docs/README.md
└── venv/                               # Virtual environment
```

## 🎯 Examples

### Example 1: Quick Analysis

```bash
# Setup once
./scripts/install.sh
source venv/bin/activate
export GITHUB_TOKEN=ghp_xxxxx

# Run analysis
python3 analyzers/monthly_productivity_analysis.py -u octocat
```

### Example 2: Detailed Report

```bash
python3 analyzers/monthly_productivity_analysis.py -u octocat --detailed > report.txt
```

### Example 3: Multiple Users

```bash
# Analyze different users
python3 analyzers/monthly_productivity_analysis.py -u user1
python3 analyzers/monthly_productivity_analysis.py -u user2  
python3 analyzers/monthly_productivity_analysis.py -u user3
```

## 🔐 Security & Privacy

✅ **What this tool does:**
- Fetches your public contribution data from GitHub's API
- Runs all analysis locally on your machine
- Stores token only in environment variables (never in code)

❌ **What this tool doesn't do:**
- Never stores your token permanently
- Never sends data to external servers
- Never accesses private repository contents
- Never modifies any GitHub data

**Best Practices:**
- Use environment variables for tokens
- Never commit tokens to git
- Regenerate tokens periodically
- Use tokens with minimal required scopes

## 🛠️ Troubleshooting

### "Module not found" Error

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r scripts/requirements.txt
```

### "GitHub token required" Error

```bash
# Set token as environment variable
export GITHUB_TOKEN=ghp_your_token_here

# Verify it's set
echo $GITHUB_TOKEN
```

### "Rate limit exceeded" Error

GitHub API has rate limits. Wait an hour or use an authenticated token (which you should already be doing!).

### Script Shows Wrong Username

The `lifetime_contribution_analysis.py` and `fetch_commit_contributions_2025.py` scripts currently have hardcoded usernames. Edit the files and replace the username on line 22.

## 📊 Understanding the Output

### Monthly Productivity Graph

- **Cyan line**: Your actual monthly productivity
- **Green line**: 6-month moving average (trend)
- **Y-axis**: Average contributions per active day
- **X-axis**: Timeline from account creation to now

**What's a good average?**
- 5-8: Solid consistent productivity
- 8-12: High productivity
- 12+: Exceptional productivity!

Remember: Quality > Quantity. These numbers are for tracking your own progress, not comparing to others.

## 🤝 Contributing

Found a bug? Have a feature request? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use this for personal or commercial projects!

## 🙏 Acknowledgments

- Built with [requests](https://requests.readthedocs.io/) for GitHub API access
- Visualizations powered by [plotext](https://github.com/piccolomo/plotext)
- Inspired by the need to track programming progress

## 📧 Support

Having issues? Check the [Troubleshooting](#-troubleshooting) section or open an issue on GitHub.

---

**Made with ❤️ by programmers, for programmers**

*Happy analyzing! 📈*
