from aiogram import types, Dispatcher

from sq_manager import sqlite_db
from skills.queue.keyboards import admin_kb
from skills.queue.queue_utils import utils
from skills.queue.client import command_queue_show
from create_bot import bot
from utils.decorators import only_admin_callback


async def add_user_in_chat(callback: types.CallbackQuery):
    if str(callback.from_user.full_name) in callback.message.text:
        await callback.answer('Ты уже состоишь в списке')
    else:
        await sqlite_db.add_member_in_chat(callback)
        await callback.message.edit_text(
            f'{callback.message.text}\n{callback.from_user.full_name}\n',
            reply_markup=admin_kb.inline_add_members_kb)
        await callback.answer('Добавлен')


async def done_add_user_in_chat(callback: types.CallbackQuery):
    member = await bot.get_chat_member(callback.message.chat.id, callback.from_user.id)
    if not member.is_chat_admin():
        await callback.answer('Только инициатор может подтвердить готовность.')
    else:
        await callback.answer('Готово')
        print('Добавление пользователей готово')
        set_members_number_in_queue_kb = await admin_kb.set_members_number_in_queue_kb(callback.message)
        await callback.message.answer(text="А теперь надо расставить кожаных мешков по очереди.\n\nПорядок кожаных мешков:\n ---\n1. ...",
                               reply_markup=set_members_number_in_queue_kb)
        await callback.message.delete()


@only_admin_callback
async def add_number_queue_member(callback: types.CallbackQuery):
    # Понять, сколько всех в очереди
    all_members_in_queue = await sqlite_db.get_all_chat_members(callback.message)
    all_members_in_queue_with_number = await sqlite_db.get_all_members_in_queue_with_number(callback.message)

    data = callback.data.split()
    chat_id = data[1]
    member_id = data[2]
    member_name = await sqlite_db.get_user_name_by_id(member_id)
    number = len(all_members_in_queue_with_number) + 1

    await sqlite_db.set_member_number_in_queue(chat_id=chat_id, member_id=member_id, number=number)

    all_members_in_queue_with_number = await sqlite_db.get_all_members_in_queue_with_number(callback.message)

    if len(all_members_in_queue_with_number) < len(all_members_in_queue):
        set_members_number_in_queue_kb = await admin_kb.set_members_number_in_queue_kb(callback.message)
        await callback.message.edit_text(
            f'{callback.message.text[:-3]}{member_name}\n{len(all_members_in_queue_with_number) + 1}. ...',
            reply_markup=set_members_number_in_queue_kb)
    else:
        set_members_number_in_queue_kb = await admin_kb.set_members_number_in_queue_kb(callback.message)
        await callback.message.edit_text(f'{callback.message.text[:-3]}{member_name}\n',
                                         reply_markup=set_members_number_in_queue_kb)


@only_admin_callback
async def set_member_on_problem(callback: types.CallbackQuery):
    data = callback.data.split()
    chat_id = data[1]
    member_id = data[2]
    await sqlite_db.set_member_on_problem(chat_id, member_id)
    await callback.message.delete()
    await bot.send_message(callback.message.chat.id, 'Человек на проблеме назначен. На этом всё')
    await command_queue_show(callback.message)


@only_admin_callback
async def done_add_number_queue_member(callback: types.CallbackQuery):
    all_members_in_queue = await sqlite_db.get_all_members_in_queue_with_number(callback.message)
    message_ = 'Выберите, кто будет сейчас на проблеме:\n'
    for member in all_members_in_queue:
        message_ += f'\n{member[1]}'
    kb = await admin_kb.set_member_on_problem_kb(callback.message)
    await callback.message.delete()
    await bot.send_message(callback.message.chat.id, message_, reply_markup=kb)
    await callback.answer('Готово')


@only_admin_callback
async def qe_delete_member_from_queue(callback: types.CallbackQuery):
    message_ = 'Кого будем удалять из очереди?'
    kb = await admin_kb.delete_member_from_problem_kb(callback.message)
    await callback.message.delete()
    await callback.message.answer(message_, reply_markup=kb)


@only_admin_callback
async def qe_delete_member_from_queue_support(callback: types.CallbackQuery):
    # all_members_in_queue = await sqlite_db.get_all_chat_members(callback.message)
    all_members_in_queue_with_number = await sqlite_db.get_all_members_in_queue_with_number(callback.message)

    data = callback.data.split()

    chat_id = data[1]
    member_id = data[2]
    user_is_on_problem = await sqlite_db.user_is_on_problem(chat_id, member_id)

    if user_is_on_problem:
        all_members_in_queue = await sqlite_db.get_queue_by_chat(callback.message)
        len_all_members_in_queue = len(all_members_in_queue)
        for member_in_queue in all_members_in_queue:
            if member_in_queue[2] == 1:
                next_place_in_queue = member_in_queue[0] + 1
                if next_place_in_queue > len_all_members_in_queue:
                    next_place_in_queue -= len_all_members_in_queue
                await sqlite_db.set_next_member_on_problem(callback.message.chat.id, next_place_in_queue)
    await sqlite_db.delete_member_from_queue(chat_id, member_id)
    await utils.recount_members_places(callback)
    await callback.message.answer('Пользователь удален. Очередь обновлена.')
    await command_queue_show(callback.message)
    await callback.message.delete()


@only_admin_callback
async def qe_add_new_member_in_queue(callback: types.CallbackQuery):
    results = await sqlite_db.known_users_in_chat(callback.message)
    if not results:
        users = ''
    else:
        users = ''
        for user in results:
            users += f'{user[0]}\n'
    kb = await admin_kb.inline_add_one_member_kb(callback.message)
    await callback.message.answer(
        text=f"Для добавления пользователей в очередь они должны быть в списке\n\nДобавленные пользователи:\n ---\n{users}",
        reply_markup=kb)
    await callback.message.delete()


async def qe_add_new_member_in_queue_support(callback: types.CallbackQuery):
    if str(callback.from_user.full_name) in callback.message.text:
        await callback.answer('Ты уже состоишь в списке')
    else:
        await sqlite_db.add_member_in_chat(callback)
        await callback.message.edit_text(
            f'{callback.message.text}\n{callback.from_user.full_name}\n',
            reply_markup=admin_kb.inline_add_members_kb)
        await callback.answer('Добавлен')



@only_admin_callback
async def qe_done_add_user_in_chat(callback: types.CallbackQuery):
    message_ = 'Выберите, кого хотите добавить в очередь:'
    kb =await admin_kb.add_new_member_in_queue(callback.message)
    await callback.message.answer(message_, reply_markup=kb)
    await callback.message.delete()


@only_admin_callback
async def qe_done_add_user_in_chat_support(callback: types.CallbackQuery):
    all_members_in_queue_with_number = await sqlite_db.get_all_members_in_queue_with_number(callback.message)

    data = callback.data.split()

    chat_id = data[1]
    member_id = data[2]
    await sqlite_db.set_member_number_in_queue(chat_id, member_id, 99)  # 99 - raw place in queue
    await utils.recount_members_places(callback)
    await callback.message.answer('Пользователь добавлен. Очередь обновлена')
    await command_queue_show(callback.message)
    await callback.message.delete()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(add_user_in_chat, lambda x: x.data and x.data.startswith('add_user_in_chat'))
    dp.register_callback_query_handler(done_add_user_in_chat, lambda x: x.data and x.data.startswith('done_add_user_in_chat'))
    dp.register_callback_query_handler(add_number_queue_member, lambda x: x.data and x.data.startswith('add_number_queue_member'))
    dp.register_callback_query_handler(done_add_number_queue_member, lambda x: x.data and x.data.startswith('done_add_number_queue_member'))
    dp.register_callback_query_handler(set_member_on_problem, lambda x: x.data and x.data.startswith('set_member_on_problem'))
    dp.register_callback_query_handler(qe_done_add_user_in_chat_support, lambda x: x.data and x.data.startswith('qe_done_add_user_in_chat_support'))
    dp.register_callback_query_handler(qe_done_add_user_in_chat, lambda x: x.data and x.data.startswith('qe_done_add_user_in_chat'))
    dp.register_callback_query_handler(qe_add_new_member_in_queue_support, lambda x: x.data and x.data.startswith('qe_add_new_member_in_queue_support'))
    dp.register_callback_query_handler(qe_add_new_member_in_queue, lambda x: x.data and x.data.startswith('qe_add_new_member_in_queue'))
    dp.register_callback_query_handler(qe_delete_member_from_queue_support, lambda x: x.data and x.data.startswith('qe_delete_member_from_queue_support'))
    dp.register_callback_query_handler(qe_delete_member_from_queue, lambda x: x.data and x.data.startswith('qe_delete_member_from_queue'))
