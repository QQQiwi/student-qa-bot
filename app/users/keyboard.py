from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обо мне')],
    [KeyboardButton(text='Что-то другое'), KeyboardButton(text='Что-то ещё')],
    [KeyboardButton(text='Ну и вкусненькое просто')]
], 
    resize_keyboard = True,
    input_field_placeholder='Выберите, что-то из списка.')

add_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='О нас', url = 'https://www.sgu.ru'), InlineKeyboardButton(text='О них', url = 'https://www.sgu/shedule')]
])

call_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Что это такое?', callback_data='another')]
])

data_base = ['Пример 1', 'Пример 2', 'Пример 3']

async def reply_data():
    data_keyboard = ReplyKeyboardBuilder() # InlineKeyboardBuilder
    for data in data_base:
        data_keyboard.add(KeyboardButton(text=data)) # InlineKeyboardButton (обязательно со вторым аргументом)
    return data_keyboard.adjust(2).as_markup()

