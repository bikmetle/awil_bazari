from aiogram.filters.callback_data import CallbackData
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


class MyCallback(CallbackData, prefix="my"):
    text: str


sender_button = InlineKeyboardButton(
    text="Sell", callback_data=MyCallback(text="sell").pack()
)

courier_button = InlineKeyboardButton(
    text="Buy", callback_data=MyCallback(text="buy").pack()
)

role_markup = InlineKeyboardMarkup(inline_keyboard=[[sender_button, courier_button]])
