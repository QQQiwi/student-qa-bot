from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.users.keyboard as kb

from telegram_bot.utils.llm_api import ask_llm
from telegram_bot.logger import logger

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}. Я - GuideBO. Готов помочь с любым вопросом! Что тебя интересует?",
                         reply_markup=kb.main_keyboard)

@router.message(F.text)
async def handle_message_to_llm(message: Message, bot: Bot):
    try:
        # Отправляем уведомление о начале обработки
        processing_msg = await message.answer("⏳ Обрабатываю ваше сообщение...")
        
        user_input = message.text
        
        # Проверка на пустое сообщение
        if not user_input.strip():
            await processing_msg.edit_text("⚠️ Вы отправили пустое сообщение.")
            return
            
        # Проверка длины сообщения
        if len(user_input) > 1000:
            await processing_msg.edit_text("⚠️ Сообщение слишком длинное (максимум 1000 символов).")
            return
            
        # Получаем ответ от LLM
        llm_reply = await ask_llm(user_input)
        
        # Проверка ответа от LLM
        if not llm_reply:
            await processing_msg.edit_text("❌ Не удалось получить ответ от сервера.")
            return
            
        await processing_msg.edit_text(llm_reply)
        
    except Exception as e:
        # Обработка ошибок
        error_msg = f"⚠️ Произошла ошибка: {str(e)}"
        await message.answer(error_msg)
        logger.error(f"Error in handle_message_to_llm: {str(e)}")

@router.message(F.text == '🕵️‍♂️ Обо мне')
async def cmd_start(message: Message):
    await message.answer(f"Я - бот-помощник, разработанный студентами факультета КНИиТ СГУ.",
                         reply_markup=kb.start_inline_keyboard)