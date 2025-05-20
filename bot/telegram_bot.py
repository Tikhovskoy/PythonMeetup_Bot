import os
import logging
from dotenv import load_dotenv

from telegram.ext import ApplicationBuilder

from bot.handlers.main_menu import main_menu_conv_handler

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден в .env файле")

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO
)

def main():
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )
    application.add_handler(main_menu_conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
