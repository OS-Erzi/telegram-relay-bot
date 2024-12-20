from aiogram import types

async def start_command(message: types.Message):
    await message.reply("Привет! Я бот для связи вас с Erzih. Просто отправь мне сообщение, и ожидайте ответа.")