from loader import dp, bot
from aiogram.utils import executor
from bot.utilslog.log import setup_logging
from bot.services import set_default_commands
from bot.handlers.main_handler import register_handlers


logger = setup_logging()

# def main():
#     bot = Bot(token=BOT_TOKEN)
#     storage = MemoryStorage()
#     dp = Dispatcher(bot, storage=storage)
    
#     register_handlers(dp, bot)
    
#     executor.start_polling(dp, skip_updates=True)

async def on_startup(dp):

    logger.info('Setting default commands...')
    await set_default_commands(dp)

    register_handlers(dp, bot)
    logger.info("Bot is started...")

async def on_shutdown(dp):
    logger.info('Shutting down...')
    await dp.storage.close()
    await dp.storage.wait_closed()
    bot_session = await bot.get_session()
    await bot_session.close()
    logger.warning('Bot is disabled...')


if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(main())
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)