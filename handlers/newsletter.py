from database.data import BotDB
from markup import inline as kb
from utils import states
from main import bot
from decouple import config

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

router = Router()
db = BotDB()
ADMIN_ID = config("ADMIN")

async def handler(name, city, link):
    chats = db.get_chats()
    for chat in chats:
        await bot.send_message(chat[2], f'{name}\n{city}\n<a href="{link}">Ссылка</a>', parse_mode='HTML')
    