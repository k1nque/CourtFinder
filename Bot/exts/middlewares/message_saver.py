from typing import Any
from aiogram import BaseMiddleware

from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class MessageSaver(BaseMiddleware):
    async def __call__(self, handler, event, data):
        fsm_context: FSMContext | None = data["state"]

        msg: Message | Any = await handler(event, data)
        if type(msg) is Message and fsm_context:
            print("jopa")
            fsm_data = await fsm_context.get_data()
            if "message_history" not in fsm_data:
                await fsm_context.update_data({"message_history": [msg.text]})
            else:
                await fsm_context.update_data({"message_history": fsm_data["message_history"] + [msg.text]})

        return msg

