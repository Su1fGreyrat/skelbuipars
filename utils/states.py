from aiogram.fsm.state import State, StatesGroup

class SelectorState(StatesGroup):
    category = State()
    under_category = State()
    city = State()
    
class KeywordState(StatesGroup):
    name = State()
    category = State()
    under_category = State()
    
class LogInState(StatesGroup):
    login = State()
    password = State()

class RequestState(StatesGroup):
    name = State()
    category = State()
    under_category = State()
    city = State()
