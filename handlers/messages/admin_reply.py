from aiogram import types, Bot
from core import settings
from .forward import user_messages

async def handle_admin_reply(message: types.Message, bot: Bot):
    if message.from_user.id == settings.OWNER and message.reply_to_message:
        original_msg_id = message.reply_to_message.message_id
        if original_msg_id in user_messages:
            original_sender = user_messages[original_msg_id]
            try:
                await bot.send_message(original_sender, message.text)
                await message.reply("Сообщение успешно отправлено пользователю.")
            except Exception as e:
                await message.reply(f"Ошибка при отправке сообщения: {e}")
        else:
            await message.reply("Не удалось определить оригинального отправителя.")