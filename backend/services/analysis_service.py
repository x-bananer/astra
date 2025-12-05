from datetime import datetime, timedelta
from sqlmodel import Session, select
from db import engine
import json

from models.analysis_cache import AnalysisCache
from models.group_client import GroupClient
from models.user import User

from clients.clients_hub import collect_clients_data
from engines.llm_engine import generate_team_report
from services.auth_service import get_user

CACHE_EXPIRE_HOURS = 1

def load_cache(session, group_id, start_date):
    # cache entry expires after 1 hour
    CACHE_EXPIRE_HOURS = 1
    
    cached = session.exec(
        select(AnalysisCache).where(
            AnalysisCache.group_id == group_id,
            AnalysisCache.start_date == start_date
        )
    ).one_or_none()

    if not cached:
        return None

    # age check
    age = datetime.utcnow() - cached.created_at
    if age >= timedelta(hours=CACHE_EXPIRE_HOURS):
        return None

    # get current integrations state
    current_state = get_group_integrations_state(session, group_id)

    # get cached state
    cached_state = json.loads(cached.config_json)

    # if integrations changed invalidate cache
    if current_state != cached_state:
        return None

    # valid cache
    return json.loads(cached.result_json)
    
def save_cache(session, group_id, start_date, result):
    current_state = get_group_integrations_state(session, group_id)

    # check if cache already exists for this group + date
    cached_analysis = session.exec(
        select(AnalysisCache).where(
            AnalysisCache.group_id == group_id,
            AnalysisCache.start_date == start_date
        )
    ).one_or_none()

    # remove old cache entry
    if cached_analysis:
        session.delete(cached_analysis)

    # save new cache entry
    session.add(
        AnalysisCache(
            group_id=group_id,
            start_date=start_date,
            result_json=result,
            config_json=json.dumps(current_state),
            created_at=datetime.utcnow()
        )
    )

    session.commit()

def get_group_integrations_state(session, group_id):
    integrations = session.exec(
        select(GroupClient).where(GroupClient.group_id == group_id)
    ).all()

    result = []

    for item in integrations:
        entry = {
            "provider": item.provider,
            "resource_ref": item.resource_ref,
            "access_token": item.access_token
        }
        result.append(entry)

    result.sort(key=lambda x: x["provider"])

    return result

def get_analysis(user_id, start_date = ""):
    with Session(engine) as session:        
        user = get_user(user_id)
        group_id = user.group_id
        
        # try returning cached result
        cached = load_cache(session, group_id, start_date)
        if cached:
            return cached

        cached_analysis = session.exec(
            select(AnalysisCache).where(
                AnalysisCache.group_id == group_id,
                AnalysisCache.start_date == start_date
            )
        ).one_or_none()

        if cached_analysis:
            cache_age = datetime.utcnow() - cached_analysis.created_at
            if cache_age < timedelta(hours=CACHE_EXPIRE_HOURS):
                return cached_analysis.result_json

        # GitHub data
        github_owner = None
        github_repo = None
        github_token = None
        
        github_data = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == user.group_id,
                GroupClient.provider == "github"
            )
        ).one_or_none()
        
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
        ).one_or_none()

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
        ).one_or_none()
        
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
            
            "start_date": start_date,
        }

        data = collect_clients_data(clients_data_config)
        
        if not any([data["github"], data["gitlab"], data["gdocs"], data["trello"]]):
            return {"error": "No data available for analysis"}, 400
        
        analysis = generate_team_report(data)

        result = {
            "data": data,
            "analysis": analysis
        }

        # save new cache
        current_state = get_group_integrations_state(session, group_id)

        new_cache = AnalysisCache(
            group_id=group_id,
            start_date=start_date,
            result_json=json.dumps(result, ensure_ascii=False),
            config_json=json.dumps(current_state, ensure_ascii=False),
            created_at=datetime.utcnow()
        )

        # remove old record
        if cached_analysis:
            session.delete(cached_analysis)

        session.add(new_cache)
        session.commit()

        return result
