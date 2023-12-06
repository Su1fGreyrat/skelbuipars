from aiogram import Bot, Dispatcher

from database.data import BotDB
from handlers import keyword

from decouple import config
import asyncio
import logging

bot = Bot(token=config('TOKEN'))
dp = Dispatcher()

from handlers import selector

db = BotDB()

logging.basicConfig(level=logging.INFO)

async def main():
    dp.include_routers(keyword.router, selector.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    db.create_table()
    asyncio.run(main())