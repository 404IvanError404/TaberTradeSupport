from bot.data_config import config
from aiogram import Bot, Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Инициализируем экземпляр бота
bot = Bot(token=config.BOT_TOKEN)
# Инициализируем хранилище для состояний
storage = MemoryStorage()
# Инициализация экземплара класса из aiogram, который исспользуется для обработки сообщений и событий от TG Bot API
dp = Dispatcher(bot, storage=storage)

