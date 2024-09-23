from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from exts.states import RetrialRouteStates as States
from exts.states import StartRouteStates

router = Router()


@router.message(StateFilter(StartRouteStates.IsItRussianCourt), F.text == "Да")
async def it_is_russian_court(msg: Message, state: FSMContext):
    await msg.answer("Есть новые обстоятельства?")
    await state.set_state(States.NewCircumstances)
    
    
@router.message(StateFilter(States.NewCircumstances), F.text == "Нет")
async def new_circumstances_no(msg: Message, state: FSMContext):
    await msg.answer("Вступило ли решение в силу?")
    await state.set_state(States.DecisionInForce)
    
    
@router.message(StateFilter(States.DecisionInForce), F.text == "Да")
async def decision_in_force_yes(msg: Message, state: FSMContext):
    await msg.answer("Прошло ли 3 месяца с этого момента?")
    await state.set_state(States.ThreeMonthHavePassed)
    
    
@router.message(StateFilter(States.ThreeMonthHavePassed), F.text == "Да")
async def three_month_have_passed_yes(msg: Message, state: FSMContext):
    await msg.answer("Есть ли у вас уважительные причины для восстановления сроков?")
    await state.set_state(States.ValidReasons)
    

@router.message(StateFilter(States.ValidReasons), F.text == "Нет")
async def valid_reasons_no(msg: Message, state: FSMContext):
    await msg.answer("GG WP") # TODO
    # TODO The end
    
    
@router.message(StateFilter(States.DecisionInForce), F.text == "Нет")
@router.message(StateFilter(States.ThreeMonthHavePassed), F.text == "Нет")
@router.message(StateFilter(States.ValidReasons), F.text == "Да")
async def decision_in_force_no(msg: Message, state: FSMContext):
    match await state.get_state():
        case States.DecisionInForce:
            complaint = "аппеляционную жалобу"
        case States.ThreeMonthHavePassed:
            complaint = "кассационную жалобу"
        case States.ValidReasons:
            complaint = "заявление о восстановлении сроков"
        case _:
            complaint = ""
    
    await msg.answer(f"Вам следует подать {complaint} в суд вынесший решение")
    # TODO The end
    