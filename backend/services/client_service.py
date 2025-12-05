from sqlmodel import Session, select
from db import engine
import requests
import datetime

from config import Config

from models.group_client import GroupClient

def github_connect(code, repo, user):
    # exchange code for access_token
    token_response = requests.post(
        Config.GITHUB_TOKEN_URL,
        headers={"Accept": "application/json"},
        data={
            "client_id": Config.GITHUB_CLIENT_ID,
            "client_secret": Config.GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": Config.GITHUB_REDIRECT_URI,
        },
    ).json()

    github_access_token = token_response.get("access_token")
    if not github_access_token:
        return {"error": "GitHub authorization failed"}, 400

    with Session(engine) as session:
        # find existing GitHub client for this group (there can be only one)
        existing_client = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == user.group_id,
                GroupClient.provider == "github"
            )
        ).first()

        # remove old GitHub client if it exists
        if existing_client:
            session.delete(existing_client)

        # create fresh GitHub client for this group
        new_client = GroupClient(
            group_id=user.group_id,
            provider="github",
            access_token=github_access_token,
            resource_ref=repo,
            created_at=datetime.datetime.utcnow(),
        )
        session.add(new_client)
        session.commit()
        
    return {
        "status": "OK"
    }

def gitlab_connect(code, repo, user):
     # exchange code for access_token
    token_response = requests.post(
        Config.GITLAB_TOKEN_URL,
        headers={"Accept": "application/json"},
        data={
            "client_id": Config.GITLAB_CLIENT_ID,
            "client_secret": Config.GITLAB_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": Config.GITLAB_REDIRECT_URI,
        },
    ).json()

    gitlab_access_token = token_response.get("access_token")
    if not gitlab_access_token:
        return {"error": "GitLab authorization failed"}, 400

    with Session(engine) as session:
        # find existing GitLab client for this group (there can be only one)
        existing_client = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == user.group_id,
                GroupClient.provider == "gitlab"
            )
        ).first()

        # remove old GitLab client if it exists
        if existing_client:
            session.delete(existing_client)

        # create fresh GitLab client for this group
        new_client = GroupClient(
            group_id=user.group_id,
            provider="gitlab",
            access_token=gitlab_access_token,
            resource_ref=repo,
            created_at=datetime.datetime.utcnow(),
        )
        session.add(new_client)
        session.commit()
    
    return {
        "status": "OK"
    }

def gdocs_connect(code, doc_id, user):
    # exchange code for access_token
    token_response = requests.post(
        Config.GDOCS_TOKEN_URL,
        data={
            "client_id": Config.GDOCS_CLIENT_ID,
            "client_secret": Config.GDOCS_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": Config.GDOCS_REDIRECT_URI,
        },
    ).json()

    gdocs_access_token = token_response.get("access_token")
    if not gdocs_access_token:
        return {"error": "Google authorization failed"}, 400

    with Session(engine) as session:
        # find existing GitLab client for this group (there can be only one)
        existing_client = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == user.group_id,
                GroupClient.provider == "gdocs"
            )
        ).first()
        
        # remove old GitLab client if it exists
        if existing_client:
            session.delete(existing_client)

        # create fresh GitLab client for this group
        new_client = GroupClient(
            group_id=user.group_id,
            provider="gitlab",
            access_token=gdocs_access_token,
            resource_ref=doc_id,
            created_at=datetime.datetime.utcnow(),
        )
        session.add(new_client)
        session.commit()
        
    return {
        "status": "OK"
    }
    