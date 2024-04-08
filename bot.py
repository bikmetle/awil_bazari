import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.markdown import hbold

from config import settings
from dao.base import UserDAO
from my_keyboards import MyCallback, role_markup

TOKEN = settings.BOT_TOKEN
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Hi, {hbold(message.from_user.full_name)}!\nWhat do you want to do?",
        reply_markup=role_markup,
    )
    await UserDAO.upsert(tg_id=message.chat.id, name=message.chat.full_name)


@dp.callback_query(MyCallback.filter(F.text == "sell"))
async def sell_button_handler(query: CallbackQuery, callback_data: MyCallback):
    await query.message.answer("What do you want to sell?")
    await query.answer()


@dp.callback_query(MyCallback.filter(F.text == "buy"))
async def buy_button_handler(query: CallbackQuery, callback_data: MyCallback):
    await query.message.answer("What do you want to buy?")
    await query.answer()


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
