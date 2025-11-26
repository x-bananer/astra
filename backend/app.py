from flask import Flask, request, jsonify, make_response, redirect
from flask_cors import CORS
from clients_hub import build_full_report
from authlib.integrations.flask_client import OAuth
from sqlmodel import Session, select
from models.user import User
from config import Config
import jwt
import datetime
from db import init_db, engine

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

    with Session(engine) as session:
        result = session.exec(select(User).where(User.email == email))
        user = result.first()

        if not user:
            user = User(email=email, name=name)
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

    return jsonify({
        "authenticated": True,
        "id": user.id,
        "email": user.email,
        "name": user.name
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

@app.route('/analyze',  methods=["GET", "POST"])
def analyze():
    owner = "veiston"
    repo = "Ufotutkija-Pekka"
    board_id = 'Ozbf2TiG'
    
    result = build_full_report(board_id, owner, repo)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=4000)
