from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ConversationHandler

from bot.constants import STATE_MENU
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.keyboards.speaker_app_keyboards import get_speaker_menu_keyboard
from bot.services.core_service import register_user, is_speaker, event_schedule


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    if is_speaker(user_id):
        performance_time = event_schedule(user_name)
        await update.message.reply_text(
            text=(f"👋 Приветcтвую Докладчик: {user_name}\n"
                  f"{performance_time}"
                  ),
            reply_markup=get_speaker_menu_keyboard()
        )
    else:
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


async def switch_to_user_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Теперь вы используете приложение как обычный пользователь.",
        reply_markup=get_main_menu_keyboard()
    )
    return STATE_MENU