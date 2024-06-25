from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from Handlers.routes.start_route import StartRouteStates

TwoQuestionsRouter = Router()

class TwoQuestionsRouteStates(StatesGroup):
    IsItCounterclaim = State()
    IsItIntellectualCase = State()


@TwoQuestionsRouter.message(StateFilter(StartRouteStates.IsItMilitaryServiceCase), F.text == "Нет")
async def start_route(msg: types.Message, state: FSMContext):
    await msg.answer("В отношении Вас подан иск?")
    await state.set_state(TwoQuestionsRouteStates.IsItCounterclaim)


@TwoQuestionsRouter.message(StateFilter(TwoQuestionsRouteStates.IsItCounterclaim), F.text == "Да")
async def is_it_counterclaim_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Обратитесь в суд, в который подан изначальный иск")
    await state.set_state(None)


@TwoQuestionsRouter.message(StateFilter(TwoQuestionsRouteStates.IsItCounterclaim), F.text == "Нет")
async def is_it_counterclaim_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с резулььтатами интеллектуальной деятельности?")
    await state.set_state(TwoQuestionsRouteStates.IsItIntellectualCase)


@TwoQuestionsRouter.message(StateFilter(TwoQuestionsRouteStates.IsItIntellectualCase), F.text == "Что это?")
async def is_it_counterclaim_what_is_it(msg: types.Message, state: FSMContext):
    await msg.answer("") # TODO расписать текстик для дурашек
