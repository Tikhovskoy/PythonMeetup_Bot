from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU, STATE_SCHEDULE
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.keyboards.schedule_keyboards import get_schedule_keyboard
from bot.logging_tools import logger
from bot.services import schedule_service
from bot.services.core_service import is_speaker
from bot.utils.telegram_utils import send_message_with_retry


def format_schedule(events: list) -> str:
    lines = []
    for event in events:
        lines.append(f'Программа мероприятия: "{event["title"]}"')
        lines.append(f"Дата: {event['date']}")
        lines.append(f"Начало: {event['start_event']}")
        lines.append(f"Конец: {event['end_event']}\n")
        if event["description"]:
            lines.append(f"{event['description']}\n")
        if not event["talks"]:
            lines.append("Доклады не запланированы.\n")
        else:
            for talk in event["talks"]:
                time = talk.get("time", "").ljust(6)
                speaker = talk.get("speaker", "")
                topic = talk.get("topic", "")
                if speaker and topic:
                    lines.append(f"{time} {speaker}\nТема: {topic}\n")
                elif speaker:
                    lines.append(f"{time} {speaker}\n")
                elif topic:
                    lines.append(f"{time} {topic}\n")
        lines.append("-" * 32)
    lines.append("Нажмите 'Назад', чтобы вернуться в меню.")
    return "\n".join(lines)


async def schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info("Пользователь %s запросил расписание мероприятия", user_id)
    try:
        events = await schedule_service.get_schedule()
        text = format_schedule(events)
        await send_message_with_retry(
            update.message, text, reply_markup=get_schedule_keyboard()
        )
    except Exception as e:
        logger.error("Ошибка получения расписания для пользователя %s: %s", user_id, e)
        await send_message_with_retry(
            update.message, "Ошибка при получении расписания."
        )
    return STATE_SCHEDULE


async def back_to_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_spk = await is_speaker(user_id)
    logger.info("Пользователь %s вернулся в меню из расписания", user_id)
    await send_message_with_retry(
        update.message,
        "Вы в главном меню. Выберите действие:",
        reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
    )
    context.user_data.clear()
    return STATE_MENU
