import asyncio
from core.loader import StartTelegramBot

if __name__ == '__main__':
    bot = StartTelegramBot()
    asyncio.run(bot.run())