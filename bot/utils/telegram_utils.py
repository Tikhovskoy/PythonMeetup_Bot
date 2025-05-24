import asyncio
from telegram.error import NetworkError, RetryAfter, TelegramError, TimedOut
from bot.logging_tools import logger

async def send_message_with_retry(
    chat_or_message, text, max_retries=5, delay=2, **kwargs
):
    """Надёжно отправляет сообщение в Telegram с повтором при ошибке сети."""
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            if hasattr(chat_or_message, "reply_text"):
                return await chat_or_message.reply_text(text, **kwargs)
            else:
                return await chat_or_message.send_message(text, **kwargs)
        except RetryAfter as exc:
            wait_time = int(getattr(exc, "retry_after", delay))
            logger.warning(f"Flood control, ждём {wait_time} сек...")
            await asyncio.sleep(wait_time)
            last_exc = exc
        except (TimedOut, NetworkError, TelegramError) as exc:
            logger.warning(
                f"Попытка {attempt}: не удалось отправить сообщение ({exc}), повтор через {delay} сек..."
            )
            await asyncio.sleep(delay)
            last_exc = exc
        except Exception as exc:
            logger.error(
                f"Неожиданная ошибка при отправке сообщения: {exc}", exc_info=True
            )
            last_exc = exc
            break
    logger.error(f"Все попытки отправить сообщение не удались: {last_exc}")
    return None
