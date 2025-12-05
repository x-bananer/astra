from clients.github_client import build_github_stats, get_github_commits
from clients.gitlab_client import build_gitlab_stats, get_gitlab_commits
from clients.gdocs_client import build_gdocs_stats, get_gdocs_revisions
# TODO Trello from clients.trello_client import build_trello_stats

def collect_clients_data(config):
    # TODO Trello trello = build_trello_stats(config["board_id"])
    trello = None

    github_data = get_github_commits(
        config["github_owner"],
        config["github_repo"],
        config["github_token"]
    )
    github = build_github_stats(github_data)

    gitlab_data = get_gitlab_commits(
        config["gitlab_owner"],
        config["gitlab_repo"],
        config["gitlab_token"]
    )
    gitlab = build_gitlab_stats(gitlab_data)

    gdocs_data = get_gdocs_revisions(
        config["gdocs_id"],
        config["gdocs_token"]
    )
    gdocs = build_gdocs_stats(gdocs_data)

    return {
        "trello": trello,
        "github": github,
        "gitlab": gitlab,
        "gdocs": gdocs,
    }
