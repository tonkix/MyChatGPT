from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')],
                                     [KeyboardButton(text='На главную')],
                                     [KeyboardButton(text='На главную')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню'                           
                           )