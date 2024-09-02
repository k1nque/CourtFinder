from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from exts.states import TerritoryRouteStates as States
from exts.states import HierarchyRouteStates
from exts.states import FinalStates
from exts.enums import CourtType, GeneralCourtType


router = Router()

# Transition from Hierarchy Route


async def send_first_msg(msg: Message, state: FSMContext):
    await msg.answer("земельные участки, недра, объекты связанные с землей")
    await state.set_state(States.LandPlots)


@router.message(StateFilter(HierarchyRouteStates.IsItInheritanceOrIP), F.text == "Нет")
@router.message(StateFilter(HierarchyRouteStates.IsItRightCase), F.text == "Да")
@router.message(StateFilter(HierarchyRouteStates.ZPP_Less100K), F.text == "Да")
async def by_magistrate_court(msg: Message, state: FSMContext):
    await state.update_data({
        "court_l0": CourtType.General,
        "court_l1": GeneralCourtType.Magistrate
    })
    await send_first_msg(msg, state)
    

@router.message(StateFilter(HierarchyRouteStates.IsItInheritanceOrIP), F.text == "Да")
@router.message(StateFilter(HierarchyRouteStates.ZPP_Less100K), F.text == "Нет")
@router.message(StateFilter(HierarchyRouteStates.IsItTopSecret), F.text == "Нет")
@router.message(StateFilter(HierarchyRouteStates.IsItSubjectOrMunicipal), F.text == "Нет")
async def by_district_court(msg: Message, state: FSMContext):
    await state.update_data({
        "court_l0": CourtType.General,
        "court_l1": GeneralCourtType.District
    })
    await send_first_msg(msg, state)


@router.message(StateFilter(HierarchyRouteStates.IsItTopSecret), F.text == "Да")
@router.message(StateFilter(HierarchyRouteStates.IsItSubjectOrMunicipal), F.text == "Да")
async def by_subject_court(msg: Message, state: FSMContext):
    await state.update_data({
        "court_l0": CourtType.General,
        "court_l1": GeneralCourtType.Subject
    })
    await send_first_msg(msg, state)


@router.message(StateFilter(HierarchyRouteStates.IsItLess50K), F.text == "Да")
async def is_it_less50k_yes(msg: Message, state: FSMContext):
    # db = DB.getInstance()
    # user = db.find_by_userid(msg.from_user.id)
    data = await state.get_data()
    print(type(data["isIntellectual"]))
    if data["isIntellectual"]:
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
async def land_plots_yes(msg: Message, state: FSMContext):
    await msg.answer("Укажите адрес земельного участка")
    # TODO Вывод финального ответа

@router.message(StateFilter(States.LandPlots), F.text == "Нет")
async def land_plots_no(msg: Message, state: FSMContext):
    await msg.answer("Иски кредиторов наследодателя, предъявляемые до принятия наследства наследниками")
    await state.set_state(States.CreditorsClaim)


@router.message(StateFilter(States.CreditorsClaim), F.text == "Да")
async def creditors_claim_yes(msg: Message, state: FSMContext):
    await msg.answer("Укажите место открытия наследования")
    # TODO Вывод финального ответа


@router.message(StateFilter(States.CreditorsClaim), F.text == "Нет")
async def creditors_claim_no(msg: Message, state: FSMContext):
    await msg.answer("Иск в защиту группы лиц?")
    await state.set_state(States.DefenseGroup)


@router.message(StateFilter(States.DefenseGroup), F.text == "Да")
async def defense_group_yes(msg: Message, state: FSMContext):
    await msg.answer("Укажите адрес ответчика")
    # TODO Вывод финального ответа


@router.message(StateFilter(States.DefenseGroup), F.text == "Нет")
async def defense_group_no(msg: Message, state: FSMContext):
    await msg.answer("Спор следует из договора?")
    await state.set_state(States.ContractDispute)


@router.message(StateFilter(States.ContractDispute), F.text == "Да")
async def contract_dispute_yes(msg: Message, state: FSMContext):
    await msg.answer("Перевозка?")
    await state.set_state(States.Transportation)


@router.message(StateFilter(States.ContractDispute), F.text == "Нет")
async def contract_dispute_no(msg: Message, state: FSMContext):
    await msg.answer("возмещении вреда, причиненного увечьем, иным повреждением здоровья или в результате смерти кормильца")
    await state.set_state(States.DamageCompensation)


@router.message(StateFilter(States.Transportation), F.text == "Да")
async def transportation_yes(msg: Message, state: FSMContext):
    await msg.answer("Укажите адрес перевозчика")
    # TODO Вывод финального ответа


@router.message(StateFilter(States.Transportation), F.text == "Нет")
async def transportation_no(msg: Message, state: FSMContext):
    await msg.answer("Подсудность определена договором?")
    await state.set_state(States.ContractDeterminedJurisdiction)


@router.message(StateFilter(States.DamageCompensation), F.text == "Да")
async def damage_compensation(msg: Message, state: FSMContext):
    await msg.answer("Укажите ваше (любое):\nМесто жительства\nМесто причинения вреда\nАдрес ответчика")
    await state.set_state(FinalStates.AddressInput)


@router.message(StateFilter(States.DamageCompensation), F.text == "Нет")
async def damage_compensation_no(msg: Message, state: FSMContext):
    await msg.answer("Спор связан с алиментами или установлением отцовства?")
    await state.set_state(States.Alimony)


@router.message(StateFilter(States.ContractDeterminedJurisdiction), F.text == "Да")
async def contract_determined_jurisdiction_yes(msg: Message, state: FSMContext):
    await msg.answer("Рекомендуем обратить внимание на суд указанный в договоре")
    # TODO Clear state


@router.message(StateFilter(States.ContractDeterminedJurisdiction), F.text == "Нет")
async def contract_determined_jurisdiction_no(msg: Message, state: FSMContext):
    await msg.answer("Указано место исполнения?")
    await state.set_state(States.AddressSpecified)


@router.message(StateFilter(States.Alimony), F.text == "Да")
@router.message(StateFilter(States.LaborRightsProtection), F.text == "Да")
@router.message(StateFilter(States.ConsumerProtection), F.text == "Да")
@router.message(StateFilter(States.PersonalData), F.text == "Да")
async def alimony_yes(msg: Message, state: FSMContext):
    await msg.answer("Укажите ваше место жительства или адрес ответчика")
    # TODO Вывод финального ответа


@router.message(StateFilter(States.Alimony), F.text == "Нет")
async def alimony_no(msg: Message, state: FSMContext):
    await msg.answer("Дело связано с столкновением судов?")
    await state.set_state(States.ShipsColision)


@router.message(StateFilter(States.AddressSpecified), F.text == "Да")
async def address_specified_yes(msg: Message, state: FSMContext):
    await msg.answer("Укажите место исполнения или адрес ответчика")
    # TODO Вывод финального ответа

@router.message(StateFilter(States.ShipsColision), F.text == "Нет")
@router.message(StateFilter(States.AddressSpecified), F.text == "Нет")
async def labor_rights_protection(msg: Message, state: FSMContext):
    await msg.answer("Спор связан с защитой трудовых прав?")
    await state.set_state(States.LaborRightsProtection)


@router.message(StateFilter(States.ShipsColision), F.text == "Да")
async def ships_collision(msg: Message, state: FSMContext):
    await msg.answer("Укажите место нахождения судна ответчика или порта приписки судна / адрес ответчика")
    # TODO Вывод финального ответа
    

@router.message(StateFilter(States.LaborRightsProtection), F.text == "Нет")
async def labor_rights_protection_no(msg: Message, state: FSMContext):
    await msg.answer("Спор связан с защитой прав потребителей?")
    await state.set_state(States.ConsumerProtection)
    
    
@router.message(StateFilter(States.ConsumerProtection), F.text == "Нет")
async def consumer_protection_no(msg: Message, state: FSMContext):
    await msg.answer("Спор связан с персональными данными?")
    await state.set_state(States.BranchActivities)
    
    
@router.message(StateFilter(States.BranchActivities), F.text == "Да")
async def branch_activities_yes(msg: Message, state: FSMContext):
    await msg.answer("Укажите адрес филиала или адрес ответчика")
    # TODO Вывод финального ответа
    

@router.message(StateFilter(States.BranchActivities), F.text == "Нет")
async def branch_activities_no(msg: Message, state: FSMContext):
    await msg.answer("Ответчик имеет место жительства в РФ?")
    await state.set_state(States.RF_Residence)
    
    
@router.message(StateFilter(States.BranchActivities), F.text == "Что это?")
async def branch_activities_what_is_it(msg: Message, state: FSMContext):
    # TODO What is it
    pass


@router.message(StateFilter(States.RF_Residence), F.text == "Да")
async def rf_residence_yes(msg: Message, state: FSMContext):
    await msg.answer("Укажите адрес ответчика")
    # TODO Вывод финального ответа
    
    
@router.message(StateFilter(States.RF_Residence), F.text == "Нет")
async def rf_residence_no(msg: Message, state: FSMContext):
    await msg.answer("Укажите последнее место жительства в РФ или адрес нахождения имущества")
    # TODO Вывод финального ответа