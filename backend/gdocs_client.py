import requests
from datetime import datetime, timedelta, timezone

DRIVE_API = "https://www.googleapis.com/drive/v3"
DOCS_API = "https://docs.googleapis.com/v1"

def safe_get(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code >= 400:
        return {"error": f"api_error_{resp.status_code}", "detail": resp.text}
    try:
        return resp.json()
    except Exception:
        return {"error": "invalid_json"}

def get_gdocs_revisions(doc_id, token):
    url = f"{DRIVE_API}/files/{doc_id}/revisions"
    data = safe_get(url, token)
    if isinstance(data, dict) and data.get("error"):
        return data

    revisions = []
    for r in data.get("revisions", []):
        revisions.append({
            "id": r.get("id"),
            "modified_time": r.get("modifiedTime"),
            "last_modifying_user": (r.get("lastModifyingUser", {}) or {}).get("displayName"),
            "size": r.get("size")
        })
    return revisions

def build_gdocs_stats(revisions):
    if isinstance(revisions, dict) and "error" in revisions:
        return {"error": revisions["error"]}

    if not revisions:
        return {
            "total_revisions": 0,
            "contributors": {},
            "contributors_count": 0,
            "last_edit": None,
            "inactive_for_days": None,
            "activity_by_day": {},
            "activity_by_hour": {}
        }

    contributors = {}
    parsed_dates = []
    sizes = []

    for r in revisions:
        user = r.get("last_modifying_user", "unknown")
        contributors[user] = contributors.get(user, 0) + 1
        try:
            parsed_dates.append(datetime.fromisoformat(r["modified_time"].replace("Z", "+00:00")))
        except Exception:
            pass
        sizes.append(r.get("size"))

    total_revisions = len(revisions)
    last_edit = max(parsed_dates)
    now = datetime.now(timezone.utc)
    inactive_for_days = (now - last_edit).days

    activity_by_day = {}
    for d in parsed_dates:
        day = d.date().isoformat()
        activity_by_day[day] = activity_by_day.get(day, 0) + 1

    activity_by_hour = {}
    for d in parsed_dates:
        hour = d.hour
        key = f"{hour:02d}:00–{(hour + 1) % 24:02d}:00"
        activity_by_hour[key] = activity_by_hour.get(key, 0) + 1

    size_deltas = []
    clean_sizes = [s for s in sizes if isinstance(s, int) or (isinstance(s, str) and s.isdigit())]
    clean_sizes = [int(s) for s in clean_sizes]

    if len(clean_sizes) >= 2:
        for i in range(1, len(clean_sizes)):
            size_deltas.append(clean_sizes[i] - clean_sizes[i - 1])

    largest_delta = max(size_deltas) if size_deltas else 0
    average_delta = sum(size_deltas) / len(size_deltas) if size_deltas else 0
    growth_total = (clean_sizes[-1] - clean_sizes[0]) if clean_sizes else 0

    return {
        "total_revisions": total_revisions,
        "contributors": contributors,
        "contributors_count": len(contributors),
        "last_edit": last_edit.isoformat(),
        "inactive_for_days": inactive_for_days,
        "activity_by_day": activity_by_day,
        "activity_by_hour": activity_by_hour,
        "size_deltas": size_deltas,
        "largest_delta": largest_delta,
        "average_delta": average_delta,
        "growth": growth_total
    }