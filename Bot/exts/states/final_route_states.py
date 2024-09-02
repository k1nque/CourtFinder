from aiogram.fsm.state import StatesGroup, State

class States(StatesGroup):
    AddressInput = State()
    SuggestionChoice = State()