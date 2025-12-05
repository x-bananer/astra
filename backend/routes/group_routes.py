from flask import Blueprint, request

from services.auth_service import get_user, get_curent_user_id
from services.group_service import create_group, add_member, remove_member


group_bp = Blueprint("groups", __name__)

@group_bp.post("/groups/create")
def groups_create():
    data = request.json
    group_name = data.get("name")
    
    # group must have a name
    if not group_name:
        return {"error": "Pass the group name"}, 400

    user_id_response = get_curent_user_id()
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response
    
    user = get_user(user_id_response["user_id"])
    print(user)
    result, status = create_group(user, group_name)
    return result, status

@group_bp.post("/groups/add-member")
def groups_add_member():
    data = request.json
    email = data.get("email")

    user_id_response = get_curent_user_id()
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response
    
    requester = get_user(user_id_response["user_id"])
    
    result, status = add_member(requester, email)
    return result, status

@group_bp.post("/groups/remove-member")
def groups_remove_member():
    data = request.json
    user_id_to_remove = data.get("user_id")

    user_id_response = get_curent_user_id()
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response

    requester = get_user(user_id_response["user_id"])
    
    result, status = remove_member(requester, user_id_to_remove)
    return result, status
    