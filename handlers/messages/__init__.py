from aiogram import Dispatcher
from .forward import forward_to_admin
from .reply_to_user import reply_to_user
from core import settings

def setup(*, dispatcher: Dispatcher):
    dispatcher.message.register(
        reply_to_user, 
        lambda message: message.from_user.id == settings.OWNER and message.reply_to_message is not None
    )
    dispatcher.message.register(forward_to_admin)