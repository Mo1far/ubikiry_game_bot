import os
import asyncio

# from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import Executor
from peewee import SqliteDatabase

from bot.config import BOT_TOKEN

# from bot.middleware import ThrottlingMiddleware

storage = MemoryStorage()
loop = asyncio.get_event_loop()
# storage = RedisStorage2(db=5)

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)
# dp.middleware.setup(ThrottlingMiddleware())
executor = Executor(dp)
