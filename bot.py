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
from dao.base import ItemDAO, SellerDAO, UserDAO
from my_keyboards import (
    ItemCallback,
    RoleCallback,
    get_item_markup,
    get_volume_markup,
    role_markup,
)

TOKEN = settings.BOT_TOKEN
dp = Dispatcher()

# TODO add menu button


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Hi, {hbold(message.from_user.full_name)}!\nWhat do you want to do?",
        reply_markup=role_markup,
    )
    await UserDAO.upsert(tg_id=message.chat.id, name=message.chat.full_name)


@dp.callback_query(RoleCallback.filter(F.text == "sell"))
async def sell_button_handler(query: CallbackQuery, callback_data: RoleCallback):
    await SellerDAO.upsert(user_id=query.message.chat.id)
    items = await ItemDAO.find_all()
    await query.message.answer(
        "What do you want to sell?", reply_markup=get_item_markup(items)
    )
    await query.answer()


@dp.callback_query(RoleCallback.filter(F.text == "buy"))
async def buy_button_handler(query: CallbackQuery, callback_data: RoleCallback):
    await query.message.answer("What do you want to buy?")
    await query.answer()


@dp.callback_query(ItemCallback.filter())
async def item_button_handler(query: CallbackQuery, callback_data: ItemCallback):
    await query.message.answer(
        f"How many/much {callback_data.volume_kind}?",
        reply_markup=get_volume_markup(callback_data.volume_kind),
    )
    await query.answer()


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
