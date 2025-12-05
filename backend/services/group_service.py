from sqlmodel import Session, select

from db import engine

from models.user import User
from models.group import Group
from models.group_member import GroupMember
from models.group_client import GroupClient

def get_group(group_id):
    with Session(engine) as session:
        group = session.get(Group, group_id)
        
        # Group users     
        group_users = []
         
        members = session.exec(
            select(GroupMember).where(GroupMember.group_id == group.id)
        ).all()

        for member in members:
            group_user = session.get(User, member.user_id)
            if group_user:
                group_users.append({
                    "id": group_user.id,
                    "email": group_user.email,
                    "name": group_user.name,
                    "avatar": group_user.avatar
                })

        # Group clients
        group_clients = []

        clients = session.exec(
            select(GroupClient).where(GroupClient.group_id == group.id)
        ).all()

        for client in clients:
            group_clients.append({
                "id": client.id,
                "provider": client.provider,
                "resource_ref": client.resource_ref
            })

        # Group final data
        group_data = {
            "id": group.id,
            "name": group.name,
            "members": group_users,
            "integrations": group_clients
        }
        
        return group_data
    
    
def create_group(user, group_name):
    if user.group_id:
        return {"error": "Group for this user already exists"}, 400

    with Session(engine) as session:
        # create new group
        new_group = Group(name=group_name)
        session.add(new_group)
        session.commit()
        session.refresh(new_group)  # ensure new_group.id is available

        # add creator as first member
        new_member = GroupMember(group_id=new_group.id, user_id=user.id)
        session.add(new_member)

        # update user's group reference
        user.group_id = new_group.id
        session.add(user)

        session.commit()

        # return group info
        return {
            "id": new_group.id,
            "name": new_group.name,
        }, 200

def add_member(requester, email):
    if requester.group_id is None:
        return {"error": "You need to be a member of the group to add new members."}, 400

    with Session(engine) as session:
        # find user by email
        invited = session.exec(
            select(User).where(User.email == email)
        ).first()
        if not invited:
            return {"error": "User not found"}, 404
        
        # check if already in another group
        if invited.group_id and invited.group_id != requester.group_id:
            return {"error": "User belongs to another group"}, 400
        
        # check if already in this group
        existing = session.exec(
            select(GroupMember).where(
                GroupMember.group_id == requester.group_id,
                GroupMember.user_id == invited.id
            )
        ).first()
        if existing:
            return {"error": "User is already in the group"}, 400
       
        # add member
        member = GroupMember(
            group_id=requester.group_id,
            user_id=invited.id
        )
        session.add(member)
        
        # update user's active group
        invited.group_id = requester.group_id
        session.add(invited)
        session.commit()
        
    return {"status": "OK"}, 200
    
def remove_member(requester, user_id_to_remove):
    if requester.group_id is None:
        return {"error": "You need to be a member of the group to remove members."}, 400

    with Session(engine) as session:
        # member to remove
        member = session.exec(
            select(GroupMember).where(
                GroupMember.group_id == requester.group_id,
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
            select(GroupMember).where(GroupMember.group_id == requester.group_id)
        ).all()

        if len(remaining_members) == 0:
            # delete group
            group = get_group(requester.group_id)
            session.delete(group)
            session.commit()

    return {"status": "OK"}, 200