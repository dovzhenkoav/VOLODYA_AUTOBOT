from aiogram import types, Dispatcher

from create_bot import bot
from sq_manager import sqlite_db
from utils.decorators import only_group_chat_command


async def command_queue_help(message: types.Message):
    """Queue skill help."""
    help_message_text = """Хелпа по очередям

    Общие команды:
    --------------------
    /q - (queue) передать очередь другому
    /qs - (queue show) показать актуальную очередь

    Админские команды:
    --------------------
    /qc - (queue create) - создать очередь
    /qd - (queue delete) - удалить очередь
    /qe - (queue edit) - редактировать очередь
        """
    await message.answer(help_message_text)
    await message.delete()


@only_group_chat_command
async def command_queue_show(message: types.Message):
    """Shows actual queue in chat."""
    queue_is_in_db = await sqlite_db.queue_is_in_db(message)
    if not queue_is_in_db:
        await message.answer('Очереди в чате не существует')
    else:
        all_members_in_queue = await sqlite_db.get_queue_by_chat(message)
        message_text = "Актуальная очередь:\n"
        for member in all_members_in_queue:
            message_text += f'\n{member[0]}. {member[1]}'
            if member[2] == 1:
                message_text += '🚨🚨🚨'
        await bot.send_message(message.chat.id, text=message_text)


@only_group_chat_command
async def command_queue_next_member(message: types.Message):
    """Calls when member in chat wants to take queue to next member in queue."""
    queue_is_in_db = await sqlite_db.queue_is_in_db(message)
    if not queue_is_in_db:
        await message.answer('Очереди в чате не существует')
    else:
        all_members_in_queue = await sqlite_db.get_queue_by_chat(message)
        len_all_members_in_queue = len(all_members_in_queue)
        for member_in_queue in all_members_in_queue:
            if member_in_queue[2] == 1:
                next_place_in_queue = member_in_queue[0] + 1
                if next_place_in_queue > len_all_members_in_queue:
                    next_place_in_queue -= len_all_members_in_queue
                next_man_in_queue = await sqlite_db.set_next_member_on_problem(message.chat.id, next_place_in_queue)
                await message.answer(f'{member_in_queue[1]} зарегал проблему, далее {next_man_in_queue[0]} @{next_man_in_queue[1]}')
                await message.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_queue_help, commands=['help_queue'])
    dp.register_message_handler(command_queue_show, commands=['qs'])
    dp.register_message_handler(command_queue_next_member, commands=['q'])
