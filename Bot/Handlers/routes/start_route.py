from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router
from dotenv import dotenv_values
from db import DB
from Keyboards.keyboards_markups import DefaultKB, WA_KB

StartRouter = Router()


class StartRouteStates(StatesGroup):
    IsItCriminalCase = State()
    IsItTreteyCourt = State()
    WasCaseBefore = State()
    IsItMilitaryServiceCase = State()
    IsItRussianCourt = State()


@StartRouter.message(Command("clear_state"))
async def clear_state(msg: types.Message, state: FSMContext):
    await state.set_state(None)


@StartRouter.message(StateFilter(None), Command("start_test"))
async def start_test(msg: types.Message, state: FSMContext):
    db = DB.getInstance()
    db.create_user(msg.from_user.id)
    await msg.answer("Есть ли нарушение в УК?", reply_markup=DefaultKB)
    await state.set_state(StartRouteStates.IsItCriminalCase)


@StartRouter.message(StateFilter(StartRouteStates.IsItCriminalCase), F.text == "Да")
async def is_it_criminal_case_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Рекомендуем Вам обратиться в иной правоохранительный орган (иди в полицию, дурашка)")
    await state.set_state(None)


@StartRouter.message(StateFilter(StartRouteStates.IsItCriminalCase), F.text == "Нет")
async def is_it_criminal_case_no(msg: types.Message, state: FSMContext):
    await msg.answer("Слышали ли Вы о третейских судах?")
    await state.set_state(StartRouteStates.IsItTreteyCourt)


@StartRouter.message(StateFilter(StartRouteStates.IsItTreteyCourt), F.text == "Нет")
async def is_it_tretey_court_no(msg: types.Message, state: FSMContext):
    await msg.answer("дело рассмкатривалось в суде ранее?")
    await state.set_state(StartRouteStates.WasCaseBefore)


@StartRouter.message(StateFilter(StartRouteStates.WasCaseBefore), F.text == "Да")
async def was_case_before_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Это был российский суд?")
    await state.set_state(StartRouteStates.IsItRussianCourt)


@StartRouter.message(StateFilter(StartRouteStates.WasCaseBefore), F.text == "Нет")
async def was_case_before_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с военной службой?")
    await state.set_state(StartRouteStates.IsItMilitaryServiceCase)

