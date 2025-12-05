from flask import request, Blueprint, jsonify, redirect
from sqlmodel import Session, select
from db import engine
import requests
import datetime
import jwt

from config import Config

from models.group_client import GroupClient

from services.auth_service import get_user


client_bp = Blueprint("client", __name__)

# GitHub integration (login and adding a repository)
@client_bp.get("/auth/github/login")
def github_login():
    repo = request.args.get("repo")  # repo passed from frontend (owner/repo)

    if not repo:
        return {"error": "Pass the owner and name of the repository"}, 400

    # build the github oauth authorize url and pack repo name into state
    redirect_url = (
        Config.GITHUB_OAUTH_URL,
        "?client_id="
        + Config.GITHUB_CLIENT_ID
        + "&redirect_uri="
        + Config.GITHUB_REDIRECT_URI
        + "&scope=repo"
        + "&state="
        + repo,
    )
    return redirect(redirect_url)

@client_bp.get("/auth/github/callback")
def github_callback():
    code = request.args.get("code")  # github oauth code
    repo = request.args.get("state")  # repo name returned back unchanged

    if not code:
        return {"error": "GitHub authorization failed"}, 400

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

    # decode astra jwt to identify which user (and group) is connecting github
    astra_access_token = request.cookies.get(Config.ACCESS_TOKEN_COOKIE)

    if not astra_access_token:
        return {"error": "Unauthenticated"}, 401

    try:
        jwt_payload = jwt.decode(astra_access_token, Config.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return {"error": "Unauthenticated"}, 401

    user_id = jwt_payload["user_id"]
    user = get_user(user_id)
    group_id = user.group_id

    with Session(engine) as session:
        # find existing GitHub client for this group (there can be only one)
        existing_client = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == group_id,
                GroupClient.provider == "github"
            )
        ).first()

        # remove old GitHub client if it exists
        if existing_client:
            session.delete(existing_client)

        # create fresh GitHub client for this group
        new_client = GroupClient(
            group_id=group_id,
            provider="github",
            access_token=github_access_token,
            resource_ref=repo,
            created_at=datetime.datetime.utcnow(),
        )
        session.add(new_client)
        session.commit()

    # return user to frontend after successful integration
    return redirect(Config.BASE_CLIENT_URL)


# GitLab integration (login and adding a repository)
@client_bp.get("/auth/gitlab/login")
def gitlab_login():
    repo = request.args.get("repo") # repo passed from frontend (owner/repo)

    if not repo:
        return {"error": "Pass the owner and name of the repository"}, 400

    redirect_url = (
        Config.GITLAB_OAUTH_URL,
        f"?client_id={Config.GITLAB_CLIENT_ID}"
        f"&redirect_uri={Config.GITLAB_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=read_api+read_user"
        f"&state={repo}"
    )
    return redirect(redirect_url)

@client_bp.get("/auth/gitlab/callback")
def gitlab_callback():
    code = request.args.get("code") # GitLab oauth code
    repo = request.args.get("state") # repo name returned back unchanged

    if not code:
        return {"error": "GitLab authorization failed"}, 400

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

    # decode astra jwt to identify which user (and group) is connecting github
    astra_access_token = request.cookies.get(Config.ACCESS_TOKEN_COOKIE)

    if not astra_access_token:
        return {"error": "Unauthenticated"}, 401

    try:
        jwt_payload = jwt.decode(astra_access_token, Config.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return {"error": "Unauthenticated"}, 401

    user_id = jwt_payload["user_id"]
    user = get_user(user_id)
    group_id = user.group_id

    with Session(engine) as session:
        # find existing GitLab client for this group (there can be only one)
        existing_client = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == group_id,
                GroupClient.provider == "gitlab"
            )
        ).first()

        # remove old GitLab client if it exists
        if existing_client:
            session.delete(existing_client)

        # create fresh GitLab client for this group
        new_client = GroupClient(
            group_id=group_id,
            provider="gitlab",
            access_token=gitlab_access_token,
            resource_ref=repo,
            created_at=datetime.datetime.utcnow(),
        )
        session.add(new_client)
        session.commit()

    # return user to frontend after successful integration
    return redirect(Config.BASE_CLIENT_URL)


# Google Docs integration (login and adding a document)
@client_bp.get("/auth/gdocs/login")
def gdocs_login():
    doc_id = request.args.get("doc")
    
    if not doc_id:
        return {"error": "Pass the link to the document"}, 400

    redirect_url = (
        f"{Config.GDOCS_OAUTH_URL}"
        f"?client_id={Config.GDOCS_CLIENT_ID}"
        f"&redirect_uri={Config.GDOCS_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={Config.GDOCS_SCOPE}"
        f"&access_type=offline"
        f"&prompt=consent"
        f"&state={doc_id}"
    )
    return redirect(redirect_url)

@client_bp.get("/auth/gdocs/callback")
def gdocs_callback():
    code = request.args.get("code") # Google Docs oauth code
    doc_id = request.args.get("state") # document id returned back unchanged

    if not code:
        return {"error": "Google authorization failed"}, 400

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

    # decode astra jwt to identify which user (and group) is connecting github
    astra_access_token = request.cookies.get(Config.ACCESS_TOKEN_COOKIE)

    if not astra_access_token:
        return {"error": "Unauthenticated"}, 401

    try:
        jwt_payload = jwt.decode(astra_access_token, Config.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return {"error": "Unauthenticated"}, 401

    user_id = jwt_payload["user_id"]
    user = get_user(user_id)
    group_id = user.group_id

    with Session(engine) as session:
        # find existing GitLab client for this group (there can be only one)
        existing_client = session.exec(
            select(GroupClient).where(
                GroupClient.group_id == group_id,
                GroupClient.provider == "gdocs"
            )
        ).first()
        
        # remove old GitLab client if it exists
        if existing_client:
            session.delete(existing_client)

        # create fresh GitLab client for this group
        new_client = GroupClient(
            group_id=group_id,
            provider="gitlab",
            access_token=gdocs_access_token,
            resource_ref=doc_id,
            created_at=datetime.datetime.utcnow(),
        )
        session.add(new_client)
        session.commit()

    # return user to frontend after successful integration
    return redirect(Config.BASE_CLIENT_URL)
