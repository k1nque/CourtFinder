from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from db import DB

from exts.enums import CourtType
from exts.states import HierarchyRouteStates as States
from exts.states import ChoiceRouteStates


router = Router()


@router.message(StateFilter(ChoiceRouteStates.AreYou_ULOrIP), F.text == "Нет")
async def are_you_ul_or_ip_no(msg: types.Message, state: FSMContext):
    await against_federal_body(msg, state)


@router.message(StateFilter(ChoiceRouteStates.IsItEconomicalCase), F.text == "Нет")
async def is_it_economical_case_no(msg: types.Message, state: FSMContext):
    await against_federal_body(msg, state)


async def against_federal_body(msg: types.Message, state: FSMContext):
    db = DB.getInstance()
    db.update_user(
        msg.from_user.id,
        court_type=CourtType.General
    )
    await msg.answer("Оспаривание решения гос. органа?")
    await state.set_state(States.IsYourDefendentCountry)


@router.message(StateFilter(ChoiceRouteStates.IsYourDefendentCountry), F.text == "Нет")
async def chioce2marriage(msg: types.Message, state: FSMContext):
    db = DB.getInstance()
    db.update_user(
        msg.from_user.id,
        court_type=CourtType.General
    )
    await is_your_defendent_country_no(msg, state)


@router.message(StateFilter(States.IsYourDefendentCountry), F.text == "Да")
async def is_it_federal(msg: types.Message, state: FSMContext):
    await msg.answer("Оспаривается решение федерального органа?")
    await state.set_state(States.IsItFederal)


@router.message(StateFilter(States.IsYourDefendentCountry), F.text == "Что это?")
async def is_it_federal_what_is_it(msg: types.Message, state: FSMContext):
    await msg.answer()  # TODO


@router.message(StateFilter(States.IsItFederal), F.text == "Да")
async def is_it_federal_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Верховный Суд")
    await state.set_state(None)


@router.message(StateFilter(States.IsItFederal), F.text == "Нет")
async def is_it_federal_no(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Оспариваются решения органов государственной власти субъектов и представительств муниципальных образований?"
    )
    await state.set_state(States.IsItSubjectOrMunicipal)


@router.message(StateFilter(States.IsYourDefendentCountry), F.text == "Нет")
async def is_your_defendent_country_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с расторжением брака?")
    await state.set_state(States.IsItDivorce)


@router.message(StateFilter(States.IsItDivorce), F.text == "Да")
async def is_it_divorce_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Есть ли спор о несовершеннолетних детях?")
    await state.set_state(States.IsItChildrenCase)


@router.message(StateFilter(States.IsItDivorce), F.text == "Нет")
async def is_it_divorce_no(msg: types.Message, state: FSMContext):
    await msg.answer("Вы хотите вернуть сумму до 50 тысяч рублей?")
    await state.set_state(States.IsItLess50K)


@router.message(StateFilter(States.IsItLess50K), F.text == "Нет")
async def is_it_less_50k_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор о защите прав потребителей?")
    await state.set_state(States.ZPP)


@router.message(StateFilter(States.ZPP), F.text == "Нет")
async def ZPP_no(msg: types.Message, state: FSMContext):
    await msg.answer("Это спор о праве?")
    await state.set_state(States.IsItRightCase)


@router.message(StateFilter(States.ZPP), F.text == "Да")
async def ZPP_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Спор меньше 100 тысяч рублей?")
    await state.set_state(States.ZPP_Less100K)  # TODO выходит в вывод


@router.message(StateFilter(States.IsItRightCase), F.text == "Что это?")
async def is_it_right_case_what_is_it(msg: types.Message, state: FSMContext):
    await msg.answer  # TODO


@router.message(StateFilter(States.IsItRightCase), F.text == "Нет")
async def is_it_right_case_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с государственной тайной?")
    await state.set_state(States.IsItTopSecret)

    # TODO вывод
