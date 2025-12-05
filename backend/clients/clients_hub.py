from clients.github_client import build_github_stats, get_github_commits
from clients.gitlab_client import build_gitlab_stats, get_gitlab_commits
from clients.gdocs_client import build_gdocs_stats, get_gdocs_revisions
# TODO Trello from clients.trello_client import build_trello_stats

def collect_clients_data(config):
    
    trello = None
    # TODO Trello
    # if config["board_id"]:
    #     trello = build_trello_stats(config["board_id"])
    #     pass

    # GitHub
    github = None
    if config["github_token"]:
        github_raw = get_github_commits(
            config["github_owner"],
            config["github_repo"],
            config["github_token"]
        )
        github = build_github_stats(github_raw)

    # GitLab
    gitlab = None
    if config["gitlab_token"]:
        gitlab_raw = get_gitlab_commits(
            config["gitlab_owner"],
            config["gitlab_repo"],
            config["gitlab_token"]
        )
        gitlab = build_gitlab_stats(gitlab_raw) 

    # Google Docs
    gdocs = None
    if config["gdocs_token"]:
        gdocs_raw = get_gdocs_revisions(
            config["gdocs_id"],
            config["gdocs_token"]
        )
        gdocs = build_gdocs_stats(gdocs_raw)

    return {
        "trello": trello,
        "github": github,
        "gitlab": gitlab,
        "gdocs": gdocs,
    }
