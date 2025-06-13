import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message,FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
import sqlite3
import aiohttp
import logging


bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    city = State()

def init_db():
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	age INTEGER NOT NULL,
	city TEXT NOT NULL)
    ''')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())