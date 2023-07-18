from aiogram import Dispatcher

from skills.queue import client, admin, callbacks


def queue_skill_register(dp: Dispatcher):
    client.register_handlers_client(dp)
    admin.register_handlers_admin(dp)
    callbacks.register_callbacks(dp)
