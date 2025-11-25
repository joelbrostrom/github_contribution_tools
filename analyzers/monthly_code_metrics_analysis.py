#!/usr/bin/env python3
"""
Monthly Code Metrics Analysis

Analyzes GitHub code metrics (lines added, deleted, and total changes) by month
from Pull Requests, filtering out vacation days and showing only active working days.
"""

import argparse
import json
import os
from collections import defaultdict
from datetime import datetime, timedelta

import plotext as plt
import requests

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description='Analyze GitHub code metrics (lines added/deleted) from PRs over time',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''
Examples:
  %(prog)s -u octocat
  %(prog)s -u octocat -t ghp_xxxxx --detailed
  %(prog)s -u octocat --workdays-per-week 6
  
Environment Variables:
  GITHUB_TOKEN    GitHub personal access token (alternative to -t)
    '''
)
parser.add_argument('-u', '--user', type=str, required=True,
                    help='GitHub username to analyze')
parser.add_argument('-t', '--token', type=str, 
                    help='GitHub personal access token (or set GITHUB_TOKEN environment variable)')
parser.add_argument('--detailed', action='store_true', 
                    help='Show detailed monthly breakdown table')
parser.add_argument('--workdays-per-week', type=int, default=5,
                    help='Number of workdays per week (default: 5 for Mon-Fri)')
args = parser.parse_args()

# Get token from argument or environment variable
TOKEN = args.token if args.token else os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    print("Error: GitHub token required. Provide via -t/--token or GITHUB_TOKEN environment variable.")
    exit(1)

# First, get account creation date
user_query = """
query($login: String!) {
  user(login: $login) {
    createdAt
    name
  }
}
"""

print("Fetching account information...")
resp = requests.post(
    "https://api.github.com/graphql",
    json={"query": user_query, "variables": {"login": args.user}},
    headers={"Authorization": f"bearer {TOKEN}"}
)
resp.raise_for_status()
data = resp.json()

if "errors" in data:
    print("API errors:", data["errors"])
    exit(1)

user_info = data["data"]["user"]
account_created = datetime.fromisoformat(user_info["createdAt"].replace("Z", "+00:00"))
account_created_year = account_created.year
current_year = datetime.now().year

print(f"Account: {user_info['name']} (@{args.user})")
print(f"Member since: {account_created.strftime('%B %d, %Y')}")
print(f"Analyzing code metrics from PRs created {account_created_year} to {current_year}...\n")

# Query for Pull Requests directly from user
# This will get all PRs authored by the user including private repositories
pr_query = """
query($login: String!, $after: String) {
  user(login: $login) {
    pullRequests(first: 100, after: $after, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        title
        createdAt
        mergedAt
        closedAt
        state
        additions
        deletions
        repository {
          nameWithOwner
          isPrivate
        }
      }
      totalCount
    }
  }
}
"""

all_prs = []

print("Fetching Pull Requests (including private repositories)...")
print("This may take a while for users with many PRs...\n")

# Fetch all PRs with pagination
has_next = True
cursor = None
total_count = None

while has_next:
    variables = {
        "login": args.user,
        "after": cursor
    }
    
    try:
        resp = requests.post(
            "https://api.github.com/graphql",
            json={"query": pr_query, "variables": variables},
            headers={"Authorization": f"bearer {TOKEN}"}
        )
        resp.raise_for_status()
        data = resp.json()
        
        if "errors" in data:
            print(f"⚠ Error fetching PRs: {data['errors']}")
            break
        
        pr_data = data["data"]["user"]["pullRequests"]
        
        # Get total count on first iteration
        if total_count is None:
            total_count = pr_data["totalCount"]
            print(f"Found {total_count} total PRs to analyze...")
        
        # Extract PRs
        prs = pr_data["nodes"]
        all_prs.extend(prs)
        
        print(f"Fetched {len(all_prs)}/{total_count} PRs...", end="\r", flush=True)
        
        page_info = pr_data["pageInfo"]
        has_next = page_info["hasNextPage"]
        cursor = page_info.get("endCursor")
        
    except Exception as e:
        print(f"\n⚠ Error: {e}")
        break

print(f"\n")

print(f"✓ Total PRs analyzed: {len(all_prs)}")

if not all_prs:
    print("\nNo Pull Requests found. This could mean:")
    print("  - The user has not created any PRs")
    print("  - The token doesn't have sufficient permissions")
    exit(1)

# Count private vs public PRs
private_prs = sum(1 for pr in all_prs if pr.get("repository", {}).get("isPrivate", False))
public_prs = len(all_prs) - private_prs

print(f"  - Public PRs:  {public_prs}")
print(f"  - Private PRs: {private_prs}")
print()

# Group by week and track metrics
# We'll use the createdAt date for when the PR was created
weekly_stats = defaultdict(lambda: {"days_by_month": defaultdict(lambda: {"count": 0, "additions": 0, "deletions": 0, "total": 0})})

for pr in all_prs:
    # Use createdAt as the date for this PR
    date = datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))
    # Get ISO week number (year, week_number)
    iso_year, iso_week, _ = date.isocalendar()
    week_key = f"{iso_year}-W{iso_week:02d}"
    month_key = date.strftime("%Y-%m")
    
    additions = pr.get("additions", 0)
    deletions = pr.get("deletions", 0)
    total_changes = additions + deletions
    
    # Track metrics per PR and which month it belongs to
    weekly_stats[week_key]["days_by_month"][month_key]["count"] += 1
    weekly_stats[week_key]["days_by_month"][month_key]["additions"] += additions
    weekly_stats[week_key]["days_by_month"][month_key]["deletions"] += deletions
    weekly_stats[week_key]["days_by_month"][month_key]["total"] += total_changes

# Calculate per-workday averages and assign to months
workdays_per_week = args.workdays_per_week
monthly_stats = defaultdict(lambda: {"additions": 0, "deletions": 0, "total": 0, "week_fraction": 0})

for week_key, week_data in weekly_stats.items():
    # Split this week's metrics across the months it spans
    for month_key, month_data in week_data["days_by_month"].items():
        days_in_this_month = month_data["count"]
        
        # Calculate what fraction of the week belongs to this month
        week_fraction = days_in_this_month / 7.0
        
        # Assign metrics and week fraction to the month
        monthly_stats[month_key]["additions"] += month_data["additions"]
        monthly_stats[month_key]["deletions"] += month_data["deletions"]
        monthly_stats[month_key]["total"] += month_data["total"]
        monthly_stats[month_key]["week_fraction"] += week_fraction

# Sort by month
sorted_months = sorted(monthly_stats.items())

# Store for potential graphing
monthly_data = []

for month_key, stats in sorted_months:
    # Calculate average per workday
    # Total workdays in the month = week_fraction * workdays_per_week
    total_workdays = stats["week_fraction"] * workdays_per_week
    
    avg_additions = stats["additions"] / total_workdays if total_workdays > 0 else 0
    avg_deletions = stats["deletions"] / total_workdays if total_workdays > 0 else 0
    avg_total = stats["total"] / total_workdays if total_workdays > 0 else 0
    
    # Format month nicely
    month_date = datetime.strptime(month_key, "%Y-%m")
    month_label = month_date.strftime("%b %Y")
    
    monthly_data.append({
        "month": month_key,
        "label": month_label,
        "avg_additions": avg_additions,
        "avg_deletions": avg_deletions,
        "avg_total": avg_total,
        "total_additions": stats["additions"],
        "total_deletions": stats["deletions"],
        "total_changes": stats["total"],
        "week_fraction": stats["week_fraction"]
    })

# Show detailed monthly breakdown if flag is set
if args.detailed:
    print("\n" + "="*110)
    print(f"MONTHLY CODE METRICS ANALYSIS (Average Lines per Workday, {workdays_per_week} workdays/week)")
    print("="*110)
    print(f"\n{'Month':<12} {'Added':<10} {'Deleted':<10} {'Total':<10} {'Weeks':<8} {'Avg Added':<12} {'Avg Deleted':<12} {'Avg Total':<12}")
    print("-"*110)
    
    for month_data_item in monthly_data:
        month_key = month_data_item["month"]
        stats = monthly_stats[month_key]
        print(f"{month_data_item['label']:<12} "
              f"{stats['additions']:<10} "
              f"{stats['deletions']:<10} "
              f"{stats['total']:<10} "
              f"{stats['week_fraction']:<8.2f} "
              f"{month_data_item['avg_additions']:>11.1f} "
              f"{month_data_item['avg_deletions']:>11.1f} "
              f"{month_data_item['avg_total']:>11.1f}")
    
    print()

# Summary statistics
print("\n" + "="*90)
print("SUMMARY STATISTICS")
print("="*90 + "\n")

active_months = [m for m in monthly_data if m["avg_total"] > 0]
if active_months:
    total_additions = sum(m["total_additions"] for m in monthly_data)
    total_deletions = sum(m["total_deletions"] for m in monthly_data)
    total_changes = sum(m["total_changes"] for m in monthly_data)
    
    overall_avg_additions = sum(m["avg_additions"] for m in active_months) / len(active_months)
    overall_avg_deletions = sum(m["avg_deletions"] for m in active_months) / len(active_months)
    overall_avg_total = sum(m["avg_total"] for m in active_months) / len(active_months)
    
    max_additions_month = max(monthly_data, key=lambda x: x["avg_additions"])
    max_deletions_month = max(monthly_data, key=lambda x: x["avg_deletions"])
    max_total_month = max(monthly_data, key=lambda x: x["avg_total"])
    
    print(f"Total lines added (all time):       {total_additions:,}")
    print(f"Total lines deleted (all time):     {total_deletions:,}")
    print(f"Total changes (all time):           {total_changes:,}")
    print()
    print(f"Active months analyzed:             {len(active_months)}")
    print(f"Overall average additions/workday:  {overall_avg_additions:.1f} lines")
    print(f"Overall average deletions/workday:  {overall_avg_deletions:.1f} lines")
    print(f"Overall average total/workday:      {overall_avg_total:.1f} lines")
    print()
    print(f"Most additions:                     {max_additions_month['label']} ({max_additions_month['avg_additions']:.1f} lines/workday)")
    print(f"Most deletions:                     {max_deletions_month['label']} ({max_deletions_month['avg_deletions']:.1f} lines/workday)")
    print(f"Most total changes:                 {max_total_month['label']} ({max_total_month['avg_total']:.1f} lines/workday)")
    
    # Recent trend (last 12 months)
    recent_months = active_months[-12:] if len(active_months) >= 12 else active_months
    recent_avg_additions = sum(m["avg_additions"] for m in recent_months) / len(recent_months) if recent_months else 0
    recent_avg_deletions = sum(m["avg_deletions"] for m in recent_months) / len(recent_months) if recent_months else 0
    recent_avg_total = sum(m["avg_total"] for m in recent_months) / len(recent_months) if recent_months else 0
    
    print(f"\nLast 12 months avg additions:       {recent_avg_additions:.1f} lines/workday")
    print(f"Last 12 months avg deletions:       {recent_avg_deletions:.1f} lines/workday")
    print(f"Last 12 months avg total:           {recent_avg_total:.1f} lines/workday")

# Create visual graphs using plotext
if active_months:
    # Prepare data for plotting
    labels = [m["label"] for m in active_months]
    additions = [m["avg_additions"] for m in active_months]
    deletions = [m["avg_deletions"] for m in active_months]
    totals = [m["avg_total"] for m in active_months]
    
    # Convert labels to indices for x-axis
    x_indices = list(range(len(labels)))
    
    # Create the main plot - Lines Added
    print("\n" + "="*90)
    print("LINES ADDED PER WORKDAY - VISUAL GRAPH")
    print("="*90 + "\n")
    
    plt.clear_figure()
    plt.plot_size(120, 25)
    plt.title(f"Monthly Code Metrics: Lines Added per Workday ({workdays_per_week} workdays/week)")
    
    plt.plot(x_indices, additions, marker="braille", color="green", label="Lines added")
    
    # Add a trend line
    window_size = 6
    if len(additions) >= window_size:
        moving_avg = []
        for i in range(len(additions)):
            if i < window_size - 1:
                moving_avg.append(sum(additions[:i+1]) / (i+1))
            else:
                moving_avg.append(sum(additions[i-window_size+1:i+1]) / window_size)
        
        plt.plot(x_indices, moving_avg, marker="hd", color="blue", label="6-month trend")
    
    plt.xlabel("Timeline")
    plt.ylabel("Avg Lines Added/Workday")
    
    step = max(1, len(labels) // 20)
    x_labels_to_show = [labels[i] if i % step == 0 else "" for i in range(len(labels))]
    plt.xticks(x_indices, x_labels_to_show)
    
    plt.grid(True, True)
    plt.show()
    
    # Create the second plot - Lines Deleted
    print("\n" + "="*90)
    print("LINES DELETED PER WORKDAY - VISUAL GRAPH")
    print("="*90 + "\n")
    
    plt.clear_figure()
    plt.plot_size(120, 25)
    plt.title(f"Monthly Code Metrics: Lines Deleted per Workday ({workdays_per_week} workdays/week)")
    
    plt.plot(x_indices, deletions, marker="braille", color="red", label="Lines deleted")
    
    if len(deletions) >= window_size:
        moving_avg = []
        for i in range(len(deletions)):
            if i < window_size - 1:
                moving_avg.append(sum(deletions[:i+1]) / (i+1))
            else:
                moving_avg.append(sum(deletions[i-window_size+1:i+1]) / window_size)
        
        plt.plot(x_indices, moving_avg, marker="hd", color="magenta", label="6-month trend")
    
    plt.xlabel("Timeline")
    plt.ylabel("Avg Lines Deleted/Workday")
    
    plt.xticks(x_indices, x_labels_to_show)
    plt.grid(True, True)
    plt.show()
    
    # Create the third plot - Total Changes
    print("\n" + "="*90)
    print("TOTAL CHANGES PER WORKDAY - VISUAL GRAPH")
    print("="*90 + "\n")
    
    plt.clear_figure()
    plt.plot_size(120, 25)
    plt.title(f"Monthly Code Metrics: Total Changes per Workday ({workdays_per_week} workdays/week)")
    
    plt.plot(x_indices, totals, marker="braille", color="cyan", label="Total changes")
    
    if len(totals) >= window_size:
        moving_avg = []
        for i in range(len(totals)):
            if i < window_size - 1:
                moving_avg.append(sum(totals[:i+1]) / (i+1))
            else:
                moving_avg.append(sum(totals[i-window_size+1:i+1]) / window_size)
        
        plt.plot(x_indices, moving_avg, marker="hd", color="yellow", label="6-month trend")
    
    plt.xlabel("Timeline")
    plt.ylabel("Avg Total Changes/Workday")
    
    plt.xticks(x_indices, x_labels_to_show)
    plt.grid(True, True)
    plt.show()
    
    # Create a combined plot
    print("\n" + "="*90)
    print("COMBINED CODE METRICS - VISUAL GRAPH")
    print("="*90 + "\n")
    
    plt.clear_figure()
    plt.plot_size(120, 30)
    plt.title(f"Monthly Code Metrics: All Metrics per Workday ({workdays_per_week} workdays/week)")
    
    plt.plot(x_indices, additions, marker="braille", color="green", label="Lines added")
    plt.plot(x_indices, deletions, marker="braille", color="red", label="Lines deleted")
    plt.plot(x_indices, totals, marker="braille", color="cyan", label="Total changes")
    
    plt.xlabel("Timeline")
    plt.ylabel("Avg Lines/Workday")
    
    plt.xticks(x_indices, x_labels_to_show)
    plt.grid(True, True)
    plt.show()
    
    print("\n" + "="*90)
    print(f"Note: Averages calculated per {workdays_per_week} workdays/week")
    print("This normalizes for weekends and provides consistent per-workday metrics")
    print("="*90 + "\n")
else:
    print("No active months to display.")
    print()

# Export data for potential plotting
print("Exporting data for plotting...")

export_data = {
    "user": args.user,
    "generated": datetime.now().isoformat(),
    "workdays_per_week": workdays_per_week,
    "total_prs": len(all_prs),
    "monthly_data": [
        {
            "month": m["month"],
            "label": m["label"],
            "avg_additions_per_workday": m["avg_additions"],
            "avg_deletions_per_workday": m["avg_deletions"],
            "avg_total_per_workday": m["avg_total"],
            "total_additions": m["total_additions"],
            "total_deletions": m["total_deletions"],
            "total_changes": m["total_changes"],
            "week_fraction": m["week_fraction"]
        }
        for m in monthly_data
    ]
}

with open("monthly_code_metrics_data.json", "w") as f:
    json.dump(export_data, f, indent=2)

print("✓ Data exported to monthly_code_metrics_data.json")
print("  You can use this file to create graphs with matplotlib or other tools!")

