from Handlers import router

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.mongo import MongoStorage

from settings import settings


ALLOWED_UPDATES = ['message', 'callback_query']

logging.basicConfig(level=logging.INFO)

storage = MongoStorage.from_url(
    url=settings.get_connection_string(),
    db_name="bot",
    collection_name="users"
)

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(storage=storage)

dp.include_router(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())
