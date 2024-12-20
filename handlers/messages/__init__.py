from aiogram import Dispatcher
from .forward import forward_to_admin
from .admin_reply import handle_admin_reply
from core import settings

def setup(*, dispatcher: Dispatcher):
    dispatcher.message.register(handle_admin_reply, lambda message: message.from_user.id == settings.OWNER and message.reply_to_message is not None)
    dispatcher.message.register(forward_to_admin)