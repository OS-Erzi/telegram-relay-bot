from aiogram import types, Bot
from core import settings

# Словарь для хранения соответствия ID сообщений и ID пользователей
user_messages = {}

async def forward_to_admin(message: types.Message, bot: Bot):
    if message.from_user.id != settings.OWNER:
        forwarded_msg = await bot.forward_message(settings.OWNER, message.chat.id, message.message_id)
        # Сохраняем соответствие ID пересланного сообщения и ID отправителя
        user_messages[forwarded_msg.message_id] = message.from_user.id