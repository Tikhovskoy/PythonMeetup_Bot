from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.logging_tools import logger
from bot.services import speaker_service
from bot.utils.telegram_utils import send_message_with_retry


async def handle_speaker_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    speaker_id = update.effective_user.id
    logger.info("Спикер %s начал выступление", speaker_id)
    await speaker_service.start_performance(speaker_id)
    await send_message_with_retry(
        update.message,
        "Ты начал выступление! Теперь ты можешь просматривать вопросы.",
        reply_markup=get_main_menu_keyboard(is_speaker=True),
    )
    return STATE_MENU


async def handle_speaker_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    speaker_id = update.effective_user.id
    logger.info("Спикер %s закончил выступление", speaker_id)
    await speaker_service.finish_performance(speaker_id)
    await send_message_with_retry(
        update.message,
        "Спасибо за выступление! Ждём тебя снова.",
        reply_markup=get_main_menu_keyboard(is_speaker=True),
    )
    return STATE_MENU


async def handle_speaker_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    speaker_id = update.effective_user.id
    questions = await speaker_service.get_questions_for_speaker(speaker_id)
    logger.info("Спикер %s запросил список вопросов", speaker_id)
    if not questions:
        await send_message_with_retry(
            update.message,
            "Пока нет новых вопросов.",
            reply_markup=get_main_menu_keyboard(is_speaker=True),
        )
    else:
        for q in questions:
            from_user_id = q["from_user_id"]
            name = q.get("name") or str(from_user_id)
            user_link = f'<a href="tg://user?id={from_user_id}">{name}</a>'
            await send_message_with_retry(
                update.message,
                f'Вопрос от {user_link}:\n{q["question_text"]}',
                reply_markup=get_main_menu_keyboard(is_speaker=True),
                parse_mode="HTML",
            )
    return STATE_MENU
