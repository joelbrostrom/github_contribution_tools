import os
from datetime import datetime

import requests

TOKEN = os.environ["GITHUB_TOKEN"]

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
    json={"query": user_query, "variables": {"login": "joelbrostrom"}},
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

print(f"Account: {user_info['name']} (@joelbrostrom)")
print(f"Member since: {account_created.strftime('%B %d, %Y')}")
print(f"Analyzing {current_year - account_created_year + 1} years of contributions...\n")

# Query for yearly contributions
yearly_query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      totalRepositoryContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""

# Collect data for each year
yearly_data = []

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
        "login": "joelbrostrom",
        "from": from_date,
        "to": to_date
    }
    
    print(f"Fetching {year} contributions...", end=" ")
    resp = requests.post(
        "https://api.github.com/graphql",
        json={"query": yearly_query, "variables": variables},
        headers={"Authorization": f"bearer {TOKEN}"}
    )
    resp.raise_for_status()
    data = resp.json()
    
    if "errors" in data:
        print(f"Error: {data['errors']}")
        continue
    
    collection = data["data"]["user"]["contributionsCollection"]
    
    year_stats = {
        "year": year,
        "total": collection["contributionCalendar"]["totalContributions"],
        "commits": collection["totalCommitContributions"],
        "issues": collection["totalIssueContributions"],
        "prs": collection["totalPullRequestContributions"],
        "reviews": collection["totalPullRequestReviewContributions"],
        "repos": collection["totalRepositoryContributions"],
        "restricted": collection["restrictedContributionsCount"]
    }
    
    yearly_data.append(year_stats)
    print(f"{year_stats['total']} contributions")

print("\n" + "="*80)
print("LIFETIME CONTRIBUTION ANALYSIS")
print("="*80 + "\n")

# Display yearly breakdown
print("Year-by-Year Breakdown:")
print("-" * 90)
print(f"{'Year':<6} {'Total':<8} {'Commits':<8} {'Issues':<8} {'PRs':<8} {'Reviews':<8} {'Repos':<8} {'Private':<8}")
print("-" * 90)

for stats in yearly_data:
    # Calculate what should be the sum
    calculated_sum = (stats['commits'] + stats['issues'] + stats['prs'] + 
                     stats['reviews'] + stats['repos'] + stats['restricted'])
    print(f"{stats['year']:<6} {stats['total']:<8} {stats['commits']:<8} "
          f"{stats['issues']:<8} {stats['prs']:<8} {stats['reviews']:<8} "
          f"{stats['repos']:<8} {stats['restricted']:<8}")

print("-" * 90)

# Calculate totals
total_all = sum(s["total"] for s in yearly_data)
total_commits = sum(s["commits"] for s in yearly_data)
total_issues = sum(s["issues"] for s in yearly_data)
total_prs = sum(s["prs"] for s in yearly_data)
total_reviews = sum(s["reviews"] for s in yearly_data)
total_repos = sum(s["repos"] for s in yearly_data)
total_restricted = sum(s["restricted"] for s in yearly_data)

print(f"{'TOTAL':<6} {total_all:<8} {total_commits:<8} "
      f"{total_issues:<8} {total_prs:<8} {total_reviews:<8} "
      f"{total_repos:<8} {total_restricted:<8}")
print()

# Year-over-year percentage change table
if len(yearly_data) > 1:
    print("\nYear-over-Year Percentage Change:")
    print("-" * 90)
    print(f"{'Year':<6} {'Total':<10} {'Commits':<10} {'Issues':<10} {'PRs':<10} {'Reviews':<10} {'Repos':<10} {'Private':<10}")
    print("-" * 90)
    
    # First year has no previous year, so show "—"
    print(f"{yearly_data[0]['year']:<6} {'—':<10} {'—':<10} {'—':<10} {'—':<10} {'—':<10} {'—':<10} {'—':<10}")
    
    # Calculate and display percentage changes for subsequent years
    for i in range(1, len(yearly_data)):
        prev = yearly_data[i-1]
        curr = yearly_data[i]
        
        def calc_pct(curr_val, prev_val):
            if prev_val == 0:
                return "N/A" if curr_val == 0 else "+∞"
            pct = ((curr_val - prev_val) / prev_val) * 100
            return f"{pct:+.1f}%"
        
        total_pct = calc_pct(curr["total"], prev["total"])
        commits_pct = calc_pct(curr["commits"], prev["commits"])
        issues_pct = calc_pct(curr["issues"], prev["issues"])
        prs_pct = calc_pct(curr["prs"], prev["prs"])
        reviews_pct = calc_pct(curr["reviews"], prev["reviews"])
        repos_pct = calc_pct(curr["repos"], prev["repos"])
        restricted_pct = calc_pct(curr["restricted"], prev["restricted"])
        
        print(f"{curr['year']:<6} {total_pct:<10} {commits_pct:<10} {issues_pct:<10} "
              f"{prs_pct:<10} {reviews_pct:<10} {repos_pct:<10} {restricted_pct:<10}")
    
    print()

# Year-over-year changes
if len(yearly_data) > 1:
    print("\n" + "="*80)
    print("YEAR-OVER-YEAR GROWTH")
    print("="*80 + "\n")
    
    for i in range(1, len(yearly_data)):
        prev = yearly_data[i-1]
        curr = yearly_data[i]
        
        total_change = curr["total"] - prev["total"]
        total_pct = (total_change / prev["total"] * 100) if prev["total"] > 0 else 0
        
        commits_change = curr["commits"] - prev["commits"]
        commits_pct = (commits_change / prev["commits"] * 100) if prev["commits"] > 0 else 0
        
        issues_change = curr["issues"] - prev["issues"]
        issues_pct = (issues_change / prev["issues"] * 100) if prev["issues"] > 0 else 0
        
        prs_change = curr["prs"] - prev["prs"]
        prs_pct = (prs_change / prev["prs"] * 100) if prev["prs"] > 0 else 0
        
        reviews_change = curr["reviews"] - prev["reviews"]
        reviews_pct = (reviews_change / prev["reviews"] * 100) if prev["reviews"] > 0 else 0
        
        print(f"{prev['year']} → {curr['year']}:")
        print(f"  Total Contributions: {prev['total']} → {curr['total']} "
              f"({total_change:+d}, {total_pct:+.1f}%)")
        print(f"  Commits:             {prev['commits']} → {curr['commits']} "
              f"({commits_change:+d}, {commits_pct:+.1f}%)")
        print(f"  Issues:              {prev['issues']} → {curr['issues']} "
              f"({issues_change:+d}, {issues_pct:+.1f}%)")
        print(f"  Pull Requests:       {prev['prs']} → {curr['prs']} "
              f"({prs_change:+d}, {prs_pct:+.1f}%)")
        print(f"  Reviews:             {prev['reviews']} → {curr['reviews']} "
              f"({reviews_change:+d}, {reviews_pct:+.1f}%)")
        print()

# Summary statistics
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80 + "\n")

years_active = len(yearly_data)
avg_per_year = total_all / years_active if years_active > 0 else 0

# Find best and worst years
if yearly_data:
    best_year = max(yearly_data, key=lambda x: x["total"])
    worst_year = min(yearly_data, key=lambda x: x["total"])
    
    print(f"Years active:           {years_active}")
    print(f"Total contributions:    {total_all:,}")
    print(f"Average per year:       {avg_per_year:.0f}")
    print(f"\nMost productive year:   {best_year['year']} ({best_year['total']:,} contributions)")
    print(f"Least productive year:  {worst_year['year']} ({worst_year['total']:,} contributions)")
    
    # Growth trend
    if len(yearly_data) > 1:
        first_year_total = yearly_data[0]["total"]
        last_year_total = yearly_data[-1]["total"]
        overall_growth = last_year_total - first_year_total
        overall_pct = (overall_growth / first_year_total * 100) if first_year_total > 0 else 0
        
        print(f"\nOverall growth:         {yearly_data[0]['year']} to {yearly_data[-1]['year']}")
        print(f"  {first_year_total} → {last_year_total} ({overall_growth:+,}, {overall_pct:+.1f}%)")

print("\n" + "="*80)

