from django.core.management.base import BaseCommand, CommandError
from telegram_bot.handlers import router as main_router
from telegram_bot.create_bot import dp, bot
import asyncio
from telegram_bot.middlewares import AuthMiddleware


async def start_polling() -> None:
    dp.include_routers(main_router)
    dp.message.middleware.register(AuthMiddleware())
    dp.callback_query.middleware.register(AuthMiddleware())
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'This command starts up the Telegram bot'

    def handle(self, *args, **kwargs):
        try:
            asyncio.run(start_polling())
        except Exception as ex:
            raise CommandError(ex)
