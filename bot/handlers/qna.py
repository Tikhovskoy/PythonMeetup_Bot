from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU, STATE_QNA_ASK_TEXT
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.services import speaker_service

async def qna_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_speaker_id = speaker_service.get_active_speaker()
    if not active_speaker_id:
        await update.message.reply_text(
            "В данный момент ни один спикер не выступает.\n"
            "Попробуйте отправить вопрос позже.",
            reply_markup=get_main_menu_keyboard()
        )
        return STATE_MENU

    speaker_name = speaker_service.get_speakers().get(active_speaker_id, "Неизвестно")
    context.user_data["active_speaker_id"] = active_speaker_id
    context.user_data["active_speaker_name"] = speaker_name

    await update.message.reply_text(
        f"Сейчас выступает {speaker_name}.\nНапиши свой вопрос:"
    )
    return STATE_QNA_ASK_TEXT

async def qna_ask_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question_text = update.message.text
    from_user_id = update.effective_user.id

    try:
        speaker_service.save_question_for_active_speaker(question_text, from_user_id)
    except ValueError:
        await update.message.reply_text(
            "В данный момент нет активного спикера. Попробуйте позже.",
            reply_markup=get_main_menu_keyboard()
        )
        return STATE_MENU

    await update.message.reply_text(
        "Спасибо, твой вопрос отправлен текущему спикеру!\n\nТы в главном меню:",
        reply_markup=get_main_menu_keyboard(),
    )
    return STATE_MENU
