from database.data import BotDB
from markup import inline as kb
from utils import states
from main import bot
from decouple import config
import asyncio

from aiogram import Router

router = Router()
db = BotDB()

async def handler(name, price, city, link):
    chats = db.get_chats()
    admins = db.get_users()
    try:
        for chat in chats:
            await bot.send_message(chat[2], f'{name}\n{price}\n{city}\n<a href="{link}">Ссылка</a>', parse_mode='HTML')
            await asyncio.sleep(1)
    except:
        pass