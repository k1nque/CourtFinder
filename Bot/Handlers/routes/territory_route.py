from stat import SF_APPEND
from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from exts.states import TerritoryRouteStates as States
from exts.states import HierarchyRouteStates
from exts.enums import CourtType, GeneralCourtType

from db import DB


router = Router()

# Transition from Hierarchy Route

async def set_court(
        id: int,
        court_l0: str,
        court_l1: str
):
    db = DB.getInstance()
    db.update_user(
        id,
        court_l0=CourtType.General,
        court_l1=GeneralCourtType.District
    )


async def send_first_msg(msg: types.Message, state: FSMContext):
    await msg.answer("земельные участки, недра, объекты связанные с землей")
    await state.set_state(States.LandPlots)


@router.message(StateFilter(HierarchyRouteStates.IsItInheritanceOrIP), F.text == "Нет")
@router.message(StateFilter(HierarchyRouteStates.IsItRightCase), F.text == "Да")
@router.message(StateFilter(HierarchyRouteStates.ZPP_Less100K), F.text == "Да")
async def by_magistrate_court(msg: types.Message, state: FSMContext):
    await set_court(
        msg.from_user.id,
        court_l0=CourtType.General,
        court_l1=GeneralCourtType.Magistrate
    )
    await send_first_msg(msg, state)


@router.message(StateFilter(HierarchyRouteStates.IsItInheritanceOrIP), F.text == "Да")
@router.message(StateFilter(HierarchyRouteStates.ZPP_Less100K), F.text == "Нет")
@router.message(StateFilter(HierarchyRouteStates.IsItTopSecret), F.text == "Нет")
@router.message(StateFilter(HierarchyRouteStates.IsItSubjectOrMunicipal), F.text == "Нет")
async def by_district_court(msg: types.Message, state: FSMContext):
    await set_court(
        msg.from_user.id,
        court_l0=CourtType.General,
        court_l1=GeneralCourtType.Magistrate
    )
    await send_first_msg(msg, state)


@router.message(StateFilter(HierarchyRouteStates.IsItTopSecret), F.text == "Да")
@router.message(StateFilter(HierarchyRouteStates.IsItSubjectOrMunicipal), F.text == "Да")
async def by_subject_court(msg: types.Message, state: FSMContext):
    await set_court(
        msg.from_user.id,
        court_l0=CourtType.General,
        court_l1=GeneralCourtType.Subject
    )
    await send_first_msg(msg, state)


@router.message(StateFilter(HierarchyRouteStates.IsItLess50K), F.text == "Да")
async def is_it_less50k_yes(msg: types.Message, state: FSMContext):
    db = DB.getInstance()
    user = db.find_by_userid(msg.from_user.id)
    # print(user)
    if user and user["isIntellectual"]:
        await set_court(
            msg.from_user.id,
            CourtType.General,
            GeneralCourtType.District
        )
        await send_first_msg(msg, state)
    else:
        await msg.answer(
            "Это наследственный спор?"
        )  # TODO посмотреть ответ на вопрос связан ли спор с интеллектуалкой, ответ аналогичен ответу про наследство
        await state.set_state(HierarchyRouteStates.IsItInheritanceOrIP)  # TODO вывод Мировой/районный суд


# The end of transition from Hierarchy Route

"""
---------------------------------------------------------------------------------------------------------
"""

@router.message(StateFilter(States.LandPlots), F.text == "Да")
async def land_plots_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес земельного участка")
    # TODO Вывод финального ответа

@router.message(StateFilter(States.LandPlots), F.text == "Да")
async def land_plots_no(msg: types.Message, state: FSMContext):
    await msg.answer("Иски кредиторов наследодателя, предъявляемые до принятия наследства наследниками")
    await state.set_state(States.CreditorsClaim)


@router.message(StateFilter(States.CreditorsClaim), F.text == "Да")
async def creditors_claim_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите место открытия наследования")
    # TODO Вывод финального ответа


@router.message(StateFilter(States.CreditorsClaim), F.text == "Нет")
async def creditors_claim_no(msg: types.Message, state: FSMContext):
    await msg.answer("Иск в защиту группы лиц?")
    await state.set_state(States.DefenseGroup)


@router.message(StateFilter(States.DefenseGroup), F.text == "Да")
async def defense_group_yes(msg: types.Message, state: FSMContext):
    await msg.answer("Укажите адрес ответчика")
    # TODO Вывод финального ответа


@router.message(StateFilter(States.DefenseGroup), F.text == "Нет")
async def defense_group_no(msg: types.Message, state: FSMContext):
    await msg.answer("Спор следует из договора?")
    await state.set_state(States.ContractDispute)
