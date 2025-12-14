from flask import Blueprint, request

from services.auth_service import get_user, get_curent_user_id
from services.group_service import create_group, add_member, remove_member, remove_client

group_bp = Blueprint("groups", __name__)

@group_bp.post("/groups/create")
def groups_create():
    data = request.json
    group_name = data.get("name")
    
    # check that group name is provided
    if not group_name:
        return {"error": "Pass the group name"}, 400

    # get current user id
    user_id_response = get_curent_user_id()
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response
    
    # get user data from database
    user = get_user(user_id_response["user_id"])

    # create group for current user
    result, status = create_group(user, group_name)
    return result, status

@group_bp.post("/groups/add-member")
def groups_add_member():
    data = request.json
    email = data.get("email")

    # get current user id
    user_id_response = get_curent_user_id()
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response
    
    # get current user data
    requester = get_user(user_id_response["user_id"])
    
    # add member to cyrrent user group
    result, status = add_member(requester, email)
    return result, status

@group_bp.post("/groups/remove-member")
def groups_remove_member():
    data = request.json
    user_id_to_remove = data.get("user_id")

    # get current user id
    user_id_response = get_curent_user_id()
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response

    # get current user data
    requester = get_user(user_id_response["user_id"])
    
    # remove member from current user group
    result, status = remove_member(requester, user_id_to_remove)
    return result, status

@group_bp.post("/groups/remove-client")
def groups_remove_lient():
    data = request.json
    provider = data.get("provider")

    # get current user id
    user_id_response = get_curent_user_id()
    if "error" in user_id_response or isinstance(user_id_response, tuple):
        return user_id_response

    # get current user data
    requester = get_user(user_id_response["user_id"])

    # remove client intergration from current user group
    result, status = remove_client(requester, provider)
    return result, status
    