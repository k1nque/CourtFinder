from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    NewCircumstances = State()
    DecisionInForce = State()
    ThreeMonthHavePassed = State()
    ValidReasons = State()
