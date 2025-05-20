from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.constants import (
    STATE_MENU,
    STATE_APPLY_TOPIC,
    STATE_APPLY_DESC,
)

def get_speaker_keyboard():
    return ReplyKeyboardMarkup(
        [["⬅️ Назад"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def speaker_app_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['speaker_app'] = {}
    await update.message.reply_text(
        "Ты хочешь стать спикером!\n\nВведи тему своего доклада:",
        reply_markup=get_speaker_keyboard()
    )
    return STATE_APPLY_TOPIC

async def speaker_topic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "⬅️ Назад":
        from bot.keyboards.main_menu import get_main_menu_keyboard
        await update.message.reply_text(
            "Вы в главном меню.",
            reply_markup=get_main_menu_keyboard()
        )
        return STATE_MENU

    context.user_data['speaker_app']['topic'] = text.strip()
    await update.message.reply_text(
        "Кратко опиши свой доклад:",
        reply_markup=get_speaker_keyboard()
    )
    return STATE_APPLY_DESC

async def speaker_desc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "⬅️ Назад":
        from bot.keyboards.main_menu import get_main_menu_keyboard
        await update.message.reply_text(
            "Вы в главном меню.",
            reply_markup=get_main_menu_keyboard()
        )
        return STATE_MENU

    context.user_data['speaker_app']['desc'] = text.strip()
    topic = context.user_data['speaker_app'].get('topic', '')
    desc = context.user_data['speaker_app'].get('desc', '')

    # Здесь можно сохранить заявку в БД
    print(f"[SPEAKER] Новая заявка: тема — {topic}; описание — {desc}")

    from bot.keyboards.main_menu import get_main_menu_keyboard
    await update.message.reply_text(
        "Спасибо! Ваша заявка на выступление отправлена.\n\nВы в главном меню.",
        reply_markup=get_main_menu_keyboard()
    )
    return STATE_MENU
