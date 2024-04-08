from aiogram.filters.callback_data import CallbackData
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MyCallback(CallbackData, prefix="my"):
    text: str


class ItemCallback(CallbackData, prefix="item"):
    id: int
    name: str
    volume_kind: str


sender_button = InlineKeyboardButton(
    text="Sell", callback_data=MyCallback(text="sell").pack()
)

courier_button = InlineKeyboardButton(
    text="Buy", callback_data=MyCallback(text="buy").pack()
)

role_markup = InlineKeyboardMarkup(inline_keyboard=[[sender_button, courier_button]])


def get_item_markup(items):
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(
            text=item.name,
            callback_data=ItemCallback(
                id=item.id, name=item.name, volume_kind=item.volume_kind
            ).pack(),
        )
    builder.adjust(2)
    reply_markup = builder.as_markup()
    return reply_markup
