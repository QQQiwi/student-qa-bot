from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.users.keyboard as kb

from telegram_bot.utils.llm_api import ask_llm

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}. Я - GuideBO. Готов помочь с любым вопросом! Что тебя интересует?",
                         reply_markup=kb.main_keyboard)

@router.message(F.text)
async def handle_message_to_llm(message: Message):
    user_input = message.text
    llm_reply = await ask_llm(user_input)
    await message.answer(llm_reply)

@router.message(F.text == '🕵️‍♂️ Обо мне')
async def cmd_start(message: Message):
    await message.answer(f"Я - бот-помощник, разработанный студентами факультета КНИиТ СГУ.",
                         reply_markup=kb.start_inline_keyboard)