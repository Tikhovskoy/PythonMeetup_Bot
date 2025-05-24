import os
import traceback

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pythonmeetup.settings")
import django

django.setup()

from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError
from telegram.ext import ApplicationBuilder, PreCheckoutQueryHandler

from bot.handlers.donations import precheckout_handler
from bot.handlers.main_menu import main_menu_conv_handler
from bot.logging_tools import logger


async def error_handler(update, context):
    logger.error("Exception while handling an update: %s", context.error, exc_info=True)
    try:
        if update and hasattr(update, "message") and update.message:
            await update.message.reply_text(
                "Произошла техническая ошибка. Попробуйте позже."
            )
    except TelegramError:
        pass
    owner_id = context.application.bot_data.get("owner_id")
    if owner_id:
        try:
            tb = "".join(traceback.format_exception(None, context.error, context.error.__traceback__))
            bot = context.bot if hasattr(context, "bot") else Bot(token=os.environ["BOT_TOKEN"])
            error_message = (
                f"⚠️ *PythonMeetupBot — Exception!*\n"
                f"`{type(context.error).__name__}`\n"
                f"```\n{tb[-1000:]}\n```"
            )
            await bot.send_message(
                chat_id=owner_id,
                text=error_message,
                parse_mode="Markdown"
            )
        except Exception as admin_exc:
            logger.error("Не удалось отправить ошибку владельцу: %s", admin_exc)


def main():
    load_dotenv()

    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("BOT_TOKEN не найден в .env файле")

    owner_id = int(os.environ.get("TELEGRAM_OWNER_ID", 0))

    application = ApplicationBuilder().token(bot_token).build()
    application.bot_data["owner_id"] = owner_id

    application.add_handler(main_menu_conv_handler)
    application.add_handler(PreCheckoutQueryHandler(precheckout_handler))
    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
