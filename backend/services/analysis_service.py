from sqlmodel import Session, select
from db import engine

from models.group_client import GroupClient
from models.user import User

from clients.clients_hub import collect_clients_data
from engines.llm_engine import generate_team_report

def get_analysis(user_id):
    with Session(engine) as session:
        user = session.get(User, user_id)

        # GitHub data
        github_owner = None
        github_repo = None
        github_token = None
        
        github_data = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == user.group_id,
                GroupClient.provider == "github"
            )
        ).one()
        
        if github_data is not None:
            github_owner, github_repo = github_data.resource_ref.split("/")
            github_token = github_data.access_token
            
            
        # GitLab data
        gitlab_owner = None
        gitlab_repo = None
        gitlab_token = None
        
        gitlab_data = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == user.group_id,
                GroupClient.provider == "gitlab"
            )
        ).one()

        if gitlab_data is not None:
            gitlab_owner, gitlab_repo = gitlab_data.resource_ref.split("/")
            gitlab_token = gitlab_data.access_token
            
            
        # Google Docs data
        gdocs_doc_id = None
        gdocs_token = None
        
        gdocs_data = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == user.group_id,
                GroupClient.provider == "gdocs"
            )
        ).one()
        
        if gdocs_data is not None:
            gdocs_doc_id = gdocs_data.resource_ref
            gdocs_token = gdocs_data.access_token
            
        # TODO Trello board_id = ""
        
        clients_data_config = {
            # TODO Trello "board_id": board_id,
            "github_owner": github_owner,
            "github_repo": github_repo,
            "github_token": github_token,
            "gitlab_owner": gitlab_owner,
            "gitlab_repo": gitlab_repo,
            "gitlab_token": gitlab_token,
            "gdocs_id": gdocs_doc_id,
            "gdocs_token": gdocs_token,
        }

        data = collect_clients_data(clients_data_config)
        analysis = generate_team_report(data)

        return {
            "data": data,
            "analysis": analysis
        }
