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
    

@router.message(F.text == 'Создать запрос')
async def suc_new_request(message: Message, state: FSMContext):
    admin_ex = db.admin_ex(message.from_user.id)
    print(admin_ex)
    if admin_ex == 0:
        print('admin_ex')
        await bot.send_message(message.from_user.id, 'Введите новое ключевое слово:')
        await state.set_state(states.RequestState.name)
  
@router.message(F.text == 'Удалить запрос')
async def delete_request(message: Message):
    admin_ex = db.admin_ex(message.from_user.id)
    if admin_ex == 0:
        requests = db.get_keywords()
        
        for request in requests:
            await bot.send_message(message.from_user.id, f'ID: {request[0]}\n\nСлово: {request[1]}\nКатегория: {request[2]}\nПод категория: {request[3]}\n Город: {request[4]}')
        
        formatted_categories = [request[0] for request in requests]
        keyboard = kb.make_row_inline_keyboard_for(for_='delete-request', items=formatted_categories)
        
        if formatted_categories:
            await bot.send_message(message.from_user.id, 'Выберите ID селектора которого хотите удалить:', reply_markup=keyboard)
        else:
            await bot.send_message(message.from_user.id, f'Нет доступных селекторов')

    
@router.message(states.RequestState.name, F.text)
async def new_request_category(message: Message, state: FSMContext):
    data = await state.get_data()
    text = message.text
    await state.update_data(rq_name=text)
    categories = db.get_categories()
    formatted_categories = [category[1] for category in categories]
    keyboard = kb.make_row_inline_keyboard_for(for_='rq-category', items=formatted_categories)
    await message.answer(f'Ключевое слово: {text}\n\nВыберите категорию:', reply_markup=keyboard)
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
async def add_request_request(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    data = await state.get_data()
    
    city = callback_data.split('_')[1] 
    await state.update_data(city=city)
    
    await bot.send_message(callback_query.from_user.id, f'Ключевое слово: {data["rq_name"]}\nКатегория: {data["rq_category"]}\nПод-категория: {data["rq_suc"]}\nГород: {city}', 
                           reply_markup=kb.yes_or_no)
    
    
@router.callback_query(F.data == 'yes')
async def suc_new_request(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
        
    answer = db.new_keyword(word=data["rq_name"], category=data["rq_category"], under_category=data["rq_suc"], city=data["city"])
    db.new_selector(category=data["rq_category"], under_category=data["rq_suc"], city=data["city"])
    
    await bot.send_message(callback_query.from_user.id, answer)
        
    await state.clear()
        

            
@router.callback_query(F.data.startswith('delete-request'))
async def delete_request_db(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    callback_data = callback_query.data
    request_id = callback_data.split('_')[1]
     
    req = db.get_requests(id=request_id)
    print(req)
    db.delete_request(word=req[1], category=req[2], under_category=req[3], city=req[4])
    
    if request_id:
        await bot.send_message(callback_query.from_user.id, f'Селектор с ID: {request_id} удален')
    else:
        await bot.send_message(callback_query.from_user.id, f'Селектор с таким ID не найден')
        
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
