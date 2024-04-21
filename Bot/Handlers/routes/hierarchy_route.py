from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

HierarchyRouter = Router()


class HierarchyRouteStates(StatesGroup):
    IsYourDefendentCountry = State()
    IsItFederal = State()
    IsItSabjectOrmunicipal = State()
    IsItdivorce = State()
    IsItChildrenCase = State()
    AreTheyLess18 = State()
    IsItLess50K = State()
    IsItinheritanceOrIP = State()
    ZPP = State()
    ZPP_Less100K = State()
    IsItRightCase = State()
    IsItTopSecret = State()