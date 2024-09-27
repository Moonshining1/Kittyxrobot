from MukeshRobot.modules.no_sql import Mukeshdb

afkdb = Mukeshdb.afk

async def is_afk(user_id: int):
    # Fetch user from NoSQL DB
    user = await afkdb.find_one({"user_id": user_id})
    
    if user:
        return True, user["reason"]  # If user is found, return True with reason
    return False, None  # If user is not found, return False with no reason

async def add_afk(user_id: int, reason: str):
    await afkdb.update_one(
        {"user_id": user_id}, {"$set": {"reason": reason}}, upsert=True
    )

async def remove_afk(user_id: int):
    await afkdb.delete_one({"user_id": user_id})

async def get_afk_users() -> list:
    users = afkdb.find({"user_id": {"$gt": 0}})
    if not users:
        return []
    
    users_list = []
    async for user in users:
        users_list.append(user)
    
    return users_list
