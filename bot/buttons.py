from db import Products
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def MenyuButtons():
    buttons = InlineKeyboardBuilder()
    for i in Products():
        buttons.add(InlineKeyboardButton(text=f"{i[1]}", callback_data=f"{i[1]}"))
    buttons.adjust(2)
    return buttons.as_markup()
