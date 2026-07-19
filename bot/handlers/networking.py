from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import (
    STATE_MENU,
    STATE_NETW_CONTACTS,
    STATE_NETW_GRADE,
    STATE_NETW_NAME,
    STATE_NETW_ROLE,
    STATE_NETW_SHOW,
    STATE_NETW_STACK,
)
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.keyboards.networking_keyboards import (
    get_next_profile_keyboard,
    get_profiles_finished_keyboard,
)
from bot.logging_tools import logger
from bot.services import networking_service
from bot.services.core_service import is_speaker
from bot.utils.telegram_utils import send_message_with_retry


async def networking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    logger.info("Пользователь %s зашёл в нетворкинг", telegram_id)
    profile = await networking_service.get_profile(telegram_id)
    if not profile:
        context.user_data["profile"] = {}
        await send_message_with_retry(update.message, "Давай познакомимся!\n\nВведи свои ФИО:")
        return STATE_NETW_NAME

    context.user_data["viewed_profiles"] = []
    return await show_next_profile(update, context)


async def show_next_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    viewed = context.user_data.get("viewed_profiles", [])
    profiles = await networking_service.get_profiles_list(telegram_id, viewed)

    if not profiles:
        logger.info("Для пользователя %s нет новых анкет для знакомства", telegram_id)
        await send_message_with_retry(
            update.message,
            "Больше новых анкет не найдено.",
            reply_markup=get_profiles_finished_keyboard(),
        )
        return STATE_NETW_SHOW

    profile = profiles[0]
    context.user_data["current_profile_id"] = profile["telegram_id"]
    logger.info(
        "Пользователь %s просматривает анкету пользователя %s",
        telegram_id,
        profile["telegram_id"],
    )
    await send_message_with_retry(
        update.message,
        f"ФИО: {profile['name']}\n"
        f"Контакты: {profile['contacts']}\n"
        f"Стек: {profile['stack']}\n"
        f"Роль: {profile['role']}\n"
        f"Грейд: {profile['grade']}",
        reply_markup=get_next_profile_keyboard(),
    )
    return STATE_NETW_SHOW


async def netw_show_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    telegram_id = update.effective_user.id
    viewed = context.user_data.get("viewed_profiles", [])

    if text == "➡️ Дальше":
        current = context.user_data.get("current_profile_id")
        if current and current not in viewed:
            viewed.append(current)
        context.user_data["viewed_profiles"] = viewed
        logger.info("Пользователь %s нажал 'Дальше' в анкетах", telegram_id)
        return await show_next_profile(update, context)
    if text == "🔄 Начать сначала":
        context.user_data["viewed_profiles"] = []
        logger.info("Пользователь %s начал просмотр анкет сначала", telegram_id)
        return await show_next_profile(update, context)
    if text == "⬅️ В меню":
        is_spk = await is_speaker(telegram_id)
        logger.info("Пользователь %s вернулся в главное меню из нетворкинга", telegram_id)
        await send_message_with_retry(
            update.message,
            "Ты в главном меню.",
            reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
        )
        return STATE_MENU

    await send_message_with_retry(
        update.message,
        "Пожалуйста, пользуйтесь кнопками!",
        reply_markup=get_next_profile_keyboard(),
    )
    return STATE_NETW_SHOW


async def netw_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["profile"]["name"] = update.message.text.strip()
    logger.info("Пользователь %s указал ФИО для анкеты", update.effective_user.id)
    await send_message_with_retry(update.message, "Укажи контакт для связи (Telegram, телефон):")
    return STATE_NETW_CONTACTS


async def netw_contacts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["profile"]["contacts"] = update.message.text.strip()
    logger.info("Пользователь %s указал контакты для анкеты", update.effective_user.id)
    await send_message_with_retry(
        update.message,
        "Опиши свой технологический стек (например: Python, Django, PostgreSQL):",
    )
    return STATE_NETW_STACK


async def netw_stack_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["profile"]["stack"] = update.message.text.strip()
    logger.info("Пользователь %s указал стек для анкеты", update.effective_user.id)
    await send_message_with_retry(
        update.message, "Твоя роль (например: Backend, Frontend, DevOps):"
    )
    return STATE_NETW_ROLE


async def netw_role_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["profile"]["role"] = update.message.text.strip()
    logger.info("Пользователь %s указал роль для анкеты", update.effective_user.id)
    await send_message_with_retry(update.message, "Твой грейд (например: Junior, Middle, Senior):")
    return STATE_NETW_GRADE


async def netw_grade_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["profile"]["grade"] = update.message.text.strip()
    profile = context.user_data["profile"]
    telegram_id = update.effective_user.id

    try:
        await networking_service.save_profile(telegram_id, profile)
        logger.info("Пользователь %s сохранил анкету", telegram_id)
        await send_message_with_retry(update.message, "Анкета успешно сохранена! 🎉")
    except ValueError as err:
        logger.warning("Ошибка при сохранении анкеты пользователя %s: %s", telegram_id, err)
        await send_message_with_retry(update.message, f"Ошибка: {err}\nПопробуй ещё раз.")
        return STATE_NETW_GRADE

    context.user_data["viewed_profiles"] = []
    return await show_next_profile(update, context)
