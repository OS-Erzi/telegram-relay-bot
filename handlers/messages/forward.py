import asyncio
from aiogram import types, Bot
from core import settings
from database import db
from cache import whitelist_users, block_cache, clear_cache_periodically

async def forward_to_admin(message: types.Message, bot: Bot):
    user_id = message.from_user.id

    # Создатель пишет в чате с ботом
    if user_id == settings.OWNER:
        return
    
    # Проверка белого списка
    if user_id not in whitelist_users:
        is_blocked = block_cache.get(user_id)
        if is_blocked is None:
            try:
                is_blocked = await db.get_block_user(user_id)
                block_cache[user_id] = is_blocked
            except Exception:
                return

        if is_blocked:
            return

        if len(whitelist_users) < settings.MAX_WHITELIST_SIZE:
            whitelist_users.add(user_id)

    # Если пользователь не игнорируется и не заблокирован, пересылаем сообщение
    try:
        forwarded_msg = await bot.forward_message(settings.OWNER, message.chat.id, message.message_id)
    except Exception:
        return

    name = message.from_user.full_name
    phone = message.contact.phone_number if message.contact else None

    # Сохраняем информацию о сообщении
    try:
        await db.save_message(
            user_id=user_id,
            name=name,
            phone=phone,
            message_id=forwarded_msg.message_id
        )
    except Exception:
        pass