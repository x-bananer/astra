from flask import Blueprint, request
from sqlmodel import Session, select
from db import engine
import jwt

from config import Config

from models.group import Group
from models.user import User
from models.group_member import GroupMember

from services.auth_service import get_user
from services.group_service import get_group


group_bp = Blueprint("groups", __name__)

@group_bp.post("/groups/create")
def create_group():
    data = request.json
    group_name = data.get("name")

    # read astra jwt from cookies
    astra_access_token = request.cookies.get(Config.ACCESS_TOKEN_COOKIE)
    
    # user must be logged in
    if not astra_access_token:
        return {"error": "Unauthenticated"}, 401
    
    # group must have a name
    if not group_name:
        return {"error": "Pass the group name"}, 400

    # decode astra jwt
    try:
        jwt_payload = jwt.decode(astra_access_token, Config.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return {"error": "Unauthenticated"}, 401

    user_id = jwt_payload["user_id"]
    user = get_user(user_id)
    group_id = user.group_id  # user may or may not already have a group
    
    if group_id:
        return {"error": "Group for this user already exists"}, 400

    with Session(engine) as session:
        # create new group
        new_group = Group(name=group_name)
        session.add(new_group)
        session.commit()
        session.refresh(new_group)  # ensure new_group.id is available

        # add creator as first member
        new_member = GroupMember(group_id=new_group.id, user_id=user_id)
        session.add(new_member)

        # update user's group reference
        user.group_id = new_group.id
        session.add(user)

        session.commit()

        # return group info
        return {
            "id": new_group.id,
            "name": new_group.name,
        }

@group_bp.post("/groups/add-member")
def add_member():
    data = request.json
    email = data.get("email")

    astra_access_token = request.cookies.get(Config.ACCESS_TOKEN_COOKIE)
    if not astra_access_token:
        return {"error": "Unauthenticated"}, 401

    # decode jwt
    try:
        jwt_payload = jwt.decode(astra_access_token, Config.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return {"error": "Unauthenticated"}, 401

    requester_id = jwt_payload["user_id"]
    requester = get_user(requester_id)
    requester_group_id = requester.group_id

    if requester_group_id is None:
        return {"error": "You need to be a member of the group to add new members."}, 400

    with Session(engine) as session:
        # find user by email
        invited_user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if not invited_user:
            return {"error": "User not found"}, 404
        
        # check if already in another group
        if invited_user.group_id and invited_user.group_id != requester_group_id:
            return {"error": "User belongs to another group"}, 400

        # check if already in this group
        existing = session.exec(
            select(GroupMember).where(
                GroupMember.group_id == requester_group_id,
                GroupMember.user_id == invited_user.id
            )
        ).first()

        if existing:
            return {"error": "User is already in the group"}, 400

        # add member
        member = GroupMember(
            group_id=requester_group_id,
            user_id=invited_user.id
        )
        session.add(member)

        # update user's active group
        invited_user.group_id = requester_group_id
        session.add(invited_user)

        session.commit()

    return {"status": "OK"}

@group_bp.post("/groups/remove-member")
def remove_member():
    data = request.json
    user_id_to_remove = data.get("user_id")

    astra_access_token = request.cookies.get(Config.ACCESS_TOKEN_COOKIE)
    if not astra_access_token:
        return {"error": "Unauthenticated"}, 401

    try:
        jwt_payload = jwt.decode(astra_access_token, Config.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return {"error": "Unauthenticated"}, 401

    requester_id = jwt_payload["user_id"]
    requester = get_user(requester_id)
    requester_group_id = requester.group_id

    if requester_group_id is None:
        return {"error": "You need to be a member of the group to remove members."}, 400

    with Session(engine) as session:
        # member to remove
        member = session.exec(
            select(GroupMember).where(
                GroupMember.group_id == requester_group_id,
                GroupMember.user_id == user_id_to_remove
            )
        ).first()

        if not member:
            return {"error": "User is not in group"}, 400

        # remove member
        session.delete(member)

        # update user's group_id
        user_to_remove = session.get(User, user_id_to_remove)
        user_to_remove.group_id = None
        session.add(user_to_remove)

        session.commit()

        # check if group is now empty
        remaining_members = session.exec(
            select(GroupMember).where(GroupMember.group_id == requester_group_id)
        ).all()

        if len(remaining_members) == 0:
            # delete group
            group = get_group(requester_group_id)
            session.delete(group)
            session.commit()

        return {"status": "OK"}