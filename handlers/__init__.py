from aiogram import Dispatcher
from handlers import messages, commands

def setup(*, dispatcher: Dispatcher):
    commands.setup(dispatcher=dispatcher)
    messages.setup(dispatcher=dispatcher)

