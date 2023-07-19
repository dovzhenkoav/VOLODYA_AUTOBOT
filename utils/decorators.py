"""
Common verifications for commands and callbacks.
"""

from aiogram import types

from create_bot import bot
from settings import BOT_ID


def only_group_chat_command(command):
    """Only for group chat command decorator."""
    async def wrapped(message: types.Message):
        if message.from_user.id == message.chat.id:
            await message.answer('Команда предназначена для использования ТОЛЬКО в групповом чате')
        else:
            bot_member = await bot.get_chat_member(message.chat.id, BOT_ID)
            if bot_member.is_chat_admin():
                await command(message)
            else:
                await message.answer('Мне нужны права администратора чата для выполнения команды')
    return wrapped


def only_admin_command(command):
    """Only for group chat command decorator."""
    async def wrapped(message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if not member.is_chat_admin():
            await message.answer('Команда предназначена ТОЛЬКО для админов чата')
        else:
            await command(message)
    return wrapped


def only_admin_callback(command):
    """Only for group chat command decorator."""
    async def wrapped(callback: types.CallbackQuery):
        member = await bot.get_chat_member(callback.message.chat.id, callback.from_user.id)
        if not member.is_chat_admin():
            await callback.answer('Только админ может нажать эту кнопку')
        else:
            await command(callback)
    return wrapped










