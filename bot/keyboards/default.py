from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def phone_request_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_phone = KeyboardButton(text="Отправить телефон", request_contact=True)
    keyboard.add(button_phone)
    return keyboard


def no_contact_markup(message_id):
    keyboard = InlineKeyboardMarkup()
    no_contact_button = InlineKeyboardButton("Со мной никто не связался", callback_data=f"no_contact:{message_id}")
    keyboard.add(no_contact_button)
    return keyboard

def contact_yes(message_id):
    keyboard = InlineKeyboardMarkup()
    no_contact_button = InlineKeyboardButton("Cвязались", callback_data=f"yes_contact:{message_id}")
    keyboard.add(no_contact_button)
    return keyboard
