from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from exts.enums import CourtType
from exts.states import HierarchyRouteStates as States
from exts.states import ChoiceRouteStates


router = Router()


@router.message(StateFilter(ChoiceRouteStates.AreYou_ULOrIP), F.text == "Нет")
@router.message(StateFilter(ChoiceRouteStates.IsItEconomicalCase), F.text == "Нет")
async def against_federal_body(msg: Message, state: FSMContext):
    await state.set_state(States.IsYourDefendentCountry)
    await state.update_data({"court_l0": CourtType.General})
    return await msg.answer("Оспаривание решения гос. органа?")


@router.message(StateFilter(ChoiceRouteStates.IsYourDefendentCountry), F.text == "Нет")
async def chioce2marriage(msg: Message, state: FSMContext):
    await state.update_data({"court_l0": CourtType.General})
    return await is_your_defendent_country_no(msg, state)


@router.message(StateFilter(States.IsYourDefendentCountry), F.text == "Да")
async def is_it_federal(msg: Message, state: FSMContext):
    await state.set_state(States.IsItFederal)
    return await msg.answer("Оспаривается решение федерального органа?")


@router.message(StateFilter(States.IsYourDefendentCountry), F.text == "Что это?")
async def is_it_federal_what_is_it(msg: Message, state: FSMContext):
    return await msg.answer()  # TODO


@router.message(StateFilter(States.IsItFederal), F.text == "Да")
async def is_it_federal_yes(msg: Message, state: FSMContext):
    await state.set_state(None)
    return await msg.answer("Верховный Суд")


@router.message(StateFilter(States.IsItFederal), F.text == "Нет")
async def is_it_federal_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsItSubjectOrMunicipal)
    return await msg.answer(
        "Оспариваются решения органов государственной власти субъектов и представительств муниципальных образований?"
    )


@router.message(StateFilter(States.IsYourDefendentCountry), F.text == "Нет")
async def is_your_defendent_country_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsItDivorce)
    return await msg.answer("Спор связан с расторжением брака?")


@router.message(StateFilter(States.IsItDivorce), F.text == "Да")
async def is_it_divorce_yes(msg: Message, state: FSMContext):
    await state.set_state(States.IsItChildrenCase)
    return await msg.answer("Есть ли спор о несовершеннолетних детях?")


@router.message(StateFilter(States.IsItDivorce), F.text == "Нет")
async def is_it_divorce_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsItLess50K)
    return await msg.answer("Вы хотите вернуть сумму до 50 тысяч рублей?")


@router.message(StateFilter(States.IsItLess50K), F.text == "Нет")
async def is_it_less_50k_no(msg: Message, state: FSMContext):
    await state.set_state(States.ZPP)
    return await msg.answer("Спор о защите прав потребителей?")


@router.message(StateFilter(States.ZPP), F.text == "Нет")
async def ZPP_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsItRightCase)
    return await msg.answer("Это спор о праве?")


@router.message(StateFilter(States.ZPP), F.text == "Да")
async def ZPP_yes(msg: Message, state: FSMContext):
    await state.set_state(States.ZPP_Less100K)  # TODO выходит в вывод
    return await msg.answer("Спор меньше 100 тысяч рублей?")


@router.message(StateFilter(States.IsItRightCase), F.text == "Что это?")
async def is_it_right_case_what_is_it(msg: Message, state: FSMContext):
    return await msg.answer()  # TODO


@router.message(StateFilter(States.IsItRightCase), F.text == "Нет")
async def is_it_right_case_no(msg: Message, state: FSMContext):
    await state.set_state(States.IsItTopSecret)
    return await msg.answer("Спор связан с государственной тайной?")

    # TODO вывод
