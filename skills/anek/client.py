from aiogram import types, Dispatcher

from create_bot import bot
from skills.anek.anek_utils import get_anek
from sq_manager.sqlite_db import anek_add_user_in_db


async def command_help_anek(message: types.Message):
    """Anek skill help."""
    await message.answer("Скилл анекдотов нужен в развлекательных целях.\n"
                         "По команде /anek бот постит в чат рандомный анекдот с сайта baneks.ru\n"
                         "Команда работает в групповом и личном чате с ботом.")
    await message.delete()


async def command_get_anek(message: types.Message):
    """Get random anek from https://baneks.ru/."""
    anek = await get_anek()
    await anek_add_user_in_db(message)
    await bot.send_message(message.chat.id, anek)
    # await message.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_help_anek, commands=['help_anek'])
    dp.register_message_handler(command_get_anek, commands=['anek'])
