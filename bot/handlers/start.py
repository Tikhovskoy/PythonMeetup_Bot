from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler

from bot.constants import STATE_MENU
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.keyboards.speaker_app_keyboards import (get_speaker_menu_keyboard,
                                                 get_speaker_or_user_keyboard)
from bot.services.core_service import event_schedule, is_speaker, register_user


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    context.user_data.clear()

    if is_speaker(user_id):
        await update.message.reply_text(
            f"👋 Приветствую, {user_name}!\nВы зарегистрированы как докладчик.",
            reply_markup=get_speaker_or_user_keyboard()
        )

    else:
        await register_user(user_id)
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


async def choose_mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_name = update.effective_user.first_name

    if text == "⬅️ Назад":
        await update.message.reply_text(
            "Возврат на шаг назад.",
            reply_markup=get_speaker_or_user_keyboard()
        )

    elif text == "Войти как докладчик":
        schedule_time = event_schedule(user_name)
        await update.message.reply_text(
            f"Вы вошли как докладчик.\n"
            f"\n{schedule_time}\n",
            reply_markup=get_speaker_menu_keyboard()
        )

    elif text == "Войти как пользователь":
        await update.message.reply_text(
            "Вы вошли как пользователь.",
            reply_markup=get_main_menu_keyboard()
        )

    else:
        await update.message.reply_text("Пожалуйста, выберите режим из предложенных.")
    return STATE_MENU