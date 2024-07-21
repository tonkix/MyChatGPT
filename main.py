import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
import os

from app.handlers import router
from app.scheduler import send_message_cron_at_start
from app.scheduler import SchedulerMiddleware


load_dotenv()
# Включите логирование
file_handler = logging.FileHandler('my_logs.log')
file_handler.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO,
                    handlers=[file_handler],
                    format='%(levelname)-8s ## %(filename)s:%(lineno)d #####'
                           '[%(asctime)s] - %(name)s - %(message)s')


async def main():
    # await async_main()

    logging.info('Starting Chat Bot')

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message_cron_at_start, trigger='date',
                      run_date=datetime.now() + timedelta(seconds=1),
                      kwargs={'bot': bot, 'tg_id': '657559316'})
    scheduler.start()
    dp.include_router(router)
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot disabled")
