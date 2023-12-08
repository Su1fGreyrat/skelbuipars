from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton 
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Селекторы'),
            KeyboardButton(text="Ключевые слова")
        ],
        [
            KeyboardButton(text='Группы')
        ]
    ],
    resize_keyboard=True
)