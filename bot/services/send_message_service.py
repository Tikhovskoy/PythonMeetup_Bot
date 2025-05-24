import asyncio

from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError

from bot.logging_tools import logger


async def send_telegram_message_async(chat_id: int, text: str):
    token = settings.BOT_TOKEN
    bot = Bot(token=token)
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        logger.info("Успешно отправлено сообщение в chat_id=%s", chat_id)
    except TelegramError as e:
        logger.error("Ошибка отправки сообщения chat_id=%s: %s", chat_id, e)


def send_telegram_message(chat_id: int, text: str):
    asyncio.run(send_telegram_message_async(chat_id, text))
