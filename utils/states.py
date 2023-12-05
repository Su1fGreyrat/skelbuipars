from aiogram.fsm.state import State, StatesGroup

class ProductState(StatesGroup):
    name = State()
    price = State()
    description = State()
    category = State()

class KeywordState(StatesGroup):
    name = State()
    
class LogInState(StatesGroup):
    login = State()
    password = State()
    
class NewLogInState(StatesGroup):
    login = State()
    password = State()
    

