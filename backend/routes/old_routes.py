
# # Authentication

# oauth = OAuth(app)

# google = oauth.register(
#     name="google",
#     client_id=Config.GOOGLE_CLIENT_ID,
#     client_secret=Config.GOOGLE_CLIENT_SECRET,
#     server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
#     client_kwargs={"scope": "openid email profile"},
# )

# @app.get("/auth/google/login")
# def google_login():
#     return google.authorize_redirect(Config.GOOGLE_REDIRECT_URI)

# @app.get("/auth/google/callback")
# def google_callback():
#     token = google.authorize_access_token()
#     userinfo_url = google.server_metadata["userinfo_endpoint"]
#     resp = google.get(userinfo_url)
#     userinfo = resp.json()

#     email = userinfo["email"]
#     name = userinfo.get("name")
#     avatar = userinfo.get("picture")

#     with Session(engine) as session:
#         result = session.exec(select(User).where(User.email == email))
#         user = result.first()

#         if not user:
#             user = User(email=email, name=name, avatar=avatar)
#             session.add(user)
#             session.commit()
#             session.refresh(user)

#         user_id = user.id

#     payload = {
#         "user_id": user_id,
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
#     }
#     jwt_token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

#     response = make_response(redirect("http://localhost:3000"))
#     response.set_cookie(
#         "astra.access_token",
#         jwt_token,
#         httponly=True,
#         samesite="Lax",
#         max_age=7 * 24 * 60 * 60
#     )
#     return response

# # User detail

# @app.get("/auth/user")
# def auth_user():
#     token = request.cookies.get("astra.access_token")
#     if not token:
#         return jsonify({"authenticated": False}, 401

#     try:
#         payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
#     except jwt.ExpiredSignatureError:
#         return jsonify({"authenticated": False, "error": "expired"}, 401
#     except jwt.InvalidTokenError:
#         return jsonify({"authenticated": False, "error": "invalid"}, 401

#     user_id = payload["user_id"]

#     with Session(engine) as session:
#         user = session.get(User, user_id)
#         if not user:
#             return jsonify({"authenticated": False}), 404

#         group_data = None

#         if user.group_id:
#             g = session.get(Group, user.group_id)

#             if g:
#                 members = session.exec(
#                     select(GroupMember).where(GroupMember.group_id == g.id)
#                 ).all()

#                 member_users = []
#                 for m in members:
#                     u = session.get(User, m.user_id)
#                     if u:
#                         member_users.append({
#                             "id": u.id,
#                             "email": u.email,
#                             "name": u.name,
#                             "avatar": u.avatar
#                         })

#                 integrations = session.exec(
#                     select(GroupClient).where(
#                         GroupClient.group_id == g.id
#                     )
#                 ).all()

#                 integrations_list = []
#                 for it in integrations:
#                     integrations_list.append({
#                         "id": it.id,
#                         "provider": it.provider,
#                         "resource_ref": it.resource_ref,
#                         "created_at": it.created_at.isoformat()
#                     })

#                 group_data = {
#                     "id": g.id,
#                     "name": g.name,
#                     "created_at": g.created_at.isoformat(),
#                     "members": member_users,
#                     "integrations": integrations_list
#                 }

#         return jsonify({
#             "authenticated": True,
#             "user": {
#                 "id": user.id,
#                 "email": user.email,
#                 "name": user.name,
#                 "avatar": user.avatar,
#                 "group": group_data
#             }
#         })
        
# # User Logout
# @app.post("/auth/logout")
# def auth_logout():
#     response = make_response(jsonify({"ok": True}))
#     response.set_cookie(
#         "astra.access_token",
#         "",
#         max_age=0,
#         httponly=True,
#         samesite="Lax",
#         path="/"
#     )
#     return response

# # AI analysis

# # @app.route('/analyze',  methods=["GET", "POST"])
# # def analyze():
# #     owner = "veiston"
# #     repo = "Ufotutkija-Pekka"
# #     board_id = 'Ozbf2TiG'
    
# #     result = build_full_report(board_id, owner, repo)

# #     return jsonify(result)
# @app.get("/analyze")
# def analyze():
#     token = request.cookies.get("astra.access_token")

#     if not token or not isinstance(token, str):
#         return {"error": "unauthenticated"}, 401

#     try:
#         payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
#     except jwt.ExpiredSignatureError:
#         return {"error": "expired"}, 401
#     except jwt.InvalidTokenError:
#         return {"error": "invalid"}, 401

#     user_id = payload["user_id"]

#     with Session(engine) as session:
#         user = session.get(User, user_id)

#         github_token = session.exec(
#             select(GroupClient).where(
#                 GroupClient.group_id == user.group_id,
#                 GroupClient.provider == "github"
#             )
#         ).first()

#         gitlab_token = session.exec(
#             select(GroupClient).where(
#                 GroupClient.group_id == user.group_id,
#                 GroupClient.provider == "gitlab"
#             )
#         ).first()

#         gdocs_token_obj = session.exec(
#             select(GroupClient).where(
#                 GroupClient.group_id == user.group_id,
#                 GroupClient.provider == "gdocs"
#             )
#         ).first()

#         github_owner = github_repo = github_access = None
#         gitlab_owner = gitlab_repo = gitlab_access = None
#         gdocs_id = gdocs_token = None

#         if github_token:
#             github_owner, github_repo = github_token.resource_ref.split("/")
#             github_access = github_token.access_token

#         if gitlab_token:
#             gitlab_owner, gitlab_repo = gitlab_token.resource_ref.split("/")
#             gitlab_access = gitlab_token.access_token

#         if gdocs_token_obj:
#             gdocs_id = gdocs_token_obj.resource_ref
#             gdocs_token = gdocs_token_obj.access_token

#         board_id = ""

#         result = build_full_report(
#             board_id,
#             github_owner, github_repo, github_access,
#             gitlab_owner, gitlab_repo, gitlab_access,
#             gdocs_id, gdocs_token
#         )

#         return jsonify(result)

# # GitHub Repository Access 
