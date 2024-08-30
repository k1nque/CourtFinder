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
    await msg.answer("Оспаривание решения гос. органа?")
    await state.set_state(States.IsYourDefendentCountry)
    await state.update_data({"court_l0": CourtType.General})


@router.message(StateFilter(ChoiceRouteStates.IsYourDefendentCountry), F.text == "Нет")
async def chioce2marriage(msg: Message, state: FSMContext):
    await state.update_data({"court_l0": CourtType.General})
    await is_your_defendent_country_no(msg, state)


@router.message(StateFilter(States.IsYourDefendentCountry), F.text == "Да")
async def is_it_federal(msg: Message, state: FSMContext):
    await msg.answer("Оспаривается решение федерального органа?")
    await state.set_state(States.IsItFederal)


@router.message(StateFilter(States.IsYourDefendentCountry), F.text == "Что это?")
async def is_it_federal_what_is_it(msg: Message, state: FSMContext):
    await msg.answer()  # TODO


@router.message(StateFilter(States.IsItFederal), F.text == "Да")
async def is_it_federal_yes(msg: Message, state: FSMContext):
    await msg.answer("Верховный Суд")
    await state.set_state(None)


@router.message(StateFilter(States.IsItFederal), F.text == "Нет")
async def is_it_federal_no(msg: Message, state: FSMContext):
    await msg.answer(
        "Оспариваются решения органов государственной власти субъектов и представительств муниципальных образований?"
    )
    await state.set_state(States.IsItSubjectOrMunicipal)


@router.message(StateFilter(States.IsYourDefendentCountry), F.text == "Нет")
async def is_your_defendent_country_no(msg: Message, state: FSMContext):
    await msg.answer("Спор связан с расторжением брака?")
    await state.set_state(States.IsItDivorce)


@router.message(StateFilter(States.IsItDivorce), F.text == "Да")
async def is_it_divorce_yes(msg: Message, state: FSMContext):
    await msg.answer("Есть ли спор о несовершеннолетних детях?")
    await state.set_state(States.IsItChildrenCase)


@router.message(StateFilter(States.IsItDivorce), F.text == "Нет")
async def is_it_divorce_no(msg: Message, state: FSMContext):
    await msg.answer("Вы хотите вернуть сумму до 50 тысяч рублей?")
    await state.set_state(States.IsItLess50K)


@router.message(StateFilter(States.IsItLess50K), F.text == "Нет")
async def is_it_less_50k_no(msg: Message, state: FSMContext):
    await msg.answer("Спор о защите прав потребителей?")
    await state.set_state(States.ZPP)


@router.message(StateFilter(States.ZPP), F.text == "Нет")
async def ZPP_no(msg: Message, state: FSMContext):
    await msg.answer("Это спор о праве?")
    await state.set_state(States.IsItRightCase)


@router.message(StateFilter(States.ZPP), F.text == "Да")
async def ZPP_yes(msg: Message, state: FSMContext):
    await msg.answer("Спор меньше 100 тысяч рублей?")
    await state.set_state(States.ZPP_Less100K)  # TODO выходит в вывод


@router.message(StateFilter(States.IsItRightCase), F.text == "Что это?")
async def is_it_right_case_what_is_it(msg: Message, state: FSMContext):
    await msg.answer  # TODO


@router.message(StateFilter(States.IsItRightCase), F.text == "Нет")
async def is_it_right_case_no(msg: Message, state: FSMContext):
    await msg.answer("Спор связан с государственной тайной?")
    await state.set_state(States.IsItTopSecret)

    # TODO вывод
