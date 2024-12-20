import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from cache import clear_cache_periodically
from handlers import setup
from core import settings
from database import db

class StartTelegramBot:
    def __init__(self):
        token = settings.TOKEN
        default = DefaultBotProperties(parse_mode=ParseMode.HTML)
        self.bot = Bot(token, default=default)
        self.dp = Dispatcher()

    async def run(self):
        await db.connect()
        setup(dispatcher=self.dp)
        asyncio.create_task(clear_cache_periodically())
        await self.dp.start_polling(self.bot)