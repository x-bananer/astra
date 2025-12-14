from sqlmodel import Session, select
from urllib.parse import quote
from db import engine
import requests
import datetime

from config import Config

from models.group_client import GroupClient

from clients.github_client import github_safe_get
from clients.gitlab_client import gitlab_safe_get
from clients.gdocs_client import gdocs_safe_get

# connect a github repo to the current user's group
def github_connect(code, repo, user):
    # exchange code for access_token
    token_response = requests.post(
        Config.GITHUB_TOKEN_URL,
        headers={"Accept": "application/json"},
        data={
            "client_id": Config.GITHUB_CLIENT_ID,
            "client_secret": Config.GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": Config.GITHUB_REDIRECT_URI
        },
    ).json()

    github_access_token = token_response.get("access_token")
    if not github_access_token:
        return {"error": "GitHub authorization failed"}, 400
    
    # check if the repo can be accessed with this token
    check_repo_url = f"{Config.GITHUB_REPO_URL}/{repo}"
    response = github_safe_get(check_repo_url, github_access_token)

    if "error" in response:
        return {"error": "GitHub cannot access this repository. Check owner and repo name."}
    
    with Session(engine) as session:
        # find existing github client for this group to replace it
        existing_client = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == user.group_id,
                GroupClient.provider == "github"
            )
        ).first()

        # remove old github client if it exists to avoid duplicates
        if existing_client:
            session.delete(existing_client)

        # create fresh github client with new token and repo info
        new_client = GroupClient(
            group_id=user.group_id,
            provider="github",
            access_token=github_access_token,
            resource_ref=repo,
            created_at=datetime.datetime.utcnow()
        )
        session.add(new_client)
        session.commit()
        
    return {
        "status": "OK"
    }

# connect a gitlab project to the current user's group
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
            "redirect_uri": Config.GITLAB_REDIRECT_URI
        },
    ).json()

    gitlab_access_token = token_response.get("access_token")
    if not gitlab_access_token:
        return {"error": "GitLab authorization failed"}, 400
    
    # encode repo name and check if accessible with token
    encoded = quote(repo, safe="")
    check_repo_url = f"{Config.GITLAB_BASE_API}/projects/{encoded}"
    response = gitlab_safe_get(check_repo_url, gitlab_access_token)

    if "error" in response:
        return {"error": "GitLab cannot access this repository. Check owner and repo name."}

    with Session(engine) as session:
        # find existing gitlab client for this group to replace it
        existing_client = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == user.group_id,
                GroupClient.provider == "gitlab"
            )
        ).first()

        # remove old gitlab client if it exists to avoid duplicates
        if existing_client:
            session.delete(existing_client)

        # create fresh gitlab client with new token and repo info
        new_client = GroupClient(
            group_id=user.group_id,
            provider="gitlab",
            access_token=gitlab_access_token,
            resource_ref=repo,
            created_at=datetime.datetime.utcnow()
        )
        session.add(new_client)
        session.commit()
    
    return {
        "status": "OK"
    }

# connect a google docs file to the current user's group
def gdocs_connect(code, doc_id, user):
    # exchange code for access_token
    response = requests.post(
        Config.GDOCS_TOKEN_URL,
        data={
            "client_id": Config.GDOCS_CLIENT_ID,
            "client_secret": Config.GDOCS_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": Config.GDOCS_REDIRECT_URI,
        },
    )

    try:
        token_response = response.json()
    except ValueError:
        return {"error": "Google returned an unexpected response while exchanging authorization code."}

    gdocs_access_token = token_response.get("access_token")
    if not gdocs_access_token:
        return {"error": "Google authorization failed"}, 400
    
    # check if the google docs file can be accessed with this token
    check_url = f"{Config.GDRIVE_BASE_API}/files/{doc_id}?fields=id,name"
    response = gdocs_safe_get(check_url, gdocs_access_token)

    if "error" in response:
        return {"error": "Google Docs file cannot be accessed. Check the document ID."}

    with Session(engine) as session:
        # find existing gdocs client for this group to replace it
        existing_client = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == user.group_id,
                GroupClient.provider == "gdocs"
            )
        ).first()
        
        # remove old gdocs client if it exists to avoid duplicates
        if existing_client:
            session.delete(existing_client)

        # create fresh gdocs client with new token and doc info
        new_client = GroupClient(
            group_id=user.group_id,
            provider="gdocs",
            access_token=gdocs_access_token,
            resource_ref=doc_id,
            created_at=datetime.datetime.utcnow(),
        )
        session.add(new_client)
        session.commit()
        
    return {
        "status": "OK"
    }