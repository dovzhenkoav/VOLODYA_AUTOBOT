from aiogram import Dispatcher

from skills.anek import client


def anek_skill_register(dp: Dispatcher):
    client.register_handlers_client(dp)
