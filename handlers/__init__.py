from aiogram import Dispatcher
from handlers import messages, commands

def setup(*, dispatcher: Dispatcher):

    messages.setup(dispatcher=dispatcher)
    commands.setup(dispatcher=dispatcher)

