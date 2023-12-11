from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton 
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Запросы")
        ]
    ],
    resize_keyboard=True
)