from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU, STATE_QNA_ASK_TEXT
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.services import speaker_service
from bot.services.core_service import is_speaker
from bot.utils.telegram_utils import send_message_with_retry

async def qna_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    talk = await speaker_service.get_active_speaker_talk()
    user_id = update.effective_user.id
    is_spk = await is_speaker(user_id)

    if not talk:
        await send_message_with_retry(
            update.message,
            "В данный момент ни один спикер не выступает.\n"
            "Попробуйте отправить вопрос позже.",
            reply_markup=get_main_menu_keyboard(is_speaker=is_spk)
        )
        return STATE_MENU

    speaker_name = talk['speaker_name']
    context.user_data["active_speaker_talk_id"] = talk['id']
    context.user_data["active_speaker_name"] = speaker_name

    await send_message_with_retry(
        update.message,
        f"Сейчас выступает {speaker_name}.\nНапиши свой вопрос:"
    )
    return STATE_QNA_ASK_TEXT

async def qna_ask_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question_text = update.message.text
    from_user_id = update.effective_user.id
    from_user_name = update.effective_user.full_name

    is_spk = await is_speaker(from_user_id)

    try:
        await speaker_service.save_question_for_active_speaker(
            question_text, from_user_id, from_user_name
        )
    except ValueError:
        await send_message_with_retry(
            update.message,
            "В данный момент нет активного спикера. Попробуйте позже.",
            reply_markup=get_main_menu_keyboard(is_speaker=is_spk)
        )
        return STATE_MENU

    await send_message_with_retry(
        update.message,
        "Спасибо, твой вопрос отправлен текущему спикеру!\n\nТы в главном меню:",
        reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
    )
    return STATE_MENU
