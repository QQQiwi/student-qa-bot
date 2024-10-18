import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from app.users.handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def main():
    logger.info("Запуск основного процесса...")
    dp.include_router(router)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Произошла ошибка во время работы бота: {e}")
    finally:
        logger.info("Поллинг остановлен.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Завершение работы программы.")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
    finally:
        logger.info("Запуск завершен.")