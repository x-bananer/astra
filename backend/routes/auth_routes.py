from flask import Blueprint, jsonify, redirect, make_response
from authlib.integrations.flask_client import OAuth

from config import Config

from services.auth_service import get_google_userinfo, resolve_user, create_jwt, get_user, get_curent_user_id
from services.group_service import get_group

# create auth blueprint
auth_bp = Blueprint("auth", __name__)

# create oauth client manager
oauth = OAuth()


 # create google oauth/openid client configuration
google = oauth.register(
    name="google",
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

 # runs once when blueprint is registered to the app
@auth_bp.record
def init_oauth(setup_state):
    app = setup_state.app
    oauth.init_app(app)

@auth_bp.get("/auth/google/login")
def google_login():
    # redirect user to google login page
    return google.authorize_redirect(Config.GOOGLE_REDIRECT_URI)

@auth_bp.get("/auth/google/callback")
def google_callback():
    
    # exchange authorization code for tokens and fetch user info
    userinfo = get_google_userinfo(google)

    email = userinfo["email"]
    name = userinfo.get("name")
    avatar = userinfo.get("picture")

    # find existing user or create a new one
    user = resolve_user(email, name, avatar)
    # create internal jwt for the user
    astra_access_token = create_jwt(user.id)
    
    # create redirect response to frontend
    response = make_response(redirect(Config.BASE_CLIENT_URL))
    # store jwt in http-only cookie
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
    # get current user id from jwt cookie
    user_id_response = get_curent_user_id()
    
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response

    # load user from database
    user = get_user(user_id_response["user_id"])
    user_group_data = None
    if user.group_id:
        user_group_data = get_group(user.group_id)
            
    user_data = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "avatar": user.avatar,
        "group": user_group_data,
        "group_id": user.group_id,
    }

    return {
        "authenticated": True,
        "user": user_data
    }

@auth_bp.post("/auth/logout")
def auth_logout():
    response = make_response(jsonify({"ok": True}))
    # clear auth cookie
    response.set_cookie(
        Config.ACCESS_TOKEN_COOKIE,
        "",
        max_age=0,
        httponly=True,
        samesite="Lax",
        path="/"
    )
    return response