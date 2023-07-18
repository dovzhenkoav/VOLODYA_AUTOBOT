from aiogram import types, Dispatcher

from create_bot import bot
from utils.decorators import only_group_chat_command, only_admin_command
from sq_manager import sqlite_db
from skills.queue.keyboards import admin_kb
from skills.queue.client import command_queue_show


@only_group_chat_command
@only_admin_command
async def command_queue_create(message: types.Message):
    queue_is_in_db = await sqlite_db.queue_is_in_db(message)
    if queue_is_in_db:
        await message.answer('Очередь уже существует. Для её удаления используйте "/qd" или "/qe" для изменения')
    else:
        results = await sqlite_db.known_users_in_chat(message)
        if not results:
            users = ''
        else:
            users = ''
            for user in results:
                users += f'{user[0]}\n'
        await message.answer(text=f"Для добавления пользователей в очередь они должны быть в списке\n\nДобавленные пользователи:\n ---\n{users}",
                               reply_markup=admin_kb.inline_add_members_kb)


@only_group_chat_command
@only_admin_command
async def command_queue_delete(message: types.Message):
    queue_is_in_db = await sqlite_db.queue_is_in_db(message)
    if queue_is_in_db:
        await sqlite_db.delete_queue(message)
        await message.answer('Очередь удалена')
    else:
        await message.answer('Нечего удалять. Очереди не существует')


@only_group_chat_command
@only_admin_command
async def command_queue_edit(message: types.Message):
    queue_is_in_db = await sqlite_db.queue_is_in_db(message)
    if not queue_is_in_db:
        await message.answer('Нечего редактировать. Очереди не существует')
    else:
        await command_queue_show(message)
        markup = await admin_kb.inline_qe_commands(message)
        await message.answer('Что необходимо сделать с очередью?', reply_markup=markup)



def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(command_queue_create, commands=['qc'])
    dp.register_message_handler(command_queue_delete, commands=['qd'])
    dp.register_message_handler(command_queue_edit, commands=['qe'])











