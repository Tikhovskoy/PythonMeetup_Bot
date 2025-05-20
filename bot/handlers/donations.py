from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.constants import (
    STATE_MENU,
    STATE_DONATE_INIT,
    STATE_DONATE_CONFIRM,
)

# Моковые суммы доната
DONATE_SUMS = [100, 200, 500, 1000]

def get_donate_keyboard():
    return ReplyKeyboardMarkup(
        [[str(amount) + " ₽" for amount in DONATE_SUMS], ["⬅️ Назад"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def donate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Спасибо, что хотите поддержать мероприятие!\n"
        "Выберите сумму доната или введите свою:",
        reply_markup=get_donate_keyboard()
    )
    return STATE_DONATE_INIT

async def donate_init_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "⬅️ Назад":
        from bot.keyboards.main_menu import get_main_menu_keyboard
        await update.message.reply_text(
            "Вы в главном меню. Выберите действие:",
            reply_markup=get_main_menu_keyboard()
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
            reply_markup=get_donate_keyboard()
        )
        return STATE_DONATE_INIT

    context.user_data["donate_amount"] = amount

    await update.message.reply_text(
        f"Вы хотите задонатить {amount} ₽?\n\nНажмите ещё раз сумму для подтверждения или '⬅️ Назад' для отмены.",
        reply_markup=ReplyKeyboardMarkup(
            [[f"{amount} ₽"], ["⬅️ Назад"]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    return STATE_DONATE_CONFIRM

async def donate_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    amount = context.user_data.get("donate_amount")
    if text == "⬅️ Назад":
        from bot.keyboards.main_menu import get_main_menu_keyboard
        await update.message.reply_text(
            "Донат отменён. Вы в главном меню.",
            reply_markup=get_main_menu_keyboard()
        )
        return STATE_MENU

    if text == f"{amount} ₽":
        # Здесь можно интегрировать платёж 
        print(f"[DONATE] Пользователь {update.effective_user.id} отправил заявку на донат: {amount} ₽")
        from bot.keyboards.main_menu import get_main_menu_keyboard
        await update.message.reply_text(
            f"Спасибо за поддержку митапа!\n\nТы в главном меню.",
            reply_markup=get_main_menu_keyboard()
        )
        return STATE_MENU

    await update.message.reply_text(
        "Ошибка подтверждения. Попробуйте снова.",
        reply_markup=get_donate_keyboard()
    )
    return STATE_DONATE_INIT
