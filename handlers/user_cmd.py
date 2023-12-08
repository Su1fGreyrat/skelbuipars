from database.data import BotDB
from markup import reply as kb
from utils import states
from main import bot
from decouple import config

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import CommandStart


router = Router()
db = BotDB()
ADMIN_ID = config("ADMIN")

   
@router.message(Command('start'))
async def start_cmd(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_ex = db.user_ex(user_id)
    if user_ex:
        await message.answer(f'Добро пожаловать! {message.from_user.full_name}', reply_markup=kb.main)
    else:
        db.new_user(user_id=user_id, name=user_name)


@router.message(Command('update'))
async def update(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except:
        pass
    
    admin = db.user_ex(message.from_user.id)
    
    if admin:
        chat_id = str(message.chat.id)
        chat_name = message.chat.title
        text = db.add_chat(chat_id, chat_name)    
        
        await bot.send_message(message.from_user.id, text)
