# 🎯 Getting Started - Complete Beginner's Guide

Never used the terminal before? No problem! This guide will walk you through everything step-by-step.

## 📋 What You'll Need

1. A computer with macOS, Linux, or Windows
2. Python 3.7 or newer installed
3. A GitHub account
4. 10 minutes of your time

## 🚀 Step-by-Step Installation

### Step 1: Download the Code

**Option A: Using Git (Recommended)**
```bash
git clone <repository-url>
cd github_averge_contributions
```

**Option B: Download ZIP**
1. Click the green "Code" button on GitHub
2. Click "Download ZIP"
3. Extract the ZIP file
4. Open terminal and navigate to the folder:
   ```bash
   cd path/to/github_averge_contributions
   ```

### Step 2: Run the Installation Script

Just copy and paste this into your terminal:

```bash
./scripts/install.sh
```

**What it does:**
- Creates a safe, isolated Python environment
- Installs all needed software packages
- Sets everything up for you

**If you see "permission denied":**
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### Step 3: Get Your GitHub Token

1. **Go to GitHub Settings**
   - Visit: https://github.com/settings/tokens
   - Or: Click your profile → Settings → Developer settings → Personal access tokens

2. **Create a New Token**
   - Click "Generate new token (classic)"
   - Give it a name: `Contribution Analyzer`
   - Select **one** checkbox: `read:user`
   - Click "Generate token" at the bottom

3. **Copy Your Token**
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Important:** Copy it now! You won't see it again!

4. **Save Your Token**
   - Paste it into a safe place temporarily
   - You'll use it in the next step

### Step 4: Set Up Your Token

In your terminal, type this (replace with your actual token):

```bash
export GITHUB_TOKEN=ghp_your_actual_token_here
```

**Verify it worked:**
```bash
echo $GITHUB_TOKEN
```
You should see your token printed out.

### Step 5: Run Your First Analysis! 🎉

```bash
# Make sure the virtual environment is active
source venv/bin/activate

# Run the analyzer (replace 'your_username' with your GitHub username)
python3 analyzers/monthly_productivity_analysis.py -u your_username
```

**That's it!** You should see a beautiful graph of your GitHub contributions! 📊

## 🎮 Using the Tool

### Basic Commands

**Analyze your contributions:**
```bash
python3 analyzers/monthly_productivity_analysis.py -u your_username
```

**Get detailed breakdown:**
```bash
python3 analyzers/monthly_productivity_analysis.py -u your_username --detailed
```

**Analyze someone else:**
```bash
python3 analyzers/monthly_productivity_analysis.py -u octocat
```

### Every Time You Use It

1. **Open Terminal**
2. **Navigate to the folder:**
   ```bash
   cd path/to/github_averge_contributions
   ```
3. **Activate the environment:**
   ```bash
   source venv/bin/activate
   ```
4. **Set your token (if not already set):**
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   ```
5. **Run the command:**
   ```bash
   python3 analyzers/monthly_productivity_analysis.py -u your_username
   ```

### Quick Start (After Initial Setup)

Use the quick start script:

```bash
./scripts/quickstart.sh
```

It will prompt you for your username and do everything automatically!

## 🆘 Common Problems & Solutions

### Problem: "python3: command not found"

**Solution:** Python is not installed.
- **macOS:** Install from https://python.org or use `brew install python3`
- **Linux:** `sudo apt-get install python3` (Ubuntu/Debian) or `sudo yum install python3` (RedHat/CentOS)
- **Windows:** Download from https://python.org

### Problem: "GitHub token required"

**Solution:** Your token isn't set.
```bash
export GITHUB_TOKEN=ghp_your_token_here
```

### Problem: "Permission denied: ./install.sh"

**Solution:** Make the script executable.
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### Problem: "Module not found"

**Solution:** Activate the virtual environment.
```bash
source venv/bin/activate
pip install -r scripts/requirements.txt
```

### Problem: "Rate limit exceeded"

**Solution:** You've made too many requests. Wait 1 hour or check that your token is set correctly.

## 💡 Pro Tips

1. **Save time:** Add this to your `~/.bashrc` or `~/.zshrc`:
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   ```
   Then you don't need to set it every time!

2. **Quick alias:** Add this to your shell config:
   ```bash
   alias ghstats="cd ~/path/to/github_averge_contributions && source venv/bin/activate && python3 analyzers/monthly_productivity_analysis.py -u your_username"
   ```
   Then just type `ghstats` to run it!

3. **Compare users:** Run multiple times with different usernames to compare!

## 📚 What's Next?

Now that you're up and running:

1. Try the `--detailed` flag to see all your monthly data
2. Check out other scripts:
   - `analyzers/lifetime_contribution_analysis.py` - Year-by-year history
   - `analyzers/fetch_commit_contributions_2025.py` - Weekly patterns
3. Read docs/README.md for advanced features

## 🎓 Understanding the Terminal

If you're new to the terminal, here are basic commands:

```bash
pwd              # Print current directory (where am I?)
ls               # List files in current directory
cd folder_name   # Change into a folder
cd ..            # Go up one folder
cd ~             # Go to your home directory
```

## ❓ Still Stuck?

1. Read the error message carefully
2. Check docs/README.md
3. Make sure Python 3.7+ is installed: `python3 --version`
4. Verify your token is set: `echo $GITHUB_TOKEN`
5. Try reinstalling: `rm -rf venv && ./scripts/install.sh`

## 🎉 Success!

If you see a graph with your contribution data, you did it! 

Welcome to the world of analyzing your programming journey! 📈

---

*Remember: The goal is to track YOUR progress, not compare with others. Happy coding!* 💻

