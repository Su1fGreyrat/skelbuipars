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

async def handler(text):
    await bot.send_message(ADMIN_ID, text)
    