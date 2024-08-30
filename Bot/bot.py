from Handlers import router

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.mongo import MongoStorage

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message', 'callback_query']

logging.basicConfig(level=logging.INFO)

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")

storage = MongoStorage.from_url(url=f"mongodb://{MONGO_HOST}:{MONGO_PORT}/bot", db_name="bot", collection_name="users")
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(storage=storage)

dp.include_router(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())
