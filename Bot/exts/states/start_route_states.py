from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    IsItCriminalCase = State()
    IsItTreteyCourt = State()
    WasCaseBefore = State()
    IsItMilitaryServiceCase = State()
    IsItRussianCourt = State()
