from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.users.keyboard as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}. Пока что я просто макет.",
                         reply_markup=kb.main_keyboard)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Чем тебе помочь?", reply_markup=kb.add_keyboard)

@router.message(Command('data'))
async def get_data(message: Message):
    await message.answer("Текущая ДБ: ", reply_markup=await kb.reply_data())

@router.message(Command('another'))
async def get_another(message: Message):
    await message.answer("Здесь чисто callback.", reply_markup=kb.call_keyboard)

@router.message(F.photo)
async def is_photo(message: Message):
    await message.answer_photo(photo = 'https://i.imgur.com/dBS6L99.jpeg', caption ="Эй! Я ещё маленький и не умею работать с фотографиями :(")

@router.callback_query(F.data == 'another')
async def catalog(callback: CallbackQuery):
    await callback.answer('Готово') # можно добавить show_alert
    await callback.message.answer("Не знаю что писать.")
    # await callback.message.edit_text("Не знаю что писать.", reply_markup = await ...) - в случае замены текста на кнопках (обязательно должен 
    # совпадать тип клавиатур)