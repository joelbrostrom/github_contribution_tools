#!/usr/bin/env python3
"""
Monthly Productivity Analysis

Analyzes GitHub contribution productivity by month, filtering out vacation days
and showing only active working days.
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
    description='Analyze GitHub contribution productivity over time',
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
print(f"Analyzing monthly productivity from {account_created_year} to {current_year}...\n")

# Query for contribution calendar
calendar_query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
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

# Collect all contribution data by fetching year by year
all_contributions = []

for year in range(account_created_year, current_year + 1):
    # For the first year, start from account creation date
    if year == account_created_year:
        from_date = account_created.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        from_date = f"{year}-01-01T00:00:00Z"
    
    # For current year, end at today
    if year == current_year:
        to_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        to_date = f"{year}-12-31T23:59:59Z"
    
    variables = {
        "login": args.user,
        "from": from_date,
        "to": to_date
    }
    
    print(f"Fetching {year} data...", end=" ")
    resp = requests.post(
        "https://api.github.com/graphql",
        json={"query": calendar_query, "variables": variables},
        headers={"Authorization": f"bearer {TOKEN}"}
    )
    resp.raise_for_status()
    data = resp.json()
    
    if "errors" in data:
        print(f"Error: {data['errors']}")
        continue
    
    calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    
    # Extract all contribution days
    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            all_contributions.append({
                "date": day["date"],
                "count": day["contributionCount"]
            })
    
    print(f"{calendar['totalContributions']} contributions")

print(f"\nTotal days tracked: {len(all_contributions)}")

# Group by week (ISO week) but track which days belong to which months
weekly_stats = defaultdict(lambda: {"days_by_month": defaultdict(lambda: {"count": 0, "contributions": 0})})

for contrib in all_contributions:
    date = datetime.fromisoformat(contrib["date"])
    # Get ISO week number (year, week_number)
    iso_year, iso_week, _ = date.isocalendar()
    week_key = f"{iso_year}-W{iso_week:02d}"
    month_key = date.strftime("%Y-%m")
    
    # Track contributions per day and which month each day belongs to
    weekly_stats[week_key]["days_by_month"][month_key]["count"] += 1
    weekly_stats[week_key]["days_by_month"][month_key]["contributions"] += contrib["count"]

# Calculate per-workday averages and assign to months
workdays_per_week = args.workdays_per_week
monthly_stats = defaultdict(lambda: {"total": 0, "week_fraction": 0})

for week_key, week_data in weekly_stats.items():
    # Get total days in this week (should be 7 for complete weeks)
    total_days_in_week = sum(m["count"] for m in week_data["days_by_month"].values())
    
    # Split this week's contribution across the months it spans
    for month_key, month_data in week_data["days_by_month"].items():
        days_in_this_month = month_data["count"]
        contributions_in_this_month = month_data["contributions"]
        
        # Calculate what fraction of the week belongs to this month
        week_fraction = days_in_this_month / 7.0
        
        # Assign contributions and week fraction to the month
        monthly_stats[month_key]["total"] += contributions_in_this_month
        monthly_stats[month_key]["week_fraction"] += week_fraction

# Sort by month
sorted_months = sorted(monthly_stats.items())

# Store for potential graphing
monthly_data = []

for month_key, stats in sorted_months:
    # Calculate average per workday
    # Total workdays in the month = week_fraction * workdays_per_week
    total_workdays = stats["week_fraction"] * workdays_per_week
    avg_per_workday = stats["total"] / total_workdays if total_workdays > 0 else 0
    
    # Format month nicely
    month_date = datetime.strptime(month_key, "%Y-%m")
    month_label = month_date.strftime("%b %Y")
    
    monthly_data.append({
        "month": month_key,
        "label": month_label,
        "avg": avg_per_workday,
        "total": stats["total"],
        "week_fraction": stats["week_fraction"]
    })

# Show detailed monthly breakdown if flag is set
if args.detailed:
    print("\n" + "="*90)
    print(f"MONTHLY PRODUCTIVITY ANALYSIS (Average Contributions per Workday, {workdays_per_week} workdays/week)")
    print("="*90)
    print(f"\n{'Month':<12} {'Total':<8} {'Weeks':<8} {'Avg/Workday':<15}")
    print("-"*90)
    
    for month_data_item in monthly_data:
        month_key = month_data_item["month"]
        stats = monthly_stats[month_key]
        print(f"{month_data_item['label']:<12} {stats['total']:<8} {stats['week_fraction']:<8.2f} "
              f"{month_data_item['avg']:>14.2f}")
    
    print()

# Summary statistics
print("\n" + "="*90)
print("SUMMARY STATISTICS")
print("="*90 + "\n")

all_averages = [m["avg"] for m in monthly_data if m["avg"] > 0]
if all_averages:
    overall_avg = sum(all_averages) / len(all_averages)
    max_month = max(monthly_data, key=lambda x: x["avg"])
    min_month = min([m for m in monthly_data if m["avg"] > 0], key=lambda x: x["avg"])
    
    print(f"Total months analyzed:      {len(monthly_data)}")
    print(f"Overall average:            {overall_avg:.2f} contributions/workday")
    print(f"Most productive month:      {max_month['label']} ({max_month['avg']:.2f} avg)")
    print(f"Least productive month:     {min_month['label']} ({min_month['avg']:.2f} avg)")
    
    # Recent trend (last 12 months)
    recent_months = monthly_data[-12:] if len(monthly_data) >= 12 else monthly_data
    recent_avg = sum(m["avg"] for m in recent_months) / len(recent_months) if recent_months else 0
    
    print(f"\nLast 12 months average:     {recent_avg:.2f} contributions/workday")

# Create visual graph using plotext
print("\n" + "="*90)
print("PRODUCTIVITY TREND - VISUAL GRAPH")
print("="*90 + "\n")

# Filter out months with zero average (no activity)
active_months = [m for m in monthly_data if m["avg"] > 0]

if active_months:
    # Prepare data for plotting
    labels = [m["label"] for m in active_months]
    averages = [m["avg"] for m in active_months]
    
    # Convert labels to indices for x-axis
    x_indices = list(range(len(labels)))
    
    # Create the main plot
    plt.clear_figure()
    plt.plot_size(120, 30)
    plt.title(f"Monthly Productivity: Average Contributions per Workday ({workdays_per_week} workdays/week)")
    
    # Plot the line
    plt.plot(x_indices, averages, marker="braille", color="cyan")
    
    # Add a trend line by calculating moving average
    window_size = 6  # 6-month moving average
    if len(averages) >= window_size:
        moving_avg = []
        for i in range(len(averages)):
            if i < window_size - 1:
                moving_avg.append(sum(averages[:i+1]) / (i+1))
            else:
                moving_avg.append(sum(averages[i-window_size+1:i+1]) / window_size)
        
        plt.plot(x_indices, moving_avg, marker="braille", color="green", label="6-month trend")
    
    plt.xlabel("Timeline")
    plt.ylabel("Avg Contributions/Workday")
    
    # Set x-axis labels (show every Nth label to avoid crowding)
    step = max(1, len(labels) // 20)  # Show ~20 labels
    x_labels_to_show = [labels[i] if i % step == 0 else "" for i in range(len(labels))]
    plt.xticks(x_indices, x_labels_to_show)
    
    # Add grid
    plt.grid(True, True)
    
    # Show the plot
    plt.show()
    
    # Print trend statistics
    print("\n" + "="*90)
    
    recent_12 = active_months[-12:] if len(active_months) >= 12 else active_months
    recent_avg = sum(m["avg"] for m in recent_12) / len(recent_12)
    
    older_months = active_months[:-12] if len(active_months) > 12 else []
    older_avg = sum(m["avg"] for m in older_months) / len(older_months) if older_months else 0
    
    if older_avg > 0:
        improvement = ((recent_avg - older_avg) / older_avg) * 100
        print(f"Last 12 months average:         {recent_avg:.2f} contributions/workday")
        print(f"Historical average (before):    {older_avg:.2f} contributions/workday")
        print(f"Improvement:                    {improvement:+.1f}%")
    
    # Recent trend
    if len(active_months) >= 3:
        last_3_avg = sum(m["avg"] for m in active_months[-3:]) / 3
        prev_3_avg = sum(m["avg"] for m in active_months[-6:-3]) / 3 if len(active_months) >= 6 else 0
        
        if prev_3_avg > 0:
            recent_trend = ((last_3_avg - prev_3_avg) / prev_3_avg) * 100
            trend_emoji = "📈" if recent_trend > 0 else "📉" if recent_trend < 0 else "➡️"
            print(f"Recent trend (last 3 months):   {recent_trend:+.1f}% {trend_emoji}")
    
    print("="*90)
    print(f"Note: Averages calculated as weekly total ÷ {workdays_per_week} workdays")
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
    "monthly_data": [
        {
            "month": m["month"],
            "label": m["label"],
            "average_per_workday": m["avg"],
            "total_contributions": m["total"],
            "week_fraction": m["week_fraction"]
        }
        for m in monthly_data
    ]
}

with open("monthly_productivity_data.json", "w") as f:
    json.dump(export_data, f, indent=2)

print("✓ Data exported to monthly_productivity_data.json")
print("  You can use this file to create graphs with matplotlib or other tools!")
