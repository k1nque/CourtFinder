from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from Keyboards.keyboards_markups import DefaultKB, WA_KB

from exts.states import StartRouteStates as States

router = Router()


@router.message(StateFilter(None), Command("start_test"))
async def start_test(msg: Message, state: FSMContext):
    await state.set_state(States.IsItCriminalCase)
    return await msg.answer("Есть ли нарушение в УК?", reply_markup=DefaultKB)


@router.message(StateFilter(States.IsItCriminalCase), F.text == "Да")
async def is_it_criminal_case_yes(msg: Message, state: FSMContext):
    await state.set_state(None)
    return await msg.answer("Рекомендуем Вам обратиться в иной правоохранительный орган (иди в полицию, дурашка)")


@router.message(StateFilter(States.IsItCriminalCase), F.text == "Нет")
async def is_it_criminal_case_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsItTreteyCourt)
    return await msg.answer("Слышали ли Вы о третейских судах?")


@router.message(StateFilter(States.IsItTreteyCourt), F.text == "Нет")
async def is_it_tretey_court_no(msg: Message, state: FSMContext):
    await state.set_state(States.WasCaseBefore)
    return await msg.answer("дело рассмкатривалось в суде ранее?")


@router.message(StateFilter(States.WasCaseBefore), F.text == "Да")
async def was_case_before_yes(msg: Message, state: FSMContext):
    await state.set_state(States.IsItRussianCourt)
    return await msg.answer("Это был российский суд?")


@router.message(StateFilter(States.WasCaseBefore), F.text == "Нет")
async def was_case_before_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsItMilitaryServiceCase)
    return await msg.answer("Спор связан с военной службой?")

