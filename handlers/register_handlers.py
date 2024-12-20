from aiogram import types, Dispatcher, Bot
from aiogram.filters import Command
from core import settings

# Словарь для хранения соответствия ID сообщений и ID пользователей
user_messages = {}
admin_id = settings.OWNER

async def start_command(message: types.Message):
    await message.reply("Привет! Я бот для связи вас с Erzih. Просто отправь мне сообщение, и ожидайте ответа.")

async def forward_to_admin(message: types.Message, bot: Bot):
    if message.from_user.id != admin_id:
        forwarded_msg = await bot.forward_message(admin_id, message.chat.id, message.message_id)
        # Сохраняем соответствие ID пересланного сообщения и ID отправителя
        user_messages[forwarded_msg.message_id] = message.from_user.id

async def handle_admin_reply(message: types.Message, bot: Bot):
    if message.from_user.id == admin_id and message.reply_to_message:
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

def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command("start"))
    dp.message.register(handle_admin_reply, lambda message: message.from_user.id == admin_id and message.reply_to_message is not None)
    dp.message.register(forward_to_admin)