"""
Main executable file. It connects to all skills.
"""
from aiogram.utils import executor

from create_bot import dp
from sq_manager import sqlite_db

from skills.start_help import start_help_skill_register
from skills.anek import anek_skill_register
from skills.queue import queue_skill_register


async def on_startup(_):
    print('Бот вышел в онлайн.')
    await sqlite_db.sql_start()

# Main block to connect skills
start_help_skill_register(dp)
anek_skill_register(dp)
queue_skill_register(dp)
#

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
