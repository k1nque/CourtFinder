from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    BusinessEconomicActivity = State()
    DebtorsAddress = State()
    DebtorsProperyAddress = State()
    Suggestions = State()