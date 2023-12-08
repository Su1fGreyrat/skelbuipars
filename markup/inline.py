from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup 
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder



keyword_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить', callback_data='new_keyword'),
            InlineKeyboardButton(text='Удалить', callback_data='delete_keyword')
        ],
        [
            InlineKeyboardButton(text='Посмотреть все', callback_data='all_keywords')
        ]
    ]
)

selectors = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить', callback_data='new_selector'),
            InlineKeyboardButton(text='Удалить', callback_data='delete_selector')
        ],
        [
            InlineKeyboardButton(text='Посмотреть все', callback_data='all_selectors')
        ]
    ]
)

yes_or_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✅ Да', callback_data='yes'),
            InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')
        ]
    ]
)

def make_row_inline_keyboard_for(items, for_: str):
    keyboard = []

    for item in items:
        button_text = f"{for_}_{item}"
        button = InlineKeyboardButton(text=str(item), callback_data=button_text)
        keyboard.append([button])

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return reply_markup

def make_row_inline_keyboard_to(cities, prefix):
    keyboard = []

    for i in range(len(cities)):
        city = cities[i]
        button_text = f"{prefix}_{city}"

        button = InlineKeyboardButton(text=city, callback_data=button_text)
        keyboard.append([button])

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return reply_markup
