from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU
from bot.keyboards.speaker_app_keyboards import (
    get_speaker_menu_keyboard,
    get_speaker_menu_speech_keyboard
)
from bot.services import speaker_service

async def handle_speaker_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    speaker_id = update.effective_user.id
    speaker_service.start_performance(speaker_id)

    await update.message.reply_text(
        "Ты начал выступление! Теперь ты можешь просматривать вопросы.",
        reply_markup=get_speaker_menu_speech_keyboard()
    )
    return STATE_MENU

async def handle_speaker_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    speaker_id = update.effective_user.id
    speaker_service.finish_performance(speaker_id)

    await update.message.reply_text(
        "Спасибо за выступление! Ждём тебя снова.",
        reply_markup=get_speaker_menu_keyboard()
    )
    return STATE_MENU

async def handle_speaker_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    speaker_id = update.effective_user.id
    questions = speaker_service.get_questions_for_speaker(speaker_id)
    if not questions:
        await update.message.reply_text("Пока нет новых вопросов.")
    else:
        for q in questions:
            await update.message.reply_text(
                f"Вопрос от пользователя {q['from_user_id']}:\n{q['question_text']}"
            )
    return STATE_MENU
