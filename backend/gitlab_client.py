import requests
import urllib.parse
from datetime import datetime, timedelta, timezone

API_BASE = "https://gitlab.metropolia.fi/api/v4"


def safe_get(url, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(url, headers=headers)

    if resp.status_code == 403:
        return {"error": "forbidden", "detail": resp.text}

    if resp.status_code >= 400:
        return {"error": f"api_error_{resp.status_code}", "detail": resp.text}

    try:
        return resp.json()
    except Exception:
        return {"error": "invalid_json"}


def get_gitlab_commits(owner, repo, token):
    MAX_COMMITS = 40
    MAX_DAYS = 300

    since = (datetime.utcnow() - timedelta(days=MAX_DAYS)).isoformat() + "Z"
    encoded = urllib.parse.quote(f"{owner}/{repo}", safe="")

    list_url = (
        f"{API_BASE}/projects/{encoded}/repository/commits"
        f"?since={since}&per_page={MAX_COMMITS}"
    )

    raw = safe_get(list_url, token)
    if isinstance(raw, dict) and raw.get("error"):
        return raw

    if not isinstance(raw, list):
        return {"error": "unexpected_format"}

    commits = []

    # чтобы получить additions/deletions, надо вызывать detail endpoint
    for c in raw[:MAX_COMMITS]:
        commit_id = c.get("id")
        if not commit_id:
            continue

        detail_url = f"{API_BASE}/projects/{encoded}/repository/commits/{commit_id}"
        detail = safe_get(detail_url, token)

        if isinstance(detail, dict) and detail.get("error"):
            continue

        stats = detail.get("stats", {}) or {}

        commits.append({
            "sha": commit_id,
            "author": c.get("author_name"),
            "date": c.get("created_at"),
            "additions": stats.get("additions", 0),
            "deletions": stats.get("deletions", 0),
            "total": stats.get("total", 0)
        })

    return commits


def build_gitlab_stats(commits):
    if isinstance(commits, dict) and "error" in commits:
        return {"error": commits["error"]}

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
            "commits_last_7_days": 0,
            "busiest_day": None,
            "active_hours": {},
            "volume_share": {}
        }

    commits_total = len(commits)

    # contributors count
    contributors = {}
    for c in commits:
        contributors[c["author"]] = contributors.get(c["author"], 0) + 1

    # volume by author
    contribution_volume = {}
    for c in commits:
        contribution_volume[c["author"]] = contribution_volume.get(c["author"], 0) + c["total"]

    # largest share
    largest_contributor_percentage = max(contributors.values()) / commits_total

    # parse dates
    parsed_dates = []
    for c in commits:
        try:
            parsed_dates.append(datetime.fromisoformat(c["date"].replace("Z", "+00:00")))
        except:
            pass

    last_commit = max(parsed_dates)
    now = datetime.now(timezone.utc)
    inactive_for_days = (now - last_commit).days

    # average
    average_commit_size = sum(c["total"] for c in commits) / len(commits)

    average_by_author = {}
    for a, vol in contribution_volume.items():
        average_by_author[a] = vol / contributors[a]

    largest_commit = max(commits, key=lambda c: c["total"])

    # last 7 days
    week_ago = now - timedelta(days=7)
    commits_last_7_days = sum(1 for c in parsed_dates if c > week_ago)

    # busiest day
    days_count = {}
    for d in parsed_dates:
        day = d.date().isoformat()
        days_count[day] = days_count.get(day, 0) + 1

    busiest_day = max(days_count, key=days_count.get) if days_count else None

    # active hours
    active_hours = {}
    for d in parsed_dates:
        hour = d.hour
        key = f"{hour:02d}:00–{(hour + 1) % 24:02d}:00"
        active_hours[key] = active_hours.get(key, 0) + 1

    # volume share %
    total_volume = sum(contribution_volume.values())
    volume_share = {
        a: round(contribution_volume[a] / total_volume, 3)
        for a in contribution_volume
    }

    return {
        "commits_total": commits_total,
        "contributors": contributors,
        "contributors_count": len(contributors),
        "contribution_volume": contribution_volume,
        "largest_contributor_percentage": round(largest_contributor_percentage, 3),
        "inactive_for_days": inactive_for_days,

        "average_commit_size": round(average_commit_size, 2),
        "average_commit_size_by_author": average_by_author,

        "largest_commit": largest_commit,
        "commits_last_7_days": commits_last_7_days,
        "busiest_day": busiest_day,
        "active_hours": active_hours,
        "volume_share": volume_share
    }