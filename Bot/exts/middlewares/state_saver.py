from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext


class StateSaver(BaseMiddleware):
    async def __call__(self, handler, event, data):
        fsm_context: FSMContext | None = data["state"]

        if fsm_context:
            state: str | None = await fsm_context.get_state()
            if state:
                fsm_data = await fsm_context.get_data()
                if "state_history" not in fsm_data:
                    await fsm_context.update_data({"state_history": [state]})
                else:
                    await fsm_context.update_data({"state_history": fsm_data["state_history"] + [state]})

        return await handler(event, data)
