from aiogram import Dispatcher

from skills.start_help import client


def start_help_skill_register(dp: Dispatcher):
    client.register_handlers_client(dp)
