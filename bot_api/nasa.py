import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from bottle import response
from conda_env.cli.main_list import description
from future.backports.datetime import timedelta

from config import TOKEN, NASA_API_KEY
import random
import requests
from datetime import datetime, timedelta



bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date-start_date)*random.random()
    date_str = random_date.strftime("%Y-%m-%d")

    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
    response = requests.get(url)
    return response.json()

@dp.message(Command("random_apod"))
async def random_apod(message: Message):
    apod = get_random_apod()
    photo_url = apod['url']
    title = apod['title']


    await message.answer_photo(photo=photo_url, caption=f"{title}")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())