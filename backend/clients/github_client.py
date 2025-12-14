from datetime import datetime, timedelta
from datetime import timezone
import requests

from config import Config

def github_safe_get(url, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers)

    # rate limit exceeded
    if response.status_code == 403 and "rate limit" in response.text.lower():
        return {"error": "GitHub rate limit exceeded. Please try again later."}

    # any other GitHub API error
    if response.status_code >= 400:
        return {"error": "GitHub returned an error while fetching data."}

    # try parsing response
    try:
        return response.json()
    except Exception:
        return {"error": "GitHub returned an unexpected response. Please try again later."}

def get_github_commits(owner, repo, token, start_date):
    MAX_COMMITS = 300
    MAX_DAYS = 14
    
    # calculate the start date 
    if start_date:
        date_from = datetime.fromisoformat(start_date)
    else:
        date_to = datetime.utcnow()
        date_from = date_to - timedelta(days=MAX_DAYS)

    date_to = date_from + timedelta(days=MAX_DAYS)

    since = date_from.isoformat() + "Z"
    until = date_to.isoformat() + "Z"

    # build URL for the list of recent commits
    repo_commits_url = (
        f"{Config.GITHUB_BASE_API_URL}/repos/{owner}/{repo}/commits"
        f"?since={since}&until={until}&per_page={MAX_COMMITS}"
    )

    # request list of commits
    repo_commits = github_safe_get(repo_commits_url, token)

    # stop if GitHub returned an error
    if "error" in repo_commits:
        return {"error": repo_commits["error"]}

    results = []

    # process each commit from the list
    for commit in repo_commits:
        sha = commit.get("sha")
        if not sha:
            continue  # skip commits without sha, aka without id for detail request

        # fetch detailed commit information
        commit_detail_url = f"{Config.GITHUB_BASE_API_URL}/repos/{owner}/{repo}/commits/{sha}"
        commit_detail = github_safe_get(commit_detail_url, token)

        if "error" in commit_detail:
            continue    
        
        # author and date from the commit metadata + commit stats
        author = commit.get("commit", {}).get("author", {}).get("name")
        date = commit.get("commit", {}).get("author", {}).get("date")
        
        additions = commit_detail.get("stats", {}).get("additions", 0)
        deletions = commit_detail.get("stats", {}).get("deletions", 0)
        total = commit_detail.get("stats", {}).get("total", 0)

        # store normalized commit data
        results.append({
            "sha": sha,
            "author": author,
            "date": date,
            "additions": additions,
            "deletions": deletions,
            "total": total, # total nubmer of lines changed
        })

    # return unified list of commits with stats
    return results

def build_github_stats(commits):
    if not commits:
        return {
            "commits_total": 0,
            "contributors": {},
            "contribution_volume": {},
            "largest_contributor_percentage": 0,
            "inactive_for_days": None,
            "contributors_count": 0,
            "average_commit_size": 0,
            "average_commit_size_by_author": {},
            "largest_commit": None,
            "commits_total": 0,
            "busiest_day": None,
            "active_hours": {},
            "volume_share": {}
        }
        
    # total number of commits
    commits_total = len(commits)

    # list authors and count commits per author
    contributors = {}
    for commit in commits:
        author = commit["author"]
        if author not in contributors:
            contributors[author] = 0
        contributors[author] += 1

    # how many lines each author changed in total
    contribution_volume = {}
    for commit in commits:
        author = commit["author"]
        if author not in contribution_volume:
            contribution_volume[author] = 0
        contribution_volume[author] += commit["total"]

    # share of the most active author
    largest_contributor_percentage = round(max(contributors.values()) / commits_total, 3)

    # parse commit dates so pythin can understand then and count days
    parsed_dates = []
    for commit in commits:
        try:
            date = commit["date"].replace("Z", "+00:00")
            parsed_dates.append(datetime.fromisoformat(date))
        except:
            pass

    # how many days since the last commit
    last_commit = max(parsed_dates)
    now = datetime.now(timezone.utc)
    inactive_for_days = (now - last_commit).days

    # average commit size for the whole repo
    total_lines = 0
    for commit in commits:
        total_lines += commit["total"]
    average_commit_size = round(total_lines / commits_total, 2)

    # average commit size per author
    average_by_author = {}
    for author, volume in contribution_volume.items():
        average_by_author[author] = volume / contributors[author]

    # biggest commit by number of changed lines
    largest_commit = None
    for commit in commits:
        if largest_commit is None:
            largest_commit = commit
        else:
            if commit["total"] > largest_commit["total"]:
                largest_commit = commit

    # which day had the most commits
    days_count = {}
    for date in parsed_dates:
        day = date.date().isoformat()
        if day not in days_count:
            days_count[day] = 0
        days_count[day] += 1

    if days_count:
        busiest_day = max(days_count, key=lambda k: days_count[k])
    else:
        busiest_day = None

    # number of commits in each hour range
    active_hours = {}
    for date in parsed_dates:
        hour = date.hour
        key = f"{hour:02d}:00–{(hour + 1) % 24:02d}:00"
        if key not in active_hours:
            active_hours[key] = 0
        active_hours[key] += 1

    # each author's share of total changed lines
    total_volume = sum(contribution_volume.values())
    volume_share = {}
    for author, volume in contribution_volume.items():
        volume_share[author] = round(volume / total_volume, 3)

    return {
        "commits_total": commits_total,
        "contributors": contributors,
        "contributors_count": len(contributors),
        "contribution_volume": contribution_volume,
        "largest_contributor_percentage": largest_contributor_percentage,
        "inactive_for_days": inactive_for_days,

        "average_commit_size": average_commit_size,
        "average_commit_size_by_author": average_by_author,

        "largest_commit": largest_commit,
        "busiest_day": busiest_day,
        "active_hours": active_hours,
        "volume_share": volume_share,
    }