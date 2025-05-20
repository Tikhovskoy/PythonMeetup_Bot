from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ConversationHandler

from bot.constants import STATE_MENU
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.services.core_service import register_user

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await register_user(user_id)
    context.user_data.clear()
    text = (
        "👋 Привет! Это бот митапа PythonMeetup.\n"
        "Вот что я умею:\n"
        "• Программа мероприятия\n"
        "• Вопросы докладчикам\n"
        "• Знакомства с другими участниками\n"
        "• Донаты и подписка на новости\n\n"
        "Выбери действие:"
    )
    await update.message.reply_text(
        text,
        reply_markup=get_main_menu_keyboard()
    )
    return STATE_MENU

async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Действие отменено.")
    return STATE_MENU
