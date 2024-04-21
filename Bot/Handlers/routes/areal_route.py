from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

ArealRouter = Router()


class ArealRouteStates(StatesGroup):
    IsItRealtyCase = State()
    IsItinheritance = State()
    IsItGroupCase = State()
    IsItContract = State()
    IsIttransportation =State()
    IsItContractualjurisdiction = State()
    ThePlaceOfExecutionIsIndicated = State()
    IsItHealthHarm = State()
    IsItDadCase = State()
    IsItCollisionOfShips = State()
    IsItJobCase = State()
    IsItZPPCase = State()
    IsItPersonalDataCase = State()
    IsItBranchCase = State()
    IsYourDefendentinRF = State()