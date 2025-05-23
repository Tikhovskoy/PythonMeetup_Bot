import asyncio
from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError
import logging

logger = logging.getLogger(__name__)
  
async def send_telegram_message_async(chat_id: int, text: str):
    token = settings.BOT_TOKEN
    bot = Bot(token=token)
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except TelegramError as e:
        logger.error(f"Ошибка отправки сообщения {chat_id}: {e}")


def send_telegram_message(chat_id: int, text: str):
    asyncio.run(send_telegram_message_async(chat_id, text))