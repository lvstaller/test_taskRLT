from datetime import datetime, timedelta
import json

from aiogram import Bot, types
from aiogram.types.message import ContentTypes
from telegraph import Telegraph
from aiogram.types import ParseMode
from aiogram.types.input_media import (
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAnimation,
    InputFile,
    MediaGroup,
)

from mics import dp, bot, collection
from texts import *
from aggregate import aggregate_data


@dp.message_handler()
async def echo(
    message: types.Message,
):
    try:
        data = json.loads(message.text)
    except:
        data = None
    if data != None:
        text = str(
            await aggregate_data(
                collection, data["dt_from"], data["dt_upto"], data["group_type"]
            )
        ).replace("'", '"')
        await message.answer(text)
    else:
        await message.answer("Error data")
