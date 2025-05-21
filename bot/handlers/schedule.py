from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU, STATE_SCHEDULE
from bot.keyboards.schedule_keyboards import get_schedule_keyboard
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.services import schedule_service

async def schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = schedule_service.get_schedule()
    lines = ["🗓 Программа мероприятия:"]
    for item in events:
        time = item.get("time", "")
        speaker = item.get("speaker")
        topic = item.get("topic", "")
        if speaker:
            lines.append(f"— {time} | {speaker} | {topic}")
        else:
            lines.append(f"— {time} | {topic}")
    lines.append("\n⬅️ Нажми 'Назад', чтобы вернуться в меню.")
    text = "\n".join(lines)
    await update.message.reply_text(text, reply_markup=get_schedule_keyboard())
    return STATE_SCHEDULE

async def back_to_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вы в главном меню. Выберите действие:",
        reply_markup=get_main_menu_keyboard(),
    )
    return STATE_MENU
