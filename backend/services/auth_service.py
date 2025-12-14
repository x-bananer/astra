from sqlmodel import Session, select
from flask import request
import datetime
import jwt

from config import Config
from db import engine

from models.user import User

# get user data from google
def get_google_userinfo(google):
    # get access token from google
    google.authorize_access_token()
    # return user profile info
    return google.get(google.server_metadata["userinfo_endpoint"]).json()

# create login token
def create_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    # encode user data to the token
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

# get user from database or create new one
def resolve_user(email, name, avatar):
    # open database connection
    with Session(engine) as session:
        # look for user by email
        user = session.exec(
            select(User).where(User.email == email)
        ).one_or_none()

        # if user exists, return it
        if user:
            return user

        user = User(email=email, name=name, avatar=avatar)
        # save new user
        session.add(user)
        session.commit()
        # update user object in the database
        session.refresh(user)

        return user

# get user id from cookie
def get_curent_user_id():
    # read token from cookie
    astra_access_token = request.cookies.get(Config.ACCESS_TOKEN_COOKIE)
    # if no token, user is not logged in
    if not astra_access_token:
        return {"error": "Unauthenticated"}, 401
    
    try:
        # decode user data from the token
        jwt_payload = jwt.decode(astra_access_token, Config.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return {"error": "Unauthenticated"}, 401
    
    return {
        "user_id": jwt_payload["user_id"]
    }

# get user by id
def get_user(user_id):    
    # open database connection
    with Session(engine) as session:
        # returns orm-object from database, ~ kind of a bug
        return session.get(User, user_id)