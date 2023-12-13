from aiogram import Bot, Dispatcher

from database.data import BotDB
from handlers import keyword

from decouple import config
import multiprocessing
import asyncio
import logging

bot = Bot(token=config('TOKEN'))
dp = Dispatcher()

from handlers import selector, newsletter, user_cmd, request
import parsing

db = BotDB()

logging.basicConfig(level=logging.INFO, filename="Skelbui.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

async def start_bot():
    dp.include_routers(request.router, newsletter.router)
    await dp.start_polling(bot) 

def start_bot_sync():
    asyncio.run(start_bot())
    
def parser():
    asyncio.run(parsing.main())
    

async def main():
    p1 = multiprocessing.Process(target=start_bot_sync)
    p2 = multiprocessing.Process(target=parser)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

if __name__ == '__main__':
    db.create_table()
    asyncio.run(main())