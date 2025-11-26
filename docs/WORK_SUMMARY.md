# Work Summary Generator

A tool to generate formatted summaries of your GitHub work (PRs) for any time period.

## Quick Start

```bash
# Today's work
analyzers/work_summary.py -u USERNAME -t YOUR_TOKEN --today --include-stats

# Yesterday
analyzers/work_summary.py -u USERNAME -t YOUR_TOKEN --yesterday --include-stats

# Last week
analyzers/work_summary.py -u USERNAME -t YOUR_TOKEN --last-week --include-stats

# This month
analyzers/work_summary.py -u USERNAME -t YOUR_TOKEN --this-month --include-stats

# Custom date range
analyzers/work_summary.py -u USERNAME -t YOUR_TOKEN --custom --start 2025-01-01 --end 2025-01-31 --include-stats
```

## Use Cases

### 1. Time Tracking / Time Logging
Export your daily work summary to add to time tracking systems:

```bash
# Generate today's work summary in text format
analyzers/work_summary.py -u USERNAME -t TOKEN --today --include-stats

# Copy the output and paste it into your time logging system
```

### 2. Status Reports
Generate markdown reports for your manager or team:

```bash
# Weekly report in markdown format
analyzers/work_summary.py -u USERNAME -t TOKEN --last-week --format markdown --include-stats --export weekly-report.md

# Monthly report
analyzers/work_summary.py -u USERNAME -t TOKEN --this-month --format markdown --include-stats --export monthly-report.md
```

### 3. Personal Productivity Tracking
Review what you've accomplished over any period:

```bash
# See what you did this week
analyzers/work_summary.py -u USERNAME -t TOKEN --this-week --include-stats

# Review last month's work
analyzers/work_summary.py -u USERNAME -t TOKEN --last-month --include-stats
```

## Time Period Options

| Option | Description | Example |
|--------|-------------|---------|
| `--today` | Work done today (00:00 to now) | Today's contributions |
| `--yesterday` | Work done yesterday | Yesterday's contributions |
| `--last-week` | Last 7 days | Rolling 7-day window |
| `--last-month` | Last 30 days | Rolling 30-day window |
| `--this-week` | This week (Monday-today) | Calendar week to date |
| `--this-month` | This month (1st-today) | Calendar month to date |
| `--last-year` | Last 365 days | Rolling year window |
| `--custom` | Custom date range | Requires `--start` and `--end` |

## Output Formats

### Text Format (Default)
Clean, terminal-friendly format perfect for copying into text fields:

```bash
analyzers/work_summary.py -u USERNAME -t TOKEN --today --format text
```

### Markdown Format
Perfect for documentation, GitHub issues, or Slack messages:

```bash
analyzers/work_summary.py -u USERNAME -t TOKEN --today --format markdown
```

Features:
- Clickable PR links
- Status emojis (🟢 merged, 🔵 open, 🔴 closed)
- Formatted statistics
- Clean hierarchy

### JSON Format
Structured data for parsing or integration with other tools:

```bash
analyzers/work_summary.py -u USERNAME -t TOKEN --today --format json
```

## Grouping Options

### Group by Repository (Default)
PRs organized by repository:

```bash
analyzers/work_summary.py -u USERNAME -t TOKEN --last-week --group-by repo
```

### Group by Date
PRs organized chronologically:

```bash
analyzers/work_summary.py -u USERNAME -t TOKEN --last-week --group-by date
```

### No Grouping
Flat list of all PRs:

```bash
analyzers/work_summary.py -u USERNAME -t TOKEN --last-week --group-by none
```

## Export Options

### Export to File
Save summary to a file instead of just printing:

```bash
# Export today's work to a markdown file
analyzers/work_summary.py -u USERNAME -t TOKEN --today --format markdown --export today-work.md

# Export weekly report as JSON for processing
analyzers/work_summary.py -u USERNAME -t TOKEN --last-week --format json --export weekly-data.json
```

## Statistics

Add `--include-stats` to get summary statistics:

- Total PR count
- Merged/Open/Closed breakdown
- Lines added/deleted
- Total code changes

```bash
analyzers/work_summary.py -u USERNAME -t TOKEN --today --include-stats
```

## Examples

### Daily Stand-up Report
```bash
analyzers/work_summary.py -u joelbrostrom -t $GITHUB_TOKEN --yesterday --format markdown --include-stats
```
Use the output for your daily stand-up to show what you accomplished yesterday.

### Weekly Team Update
```bash
analyzers/work_summary.py -u joelbrostrom -t $GITHUB_TOKEN --this-week --format markdown --include-stats --export weekly-update.md
```
Generate a weekly update document to share with your team.

### Time Logging
```bash
analyzers/work_summary.py -u joelbrostrom -t $GITHUB_TOKEN --today --format text
```
Copy the output directly into your time tracking system's description field.

### Quarterly Review
```bash
analyzers/work_summary.py -u joelbrostrom -t $GITHUB_TOKEN --custom --start 2025-01-01 --end 2025-03-31 --format markdown --include-stats --export q1-2025.md
```
Generate a comprehensive report for performance reviews.

## Environment Variables

Instead of passing the token every time, set it as an environment variable:

```bash
export GITHUB_TOKEN=your_token_here

# Now you can omit -t flag
analyzers/work_summary.py -u joelbrostrom --today --include-stats
```

Add this to your `.zshrc` or `.bashrc`:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

## Tips

1. **Alias for Quick Access**: Add to your shell config:
   ```bash
   alias worktoday="analyzers/work_summary.py -u YOUR_USERNAME -t $GITHUB_TOKEN --today --include-stats"
   alias workweek="analyzers/work_summary.py -u YOUR_USERNAME -t $GITHUB_TOKEN --last-week --format markdown --include-stats"
   ```

2. **Automation**: Schedule daily summaries:
   ```bash
   # Add to crontab to email yourself daily summaries
   0 18 * * * cd ~/path/to/repo && analyzers/work_summary.py -u USERNAME -t TOKEN --today --format markdown --export /tmp/today.md
   ```

3. **Integration**: Pipe to clipboard:
   ```bash
   # macOS
   analyzers/work_summary.py -u USERNAME -t TOKEN --today | pbcopy
   
   # Linux
   analyzers/work_summary.py -u USERNAME -t TOKEN --today | xclip -selection clipboard
   ```

## Required Token Permissions

The GitHub token needs:
- `repo` scope (to access private repositories)
- `read:org` scope (to access organization repositories)

See the main README for instructions on creating a token.

