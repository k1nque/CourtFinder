from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

usual_kblist = [[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]]

DefaultKB = ReplyKeyboardMarkup(
    keyboard=usual_kblist, 
    resize_keyboard=True,
    one_time_keyboard=False
)

WA_KB = ReplyKeyboardMarkup(
    keyboard=usual_kblist + [[KeyboardButton(text="Что это?")]],
    resize_keyboard=True,
    one_time_keyboard=False,
)

choice_kb = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Физического лица"),
        KeyboardButton(text="Юридического лица")
        ]],
    resize_keyboard=True,
    one_time_keyboard=False
)