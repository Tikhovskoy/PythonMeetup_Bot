from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.services.core_service import register_user, is_speaker, event_schedule
from bot.utils.telegram_utils import send_message_with_retry

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    spk = await is_speaker(user_id)
    await register_user(user_id)
    context.user_data.clear()

    if spk:
        text = (
            f"👋 Привет, {user_name}!\n"
            f"Ты докладчик на этом мероприятии.\n"
            f"Вот что доступно в этом боте:\n"
            "• Программа мероприятия\n"
            "• Вопросы докладчикам\n"
            "• Знакомства с другими участниками\n"
            "• Донаты и подписка на новости\n\n"
            "Выбери действие:"
        )
    else:
        text = (
            "👋 Привет! Это бот митапа PythonMeetup.\n"
            "Вот что я умею:\n"
            "• Программа мероприятия\n"
            "• Вопросы докладчикам\n"
            "• Знакомства с другими участниками\n"
            "• Донаты и подписка на новости\n\n"
            "Выбери действие:"
        )

    await send_message_with_retry(
        update.message,
        text,
        reply_markup=get_main_menu_keyboard(is_speaker=spk)
    )
    return STATE_MENU

async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_spk = await is_speaker(user_id)
    await send_message_with_retry(
        update.message,
        "❌ Действие отменено. Ты в главном меню.",
        reply_markup=get_main_menu_keyboard(is_speaker=is_spk)
    )
    context.user_data.clear()
    return STATE_MENU
