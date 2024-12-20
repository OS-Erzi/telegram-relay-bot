from aiogram import Dispatcher
from aiogram.filters import Command
from filters import IsAdminFilter

from .start import start_command
from .admin import ban_command, unban_command, clear_command

def setup(dispatcher: Dispatcher):
    dispatcher.message.register(start_command, Command("start"))
    dispatcher.message.register(clear_command, Command("clear"), IsAdminFilter())

    dispatcher.message.register(ban_command, Command("ban"), IsAdminFilter())
    dispatcher.message.register(unban_command, Command("unban"), IsAdminFilter())