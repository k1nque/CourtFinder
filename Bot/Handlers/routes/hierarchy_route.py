from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from .choice_route import ChoiceRouteStates
from db import DB
from exts.enums import CourtType


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

    # TODO начало мышь
@HierarchyRouter.message(StateFilter(ChoiceRouteStates.AreYou_ULOrIP), F.text == "Нет")
async def are_you_ul_or_ip_no(msg: types.Message, state: FSMContext):
    await against_federal_body(msg, state)


@HierarchyRouter.message(StateFilter(ChoiceRouteStates.IsItEconomicalCase), F.text == "Нет")
async def is_it_economical_case_no(msg: types.Message, state: FSMContext):
    await against_federal_body(msg, state)
    

async def against_federal_body(msg: types.Message, state: FSMContext):
    db = DB.getInstance()
    db.update_user(
        msg.from_user.id,
        court_type=CourtType.General
    )
    await msg.answer("Оспаривание решения гос. органа?")
    await state.set_state(HierarchyRouteStates.IsYourDefendentCountry)


@HierarchyRouter.message(StateFilter(ChoiceRouteStates.IsYourDefendentCountry), F.text == "Нет")
async def chioce2marriage(msg: types.Message, state: FSMContext):
    db = DB.getInstance()
    db.update_user(
        msg.from_user.id,
        court_type=CourtType.General
    )
    await is_your_defendent_country_no(msg, state)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsYourDefendentCountry), F.text == "Да")
async def is_it_federal(msg: types.Message, state: FSMContext):
    await msg.answer("Оспаривается решение федерального органа?")
    await state.set_state(HierarchyRouteStates.IsItFederal)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsYourDefendentCountry), F.text == "Что это?")
async def is_it_federal_what_is_it(msg: types.Message, state: FSMContext):
    await msg.answer()  # TODO


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItFederal), F.text == "Да")
async def is_it_federal_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Верховный Суд")
    await state.set_state(None)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItFederal), F.text == "Нет")
async def is_it_federal_no(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Оспариваются решения органов государственной власти субъектов и представительств муниципальных образований?"
    )
    await state.set_state(HierarchyRouteStates.IsItSabjectOrmunicipal)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsYourDefendentCountry), F.text == "Нет")
async def is_your_defendent_country_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с расторжением брака?")
    await state.set_state(HierarchyRouteStates.IsItdivorce)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItdivorce), F.text == "Да")
async def is_it_divorce_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Есть  ли спор о несовершеннолетних детях?")
    await state.set_state(HierarchyRouteStates.IsItChildrenCase)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItdivorce), F.text == "Нет")
async def is_it_divorce_no(msg: types.Message, state: FSMContext):
    await msg.answer("Вы хотите вернуть сумму до 50 тысяч рублей?")
    await state.set_state(HierarchyRouteStates.IsItLess50K)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItLess50K), F.text == "Нет")
async def is_it_less_50k_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор о защите прав потребителей?")
    await state.set_state(HierarchyRouteStates.ZPP)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItLess50K), F.text == "Да")
async def is_it_less50k_yes(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Это наследственный спор?"
    )  # TODO посмотреть ответ на вопрос связан ли спор с интеллектуалкой, ответ аналогичен ответу про наследство
    await state.set_state(HierarchyRouteStates.IsItinheritanceOrIP)  # TODO вывод Мировой/районный суд


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.ZPP), F.text == "Нет")
async def ZPP_no(msg: types.Message, state: FSMContext):
    await msg.answer("Это спор о праве?")
    await state.set_state(HierarchyRouteStates.IsItRightCase)


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.ZPP), F.text == "Да")
async def ZPP_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Спор меньше 100 тысяч рублей?")
    await state.set_state(HierarchyRouteStates.ZPP_Less100K)  # TODO выходит в вывод


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItRightCase), F.text == "Что это?")
async def is_it_right_case_what_is_it(msg: types.Message, state: FSMContext):
    await msg.answer  # TODO


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItRightCase), F.text == "Да?")
async def is_it_right_case_yes(msg: types.Message, state: FSMContext):
    await msg.answer  # TODO вывод


@HierarchyRouter.message(StateFilter(HierarchyRouteStates.IsItRightCase), F.text == "Нет")
async def is_it_right_case_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор связан с государственной тайной?")
    await state.set_state(HierarchyRouteStates.IsItTopSecret)

    # TODO вывод
