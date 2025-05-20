from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU, STATE_QNA_SELECT_SPEAKER, STATE_QNA_ASK_TEXT
from bot.keyboards.qna_keyboards import get_speakers_keyboard
from bot.keyboards.main_menu import get_main_menu_keyboard

MOCK_SPEAKERS = [
    {"id": 1, "name": "Иван Иванов"},
    {"id": 2, "name": "Мария Петрова"},
]
MOCK_ACTIVE_SESSION = {"speaker": MOCK_SPEAKERS[0]}  # Или None, если нет активной сессии

async def qna_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if MOCK_ACTIVE_SESSION:
        context.user_data["qna_speaker"] = MOCK_ACTIVE_SESSION["speaker"]["name"]
        await update.message.reply_text(
            f"Сейчас выступает {MOCK_ACTIVE_SESSION['speaker']['name']}.\n"
            "Напиши свой вопрос:"
        )
        return STATE_QNA_ASK_TEXT
    await update.message.reply_text(
        "Выбери, кому из спикеров ты хочешь задать вопрос:",
        reply_markup=get_speakers_keyboard(MOCK_SPEAKERS),
    )
    return STATE_QNA_SELECT_SPEAKER

async def qna_select_speaker_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    speaker_name = update.message.text
    if speaker_name == "⬅️ Назад":
        await update.message.reply_text(
            "Вы в главном меню. Выберите действие:",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU
    speaker_names = [s["name"] for s in MOCK_SPEAKERS]
    if speaker_name not in speaker_names:
        await update.message.reply_text(
            "Пожалуйста, выбери спикера из списка.",
            reply_markup=get_speakers_keyboard(MOCK_SPEAKERS),
        )
        return STATE_QNA_SELECT_SPEAKER
    context.user_data["qna_speaker"] = speaker_name
    await update.message.reply_text(
        f"Отправь свой вопрос для {speaker_name}:"
    )
    return STATE_QNA_ASK_TEXT

async def qna_ask_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question_text = update.message.text
    speaker = context.user_data.get("qna_speaker", "не выбран")
    print(f"[QNA] Вопрос для {speaker}: {question_text}")
    await update.message.reply_text(
        "Спасибо, твой вопрос отправлен спикеру!\n\nТы в главном меню:",
        reply_markup=get_main_menu_keyboard(),
    )
    return STATE_MENU
