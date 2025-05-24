from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_APPLY_DESC, STATE_APPLY_TOPIC, STATE_MENU
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.keyboards.speaker_app_keyboards import get_speaker_keyboard
from bot.logging_tools import logger
from bot.services import speaker_app_service
from bot.services.core_service import is_speaker
from bot.utils.telegram_utils import send_message_with_retry


async def speaker_app_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['speaker_app'] = {}
    logger.info("Пользователь %s начал заявку на спикера", update.effective_user.id)
    await send_message_with_retry(
        update.message,
        "Ты хочешь стать спикером!\n\nВведи тему своего доклада:",
        reply_markup=get_speaker_keyboard(),
    )
    return STATE_APPLY_TOPIC

async def speaker_topic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    is_spk = await is_speaker(user_id)
    if text == "⬅️ Назад":
        logger.info("Пользователь %s отменил заявку на спикера на этапе ввода темы", user_id)
        await send_message_with_retry(
            update.message,
            "Вы в главном меню.",
            reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
        )
        return STATE_MENU

    context.user_data['speaker_app']['topic'] = text.strip()
    logger.info("Пользователь %s ввёл тему заявки на спикера: %s", user_id, text.strip())
    await send_message_with_retry(
        update.message,
        "Кратко опиши свой доклад:",
        reply_markup=get_speaker_keyboard(),
    )
    return STATE_APPLY_DESC

async def speaker_desc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    is_spk = await is_speaker(user_id)
    if text == "⬅️ Назад":
        logger.info("Пользователь %s отменил заявку на спикера на этапе описания", user_id)
        await send_message_with_retry(
            update.message,
            "Вы в главном меню.",
            reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
        )
        return STATE_MENU

    context.user_data['speaker_app']['desc'] = text.strip()
    topic = context.user_data['speaker_app'].get('topic', '')
    desc = context.user_data['speaker_app'].get('desc', '')
    telegram_id = update.effective_user.id

    try:
        await sync_to_async(speaker_app_service.save_speaker_app)({
            "telegram_id": telegram_id,
            "topic": topic,
            "desc": desc,
        })
        logger.info("Пользователь %s отправил заявку на спикера. Тема: %s, Описание: %s", telegram_id, topic, desc)
    except ValueError as err:
        logger.warning("Ошибка при сохранении заявки на спикера пользователя %s: %s", telegram_id, err)
        await send_message_with_retry(update.message, f"Ошибка: {err}\nПопробуй снова.")
        return STATE_APPLY_DESC

    await send_message_with_retry(
        update.message,
        "Спасибо! Ваша заявка на выступление отправлена.\n\nВы в главном меню.",
        reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
    )
    return STATE_MENU
