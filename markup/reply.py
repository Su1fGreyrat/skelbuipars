from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton 
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать запрос")
        ],
        [
            KeyboardButton(text="Удалить запрос")
        ]
    ],
    resize_keyboard=True
)