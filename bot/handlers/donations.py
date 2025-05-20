from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import (
    STATE_MENU, STATE_DONATE_INIT, STATE_DONATE_CONFIRM,
)
from bot.keyboards.donations_keyboards import (
    get_donate_keyboard, get_donate_confirm_keyboard,
)
from bot.keyboards.main_menu import get_main_menu_keyboard

async def donate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Спасибо, что хотите поддержать мероприятие!\n"
        "Выберите сумму доната или введите свою:",
        reply_markup=get_donate_keyboard(),
    )
    return STATE_DONATE_INIT

async def donate_init_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "⬅️ Назад":
        await update.message.reply_text(
            "Вы в главном меню. Выберите действие:",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU

    # Определяем сумму
    amount = None
    if text.endswith("₽"):
        try:
            amount = int(text[:-1].strip())
        except Exception:
            pass
    else:
        try:
            amount = int(text.strip())
        except Exception:
            pass

    if not amount or amount <= 0:
        await update.message.reply_text(
            "Пожалуйста, выберите сумму кнопкой или введите целое число больше 0.",
            reply_markup=get_donate_keyboard(),
        )
        return STATE_DONATE_INIT

    context.user_data["donate_amount"] = amount

    await update.message.reply_text(
        f"Вы хотите задонатить {amount} ₽?\n"
        "Нажмите ещё раз сумму для подтверждения или '⬅️ Назад' для отмены.",
        reply_markup=get_donate_confirm_keyboard(amount),
    )
    return STATE_DONATE_CONFIRM

async def donate_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    amount = context.user_data.get("donate_amount")
    if text == "⬅️ Назад":
        await update.message.reply_text(
            "Донат отменён. Вы в главном меню.",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU

    if text == f"{amount} ₽":
        print(f"[DONATE] Пользователь {update.effective_user.id} отправил заявку на донат: {amount} ₽")
        await update.message.reply_text(
            f"Спасибо за поддержку митапа!\n\nТы в главном меню.",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU

    await update.message.reply_text(
        "Ошибка подтверждения. Попробуйте снова.",
        reply_markup=get_donate_keyboard(),
    )
    return STATE_DONATE_INIT
