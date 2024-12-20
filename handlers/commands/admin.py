from aiogram import types
from filters import IsAdminFilter

from database import db
from core import settings
from cache import whitelist_users, block_cache

async def get_user_info_by_forwarded_id(forwarded_id: int):
    user = await db.get_info({"messages": forwarded_id})
    return user

async def ban_command(message: types.Message):
    if not await IsAdminFilter()(message):
        return

    if not message.reply_to_message:
        return await message.reply("Эта команда должна быть ответом на сообщение пользователя.")

    forwarded_id = message.reply_to_message.message_id
    user_info = await get_user_info_by_forwarded_id(forwarded_id)

    if not user_info:
        await message.reply("Не удалось определить пользователя для блокировки.")
        return

    user_id = user_info["_id"]
    user = await message.bot.get_chat(user_id)
    name = user.full_name

    args = message.text.split()[1:]
    
    if args and args[0]:
        await db.block_user(user_id, name, args[0])
        await message.reply(f"Пользователь {name} заблокирован - {args[0]}")
    else:
        await db.block_user(user_id, name)
        await message.reply(f"Пользователь {name} заблокирован.")

    # Удаляем пользователя из белого списка и обновляем кэш блокировок
    if user_id in whitelist_users:
        whitelist_users.remove(user_id)
    block_cache[user_id] = True

async def unban_command(message: types.Message):
    if not await IsAdminFilter()(message):
        return

    if not message.reply_to_message:
        return await message.reply("Введите команду как ответ на сообщение пользователя.")
    
    forwarded_id = message.reply_to_message.message_id
    user_info = await get_user_info_by_forwarded_id(forwarded_id)

    if not user_info:
        return await message.reply("Не удалось определить пользователя для разблокировки.")

    result = await db.unblock_user(user_info["_id"])
    
    if result.deleted_count > 0:
        await message.reply("Пользователь разблокирован.")
    else:
        await message.reply("Не удалось разблокировать пользователя. Пожалуйста, попробуйте снова.")

    # Добавляем пользователя в белый список и обновляем кэш блокировок
    if len(whitelist_users) < settings.MAX_WHITELIST_SIZE:
        whitelist_users.add(user_info["_id"])
    block_cache[user_info["_id"]] = False

async def clear_command(message: types.Message):
    if not await IsAdminFilter()(message):
        return

    if not message.reply_to_message:
        return await message.reply("Эта команда должна быть ответом на сообщение пользователя.")

    forwarded_id = message.reply_to_message.message_id
    user_info = await get_user_info_by_forwarded_id(forwarded_id)

    if not user_info:
        await message.reply("Не удалось определить пользователя для очистки истории.")
        return
    
    await db.clear_card(user_info['_id'])
    await message.reply(f"Данные базы стёрты.\nИнформация о юзере - {user_info['name']}\nСтёрто - {len(user_info['messages'])} сообщений")
    