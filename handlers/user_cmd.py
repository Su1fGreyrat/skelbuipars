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

   
@router.message(Command('start'))
async def start_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    await message.answer(f'Добро пожаловать! {message.from_user.full_name}', reply_markup=kb.main)
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

@router.message(F.text == 'Чаты')
async def chats(message: Message):
    chats = db.get_chats()
    if chats:
        length = len(chats)
        answer = f"Бот задействован в {length} чатах"
    else:
        answer = "Нет добавленных чатов."
        
    await bot.send_message(message.from_user.id, answer)
    

    
@router.message()
async def handler_msg(message: Message):
    try:
        answer = db.add_chat(message.forward_from_chat.id)
        await message.answer(answer)
    except:
        pass
    
@router.callback_query()
async def callback_query_handler(callback_query: types.CallbackQuery, state: FSMContext):
    text = callback_query.data
    if 'cancel' in text:
        await state.clear()
        await bot.send_message(callback_query.from_user.id, 'Операция отменена')