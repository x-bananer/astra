from flask import Blueprint, request, jsonify, redirect, make_response
from authlib.integrations.flask_client import OAuth
import jwt

from config import Config

from services.auth_service import get_google_userinfo, resolve_user, create_jwt, get_user, get_curent_user_id


auth_bp = Blueprint("auth", __name__)

oauth = OAuth()
google = oauth.register(
    name="google",
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@auth_bp.record
def init_oauth(setup_state):
    app = setup_state.app
    oauth.init_app(app)

@auth_bp.get("/auth/google/login")
def google_login():
    return google.authorize_redirect(Config.GOOGLE_REDIRECT_URI)

@auth_bp.get("/auth/google/callback")
def google_callback():
    
    userinfo = get_google_userinfo(google)

    email = userinfo["email"]
    name = userinfo.get("name")
    avatar = userinfo.get("picture")

    user = resolve_user(email, name, avatar)
    astra_access_token = create_jwt(user.id)
    
    response = make_response(redirect(Config.BASE_CLIENT_URL))
    response.set_cookie(
        Config.ACCESS_TOKEN_COOKIE,
        astra_access_token,
        httponly=True,
        samesite="Lax",
        max_age=7 * 24 * 60 * 60
    )
    return response

@auth_bp.get("/auth/user")
def auth_user():
    user_id_response = get_curent_user_id()
    
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response

    user = get_user(user_id_response["user_id"])

    return {
        "authenticated": True,
        "user": user
    }

@auth_bp.post("/auth/logout")
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