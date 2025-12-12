from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode 
from src.configs import BotConfig
from src.handler import router
from src.logger import setup_logger
import asyncio

logger = setup_logger()
async def main():
    try:
        config = BotConfig()
        bot_token = config.BOT_TOKEN
        
        bot = Bot(
            token=bot_token, 
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        dp = Dispatcher()
        dp.include_router(router)
        
        logger.info(f"Бот запускается с токеном: {bot_token[:10]}...")
        logger.info("Бот запущен и готов к работе!")
        
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")