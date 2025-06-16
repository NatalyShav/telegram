import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import requests
from datetime import datetime, timedelta
import random

from config import TOKEN, BOOK_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

POPULAR_GENRES = [
    "фантастика",
    "детектив",
    "роман",
    "фэнтези",
    "историческая литература",
    "приключения",
    "мистика",
    "биография",
    "саморазвитие",
    "поэзия"
]
@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Я бот, который делится интересными фактами о кино и книгах.\n Используйте /help для списка команд.")

@dp.message(Command("help"))
async def handle_help(message: Message):
    await message.answer(
        "/fact - получить интересный факт о кино или книгах\n"
        "/newbooks <жанр> - получить список книжных новинок по жанру\n"
        "/genres - список доступных жанров\n"
        "/stop - остановить бота (если нужно)"
    )

@dp.message(Command("fact"))
async def handle_fact(message: Message):
    fact = get_random_fact()
    await message.answer(fact)

@dp.message(Command("genres"))
async def handle_genres(message: Message):
    genres_str = ", ".join(POPULAR_GENRES)
    await message.answer(f"Доступные жанры:\n{genres_str}")

@dp.message(Command("newbooks"))
async def handle_newbooks(message: Message):
    # Получение аргумента (жанра) из текста команды
    text = message.text
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Пожалуйста, укажите жанр. Например: /newbooks фантастика")
        return
    genre = parts[1].lower()

    # Проверка, есть ли жанр в списке
    if genre not in [g.lower() for g in POPULAR_GENRES]:
        await message.answer(
            f"Извините, жанр '{genre}' недоступен. Выберите из списка:\n" +
            ", ".join(POPULAR_GENRES)
        )
        return

    books_list = get_books_by_genre(genre)

    if books_list:
        response = f"Книжные новинки в жанре '{genre}':\n"
        for book in books_list:
            response += f"📚 {book['title']} — {book['authors']}\n"
        await message.answer(response)
    else:
        # Можно объяснить, что по жанру нет новинок, или предложить выбрать другой
        await message.answer(
            f"Не удалось найти новинки в жанре '{genre}'. Попробуйте другой жанр.\n"
            "Также вы можете выбрать из списка доступных жанров: /genres"
        )


def get_books_by_genre(genre):
    # Используем Google Books API для поиска книг по жанру
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': f'subject:{genre}',
        'orderBy': 'newest',
        'maxResults': 10,
        'key': BOOK_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        books = []
        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            title = volume_info.get('title', 'Без названия')
            authors = volume_info.get('authors', ['Неизвестный автор'])
            books.append({
                'title': title,
                'authors': ', '.join(authors)
            })
        return books
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return []
def get_random_fact():
    # Простая функция, возвращающая случайный факт
    facts = [
        "Книги сдерживают время. Чем больше читаешь — тем дольше живёшь.",
        "Самая продаваемая книга — Библия.",
        "Первая печатная книга — Библия Гутенберга, созданная в 1455 году.",
        "Самая толстая книга в мире — «Машина», которая весит около 8 кг.",
        "Чтение книг помогает развивать воображение и улучшает память."
    ]
    return random.choice(facts)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())