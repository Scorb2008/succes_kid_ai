from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_mode_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🧒 Детский режим",
                    callback_data="mode_child"
                ),
                InlineKeyboardButton(
                    text="👨‍👩‍👧 Родительский",
                    callback_data="mode_parent"
                )
            ],
        ]
    )
    return keyboard
