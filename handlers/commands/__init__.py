from aiogram import Dispatcher
from aiogram.filters import Command

from .start import start_command

def setup(*, dispatcher: Dispatcher):
    dispatcher.message.register(start_command, Command("start"))