from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from .routes import router as routes_router


router = Router()
router.include_router(routes_router)


@router.message(Command("clear_state"))
async def clear_state(msg: Message, state: FSMContext):
    await state.set_state(None)
    data = await state.get_data()
    address = data.get("address")
    await state.clear()
    if address:
        await state.set_data({"address": address})


@router.message(F.text == "Назад")
async def back(msg: Message, state: FSMContext):
    data = await state.get_data()
    if "message_history" in data and "state_history" in data:
        message_history: list[str] = data["message_history"]
        state_history: list[str] = data["state_history"]
        try:
            await state.set_state(state_history.pop())
            message_history.pop()
            await msg.answer(message_history[-1])
            await state.update_data({"message_history": message_history, "state_history": state_history})
        except IndexError:
            await msg.answer("Вы не можете вернуться назад")
    else:
        await msg.answer("Вы не можете вернуться назад")
