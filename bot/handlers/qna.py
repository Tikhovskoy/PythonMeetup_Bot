from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU

async def qna_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Задать вопрос докладчику (ещё не реализовано)")
    return STATE_MENU
