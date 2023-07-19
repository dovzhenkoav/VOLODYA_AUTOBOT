from aiogram import types

from sq_manager import sqlite_db


async def recount_members_places(callback: types.CallbackQuery):
    """Helpful util to recount members places in chat queue."""
    all_members_in_queue = await sqlite_db.get_queue_by_chat(callback.message)
    counter = 0
    for member_in_queue in all_members_in_queue:
        counter += 1
        await sqlite_db.update_members_places_in_queue(counter, callback.message.chat.id, member_in_queue[3])
