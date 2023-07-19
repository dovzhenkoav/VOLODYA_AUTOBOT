from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram import types
from sq_manager import sqlite_db

# Add members kb
inl_add_member_btn = InlineKeyboardButton(text='Добавить меня', callback_data='add_user_in_chat')
inl_ready_member_btn = InlineKeyboardButton(text='Следующий шаг', callback_data='done_add_user_in_chat')

inline_add_members_kb = InlineKeyboardMarkup(row_width=2)
inline_add_members_kb.add(inl_add_member_btn, inl_ready_member_btn)


# Set members in queue
async def set_members_number_in_queue_kb(message: types.Message):
    all_members = await sqlite_db.get_all_chat_members_in_queue_without_numbers(message)
    queue_numbers = InlineKeyboardMarkup(row_width=2)
    for member in all_members:
        member_name = member[1]
        queue_numbers.add(InlineKeyboardButton(text=f'{member_name}', callback_data=f'add_number_queue_member {member[0]} {member[2]}'))

    queue_numbers.add(InlineKeyboardButton(text='Готово.', callback_data='done_add_number_queue_member'))
    return queue_numbers


async def set_member_on_problem_kb(message: types.Message):
    all_members_in_queue = await sqlite_db.get_all_members_in_queue_with_number(message)
    queue_numbers = InlineKeyboardMarkup(row_width=2)
    for member in all_members_in_queue:
        # member[0] - chat_id, member[1] - member name, member[2] - member id
        queue_numbers.add(InlineKeyboardButton(text=f'{member[1]}', callback_data=f'set_member_on_problem {member[0]} {member[2]}'))
    return queue_numbers


async def inline_qe_commands(message: types.Message):
    inl_markup = InlineKeyboardMarkup(row_width=2)
    inl_markup.add(InlineKeyboardButton(text='Переназначить ответственного', callback_data='done_add_number_queue_member'))
    inl_markup.add(InlineKeyboardButton(text='Удалить участника', callback_data='qe_delete_member_from_queue'))
    inl_markup.add(InlineKeyboardButton(text='Добавить участника', callback_data='qe_add_new_member_in_queue'))
    return inl_markup


async def delete_member_from_problem_kb(message: types.Message):
    all_members_in_queue = await sqlite_db.get_all_members_in_queue_with_number(message)
    queue_numbers = InlineKeyboardMarkup(row_width=2)
    for member in all_members_in_queue:
        # member[0] - chat_id, member[1] - member name, member[2] - member id
        queue_numbers.add(InlineKeyboardButton(text=f'{member[1]}', callback_data=f'qe_delete_member_from_queue_support {member[0]} {member[2]}'))
    return queue_numbers


async def inline_add_one_member_kb(message: types.Message):
    inl_add_member_btn = InlineKeyboardButton(text='Добавить меня', callback_data='qe_add_new_member_in_queue_support')
    inl_ready_member_btn = InlineKeyboardButton(text='Следующий шаг', callback_data='qe_done_add_user_in_chat')

    inline_add_members_kb = InlineKeyboardMarkup(row_width=2)
    inline_add_members_kb.add(inl_add_member_btn, inl_ready_member_btn)
    return inline_add_members_kb

async def add_new_member_in_queue(message: types.Message):
    all_members = await sqlite_db.get_all_chat_members_in_queue_without_numbers(message)
    queue_numbers = InlineKeyboardMarkup(row_width=2)
    for member in all_members:
        member_name = member[1]
        queue_numbers.add(InlineKeyboardButton(text=f'{member_name}', callback_data=f'qe_done_add_user_in_chat_support {member[0]} {member[2]}'))
    return queue_numbers