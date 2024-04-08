from aiogram.filters.callback_data import CallbackData
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class RoleCallback(CallbackData, prefix="my"):
    text: str


class ItemCallback(CallbackData, prefix="item"):
    id: int
    name: str
    volume_kind: str


class VolumeCallback(CallbackData, prefix="volume"):
    volume: int
    volume_kind: str


sender_button = InlineKeyboardButton(
    text="Sell", callback_data=RoleCallback(text="sell").pack()
)

courier_button = InlineKeyboardButton(
    text="Buy", callback_data=RoleCallback(text="buy").pack()
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


def get_volume_markup(volume_kind):
    builder = InlineKeyboardBuilder()
    if volume_kind == "litre":
        for volume in range(1, 10):
            builder.button(
                text=str(volume),
                callback_data=VolumeCallback(
                    volume=volume, volume_kind=volume_kind
                ).pack(),
            )
    builder.adjust(3)
    reply_markup = builder.as_markup()
    return reply_markup
