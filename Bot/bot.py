import os
import asyncio
from datetime import datetime
from typing import Any, Dict

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
from loguru import logger
import aiohttp

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logger.add("logs/bot_{time}.log", rotation="1 day", compression="zip")

# Инициализация бота
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# Создание клавиатуры
def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="❓ Задать вопрос")],
        [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="⚙️ Настройки")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Обработчик команды /start
@dp.message(Command("start"))
async def command_start_handler(message: types.Message) -> None:
    """
    Обработчик команды /start
    """
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        "👋 Привет! Я бот, который поможет вам получить ответы на ваши вопросы.\n"
        "Используйте кнопку 'Задать вопрос' или просто напишите свой вопрос.",
        reply_markup=get_main_keyboard()
    )

# Обработчик команды /help
@dp.message(Command("help"))
async def command_help_handler(message: types.Message) -> None:
    """
    Обработчик команды /help
    """
    logger.info(f"User {message.from_user.id} requested help")
    help_text = (
        "🤖 Как использовать бота:\n\n"
        "1. Просто напишите свой вопрос или используйте кнопку 'Задать вопрос'\n"
        "2. Дождитесь ответа от ИИ\n"
        "3. Для дополнительной информации используйте кнопку 'Помощь'\n"
        "4. Настройки доступны через кнопку 'Настройки'\n\n"
        "Команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение"
    )
    await message.answer(help_text, reply_markup=get_main_keyboard())

# Обработчик кнопки "Задать вопрос"
@dp.message(lambda message: message.text == "❓ Задать вопрос")
async def ask_question_handler(message: types.Message) -> None:
    """
    Обработчик кнопки "Задать вопрос"
    """
    await message.answer(
        "Пожалуйста, напишите ваш вопрос:",
        reply_markup=get_main_keyboard()
    )

# Обработчик кнопки "Помощь"
@dp.message(lambda message: message.text == "ℹ️ Помощь")
async def help_button_handler(message: types.Message) -> None:
    """
    Обработчик кнопки "Помощь"
    """
    await command_help_handler(message)

# Обработчик кнопки "Настройки"
@dp.message(lambda message: message.text == "⚙️ Настройки")
async def settings_handler(message: types.Message) -> None:
    """
    Обработчик кнопки "Настройки"
    """
    await message.answer(
        "⚙️ Настройки пока недоступны.",
        reply_markup=get_main_keyboard()
    )

async def send_request_to_api(question: str) -> Dict[str, Any]:
    """
    Временная заглушка для API
    В будущем здесь будет реальное обращение к веб-сервису
    """
    logger.info(f"Получен вопрос: {question}")
    
    # Заглушка - просто возвращаем сообщение о том, что API пока не подключено
    return {
        "answer": (
            "🚧 Извините, но в данный момент я работаю в тестовом режиме.\n"
            f"Ваш вопрос: {question}\n\n"
            "В будущем здесь будет ответ от Llama 3.1 😊"
        )
    }

# Обработчик текстовых сообщений
@dp.message()
async def message_handler(message: types.Message) -> None:
    """
    Обработчик всех текстовых сообщений
    """
    if message.text and not message.text.startswith('/'):
        user_id = message.from_user.id
        question = message.text
        
        logger.info(f"Received question from user {user_id}: {question}")
        
        # Отправляем сообщение о том, что бот обрабатывает запрос
        processing_msg = await message.answer("🤔 Обрабатываю ваш вопрос...")
        
        try:
            # Отправляем запрос к API
            response = await send_request_to_api(question)
            
            if "error" in response:
                await processing_msg.edit_text(
                    "😔 Извините, произошла ошибка при обработке вашего запроса. "
                    "Пожалуйста, попробуйте позже."
                )
                logger.error(f"Error processing request for user {user_id}: {response['error']}")
            else:
                # Отправляем ответ пользователю
                await processing_msg.edit_text(response.get("answer", "Нет ответа от API"))
                logger.info(f"Sent answer to user {user_id}")
                
        except Exception as e:
            await processing_msg.edit_text(
                "😔 Произошла ошибка при обработке вашего запроса. "
                "Пожалуйста, попробуйте позже."
            )
            logger.error(f"Error in message handler for user {user_id}: {str(e)}")

async def main() -> None:
    """
    Главная функция запуска бота
    """
    logger.info("Starting bot")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot stopped with error: {str(e)}")
    finally:
        logger.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
