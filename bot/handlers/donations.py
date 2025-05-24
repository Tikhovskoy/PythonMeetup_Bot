import os

from asgiref.sync import sync_to_async
from telegram import LabeledPrice, Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU
from bot.keyboards.donations_keyboards import get_cancel_keyboard
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.logging_tools import logger
from bot.services import donations_service
from bot.services.core_service import is_speaker
from bot.utils.telegram_utils import send_message_with_retry

PAYMENT_TITLE = "Донат на PythonMeetup"
PAYMENT_DESC = "Поддержи митап — любая сумма помогает сообществу!"
CURRENCY = "RUB"


async def donate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Пользователь %s начал процесс доната", update.effective_user.id)
    await send_message_with_retry(
        update.message,
        "Спасибо, что хотите поддержать мероприятие!\nВведите сумму доната (в рублях, целое число):",
        reply_markup=get_cancel_keyboard(),
    )
    return "DONATE_WAIT_AMOUNT"


async def donate_wait_amount_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    if update.message.text == "⬅️ Назад":
        is_spk = await is_speaker(user_id)
        logger.info("Пользователь %s отменил донат на этапе ввода суммы", user_id)
        await send_message_with_retry(
            update.message,
            "Оплата отменена.",
            reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
        )
        return STATE_MENU
    try:
        amount = int(update.message.text.strip())
        data = {"telegram_id": user_id, "amount": amount}
        await sync_to_async(donations_service.save_donation)(data)
        logger.info("Пользователь %s ввёл сумму доната: %s", user_id, amount)
    except Exception as e:
        logger.warning("Ошибка ввода суммы доната пользователем %s: %s", user_id, e)
        await send_message_with_retry(
            update.message,
            "Введите сумму целым числом больше 0 (например: 500):",
            reply_markup=get_cancel_keyboard(),
        )
        return "DONATE_WAIT_AMOUNT"
    context.user_data["donate_amount"] = amount
    provider_token = os.environ.get("PAYMENTS_PROVIDER_TOKEN")
    is_spk = await is_speaker(user_id)
    if not provider_token:
        logger.error(
            "PAYMENTS_PROVIDER_TOKEN не найден, пользователь %s не смог провести платёж",
            user_id,
        )
        await send_message_with_retry(
            update.message,
            "Платёжная система временно недоступна. Попробуйте позже.",
            reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
        )
        return STATE_MENU
    prices = [LabeledPrice(label="Донат на митап", amount=amount * 100)]
    logger.info("Пользователь %s получает инвойс на сумму %s", user_id, amount)
    await update.message.reply_invoice(
        title=PAYMENT_TITLE,
        description=PAYMENT_DESC,
        payload="meetup-donation",
        provider_token=provider_token,
        currency=CURRENCY,
        prices=prices,
        start_parameter="donate",
    )
    return "DONATE_WAIT_PAYMENT"


async def donate_cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_spk = await is_speaker(user_id)
    logger.info("Пользователь %s отменил донат", user_id)
    await send_message_with_retry(
        update.message,
        "Оплата отменена.",
        reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
    )
    return STATE_MENU


async def precheckout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


async def successful_payment_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    amount = update.message.successful_payment.total_amount // 100
    is_spk = await is_speaker(user_id)
    logger.info("Пользователь %s успешно задонатил %s руб.", user_id, amount)
    await send_message_with_retry(
        update.message,
        f"Спасибо за донат! Ты поддержал митап на {amount} ₽ 🙏",
        reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
    )
    return STATE_MENU
