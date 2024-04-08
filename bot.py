import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.markdown import hbold
from sqlalchemy import insert

from config import settings
from database import User, async_session_maker
from my_keyboards import MyCallback, role_markup

TOKEN = settings.BOT_TOKEN
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}!\nВыбери свою роль.",
        reply_markup=role_markup,
    )


@dp.callback_query(MyCallback.filter(F.text == "sender"))
async def sender_button_handler(
    callback_query: CallbackQuery, callback_data: MyCallback
):
    await callback_query.message.answer("hello")
    async with async_session_maker() as session:
        query = insert(User).values(
            tg_id=callback_query.message.chat.id,
            name=callback_query.message.chat.first_name,
        )
        await session.execute(query)
        await session.commit()

    await callback_query.answer()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
