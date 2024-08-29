from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router
from db import DB
from Keyboards.keyboards_markups import DefaultKB, WA_KB

from exts.states import StartRouteStates as States

router = Router()



@router.message(Command("clear_state"))
async def clear_state(msg: types.Message, state: FSMContext):
    await state.set_state(None)


@router.message(StateFilter(None), Command("start_test"))
async def start_test(msg: types.Message, state: FSMContext):
    db = DB.getInstance()
    db.create_user(msg.from_user.id)
    await msg.answer("Есть ли нарушение в УК?", reply_markup=DefaultKB)
    await state.set_state(States.IsItCriminalCase)


@router.message(StateFilter(States.IsItCriminalCase), F.text == "Да")
async def is_it_criminal_case_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Рекомендуем Вам обратиться в иной правоохранительный орган (иди в полицию, дурашка)")
    await state.set_state(None)


@router.message(StateFilter(States.IsItCriminalCase), F.text == "Нет")
async def is_it_criminal_case_no(msg: types.Message, state: FSMContext):
    await msg.answer("Слышали ли Вы о третейских судах?")
    await state.set_state(States.IsItTreteyCourt)


@router.message(StateFilter(States.IsItTreteyCourt), F.text == "Нет")
async def is_it_tretey_court_no(msg: types.Message, state: FSMContext):
    await msg.answer("дело рассмкатривалось в суде ранее?")
    await state.set_state(States.WasCaseBefore)


@router.message(StateFilter(States.WasCaseBefore), F.text == "Да")
async def was_case_before_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Это был российский суд?")
    await state.set_state(States.IsItRussianCourt)


@router.message(StateFilter(States.WasCaseBefore), F.text == "Нет")
async def was_case_before_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с военной службой?")
    await state.set_state(States.IsItMilitaryServiceCase)

