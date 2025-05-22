import os
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pythonmeetup.settings")
import django
django.setup()

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, PreCheckoutQueryHandler

from bot.handlers.main_menu import main_menu_conv_handler
from bot.handlers.donations import precheckout_handler
from telegram.error import TelegramError

async def error_handler(update, context):
    logging.error(f'Exception while handling an update: {context.error}', exc_info=context.error)
    try:
        if update and hasattr(update, "message") and update.message:
            await update.message.reply_text("Произошла техническая ошибка. Попробуйте позже.")
    except TelegramError:
        pass  

def main():
    load_dotenv()

    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("BOT_TOKEN не найден в .env файле")

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=logging.INFO
    )

    application = (
        ApplicationBuilder()
        .token(bot_token)
        .build()
    )
    application.add_handler(main_menu_conv_handler)
    application.add_handler(PreCheckoutQueryHandler(precheckout_handler))
    application.add_error_handler(error_handler) 

    application.run_polling()

if __name__ == "__main__":
    main()
