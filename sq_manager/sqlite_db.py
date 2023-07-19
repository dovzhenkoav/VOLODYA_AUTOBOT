import sqlite3

import aiosqlite
from create_bot import dp, bot
from aiogram import types
from settings import DB_NAME


async def sql_start():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
                CREATE TABLE IF NOT EXISTS chat
                (
                id INTEGER PRIMARY KEY,
                name varchar(255)
                );""")
        await db.execute("""
                CREATE TABLE IF NOT EXISTS members
                (
                id INTEGER PRIMARY KEY,
                member_name varchar(255),
                member_tag varchar(255)
                );""")
        await db.execute("""
                CREATE TABLE IF NOT EXISTS chat_members
                (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                member_id INTEGER,
                FOREIGN KEY(chat_id) REFERENCES chat(id),
                FOREIGN KEY(member_id) REFERENCES member(id)
                );
                """)
        await db.execute("""
                CREATE TABLE IF NOT EXISTS queue
                (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                member_id INTEGER,
                place_in_queue INTEGER,
                is_on_problem INTEGER,
                FOREIGN KEY(chat_id) REFERENCES chat(id),
                FOREIGN KEY(member_id) REFERENCES member(id)
                );
                """)
        await db.commit()


async def queue_is_in_db(message: types.Message):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT *
        FROM queue
        WHERE chat_id = ?
        """, (message.chat.id,))
        row = await cursor.fetchone()
        if row:
            return True
        else:
            return False


async def delete_queue(message: types.Message):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        DELETE FROM queue WHERE chat_id = ?
        """, (message.chat.id,))
        await db.commit()


async def known_users_in_chat(message: types.Message):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT member_name
        FROM chat_members
        JOIN members ON members.id = chat_members.member_id
        WHERE chat_id = ?
        """, (message.chat.id,))
        results = await cursor.fetchall()
        return results


async def add_member_in_chat(callback: types.CallbackQuery):
    async with aiosqlite.connect(DB_NAME) as db:
        try:
            await db.execute("""
            INSERT INTO members(id, member_name, member_tag)
            VALUES(?, ?, ?)
            """, (callback.from_user.id, callback.from_user.full_name, callback.from_user.username))
            await db.commit()
        except sqlite3.IntegrityError as err:
            print('Юзер уже в БД. Таблица members')
        try:
            await db.execute("""
            INSERT INTO chat_members(chat_id, member_id)
            VALUES(?, ?)
            """, (callback.message.chat.id, callback.from_user.id))
            await db.commit()
        except sqlite3.IntegrityError as err:
            print('Юзер уже в БД. Таблица chat_members')


async def get_all_chat_members(message: types.Message):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT chat_members.chat_id, members.member_name, members.id
        FROM chat_members
        JOIN members ON chat_members.member_id = members.id
        WHERE chat_id = ?
        """, (message.chat.id,))
        results = await cursor.fetchall()
        return results


async def get_all_chat_members_in_queue_without_numbers(message: types.Message):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT chat_id, member_name, member_id FROM
        (SELECT *
        FROM chat_members
        WHERE NOT EXISTS(SELECT place_in_queue
                         FROM queue
                         WHERE queue.chat_id=chat_members.chat_id
                         AND queue.member_id=chat_members.member_id)) as q1
        LEFT JOIN members ON members.id = q1.member_id
        WHERE chat_id = ?
        """, (message.chat.id,))

        data = await cursor.fetchall()
        return data


async def get_all_members_in_queue_with_number(message: types.Message):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT chat_id, member_name, member_id FROM
        (SELECT *
        FROM chat_members
        WHERE EXISTS(SELECT place_in_queue
                         FROM queue
                         WHERE queue.chat_id=chat_members.chat_id
                         AND queue.member_id=chat_members.member_id
                         ORDER BY place_in_queue)) as q1
        LEFT JOIN members ON members.id = q1.member_id
        WHERE chat_id = ?
        """, (message.chat.id,))

        data = await cursor.fetchall()
        return data


async def set_member_number_in_queue(chat_id, member_id, number):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT INTO queue(chat_id, member_id, place_in_queue, is_on_problem)
        VALUES (?,?,?, 0)
        """, (chat_id, member_id, number))
        await db.commit()


async def set_member_on_problem(chat_id, member_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        UPDATE queue
        SET is_on_problem = 0
        WHERE chat_id = ?
        """, (chat_id,))
        await db.execute("""
        UPDATE queue
        SET is_on_problem = 1
        WHERE chat_id = ? AND member_id = ?
        """, (chat_id, member_id))
        await db.commit()


async def get_queue_by_chat(message: types.Message):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT queue.place_in_queue, members.member_name, queue.is_on_problem, queue.member_id
        FROM queue
        JOIN members ON members.id = queue.member_id
        WHERE queue.chat_id = ?
        ORDER BY place_in_queue ASC
        """, (message.chat.id,))
        data = await cursor.fetchall()
        return data


async def set_next_member_on_problem(chat_id, member_place_in_queue):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        UPDATE queue
        SET is_on_problem = 0
        WHERE chat_id = ?
        """, (chat_id,))
        await db.execute("""
        UPDATE queue
        SET is_on_problem = 1
        WHERE chat_id = ? AND place_in_queue = ?
        """, (chat_id, member_place_in_queue))
        await db.commit()

        cursor = await db.execute("""
        SELECT member_name, member_tag, members.id
        FROM queue
        JOIN members ON members.id = queue.member_id
        WHERE queue.chat_id = ? AND is_on_problem = 1
        """, (chat_id,))
        data = await cursor.fetchone()
        return data


async def get_user_name_by_id(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT id, member_name
        FROM members
        WHERE id = ?
        """, (user_id,))
        data = await cursor.fetchone()
        return data[1]


async def user_is_on_problem(chat_id: int, user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT is_on_problem
        FROM queue
        WHERE chat_id = ? AND member_id = ?
        """, (chat_id, user_id))
        data = await cursor.fetchone()
        return data[0]


async def delete_member_from_queue(chat_id, member_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        DELETE FROM queue
        WHERE chat_id = ? AND member_id = ?
        """, (chat_id, member_id))
        await db.commit()


async def update_members_places_in_queue(place_in_queue: int, chat_id: int, member_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        UPDATE queue
        SET place_in_queue = ?
        WHERE chat_id = ? AND member_id = ?
        """, (place_in_queue, chat_id, member_id))
        await db.commit()
