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


@router.message(F.text == 'Селекторы')
async def new_selector(message: Message, state: FSMContext):
    await message.answer('🛍 Выберите желаемое действие:', reply_markup=kb.selectors)
    
    
@router.callback_query(F.data == 'new_selector')
async def suc_new_selector(callback_query: types.CallbackQuery, state: FSMContext):
    categories = db.get_categories()
    formatted_categories = [category[1] for category in categories]
    
    keyboard = kb.make_row_inline_keyboard_for(for_='set-category', items=formatted_categories)
    
    await bot.send_message(callback_query.from_user.id, 'Выберите категорию:', reply_markup=keyboard)
    await state.set_state(states.SelectorState.category)

@router.callback_query(F.data.startswith('set-category'))
async def add_selector_selector(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data

    selector_category = callback_data.split('_')[1] 
    await state.update_data(category=selector_category)
    
    categories = db.get_under_categories(parametr=selector_category)
    formatted_categories = [category[1] for category in categories]
    
    keyboard = kb.make_row_inline_keyboard_for(for_='set-under-category', items=formatted_categories)
    
    await bot.send_message(callback_query.from_user.id, f'Категория: {selector_category}\n\nВыберите под-категорию:',
                           reply_markup=keyboard)
    await state.set_state(states.SelectorState.under_category)
    
@router.callback_query(F.data.startswith('set-under-category'))
async def add_selector_selector(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    data = await state.get_data()

    selector_under_category = callback_data.split('_')[1] 
    await state.update_data(under_category=selector_under_category)
    
    cities = db.get_cities()
    formatted_cities = [city[1] for city in cities]
    
    keyboard = kb.make_row_inline_keyboard_to(prefix='set-city', cities=formatted_cities)
    
    await bot.send_message(callback_query.from_user.id, f'Категория: {data["category"]}\nПод-категория: {selector_under_category}\n\nВыберите город:',
                           reply_markup=keyboard)
    await state.set_state(states.SelectorState.city)
    
@router.callback_query(F.data.startswith('set-city'))
async def add_selector_selector(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    data = await state.get_data()
    
    city = callback_data.split('_')[1] 
    await state.update_data(city=city)
    
    new_selector = db.new_selector(category=data["category"], under_category=data["under_category"], city=city)
    
    if new_selector == 0:
        await bot.send_message(callback_query.from_user.id, f'Создан новый селектор!\n\nКатегория: {data["category"]}\nПод-категория: {data["under_category"]}\nГород: {city}')
    elif new_selector == 1:
        await bot.send_message(callback_query.from_user.id, f'Селектор с такими параметрами существует!\n\nКатегория: {data["category"]}\nПод-категория: {data["under_category"]}\nГород: {city}')
        
    await state.clear()
    
@router.callback_query(F.data == 'delete_selector')
async def delete_selector(callback_query: types.CallbackQuery, state: FSMContext):
    categories = db.get_categories()
    formatted_categories = [category[1] for category in categories]
    
    keyboard = kb.make_row_inline_keyboard_for(for_='delete-selector-category', items=formatted_categories)
    
    await bot.send_message(callback_query.from_user.id, 'Выберите категорию:', reply_markup=keyboard)

@router.callback_query(F.data.startswith('delete-selector-category'))
async def delete_selector_from(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    selector_category = callback_data.split('_')[1] 
    
    selectors_with_category = db.get_selectors_with_category(selector_category)
    print(selectors_with_category)
    for selector in selectors_with_category:
        await bot.send_message(callback_query.from_user.id, f'ID: {selector[0]}\n\nКатегория: {selector[1]}\nПод категория: {selector[2]}\n Город: {selector[3]}')
        
    formatted_categories = [selector[0] for selector in selectors_with_category]
    keyboard = kb.make_row_inline_keyboard_for(for_='delete-selector', items=formatted_categories)
    if formatted_categories:
        await bot.send_message(callback_query.from_user.id, 'Выберите ID селектора которого хотите удалить:', reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, f'В это категории нет селекторов')
        
@router.callback_query(F.data.startswith('delete-selector'))
async def delete_selector_db(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data

    selector_id = callback_data.split('_')[1] 
    
    db.delete_selector(id=selector_id)
    if selector_id:
        await bot.send_message(callback_query.from_user.id, f'Селектор с ID: {selector_id} удален')
    else:
        await bot.send_message(callback_query.from_user.id, f'Селектор с таким ID не найден')
        
@router.callback_query(F.data == 'all_selectors')
async def delete_selector(callback_query: types.CallbackQuery, state: FSMContext):
    selectors= db.get_selectors()
    
    for selector in selectors:
        await bot.send_message(callback_query.from_user.id, f'ID: {selector[0]}\n\nКатегория: {selector[1]}\nПод категория: {selector[2]}\n Город: {selector[3]}')









