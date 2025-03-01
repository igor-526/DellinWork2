from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from dellin_work.settings import TG_BOT_TOKEN, TG_REDIS_URL

storage = RedisStorage.from_url(TG_REDIS_URL)
dp = Dispatcher(storage=storage)
bot = Bot(token=TG_BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
