from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from exts.enums import CourtType, GeneralCourtType, ArbitrationCourtTypes
from exts.states import ForeignRouteStates as States
from exts.states import StartRouteStates
from exts.funcs import get_suggestions
from Keyboards.inline_keyboards import get_foreign_address_kb, get_suggestion_kb


router = Router()


@router.message(StateFilter(StartRouteStates.IsItRussianCourt), F.text == "Нет")
async def is_it_not_russian_court(msg: Message, state: FSMContext):
    await msg.answer("Связан ли спор с предпринимательской или другой экономической деятельностью")
    await state.set_state(States.BusinessEconomicActivity)
    

@router.message(StateFilter(States.BusinessEconomicActivity))
async def get_debtors_address(msg: Message, state: FSMContext):
    match msg.text:
        case "Да":
            await state.update_data({
                "court_l0": CourtType.Arbitration,
                "court_l1": ArbitrationCourtTypes.Subject   
            })
        case "Нет":
            await state.update_data({
                "court_l0": CourtType.General,
                "court_l1": GeneralCourtType.Subject
            })
            
    await msg.answer("Укажите адрес должника", reply_markup=get_foreign_address_kb())
    await state.set_state(States.DebtorsAddress)
    

@router.callback_query(StateFilter(States.DebtorsAddress), F.data == "unknown_addr")
async def unknown_debtors_adress(data: CallbackQuery, state: FSMContext):
    msg = data.message
    await data.message.answer("Укажите адрес имущества должника")
    await state.set_state(States.DebtorsProperyAddress)
    await data.answer()


# @router.message(StateFilter(States.DebtorsAddress))
# @router.message(StateFilter(States.DebtorsProperyAddress))
# async def get_suggestions_handler(msg: Message, state: FSMContext):
#     if msg.text:
#         suggs = await get_suggestions(msg.text)
#         kb = get_suggestion_kb(suggs)
#         await msg.answer(text="Выберете подходящий адрес", reply_markup=kb)
#         await state.set_state(States.Suggestions)
        
        
# @router.callback_query(StateFilter(States.Suggestions))
# async def get_court_answer()
