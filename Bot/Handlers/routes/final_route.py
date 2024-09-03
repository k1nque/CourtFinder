from exts.states import FinalStates as States
from exts.funcs import get_suggestions, find_court
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from Keyboards.inline_keyboards import get_suggestion_kb

router = Router()


@router.message(StateFilter(States.AddressInput))
async def suggest(msg: Message, state: FSMContext):
    if msg.text:
        # try:
        data = await get_suggestions(msg.text)
        kb = get_suggestion_kb(data)
        await state.set_state(States.SuggestionChoice)
        return await msg.answer("Выберете подходящий адрес", reply_markup=kb)
        # except Exception as ex:
        #     # await msg.answer("Что-то пошло не так, введите корректный адрес")
        #     await msg.answer(str(ex)
    else:
        return await msg.answer("Введите корректный адрес")
        
        
@router.callback_query(StateFilter(States.SuggestionChoice))
async def recieve_info(callback: CallbackQuery, state: FSMContext):
    if callback.data:
        court = await find_court(callback.data, state)
        await callback.answer()
        return await callback.message.answer(
            f"Название суда: {court["NAME"]}\n"
            f"Адрес суда: {court["ADDRESS"]}\n"
            f"Ссылка на сайт суда: {court["LINK"]}"
        )
