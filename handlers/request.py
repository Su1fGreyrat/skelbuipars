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

@router.message(F.text == 'Запросы')
async def request_menu(message: Message):
    admin_ex = db.admin_ex(user_id=message.from_user.id)
    if admin_ex:
        await message.answer('📒 Выберите действие:', reply_markup=kb.request_main)
    
@router.callback_query(F.data == 'new_request')
async def suc_new_request(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    
    await bot.send_message(callback_query.from_user.id, 'Введите новое ключевое слово:')
    await state.set_state(states.RequestState.name)
    
@router.message(states.RequestState.name, F.text)
async def new_request_category(message: Message, state: FSMContext):
    data = await state.get_data()
    text = message.text
    await state.update_data(rq_name=text)
    
    categories = db.get_categories()
    formatted_categories = [category[1] for category in categories]
    
    keyboard = kb.make_row_inline_keyboard_for(for_='rq-category', items=formatted_categories)
        
    await message.answer(f'Ключевое слово: {text}\nВыберите категорию:', reply_markup=keyboard)
    
    await state.set_state(states.RequestState.category)

@router.callback_query(F.data.startswith('rq-category'))
async def add_category_rq(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    data = await state.get_data()
    
    request_category = callback_data.split('_')[1] 
    await state.update_data(rq_category=request_category)
    
    categories = db.get_under_categories(parametr=request_category)
    formatted_categories = [category[1] for category in categories]
    
    keyboard = kb.make_row_inline_keyboard_for(for_='rq-suc', items=formatted_categories)
    
    await bot.send_message(callback_query.from_user.id, f'Ключевое слово: {data["rq_name"]}\nКатегория: {request_category}\n\nВыберите под-категорию:',
                           reply_markup=keyboard)
    
    await state.set_state(states.RequestState.under_category)

@router.callback_query(F.data.startswith('rq-suc'))
async def add_category_rq(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    data = await state.get_data()
    
    request_under_category = callback_data.split('_')[1] 
    await state.update_data(rq_suc=request_under_category)
    
    cities = db.get_cities()
    formatted_cities = [city[1] for city in cities]
    
    keyboard = kb.make_row_inline_keyboard_to(prefix='set-city', cities=formatted_cities)
    
    await bot.send_message(callback_query.from_user.id, f'Ключевое слово: {data["rq_name"]}\nКатегория: {data["rq_category"]}\nПод-категория: {request_under_category}\n\nВыберите город:', 
                           reply_markup=keyboard)
    
    
@router.callback_query(F.data.startswith('set-city'))
async def add_selector_selector(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    data = await state.get_data()
    
    city = callback_data.split('_')[1] 
    await state.update_data(city=city)
    
    await bot.send_message(callback_query.from_user.id, f'Ключевое слово: {data["rq_name"]}\nКатегория: {data["rq_category"]}\nПод-категория: {data["rq_suc"]}\n\Город: {city}', 
                           reply_markup=kb.yes_or_no)
    
    
@router.callback_query(F.data == 'yes')
async def suc_new_request(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
        
    answer = db.new_keyword(word=data["rq_name"], category=data["rq_category"], under_category=data["rq_suc"], city=data["city"])
    db.new_selector(category=data["rq_category"], under_category=data["rq_suc"], city=data["city"])
    
    await bot.send_message(callback_query.from_user.id, answer)
        
    await state.clear()
        
        
@router.callback_query(F.data == 'delete_request')
async def del_request(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    all_requests_name = db.get_requests()
    formatted_requests = [name[1] for name in all_requests_name]
    
    keyboard = kb.make_row_inline_keyboard_for(for_='delete-request', items=formatted_requests)
    
    await bot.send_message(callback_query.from_user.id, 'Выберите ключевое слово которое вы хотите удалить:', reply_markup=keyboard)
    
@router.callback_query(F.data.startswith('delete-request'))
async def del_request_product(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    request = callback_data.split('_')[1] 
    
    answer = db.delete_request(request)
    await bot.send_message(callback_query.from_user.id, answer)
    
