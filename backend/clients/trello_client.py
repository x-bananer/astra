# TODO Trello

# import os
# import requests
# from datetime import datetime, timedelta, timezone

# TRELLO_KEY = os.getenv("TRELLO_KEY")
# TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")

# API_BASE = "https://api.trello.com/1"

# def build_trello_stats(board_id):
#     now = datetime.now(timezone.utc)
#     week_ago = now - timedelta(days=7)

#     url = f"{API_BASE}/boards/{board_id}?key={TRELLO_KEY}&token={TRELLO_TOKEN}&actions=all&cards=all"
#     try:
#         resp = requests.get(url, timeout=10)
#         resp.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         return {
#             "error": str(e)
#         }

#     data = resp.json()

#     filtered_actions = []
#     for a in data.get("actions", []):
#         dt = a.get("date")
#         if dt:
#             try:
#                 ts = datetime.fromisoformat(dt.replace("Z", "+00:00"))
#                 if ts >= week_ago:
#                     filtered_actions.append(a)
#             except:
#                 pass

#     cleaned_board = {
#         "id": data.get("id"),
#         "name": data.get("name"),
#         "url": data.get("url"),
#     }

#     cleaned_cards = []
#     for c in data.get("cards", []):
#         cleaned_cards.append({
#             "id": c.get("id"),
#             "name": c.get("name"),
#             "desc": c.get("desc"),
#             "idList": c.get("idList"),
#             "dateLastActivity": c.get("dateLastActivity"),
#             "url": c.get("url"),
#         })

#     cleaned_actions = []
#     for a in filtered_actions:
#         cleaned_actions.append({
#             "id": a.get("id"),
#             "type": a.get("type"),
#             "date": a.get("date"),
#             "idMemberCreator": a.get("idMemberCreator"),
#             "memberCreator": {
#                 "fullName": a.get("memberCreator", {}).get("fullName"),
#                 "username": a.get("memberCreator", {}).get("username")
#             },
#             "data": {
#                 "card": {
#                     "id": a.get("data", {}).get("card", {}).get("id"),
#                     "name": a.get("data", {}).get("card", {}).get("name"),
#                 },
#                 "listBefore": {
#                     "id": a.get("data", {}).get("listBefore", {}).get("id"),
#                     "name": a.get("data", {}).get("listBefore", {}).get("name"),
#                 },
#                 "listAfter": {
#                     "id": a.get("data", {}).get("listAfter", {}).get("id"),
#                     "name": a.get("data", {}).get("listAfter", {}).get("name"),
#                 }
#             }
#         })

#     cleaned_members = {}
#     for a in filtered_actions:
#         mc = a.get("memberCreator", {})
#         mid = mc.get("id")
#         if mid:
#             cleaned_members[mid] = {
#                 "id": mid,
#                 "fullName": mc.get("fullName"),
#                 "username": mc.get("username")
#             }
#     cleaned_members = list(cleaned_members.values())

#     return {
#         "board": cleaned_board,
#         "members": cleaned_members,
#         "cards": cleaned_cards,
#         "actions": cleaned_actions
#     }