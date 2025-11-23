#!/usr/bin/env python3
"""
Fetch Commit Contributions for 2025

Fetches and analyzes GitHub contribution data for the year 2025.
"""

import argparse
import os
from collections import Counter
from datetime import datetime

import requests

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description='Fetch and analyze GitHub contributions for 2025',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''
Examples:
  %(prog)s -u octocat
  %(prog)s -u octocat -t ghp_xxxxx
  
Environment Variables:
  GITHUB_TOKEN    GitHub personal access token (alternative to -t)
    '''
)
parser.add_argument('-u', '--user', type=str, required=True,
                    help='GitHub username to analyze')
parser.add_argument('-t', '--token', type=str, 
                    help='GitHub personal access token (or set GITHUB_TOKEN environment variable)')
args = parser.parse_args()

# Get token from argument or environment variable
TOKEN = args.token if args.token else os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    print("Error: GitHub token required. Provide via -t/--token or GITHUB_TOKEN environment variable.")
    exit(1)

# Query using contribution calendar which includes ALL repositories (personal + org)
query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

variables = {
    "login": args.user,
    "from": "2025-01-01T00:00:00Z",
    "to": "2025-12-31T23:59:59Z"
}

print("Fetching contribution data...")
resp = requests.post(
    "https://api.github.com/graphql",
    json={"query": query, "variables": variables},
    headers={"Authorization": f"bearer {TOKEN}"}
)
resp.raise_for_status()
data = resp.json()

if "errors" in data:
    print("API errors:", data["errors"])
    exit(1)

collection = data["data"]["user"]["contributionsCollection"]
calendar = collection["contributionCalendar"]

# Summary
print(f"\n{'='*60}")
print(f"CONTRIBUTION SUMMARY (2025)")
print(f"{'='*60}")
print(f"Total Contributions (all types): {calendar['totalContributions']}")
print(f"  - Commits:                     {collection['totalCommitContributions']}")
print(f"  - Issues:                      {collection['totalIssueContributions']}")
print(f"  - Pull Requests:               {collection['totalPullRequestContributions']}")
print(f"  - PR Reviews:                  {collection['totalPullRequestReviewContributions']}")
print(f"{'='*60}\n")

# Aggregate by weekday
day_counts = Counter()
weekday_counts = Counter()
weekday_total_days = Counter()  # Count ALL days (including 0-contribution days)
weekday_active_days = Counter()  # Count only days with contributions

for week in calendar["weeks"]:
    for day in week["contributionDays"]:
        date_str = day["date"]
        count = day["contributionCount"]
        
        # Parse the date and get weekday
        dt = datetime.fromisoformat(date_str)
        weekday = dt.strftime("%A")
        
        # Count contributions
        weekday_counts[weekday] += count
        
        # Count total days (including days with 0 contributions)
        weekday_total_days[weekday] += 1
        
        # Track days with actual contributions
        if count > 0:
            day_counts[date_str] = count
            weekday_active_days[weekday] += 1

print(f"Days with contributions: {len(day_counts)}\n")

# Show breakdown by weekday
print("Contributions per weekday (UTC based):")
for wd in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
    contribs = weekday_counts.get(wd, 0)
    total_days = weekday_total_days.get(wd, 0)
    active_days = weekday_active_days.get(wd, 0)
    avg = contribs / total_days if total_days else 0
    print(f"{wd:10s}: total={contribs:4d} active_days={active_days:3d}/{total_days:<3d} avg_per_day={avg:5.2f}")

print(f"\n{'='*60}")
print("Note: Includes ALL contribution types across ALL repositories")
print("(personal, organization, public, and private)")
print(f"{'='*60}\n")
