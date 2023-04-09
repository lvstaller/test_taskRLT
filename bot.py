import asyncio

from aiogram.utils import executor

from mics import dp, bot
import handlers

DELAY = 20


async def bot_get_me():
    print(await bot.get_me())


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, bot_get_me, loop)
    executor.start_polling(dp)
