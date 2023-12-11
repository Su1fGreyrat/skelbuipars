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

@router.message(F.text == 'Ключевые слова')
async def keyword_menu(message: Message):
    admin_ex = db.admin_ex(user_id=message.from_user.id)
    if admin_ex:
        await message.answer('📒 Выберите действие:', reply_markup=kb.keyword_main)
    
@router.callback_query(F.data == 'new_keyword')
async def suc_new_keyword(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    
    await bot.send_message(callback_query.from_user.id, 'Введите новое ключевое слово:')
    await state.set_state(states.KeywordState.name)


    
    
@router.message(states.KeywordState.name, F.text)
async def new_keyword_category(message: Message, state: FSMContext):
    data = await state.get_data()
    text = message.text
    await state.update_data(kw_name=text)
    
    categories = db.get_categories()
    formatted_categories = [category[1] for category in categories]
    
    keyboard = kb.make_row_inline_keyboard_for(for_='kw-category', items=formatted_categories)
        
    await message.answer(f'Ключевое слово: {text}\nВыберите категорию:', reply_markup=keyboard)
    
    await state.set_state(states.KeywordState.category)

@router.callback_query(F.data.startswith('kw-category'))
async def add_category_kw(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    data = await state.get_data()
    
    keyword_category = callback_data.split('_')[1] 
    await state.update_data(kw_category=keyword_category)
    
    categories = db.get_under_categories(parametr=keyword_category)
    formatted_categories = [category[1] for category in categories]
    
    keyboard = kb.make_row_inline_keyboard_for(for_='kw-suc', items=formatted_categories)
    
    await bot.send_message(callback_query.from_user.id, f'Ключевое слово: {data["kw_name"]}\nКатегория: {keyword_category}\n\nВыберите под-категорию:',
                           reply_markup=keyboard)
    
    await state.set_state(states.KeywordState.under_category)

@router.callback_query(F.data.startswith('kw-suc'))
async def add_category_kw(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    data = await state.get_data()
    
    keyword_under_category = callback_data.split('_')[1] 
    await state.update_data(kw_suc=keyword_under_category)
    
    await bot.send_message(callback_query.from_user.id, f'Ключевое слово: {data["kw_name"]}\nКатегория: {data["kw_category"]}\nПод-категория: {keyword_under_category}',
                           reply_markup=kb.yes_or_no)

@router.callback_query(F.data == 'yes')
async def suc_new_keyword(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
        
    answer = db.new_keyword(word=data["kw_name"], category=data["kw_category"], under_category=data["kw_suc"])
        
    await bot.send_message(callback_query.from_user.id, answer)
        
    await state.clear()
        
    

@router.callback_query(F.data == 'all_keywords')
async def all_keywords(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    
    keywords = db.get_keywords() # [(3, 'Baldų valymas / Generalinis patalpų valymas /'), (5, None), (6, '3')]

    if keywords:
        message = "Список ключевых слов:\n"
        for keyword in keywords:
            message += f"- Слово: {keyword[1]}, Категория: {keyword[2]}, Подкатегория: {keyword[3]}\n"
    else:
        message = "Нет ключевых слов."

    # Send the message to the user (you might want to replace this with your actual code to send messages)
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
    
