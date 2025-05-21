from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU
from bot.keyboards.speaker_app_keyboards import (
    get_speaker_menu_keyboard,
    get_speaker_menu_speech_keyboard
)


async def handle_speaker_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    now = datetime.now()
    # запись в БД
    print(f"{user_name} начал выступление в {now}")

    await update.message.reply_text(
        "Ты начал выступление! Теперь ты можешь просматривать вопросы.",
        reply_markup=get_speaker_menu_speech_keyboard()
    )
    return STATE_MENU


async def handle_speaker_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    now = datetime.now()
    # запись в БД
    print(f"{user_name} закончил выступление в {now}")

    await update.message.reply_text(
        "Спасибо за выступление! Ждём тебя снова.",
        reply_markup=get_speaker_menu_keyboard()
    )
    return STATE_MENU


async def handle_speaker_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получить из Бд
    questions = [
        {"text": "Какая тема доклада?", "user_id": 7956301673},
        {"text": "Какая версия продукта?", "user_id": 7956301673}
    ]
    if not questions:
        await update.message.reply_text("Пока нет новых вопросов.")
    else:
        for q in questions:
            await update.message.reply_text(
                f"Вопрос от пользователя {q['user_id']}:\n{q['text']}"
            )
    return STATE_MENU

