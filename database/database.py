from motor.motor_asyncio import AsyncIOMotorClient
from core import settings

class Database:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None
        self.users = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.DBConnect)
        self.db = self.client[settings.DBBase]
        self.users = self.db[settings.DBUsers]
        self.block = self.db[settings.DBBlock]
    
    async def save_message(self, user_id: int, name: str, phone: str, message_id: int):
        """
        Сохраняет информацию о пользователе и его сообщении в базу данных.
        """
        await self.users.update_one(
            {'_id': user_id},
            {
                '$set': {
                    'name': name,
                    'number': phone
                },
                '$push': {
                    'messages': message_id
                }
            },
            upsert=True
        )

    async def get_info(self, _dict: dict):
        return await self.users.find_one(_dict)

    async def clear_card(self, user_id: int):
        return await self.users.delete_one({"_id": user_id})

    async def block_user(self, user_id: int, user_name: str, reason: str = None):
        data = {
            "_id": user_id,
            "user_name": user_name,
            "reason": reason
        }
        return await self.block.insert_one(data)
    
    async def unblock_user(self, user_id):
        return await self.block.delete_one({"_id": user_id})
    
    async def get_block_user(self, user_id):
        return await self.block.find_one({"_id": user_id})
