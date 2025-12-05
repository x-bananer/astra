from flask import request, Blueprint, redirect

from config import Config

from services.auth_service import get_user, get_curent_user_id
from services.client_service import github_connect, gitlab_connect, gdocs_connect

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
    
    user_id_response = get_curent_user_id()
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response
    
    user = get_user(user_id_response["user_id"])
    
    result = github_connect(code, repo, user)
    
    if "error" in result:
        return result

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
    
    user_id_response = get_curent_user_id()
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response
    
    user = get_user(user_id_response["user_id"])
    
    result = gitlab_connect(code, repo, user)
    
    if "error" in result:
        return result

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
    
    user_id_response = get_curent_user_id()
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response
    
    user = get_user(user_id_response["user_id"])
    
    result = gdocs_connect(code, doc_id, user)
    
    if "error" in result:
        return result

    # return user to frontend after successful integration
    return redirect(Config.BASE_CLIENT_URL)
