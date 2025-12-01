from flask import Flask, request, jsonify, make_response, redirect
from flask_cors import CORS
from clients_hub import build_full_report
from authlib.integrations.flask_client import OAuth
from sqlmodel import Session, select
from models.user import User
from config import Config
import jwt
import datetime
from datetime import timedelta
from db import init_db, engine
import requests

from models.group import Group
from models.group_member import GroupMember
from models.group_integration_token import GroupIntegrationToken

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:3000"]
)

init_db()

# Authentication

oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@app.get("/auth/google/login")
def google_login():
    return google.authorize_redirect(Config.GOOGLE_REDIRECT_URI)

@app.get("/auth/google/callback")
def google_callback():
    token = google.authorize_access_token()
    userinfo_url = google.server_metadata["userinfo_endpoint"]
    resp = google.get(userinfo_url)
    userinfo = resp.json()

    email = userinfo["email"]
    name = userinfo.get("name")
    avatar = userinfo.get("picture")

    with Session(engine) as session:
        result = session.exec(select(User).where(User.email == email))
        user = result.first()

        if not user:
            user = User(email=email, name=name, avatar=avatar)
            session.add(user)
            session.commit()
            session.refresh(user)

        user_id = user.id

    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    jwt_token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

    response = make_response(redirect("http://localhost:3000"))
    response.set_cookie(
        "astra.access_token",
        jwt_token,
        httponly=True,
        samesite="Lax",
        max_age=7 * 24 * 60 * 60
    )
    return response

# User detail

@app.get("/auth/user")
@app.get("/auth/user")
def auth_user():
    token = request.cookies.get("astra.access_token")
    if not token:
        return jsonify({"authenticated": False}), 401

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"authenticated": False, "error": "expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"authenticated": False, "error": "invalid"}), 401

    user_id = payload["user_id"]

    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            return jsonify({"authenticated": False}), 404

        group_data = None

        if user.group_id:
            g = session.get(Group, user.group_id)

            if g:
                members = session.exec(
                    select(GroupMember).where(GroupMember.group_id == g.id)
                ).all()

                member_users = []
                for m in members:
                    u = session.get(User, m.user_id)
                    if u:
                        member_users.append({
                            "id": u.id,
                            "email": u.email,
                            "name": u.name,
                            "avatar": u.avatar
                        })

                integrations = session.exec(
                    select(GroupIntegrationToken).where(
                        GroupIntegrationToken.group_id == g.id
                    )
                ).all()

                integrations_list = []
                for it in integrations:
                    integrations_list.append({
                        "id": it.id,
                        "provider": it.provider,
                        "repo_full_name": it.repo_full_name,
                        "created_at": it.created_at.isoformat()
                    })

                group_data = {
                    "id": g.id,
                    "name": g.name,
                    "created_at": g.created_at.isoformat(),
                    "members": member_users,
                    "integrations": integrations_list
                }

        return jsonify({
            "authenticated": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "avatar": user.avatar,
                "group": group_data
            }
        })
        
# User Logout
@app.post("/auth/logout")
def auth_logout():
    response = make_response(jsonify({"ok": True}))
    response.set_cookie(
        "astra.access_token",
        "",
        max_age=0,
        httponly=True,
        samesite="Lax",
        path="/"
    )
    return response

# AI analysis

# @app.route('/analyze',  methods=["GET", "POST"])
# def analyze():
#     owner = "veiston"
#     repo = "Ufotutkija-Pekka"
#     board_id = 'Ozbf2TiG'
    
#     result = build_full_report(board_id, owner, repo)

#     return jsonify(result)
@app.get("/analyze")
def analyze():
    token = request.cookies.get("astra.access_token")

    if not token or not isinstance(token, str):
        return jsonify({"error": "unauthenticated"}), 401

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid"}), 401

    user_id = payload["user_id"]

    with Session(engine) as session:
        user = session.get(User, user_id)

        github_token = session.exec(
            select(GroupIntegrationToken).where(
                GroupIntegrationToken.group_id == user.group_id,
                GroupIntegrationToken.provider == "github"
            )
        ).first()

        gitlab_token = session.exec(
            select(GroupIntegrationToken).where(
                GroupIntegrationToken.group_id == user.group_id,
                GroupIntegrationToken.provider == "gitlab"
            )
        ).first()

        github_owner = github_repo = github_access = None
        gitlab_owner = gitlab_repo = gitlab_access = None

        if github_token:
            github_owner, github_repo = github_token.repo_full_name.split("/")
            github_access = github_token.access_token

        if gitlab_token:
            gitlab_owner, gitlab_repo = gitlab_token.repo_full_name.split("/")
            gitlab_access = gitlab_token.access_token

        # board_id = "Ozbf2TiG"
        board_id = ""

        result = build_full_report(
            board_id,
            github_owner, github_repo, github_access,
            gitlab_owner, gitlab_repo, gitlab_access
        )

        return jsonify(result)


# GitHub Repository Access 

@app.get("/auth/github/login")
def github_login():
    repo = request.args.get("repo", "")
    url = (
        "https://github.com/login/oauth/authorize"
        "?client_id=" + Config.GITHUB_CLIENT_ID +
        "&redirect_uri=" + Config.GITHUB_REDIRECT_URI +
        "&scope=repo" +
        "&state=" + repo
    )
    return redirect(url)

@app.get("/auth/github/callback")
def github_callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "no_code"}), 400

    token_resp = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": Config.GITHUB_CLIENT_ID,
            "client_secret": Config.GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": Config.GITHUB_REDIRECT_URI,
        },
    ).json()

    access_token = token_resp.get("access_token")
    if not access_token:
        return jsonify({"error": "no_token"}), 400

    repos = requests.get(
        "https://api.github.com/user/repos",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    if not isinstance(repos, list) or len(repos) == 0:
        return jsonify({"error": "no_repos_granted"}), 400

    full_name = request.args.get("state")

    token = request.cookies.get("astra.access_token")
    payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    user_id = payload["user_id"]

    with Session(engine) as session:
        user = session.get(User, user_id)
        group_id = user.group_id

        old = session.exec(
            select(GroupIntegrationToken).where(
                GroupIntegrationToken.group_id == group_id,
                GroupIntegrationToken.provider == "github"
            )
        ).all()

        for item in old:
            session.delete(item)

        new_item = GroupIntegrationToken(
            group_id=group_id,
            provider="github",
            access_token=access_token,
            repo_full_name=full_name,
            created_at=datetime.datetime.utcnow()
        )
        session.add(new_item)
        session.commit()

    return redirect("http://localhost:3000")

@app.post("/groups/create")
def create_group():
    data = request.json
    name = data.get("name")

    token = request.cookies.get("astra.access_token")
    if not token:
        return {"error": "unauthenticated"}, 401
    
    if not name:
        return {"error": "name field is required"}, 400

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except:
        return {"error": "invalid_token"}, 401

    user_id = payload["user_id"]

    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            return {"error": "user_not_found"}, 404

        if user.group_id is not None:
            return {"error": "group for this user already exists"}, 400

        g = Group(name=name)
        session.add(g)
        session.commit()
        session.refresh(g)

        m = GroupMember(group_id=g.id, user_id=user_id)
        session.add(m)

        user.group_id = g.id
        session.add(user)

        session.commit()

        return {
            "id": g.id,
            "name": g.name,
            "created_at": g.created_at.isoformat()
        }
        
@app.get("/auth/gitlab/login")
def gitlab_login():
    repo = request.args.get("repo", "")

    url = (
        f"{Config.GITLAB_BASE_URL}/oauth/authorize"
        f"?client_id={Config.GITLAB_CLIENT_ID}"
        f"&redirect_uri={Config.GITLAB_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=read_api+read_user"
        f"&state={repo}"
    )
    return redirect(url)

@app.get("/auth/gitlab/callback")
def gitlab_callback():
    code = request.args.get("code")
    repo_full_name = request.args.get("state")

    if not code:
        return jsonify({"error": "no_code"}), 400

    token_resp = requests.post(
        f"{Config.GITLAB_BASE_URL}/oauth/token",
        data={
            "client_id": Config.GITLAB_CLIENT_ID,
            "client_secret": Config.GITLAB_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": Config.GITLAB_REDIRECT_URI
        }
    ).json()

    access_token = token_resp.get("access_token")
    if not access_token:
        return jsonify({"error": "no_token"}), 400

    token = request.cookies.get("astra.access_token")

    if not token or not isinstance(token, str):
        return jsonify({"error": "no_valid_jwt"}), 400

    payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    user_id = payload["user_id"]

    with Session(engine) as session:
        user = session.get(User, user_id)
        group_id = user.group_id

        old = session.exec(
            select(GroupIntegrationToken).where(
                GroupIntegrationToken.group_id == group_id,
                GroupIntegrationToken.provider == "gitlab"
            )
        ).all()

        for item in old:
            session.delete(item)

        new_item = GroupIntegrationToken(
            group_id=group_id,
            provider="gitlab",
            access_token=access_token,
            repo_full_name=repo_full_name,
            created_at=datetime.datetime.utcnow()
        )
        session.add(new_item)
        session.commit()

    return redirect("http://localhost:3000")


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=4000)