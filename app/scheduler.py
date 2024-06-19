from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject
from typing import Dict, Any, Callable, Awaitable


class SchedulerMiddleware(BaseMiddleware):

    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler
        
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data["scheduler"] = self.scheduler
        return await handler(event, data)




        
async def send_message_cron_at_start(bot: Bot, tg_id):
    await bot.send_message(str(tg_id), (f"Привет\n"
                f"Бот запущен"))