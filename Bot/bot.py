from Handlers import router

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message', 'callback_query']

logging.basicConfig(level=logging.INFO)

# storage = SQLiteStorage(db_path="database.db")
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())
