from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_suggestion_kb(suggestions: list[dict[str, str]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    # print(suggestions)
    for sugg in suggestions:
        # print(type(sugg), type(suggestions))
        builder.button(
            text=sugg["address"],
            callback_data=sugg["fias"]
        )
    builder.adjust(*[1 for s in suggestions if s.get("fias")])
    return builder.as_markup()


def get_foreign_address_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Адрес должника неизвестен", callback_data="unknown_addr")
    return builder.as_markup()