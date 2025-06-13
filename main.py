import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message,FSInputFile
from googletrans import Translator

from config import TOKEN
from config import API_KEY
import random
import aiohttp

from gtts import gTTS


api_key = 'API_KEY'

bot = Bot(token=TOKEN)
dp = Dispatcher()

translator = Translator()

@dp.message(Command('weather'))
async def weather(message: Message):
    city = 'Moscow'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                reply = f"Погода в Москве:\nТемпература: {temp}°C\nОписание: {description.capitalize()}"
                await message.answer(reply)
            else:
                await message.answer("Не удалось получить информацию о погоде.")


@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    file_path = r'D:\ФИЛЬМЫ\Авиацентр\video.mp4'
    video = FSInputFile(file_path)
    await bot.send_video(chat_id=message.chat.id, video=video)


@dp.message(Command('audio'))
async def audio(message: Message):
    file_path = r'D:\ФИЛЬМЫ\Авиацентр\sound2.mp3'
    audio = FSInputFile(file_path)
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1: 1. Скручивания: 3 подхода по 15 повторений 2. Велосипед: 3 подхода по 20 повторений (каждая сторона) 3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2: 1. Подъемы ног: 3 подхода по 15 повторений 2. Русский твист: 3 подхода по 20 повторений (каждая сторона) 3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3: 1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений 2. Горизонтальные ножницы: 3 подхода по 20 повторений 3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

   tts = gTTS(text=rand_tr,lang='ru')
   tts.save("training.ogg")
   audio = FSInputFile("training.ogg")
   await bot.send_voice(message.chat.id, audio)
   os.remove("training.ogg")

@dp.message(Command('doc'))
async def doc(message: Message):
    file_path = r'C:\TG_aiogramm\tg_aiogramm\Великие спящие 1.txt'
    doc = FSInputFile(file_path)
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('photo'))
async def photo(message: Message):
    photo_list = [
        "https://i.pinimg.com/originals/e4/21/50/e4215008df6962d94248502bed11a113.jpg",
        "https://ae01.alicdn.com/kf/H09e6e06905e043e89de4a6a14bbbfea8L/-.jpg"
    ]
    rand_photo = random.choice(photo_list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer("Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ")

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/audion\n/photo\n/training\n/weather")


@dp.message(Command('start'))
async def start(message:Message):
    await message.answer('Приветики. Я бот!')

@dp.message(F.text)
async def translate_to_english(message: Message):
    # Переводим текст на английский
    try:
        translated = translator.translate(message.text, dest='en')
        await message.answer(f"Перевод: {translated.text}")
    except Exception as e:
        await message.answer("Ошибка при переводе: " + str(e))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())