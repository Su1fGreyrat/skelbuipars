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

@router.message(F.text == 'Ключевые слова')
async def keyword_menu(message: Message):
    await message.answer('📒 Выберите действие:', reply_markup=kb.keyword_main)
    
@router.callback_query(F.data == 'new_keyword')
async def suc_new_keyword(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    
    await bot.send_message(callback_query.from_user.id, 'Введите новое ключевое слово:')
    await state.set_state(states.KeywordState.name)
    
@router.message(states.KeywordState.name, F.text)
async def new_keyword(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
        
    await message.answer(f'Новое ключевое слово это: {data["name"]}?', reply_markup=kb.yes_or_no)

@router.callback_query(states.KeywordState.name, F.data == 'yes')
async def suc_new_keyword(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if 'name' in data:
        answer = db.new_keyword(word=data["name"])
        await bot.send_message(callback_query.from_user.id, answer)
        await state.clear()

@router.callback_query(F.data == 'all_keywords')
async def all_keywords(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    
    keywords = db.get_keywords()
    
    message = "Список ключевых слов:\n- " + "\n- ".join(keyword[1] for keyword in keywords)
    
    await bot.send_message(callback_query.from_user.id, message)
    
@router.callback_query(F.data == 'delete_keyword')
async def del_keyword(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    all_keywords_name = db.get_keywords()
    formatted_keywords = [name[1] for name in all_keywords_name]
    
    keyboard = kb.make_row_inline_keyboard_for(for_='delete-keyword', items=formatted_keywords)
    
    await bot.send_message(callback_query.from_user.id, 'Выберите ключевое слово которое вы хотите удалить:', reply_markup=keyboard)
    
@router.callback_query(F.data.startswith('delete-keyword'))
async def del_keyword_product(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    keyword = callback_data.split('_')[1] 
    
    answer = db.delete_keyword(keyword)
    await bot.send_message(callback_query.from_user.id, answer)
    
