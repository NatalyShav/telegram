from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="кнопка №1")],
    [KeyboardButton(text="кнопка №2"),KeyboardButton(text="кнопка 3")]
], resize_keyboard=True)

inlline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каталог", callback_data='catalog')],
    [InlineKeyboardButton(text="Новости", url="https://university.zerocoder.ru/pl/teach/control/lesson/view?id=336393181&editMode=0")],
    [InlineKeyboardButton(text="Профиль", callback_data='person')]
])

test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]
async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, url='https://opusdeco.ru/catalog/uniwal_13'))
    return keyboard.adjust(2).as_markup()