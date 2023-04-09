from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from motor.motor_asyncio import AsyncIOMotorClient

from config import token, mongoclient_uri

bot = Bot(token, parse_mode="html")
dp = Dispatcher(bot, storage=MemoryStorage())


client = AsyncIOMotorClient(mongoclient_uri)
db = client.sampleDB
collection = db.sample_collection
