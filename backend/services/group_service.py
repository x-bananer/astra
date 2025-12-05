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