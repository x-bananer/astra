from trello_client import build_trello_stats
from github_client import build_github_stats, get_github_commits
from gitlab_client import build_gitlab_stats, get_gitlab_commits
from gdocs_client import build_gdocs_stats, get_gdocs_revisions 
from astra_ai import analyze_teamwork

def collect_all_stats(board_id, github_owner, github_repo, github_token, gitlab_owner, gitlab_repo, gitlab_token, gdocs_id, gdocs_token):
    trello = build_trello_stats(board_id)
    
    github_data = get_github_commits(github_owner, github_repo, github_token)
    github = build_github_stats(github_data)
    
    gitlab_data = get_gitlab_commits(gitlab_owner, gitlab_repo, gitlab_token)
    gitlab = build_gitlab_stats(gitlab_data)
    
    revisions = get_gdocs_revisions(gdocs_id, gdocs_token)
    gdocs = build_gdocs_stats(revisions)

    payload = {
        "trello": trello,
        "github": github,
        "gitlab": gitlab,
        "gdocs": gdocs,
    }

    return payload

def run_ai_analysis(payload):
    result = analyze_teamwork(payload)
    return result

def build_full_report(board_id, github_owner, github_repo, github_token, gitlab_owner, gitlab_repo, gitlab_token, gdocs_id, gdocs_token):
    data = collect_all_stats(board_id, github_owner, github_repo, github_token, gitlab_owner, gitlab_repo, gitlab_token, gdocs_id, gdocs_token)
    analysis = run_ai_analysis(data)

    return {
        "data": data,
        "analysis": analysis
    }