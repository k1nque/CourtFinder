from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from exts.enums import CourtType, MilitaryCourtType
from exts.funcs import find_court
from exts.states import MilitaryRouteStates as States
from exts.states import StartRouteStates, FinalStates


router = Router()

@router.message(StateFilter(StartRouteStates.IsItMilitaryServiceCase), F.text == "Да")
async def is_it_military_service_case_yes(msg: Message, state: FSMContext):
    await msg.answer("Оспариваются действий (бездействия) органов военного управления, воинских должностных лиц и принятых ими решений?")
    await state.set_state(States.ActionDispute)
    
    
@router.message(StateFilter(States.ActionDispute), F.text == "Да")
async def actions_dispute_yes(msg: Message, state: FSMContext):
    await msg.answer("Акт федерального органа?")
    await state.set_state(States.FederalAgencyAct)
    

@router.message(StateFilter(States.FederalAgencyAct), F.text == "Нет")
async def federal_agency_act_no(msg: Message, state: FSMContext):
    await msg.answer("Спор связан с государственной тайной?")
    await state.set_state(States.StateSecret)
    
    
@router.message(StateFilter(States.FederalAgencyAct), F.text == "Да")
async def federal_agency_act_yes(msg: Message, state: FSMContext):
    await msg.answer("Верховный суд") # TODO Answer string for supreme court


@router.message(StateFilter(States.StateSecret), F.text == "Да")
async def state_secret_yes(msg: Message, state: FSMContext):
    await state.update_data({
        "court_l0": CourtType.Military,
        "court_l1": MilitaryCourtType.District
    })
    
    await msg.answer("Введите адрес вашего воинского формирования")
    await state.set_state(FinalStates.AddressInput)
    
    
@router.message(StateFilter(States.StateSecret), F.text == "Нет")
async def state_secret_no(msg: Message, state: FSMContext):
    await state.update_data({
        "court_l0": CourtType.Military,
        "court_l1": MilitaryCourtType.Garrison
    })
    
    await msg.answer("Введите адрес вашего воинского формирования")
    await state.set_state(FinalStates.AddressInput)