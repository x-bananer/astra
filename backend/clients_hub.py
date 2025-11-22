from trello_client import build_trello_stats
from github_client import build_github_stats, get_github_commits
from astra_ai import analyze_teamwork

def collect_all_stats(board_id, owner, repo):
    trello = build_trello_stats(board_id)
    github_data = get_github_commits(owner, repo)
    github = build_github_stats(github_data)

    payload = {
        "trello": trello,
        "github": github,
    }

    return payload

def run_ai_analysis(payload):
    result = analyze_teamwork(payload)
    return result

def build_full_report(board_id, owner, repo):
    data = collect_all_stats(board_id, owner, repo)
    analysis = run_ai_analysis(data)

    return {
        "data": data,
        "analysis": analysis
    }