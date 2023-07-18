from aiogram import types, Dispatcher

from create_bot import bot


async def command_start(message: types.Message):
    """Greetings handler. Just to say hi and inform about /help."""
    await bot.send_message(message.chat.id, 'Привет!')
    await bot.send_message(message.chat.id, 'Если понадобится помощь: /help')
    await message.delete()


async def command_help(message: types.Message):
    """It says to people that bot has skills system.
    Each skill has separate /help_[skill_name] command"""
    await message.answer('Бот имеет систему скиллов.\n'
                         'Для каждого скилла написана отдельная помощь.\n\n'
                         'Помощь по отдельным скиллам:\n'
                         '/help_anek - система анекдотов;\n'
                         '/help_queue - система менеджмента очереди в групповом чате;\n')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])