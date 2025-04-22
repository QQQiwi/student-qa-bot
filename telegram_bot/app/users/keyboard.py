from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🕵️‍♂️ Обо мне')]
], 
    resize_keyboard = True)

start_inline_keyboard = InlineKeyboardMarkup(keyboard = [
    [InlineKeyboardButton(text = 'Сайт СГУ', url= "www.sgu.ru")]
])