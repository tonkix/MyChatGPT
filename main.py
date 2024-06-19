import asyncio
from datetime import datetime, timedelta
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

load_dotenv()

from app.handlers import router
from app.scheduler import send_message_cron_at_start
from app.scheduler import SchedulerMiddleware

# Инициализируем логгер
logger = logging.getLogger(__name__)

async def main():
    #await async_main()   
    
    # Конфигурируем логирование
    logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s')
    # Выводим в консоль информацию о начале запуска
    logger.info('Starting 2147')
    
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