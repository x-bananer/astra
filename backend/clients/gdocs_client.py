import requests
from datetime import datetime, timezone

from config import Config

def gdocs_save_get(url, token):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = requests.get(url, headers=headers)

    # rate limit exceeded
    if response.status_code == 403 and "rateLimit" in response.text:
        return {"error": "Google API rate limit exceeded. Please try again later."}, response.status_code

    # any other API error
    if response.status_code >= 400:
        return {"error": "Google API returned an error while fetching data."}, response.status_code

    # parse JSON
    try:
        return response.json()
    except Exception:
        return {"error": "Google API returned an unexpected response. Please try again later."}, 401

def get_gdocs_revisions(doc_id, token):
    # build URL for the list of revisions
    doc_revisions_url = f"{Config.GDRIVE_BASE_API}/files/{doc_id}/revisions"
    
    doc_data = gdocs_save_get(doc_revisions_url, token)
    
    # stop if GitHub returned an error
    if "error" in doc_data:
        return {"error": doc_data["error"]}
    fetched_revisions = doc_data.get("revisions", [])

    revisions = []
    
    for revision in fetched_revisions:
        revisions.append({
            "id": revision.get("id"),
            "modified_time": revision.get("modifiedTime"),
            "last_modifying_user": (revision.get("lastModifyingUser", {}) or {}).get("displayName"),
            "size": revision.get("size")
        })
    return revisions

def build_gdocs_stats(revisions):
    # if there are no revisions at all
    if not revisions:
        return {
            "total_revisions": 0,
            "contributors": {},
            "contributors_count": 0,
            "last_edit": None,
            "inactive_for_days": None,
            "activity_by_day": {},
            "activity_by_hour": {},
        }

    # count edits per contributor
    contributors = {}
    parsed_dates = []

    for revision in revisions:
        user = revision.get("last_modifying_user", "unknown")
        contributors[user] = contributors.get(user, 0) + 1

        # parse revision date
        try:
            date = datetime.fromisoformat(revision["modified_time"].replace("Z", "+00:00"))
            parsed_dates.append(date)
        except Exception:
            pass

    # total number of revisions
    total_revisions = len(revisions)

    # last edit time and inactivity
    last_edit = max(parsed_dates)
    now = datetime.now(timezone.utc)
    inactive_for_days = (now - last_edit).days
    last_edit = last_edit.isoformat()

    # activity by day
    activity_by_day = {}
    for date in parsed_dates:
        day = date.date().isoformat()
        activity_by_day[day] = activity_by_day.get(day, 0) + 1

    # activity by hour
    activity_by_hour = {}
    for date in parsed_dates:
        hour = date.hour
        key = f"{hour:02d}:00–{(hour + 1) % 24:02d}:00"
        activity_by_hour[key] = activity_by_hour.get(key, 0) + 1

    return {
        "total_revisions": total_revisions,
        "contributors": contributors,
        "contributors_count": len(contributors),
        "last_edit": last_edit,
        "inactive_for_days": inactive_for_days,
        "activity_by_day": activity_by_day,
        "activity_by_hour": activity_by_hour,
    }