import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message,FSInputFile, CallbackQuery
from googletrans import Translator

from config import TOKEN
from config import API_KEY
import random
import aiohttp

from gtts import gTTS
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.text == "Привет")
async def user_button(message: Message):
    await message.answer(f" Привет, {message.from_user.first_name}")

@ dp.message(F.text == "Пока")
async def user_button2(message: Message):
    await message.answer(f"Пока, {message.from_user.first_name}")

@dp.message(CommandStart())
async def start(message:Message):
    await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=kb.main)

@dp.message(Command('links'))
async def links(message: Message):
    await message.answer("Вот лучшие фильмы, новости и музыку",reply_markup=kb.inlline_keyboard_test)

@dp.callback_query()
async def handle_callback(callback: CallbackQuery):
    selected_option = callback.data
    await callback.answer()
    await callback.message.answer(f'Вы выбрали: {selected_option}')


@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer("Показать больше", reply_markup=await kb.test_keyboard())


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())