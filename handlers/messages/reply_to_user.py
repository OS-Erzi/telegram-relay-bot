from aiogram import types, Bot
from aiogram.types import ContentType
from functools import wraps

from database import db

content_handlers = {}

def content_handler(content_type):
    def decorator(func):
        @wraps(func)
        async def wrapper(bot, user_id, message):
            try:
                await func(bot, user_id, message)
            except Exception as e:
                print(f"Ошибка отправки {content_type}: {e}")
        content_handlers[content_type] = wrapper
        return wrapper
    return decorator

async def get_user_info_by_forwarded_id(forwarded_id: int):
    user = await db.get_info({'messages': forwarded_id})
    return user

async def reply_to_user(message: types.Message, bot: Bot):
    if not message.reply_to_message:
        await message.reply("Пожалуйста, ответьте на сообщение пользователя.")
        return

    forwarded_id = message.reply_to_message.message_id
    user_info = await get_user_info_by_forwarded_id(forwarded_id)
    
    if not user_info:
        await message.reply("Не удалось найти пользователя для ответа.")
        return

    user_id = user_info['_id']
    
    handler = content_handlers.get(message.content_type)
    if handler:
        await handler(bot, user_id, message)
    else:
        await message.reply("Этот тип контента пока не поддерживается для пересылки.")

@content_handler(ContentType.TEXT)
async def send_text(bot, user_id, message):
    await bot.send_message(user_id, message.text)

@content_handler(ContentType.PHOTO)
async def send_photo(bot, user_id, message):
    await bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)

@content_handler(ContentType.VIDEO)
async def send_video(bot, user_id, message):
    await bot.send_video(user_id, message.video.file_id, caption=message.caption)

@content_handler(ContentType.VOICE)
async def send_voice(bot, user_id, message):
    await bot.send_voice(user_id, message.voice.file_id)

@content_handler(ContentType.VIDEO_NOTE)
async def send_video_note(bot, user_id, message):
    await bot.send_video_note(user_id, message.video_note.file_id)

@content_handler(ContentType.STICKER)
async def send_sticker(bot, user_id, message):
    await bot.send_sticker(user_id, message.sticker.file_id)

@content_handler(ContentType.DOCUMENT)
async def send_document(bot, user_id, message):
    await bot.send_document(user_id, message.document.file_id, caption=message.caption)

@content_handler(ContentType.AUDIO)
async def send_audio(bot, user_id, message):
    await bot.send_audio(user_id, message.audio.file_id, caption=message.caption)