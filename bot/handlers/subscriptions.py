from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU

async def subscribe_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Подписка (ещё не реализовано)")
    return STATE_MENU
