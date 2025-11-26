#!/usr/bin/env python3
"""
Work Summary Generator

Generates formatted summaries of your GitHub work (PRs and commits) for a given time period.
Perfect for time tracking, status reports, and personal productivity tracking.
"""

import argparse
import json
import os
from collections import defaultdict
from datetime import datetime, timedelta

import requests

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description='Generate a formatted summary of your GitHub work',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''
Examples:
  %(prog)s -u octocat --today
  %(prog)s -u octocat --yesterday
  %(prog)s -u octocat --last-week
  %(prog)s -u octocat --last-month
  %(prog)s -u octocat --start 2025-01-01 --end 2025-01-31
  %(prog)s -u octocat --last-week --format markdown
  %(prog)s -u octocat --today --export summary.json
  
Environment Variables:
  GITHUB_TOKEN    GitHub personal access token (alternative to -t)
    '''
)
parser.add_argument('-u', '--user', type=str, required=True,
                    help='GitHub username to analyze')
parser.add_argument('-t', '--token', type=str, 
                    help='GitHub personal access token (or set GITHUB_TOKEN environment variable)')

# Time period options (mutually exclusive)
period_group = parser.add_mutually_exclusive_group(required=True)
period_group.add_argument('--today', action='store_true',
                          help='Show work done today')
period_group.add_argument('--yesterday', action='store_true',
                          help='Show work done yesterday')
period_group.add_argument('--last-week', action='store_true',
                          help='Show work done in the last 7 days')
period_group.add_argument('--last-month', action='store_true',
                          help='Show work done in the last 30 days')
period_group.add_argument('--this-week', action='store_true',
                          help='Show work done this week (Monday-today)')
period_group.add_argument('--this-month', action='store_true',
                          help='Show work done this month')
period_group.add_argument('--last-year', action='store_true',
                          help='Show work done in the last 365 days')
period_group.add_argument('--custom', action='store_true',
                          help='Use custom date range (requires --start and --end)')

# Custom date range
parser.add_argument('--start', type=str,
                    help='Start date (YYYY-MM-DD) for custom range')
parser.add_argument('--end', type=str,
                    help='End date (YYYY-MM-DD) for custom range')

# Output options
parser.add_argument('--format', type=str, default='text', choices=['text', 'markdown', 'json'],
                    help='Output format (default: text)')
parser.add_argument('--group-by', type=str, default='repo', choices=['repo', 'date', 'none'],
                    help='How to group the results (default: repo)')
parser.add_argument('--export', type=str,
                    help='Export summary to file')
parser.add_argument('--include-stats', action='store_true',
                    help='Include statistics (line counts, PR counts)')

args = parser.parse_args()

# Get token from argument or environment variable
TOKEN = args.token if args.token else os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    print("Error: GitHub token required. Provide via -t/--token or GITHUB_TOKEN environment variable.")
    exit(1)

# Calculate date range based on arguments
# Use timezone-aware datetimes
from datetime import timezone

now = datetime.now(timezone.utc)
today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

if args.today:
    start_date = today_start
    end_date = now
    period_name = "Today"
elif args.yesterday:
    start_date = today_start - timedelta(days=1)
    end_date = today_start
    period_name = "Yesterday"
elif args.last_week:
    start_date = now - timedelta(days=7)
    end_date = now
    period_name = "Last 7 Days"
elif args.last_month:
    start_date = now - timedelta(days=30)
    end_date = now
    period_name = "Last 30 Days"
elif args.this_week:
    # Monday of current week
    days_since_monday = now.weekday()
    start_date = today_start - timedelta(days=days_since_monday)
    end_date = now
    period_name = "This Week"
elif args.this_month:
    # First day of current month
    start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date = now
    period_name = "This Month"
elif args.last_year:
    start_date = now - timedelta(days=365)
    end_date = now
    period_name = "Last Year"
elif args.custom:
    if not args.start or not args.end:
        print("Error: --custom requires both --start and --end dates")
        exit(1)
    try:
        start_date = datetime.strptime(args.start, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(args.end, "%Y-%m-%d").replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
        period_name = f"{args.start} to {args.end}"
    except ValueError as e:
        print(f"Error: Invalid date format. Use YYYY-MM-DD. {e}")
        exit(1)

# Query for Pull Requests
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
        number
        url
        createdAt
        mergedAt
        closedAt
        updatedAt
        state
        additions
        deletions
        repository {
          name
          nameWithOwner
          isPrivate
        }
        reviews(first: 5) {
          nodes {
            state
            createdAt
          }
        }
      }
      totalCount
    }
  }
}
"""

print(f"Fetching work summary for {args.user}...")
print(f"Period: {period_name}")
print(f"Date range: {start_date.strftime('%Y-%m-%d %H:%M')} to {end_date.strftime('%Y-%m-%d %H:%M')}\n")

all_prs = []
has_next = True
cursor = None

# Fetch PRs with pagination
while has_next:
    variables = {
        "login": args.user,
        "after": cursor
    }
    
    try:
        resp = requests.post(
            "https://api.github.com/graphql",
            json={"query": pr_query, "variables": variables},
            headers={"Authorization": f"bearer {TOKEN}"},
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        
        if "errors" in data:
            print(f"Error: {data['errors']}")
            break
        
        pr_data = data["data"]["user"]["pullRequests"]
        prs = pr_data["nodes"]
        
        # Filter PRs by date range
        for pr in prs:
            created_at = datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))
            updated_at = datetime.fromisoformat(pr["updatedAt"].replace("Z", "+00:00"))
            
            # Include PR if it was created or updated in the date range
            if (start_date <= created_at <= end_date) or (start_date <= updated_at <= end_date):
                all_prs.append(pr)
            
            # If we've gone past our start date, stop fetching
            if created_at < start_date and updated_at < start_date:
                has_next = False
                break
        
        page_info = pr_data["pageInfo"]
        if not has_next:
            break
        has_next = page_info["hasNextPage"]
        cursor = page_info.get("endCursor")
        
    except Exception as e:
        print(f"Error fetching PRs: {e}")
        break

print(f"Found {len(all_prs)} PRs in this period.\n")

if not all_prs:
    print("No work found for this period.")
    exit(0)

# Group PRs
grouped_prs = defaultdict(list)

if args.group_by == 'repo':
    for pr in all_prs:
        repo_name = pr["repository"]["nameWithOwner"]
        grouped_prs[repo_name].append(pr)
elif args.group_by == 'date':
    for pr in all_prs:
        date = datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00")).strftime("%Y-%m-%d")
        grouped_prs[date].append(pr)
else:
    grouped_prs["all"] = all_prs

# Calculate statistics
total_additions = sum(pr["additions"] for pr in all_prs)
total_deletions = sum(pr["deletions"] for pr in all_prs)
total_changes = total_additions + total_deletions
merged_prs = sum(1 for pr in all_prs if pr["state"] == "MERGED")
open_prs = sum(1 for pr in all_prs if pr["state"] == "OPEN")
closed_prs = sum(1 for pr in all_prs if pr["state"] == "CLOSED")

# Generate output based on format
def generate_text_output():
    output = []
    output.append("=" * 90)
    output.append(f"WORK SUMMARY: {period_name}")
    output.append("=" * 90)
    output.append("")
    
    if args.include_stats:
        output.append("STATISTICS")
        output.append("-" * 90)
        output.append(f"Total PRs:          {len(all_prs)}")
        output.append(f"  Merged:           {merged_prs}")
        output.append(f"  Open:             {open_prs}")
        output.append(f"  Closed:           {closed_prs}")
        output.append(f"Lines added:        {total_additions:,}")
        output.append(f"Lines deleted:      {total_deletions:,}")
        output.append(f"Total changes:      {total_changes:,}")
        output.append("")
    
    output.append("PULL REQUESTS")
    output.append("-" * 90)
    output.append("")
    
    for group_name in sorted(grouped_prs.keys()):
        prs = grouped_prs[group_name]
        
        if args.group_by != 'none':
            output.append(f"### {group_name}")
            output.append("")
        
        for pr in prs:
            status_emoji = {
                "MERGED": "✓",
                "OPEN": "○",
                "CLOSED": "✗"
            }.get(pr["state"], "?")
            
            created = datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))
            date_str = created.strftime("%Y-%m-%d")
            
            output.append(f"{status_emoji} #{pr['number']} - {pr['title']}")
            output.append(f"   Date: {date_str} | +{pr['additions']} -{pr['deletions']} | {pr['state']}")
            output.append(f"   URL: {pr['url']}")
            output.append("")
    
    output.append("=" * 90)
    return "\n".join(output)

def generate_markdown_output():
    output = []
    output.append(f"# Work Summary: {period_name}")
    output.append("")
    output.append(f"**Period:** {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    output.append("")
    
    if args.include_stats:
        output.append("## Statistics")
        output.append("")
        output.append(f"- **Total PRs:** {len(all_prs)}")
        output.append(f"  - Merged: {merged_prs}")
        output.append(f"  - Open: {open_prs}")
        output.append(f"  - Closed: {closed_prs}")
        output.append(f"- **Lines added:** {total_additions:,}")
        output.append(f"- **Lines deleted:** {total_deletions:,}")
        output.append(f"- **Total changes:** {total_changes:,}")
        output.append("")
    
    output.append("## Pull Requests")
    output.append("")
    
    for group_name in sorted(grouped_prs.keys()):
        prs = grouped_prs[group_name]
        
        if args.group_by != 'none':
            output.append(f"### {group_name}")
            output.append("")
        
        for pr in prs:
            status = pr["state"]
            status_badge = {
                "MERGED": "🟢",
                "OPEN": "🔵",
                "CLOSED": "🔴"
            }.get(status, "⚪")
            
            created = datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))
            date_str = created.strftime("%Y-%m-%d")
            
            output.append(f"- {status_badge} **[#{pr['number']}]({pr['url']})** {pr['title']}")
            output.append(f"  - Date: {date_str}")
            output.append(f"  - Changes: +{pr['additions']} -{pr['deletions']}")
            output.append(f"  - Status: {status}")
            output.append("")
    
    return "\n".join(output)

def generate_json_output():
    summary = {
        "user": args.user,
        "period": period_name,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "statistics": {
            "total_prs": len(all_prs),
            "merged": merged_prs,
            "open": open_prs,
            "closed": closed_prs,
            "lines_added": total_additions,
            "lines_deleted": total_deletions,
            "total_changes": total_changes
        },
        "pull_requests": []
    }
    
    for pr in all_prs:
        summary["pull_requests"].append({
            "number": pr["number"],
            "title": pr["title"],
            "url": pr["url"],
            "repository": pr["repository"]["nameWithOwner"],
            "state": pr["state"],
            "created_at": pr["createdAt"],
            "updated_at": pr["updatedAt"],
            "merged_at": pr["mergedAt"],
            "additions": pr["additions"],
            "deletions": pr["deletions"],
            "is_private": pr["repository"]["isPrivate"]
        })
    
    return json.dumps(summary, indent=2)

# Generate output
if args.format == 'text':
    output = generate_text_output()
elif args.format == 'markdown':
    output = generate_markdown_output()
elif args.format == 'json':
    output = generate_json_output()

# Print to console
print(output)

# Export to file if requested
if args.export:
    with open(args.export, 'w') as f:
        f.write(output)
    print(f"\n✓ Summary exported to {args.export}")

