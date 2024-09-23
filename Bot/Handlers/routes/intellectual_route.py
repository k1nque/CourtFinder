from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from exts.states import TwoQuestionsRouteStates
from exts.states import IntellectualRouteStates as States


router = Router()


@router.message(StateFilter(TwoQuestionsRouteStates.IsItIntellectualCase), F.text == "Да")
async def is_it_intellectual_yes(msg: Message, state: FSMContext):
    await msg.answer("вы оспариваете нормативный акт?")
    await state.set_state(States.RegulationChallenging)


@router.message(StateFilter(States.RegulationChallenging), F.text == "Да")
async def regulation_challenging_yes(msg: Message, state: FSMContext):
    await msg.answer("Оспариваются акты ФОИП?")
    await state.set_state(States.FOIP)
    
    
@router.message(StateFilter(States.RegulationChallenging), F.text == "Нет")
async def regulation_challenging_no(msg: Message, state: FSMContext):
    await msg.answer("Спор связан с объектами авторских и смежных прав, топологиями интегральных микросхем")
    await state.set_state(States.Copyright)
    
    
@router.message(StateFilter(States.Copyright), F.text == "Нет")
async def copyright(msg: Message, state: FSMContext):
    await msg.answer("Досрочное прекращение охраны товарного знака?")
    await state.set_state(States.NotSatisfiedWithEntryInRegistry)
    

@router.message(StateFilter(States.NotSatisfiedWithEntryInRegistry), F.text == "Нет")
async def not_satisfied_with_entry_in_registry_no(msg: Message, state: FSMContext):
    await msg.answer("Вас не устраивает запись в реестре?")
    await state.set_state(States.Rospatent)
    
    
@router.message(StateFilter(States.TrademarkTermination), F.text == "Да")
@router.message(StateFilter(States.NotSatisfiedWithEntryInRegistry), F.text == "Да")
@router.message(StateFilter(States.FOIP), F.text == "Да")
@router.message(StateFilter(States.Rospatent), F.text == "Да")
async def SIP(msg: Message, state: FSMContext):
    await msg.answer("СИП") # TODO вывод СИП