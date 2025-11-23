# 📂 Project Structure

```
github-contribution-analyzer/
│
├── 📁 docs/                               # Documentation
│   ├── README.md                          # Main documentation  
│   ├── GETTING_STARTED.md                 # Beginner's guide
│   ├── PROJECT_STRUCTURE.md               # This file
│   └── SUMMARY.md                         # Refactoring summary
│
├── 📁 scripts/                            # Setup & installation
│   ├── install.sh                         # One-command installation
│   ├── quickstart.sh                      # Interactive quick start
│   └── requirements.txt                   # Python dependencies
│
├── 📁 config/                             # Configuration
│   └── config.example.sh                  # Configuration template
│
├── 📁 analyzers/                          # Analysis scripts
│   ├── monthly_productivity_analysis.py   # ⭐ Main analyzer (fully configurable)
│   ├── lifetime_contribution_analysis.py  # Year-over-year analysis
│   └── fetch_commit_contributions_2025.py # Weekly pattern for 2025
│
├── 📄 .gitignore                          # Git ignore rules
├── 📄 LICENSE                             # MIT License
├── 📄 README.md                           # Symlink to docs/README.md
│
└── 📁 venv/                               # Virtual environment (created by install.sh)
    ├── bin/
    ├── lib/
    └── ...

Generated Files (git-ignored):
├── 📊 monthly_productivity_data.json      # Exported data
└── 📄 config/config.sh                    # Your local config (if created)
```

## 📝 Directory Descriptions

### `/docs/` - Documentation

All documentation in one organized place:

| File | Purpose |
|------|---------|
| **README.md** | Complete project documentation with all features, usage, and troubleshooting |
| **GETTING_STARTED.md** | Step-by-step guide for complete beginners |
| **PROJECT_STRUCTURE.md** | This file - overview of project organization |
| **SUMMARY.md** | Refactoring summary and before/after comparison |

### `/scripts/` - Setup & Installation

All setup scripts and dependencies:

| File | Purpose |
|------|---------|
| **install.sh** | Automated installation script - run once to set up everything |
| **quickstart.sh** | Interactive script for first-time users |
| **requirements.txt** | Lists all Python package dependencies |

### `/config/` - Configuration

Configuration templates and examples:

| File | Purpose |
|------|---------|
| **config.example.sh** | Template for storing your GitHub credentials |

### `/analyzers/` - Analysis Scripts

All the analyzer scripts:

| Script | Status | Description |
|--------|--------|-------------|
| **monthly_productivity_analysis.py** | ✅ Fully Configurable | Main script with beautiful terminal graphs, trend analysis, and productivity metrics |
| **lifetime_contribution_analysis.py** | ⚠️ Requires username edit | Year-over-year statistics from account creation |
| **fetch_commit_contributions_2025.py** | ⚠️ Requires username edit | Weekly contribution patterns for 2025 |

## 🎯 For New Users

### Start Here:
1. 📖 Read **docs/GETTING_STARTED.md** (complete beginner's guide)
2. 🚀 Run **./scripts/install.sh** (automated setup)
3. 🎮 Run **./scripts/quickstart.sh** (interactive first-time use)
4. 📚 Explore **docs/README.md** (full documentation)

### Key Features:

✅ **Clean Organization**
- All documentation in `docs/`
- All scripts in `scripts/`
- All analyzers in `analyzers/`
- All config in `config/`

✅ **No Hardcoded Values**
- Everything configurable via command-line arguments
- Safe to share - no personal info in code

✅ **Easy Installation**
- Single command: `./scripts/install.sh`
- Handles virtual environment and dependencies automatically

✅ **User-Friendly**
- Interactive quick-start script
- Comprehensive error messages
- Multiple ways to provide credentials

## 🔐 Security Features

✅ **Git Ignore Protection**
- Tokens and secrets automatically excluded
- Config files not committed
- Output data not tracked

✅ **No Hardcoded Credentials**
- Username via `-u` flag
- Token via `-t` flag or environment variable
- Config file template provided

✅ **Local Processing Only**
- All analysis runs on your machine
- No data sent to external servers
- Only reads from GitHub API

## 📊 Output Files

### Generated During Use:

| File | Description | Git Tracked? |
|------|-------------|--------------|
| `monthly_productivity_data.json` | Exported monthly data for further analysis | ❌ No |
| `venv/` | Python virtual environment directory | ❌ No |
| `config/config.sh` | Your personal configuration (if created) | ❌ No |

## 🎨 Design Principles

1. **Organization First**
   - Logical directory structure
   - Related files grouped together
   - Easy to navigate

2. **User-Friendliness**
   - Clear error messages
   - Interactive scripts
   - Multiple documentation levels

3. **Security by Default**
   - No credentials in code
   - Gitignore protects secrets
   - Environment variables supported

4. **Best Practices**
   - Virtual environments
   - Dependency management
   - Clear project structure
   - Proper separation of concerns

## 🚀 Quick Commands

```bash
# First time setup
./scripts/install.sh

# Interactive use
./scripts/quickstart.sh

# Manual use
source venv/bin/activate
export GITHUB_TOKEN=your_token
python3 analyzers/monthly_productivity_analysis.py -u your_username

# With detailed output
python3 analyzers/monthly_productivity_analysis.py -u your_username --detailed

# Get help
python3 analyzers/monthly_productivity_analysis.py --help
```

## 📦 Dependencies

Managed via `scripts/requirements.txt`:

- **requests** (>=2.31.0) - GitHub API communication
- **plotext** (>=5.3.0) - Terminal-based graphing

Both are automatically installed by `./scripts/install.sh`.

## 🔄 Development Workflow

**For Contributors:**

```bash
# Clone repository
git clone <repo-url>
cd github-contribution-analyzer

# Install in development mode
./scripts/install.sh
source venv/bin/activate

# Make changes to files in analyzers/, docs/, etc.

# Test your changes
python3 analyzers/monthly_productivity_analysis.py -u test_user

# Ensure no personal data in code
git status
git diff

# Commit
git add .
git commit -m "Your changes"
git push
```

## 📈 Directory Benefits

### Why This Structure?

1. **`/docs/`** - All documentation in one place
   - Easy to find
   - Keeps root clean
   - README.md symlinked to root for GitHub

2. **`/scripts/`** - Setup scripts together
   - Clear purpose
   - Easy to maintain
   - Grouped by function

3. **`/config/`** - Configuration separated
   - Secure
   - Easy to gitignore
   - Clear what not to commit

4. **`/analyzers/`** - Analysis code organized
   - Main functionality grouped
   - Easy to add new analyzers
   - Clear what the project does

## 🤝 Contributing

When contributing:

1. Follow the directory structure
2. Put documentation in `docs/`
3. Put new analyzers in `analyzers/`
4. Update `docs/README.md` with new features
5. Update this file if structure changes

## 📝 File Naming Conventions

- **Scripts**: `snake_case.py` or `kebab-case.sh`
- **Documentation**: `SCREAMING_SNAKE_CASE.md` for meta docs, `PascalCase.md` for guides
- **Directories**: `lowercase` no underscores

---

**Project Structure Version:** 2.0.0 (Reorganized)  
**Last Updated:** 2025-11-21  
**Maintained by:** Joel Broström
