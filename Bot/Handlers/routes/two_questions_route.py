from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from exts.states import StartRouteStates
from exts.states import TwoQuestionsRouteStates as States


router = Router()


@router.message(StateFilter(StartRouteStates.IsItMilitaryServiceCase), F.text == "Нет")
async def start_route(msg: types.Message, state: FSMContext):
    await msg.answer("В отношении Вас подан иск?")
    await state.set_state(States.IsItCounterclaim)


@router.message(StateFilter(States.IsItCounterclaim), F.text == "Да")
async def is_it_counterclaim_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Обратитесь в суд, в который подан изначальный иск")
    await state.set_state(None)


@router.message(StateFilter(States.IsItCounterclaim), F.text == "Нет")
async def is_it_counterclaim_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с резулььтатами интеллектуальной деятельности?")
    await state.set_state(States.IsItIntellectualCase)


@router.message(StateFilter(States.IsItIntellectualCase), F.text == "Что это?")
async def is_it_counterclaim_what_is_it(msg: types.Message, state: FSMContext):
    await msg.answer("")  # TODO расписать текстик для дурашек
