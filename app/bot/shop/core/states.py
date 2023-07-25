from aiogram.filters.state import State, StatesGroup


class FormOrderContext(StatesGroup):
    get_city = State()
    get_address = State()
    get_name = State()
    get_phone = State()
    get_accord = State()
