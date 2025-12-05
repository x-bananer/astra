from flask import request
import jwt
import datetime
from sqlmodel import Session, select

from db import engine
from config import Config

from models.user import User

from services.group_service import get_group

def get_google_userinfo(google):
    google.authorize_access_token()
    return google.get(google.server_metadata["userinfo_endpoint"]).json()

def create_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def resolve_user(email, name, avatar):
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email == email)
        ).one()

        if user:
            return user

        user = User(email=email, name=name, avatar=avatar)
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

def get_curent_user_id():
    astra_access_token = request.cookies.get(Config.ACCESS_TOKEN_COOKIE)
    if not astra_access_token:
        return {"error": "Unauthenticated"}, 401

    try:
        jwt_payload = jwt.decode(astra_access_token, Config.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return {"error": "Unauthenticated"}, 401
    
    return {
        "user_id": jwt_payload["user_id"]
    }

def get_user(user_id):    
    with Session(engine) as session:
        user = session.get(User, user_id)
        
        user_group_data = None
        user_data = None
        
        if user.group_id:
            user_group_data = get_group(user.group_id)
            
        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "avatar": user.avatar,
            "group": user_group_data
        }
        
        return user_data
    