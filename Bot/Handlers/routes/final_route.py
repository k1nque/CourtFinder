from exts.states import FinalStates as States
from exts.states import ForeignRouteStates
from exts.funcs import get_suggestions, find_court
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from Keyboards.inline_keyboards import get_suggestion_kb

router = Router()


@router.message(StateFilter(States.AddressInput))
@router.message(StateFilter(ForeignRouteStates.DebtorsAddress))
@router.message(StateFilter(ForeignRouteStates.DebtorsProperyAddress))
async def suggest(msg: Message, state: FSMContext):
    if msg.text:
        data = await get_suggestions(msg.text)
        suggestions = [val for val in data if val.get("fias")]
        print(suggestions)
        if suggestions is None or len(suggestions) == 0:
            await msg.answer("Адрес не найден. Введите корректный адрес. В случае корректного адреса, уточните его (укажите населенный пункт)")
        else:
            await state.update_data({
                "suggestions": suggestions
            })
            kb = get_suggestion_kb(suggestions)
            await msg.answer(text="Выберете подходящий адрес", reply_markup=kb)
            await state.set_state(States.SuggestionChoice)
    else:
        return await msg.answer("Введите корректный адрес")
        
        
@router.callback_query(StateFilter(States.SuggestionChoice))
async def recieve_info(callback: CallbackQuery, state: FSMContext):
    if callback.data:
        court = await find_court(callback.data, state)
        if court is None or len(court) == 0:
            await callback.message.answer("Адрес не найден в базе sudrf. Введите ближайщий адрес на соседней крупной улице.")
            await state.set_state(States.AddressInput)
        else:
            await callback.message.answer(
                f"Название суда: {court["NAME"]}\n"
                f"Адрес суда: {court["ADDRESS"]}\n"
                f"Ссылка на сайт суда: {court["LINK"]}"
            )
    await callback.answer()
