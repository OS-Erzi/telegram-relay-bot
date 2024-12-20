from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers import setup
from core import settings

class StartTelegramBot:
    def __init__(self):
        token = settings.TOKEN
        default = DefaultBotProperties(parse_mode=ParseMode.HTML)
        self.bot = Bot(token, default=default)
        self.dp = Dispatcher()

    async def run(self):
        setup(dispatcher=self.dp)
        await self.dp.start_polling(self.bot)