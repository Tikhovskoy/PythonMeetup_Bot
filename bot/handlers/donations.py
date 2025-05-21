import os
from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes
from bot.constants import STATE_MENU
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.keyboards.donations_keyboards import get_cancel_keyboard

PAYMENT_TITLE = "Донат на PythonMeetup"
PAYMENT_DESC = "Поддержи митап — любая сумма помогает сообществу!"
CURRENCY = "RUB"

async def donate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Спасибо, что хотите поддержать мероприятие!\n"
        "Введите сумму доната (в рублях, целое число):",
        reply_markup=get_cancel_keyboard(),
    )
    return "DONATE_WAIT_AMOUNT"

async def donate_wait_amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Назад":
        await update.message.reply_text(
            "Оплата отменена.",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU
    try:
        amount = int(update.message.text.strip())
        if amount <= 0:
            raise ValueError()
    except Exception:
        await update.message.reply_text(
            "Введите сумму целым числом больше 0 (например: 500):",
            reply_markup=get_cancel_keyboard(),
        )
        return "DONATE_WAIT_AMOUNT"
    context.user_data["donate_amount"] = amount
    provider_token = os.environ.get("PAYMENTS_PROVIDER_TOKEN")
    if not provider_token:
        await update.message.reply_text(
            "Платёжная система временно недоступна. Попробуйте позже.",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU
    prices = [LabeledPrice(label="Донат на митап", amount=amount * 100)]
    await update.message.reply_invoice(
        title=PAYMENT_TITLE,
        description=PAYMENT_DESC,
        payload="meetup-donation",
        provider_token=provider_token,
        currency=CURRENCY,
        prices=prices,
        start_parameter="donate"
    )
    return "DONATE_WAIT_PAYMENT"

async def donate_cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Оплата отменена.",
        reply_markup=get_main_menu_keyboard(),
    )
    return STATE_MENU

async def precheckout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.successful_payment.total_amount // 100
    await update.message.reply_text(
        f"Спасибо за донат! Ты поддержал митап на {amount} ₽ 🙏",
        reply_markup=get_main_menu_keyboard(),
    )
    return STATE_MENU
