from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from exts.states import StartRouteStates, MilitaryRouteStates
from exts.states import TwoQuestionsRouteStates as States


router = Router()


@router.message(StateFilter(StartRouteStates.IsItMilitaryServiceCase), F.text == "Нет")
@router.message(StateFilter(MilitaryRouteStates.ActionDispute), F.text == "Нет")
async def start_route(msg: Message, state: FSMContext):
    await state.set_state(States.IsItCounterclaim)
    return await msg.answer("В отношении Вас подан иск?")


@router.message(StateFilter(States.IsItCounterclaim), F.text == "Да")
async def is_it_counterclaim_yes(msg: Message, state: FSMContext):
    await state.set_state(None) # TODO Clear state
    return await msg.answer("Обратитесь в суд, в который подан изначальный иск")


@router.message(StateFilter(States.IsItCounterclaim), F.text == "Нет")
async def is_it_counterclaim_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsItIntellectualCase)
    return await msg.answer("Спор связан с резулььтатами интеллектуальной деятельности?")


@router.message(StateFilter(States.IsItIntellectualCase), F.text == "Что это?")
async def is_it_counterclaim_what_is_it(msg: Message, state: FSMContext):
    await msg.answer("")  # TODO расписать текстик для дурашек
