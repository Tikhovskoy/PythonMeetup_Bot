import os

from asgiref.sync import sync_to_async
from telegram import LabeledPrice, Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU
from bot.keyboards.donations_keyboards import get_cancel_keyboard
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.logging_tools import logger
from bot.services import payments_service
from bot.services.core_service import is_speaker
from bot.utils.telegram_utils import send_message_with_retry

PAYMENT_TITLE = "Донат на PythonMeetup"
PAYMENT_DESC = "Поддержи митап — любая сумма помогает сообществу!"
CURRENCY = "RUB"
MAX_DONATE_AMOUNT = 99999


async def donate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Пользователь %s начал процесс доната", update.effective_user.id)
    await send_message_with_retry(
        update.message,
        "Спасибо, что хотите поддержать мероприятие!\nВведите сумму доната (в рублях, целое число, максимум 99 999):",
        reply_markup=get_cancel_keyboard(),
    )
    return "DONATE_WAIT_AMOUNT"


async def donate_wait_amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        if amount <= 0:
            raise ValueError("Сумма должна быть больше 0")
        if amount > MAX_DONATE_AMOUNT:
            await send_message_with_retry(
                update.message,
                f"Максимальная сумма доната — {MAX_DONATE_AMOUNT} руб.\n"
                "Пожалуйста, введите меньшую сумму.",
                reply_markup=get_cancel_keyboard(),
            )
            return "DONATE_WAIT_AMOUNT"
        logger.info("Пользователь %s ввёл сумму доната: %s", user_id, amount)
    except Exception as e:
        logger.warning("Ошибка ввода суммы доната пользователем %s: %s", user_id, e)
        await send_message_with_retry(
            update.message,
            "Введите сумму целым числом больше 0 (например: 500):",
            reply_markup=get_cancel_keyboard(),
        )
        return "DONATE_WAIT_AMOUNT"
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
    payment = await sync_to_async(payments_service.create_payment)(user_id, amount * 100, CURRENCY)
    prices = [LabeledPrice(label="Донат на митап", amount=payment.amount)]
    logger.info("Пользователь %s получает инвойс на сумму %s", user_id, amount)
    try:
        await update.message.reply_invoice(
            title=PAYMENT_TITLE,
            description=PAYMENT_DESC,
            payload=str(payment.payload),
            provider_token=provider_token,
            currency=CURRENCY,
            prices=prices,
            start_parameter="donate",
        )
    except BadRequest as e:
        logger.warning("Ошибка при создании инвойса для пользователя %s: %s", user_id, e)
        await send_message_with_retry(
            update.message,
            "Слишком большая сумма! Пожалуйста, введите сумму поменьше (например, до 99 999).",
            reply_markup=get_cancel_keyboard(),
        )
        return "DONATE_WAIT_AMOUNT"
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
    query = update.pre_checkout_query
    is_valid = await sync_to_async(payments_service.validate_precheckout)(
        query.invoice_payload, query.from_user.id, query.total_amount, query.currency
    )
    await query.answer(
        ok=is_valid, error_message=None if is_valid else "Счёт устарел или некорректен."
    )


async def successful_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    payment_data = update.message.successful_payment
    amount = payment_data.total_amount // 100
    is_spk = await is_speaker(user_id)
    try:
        _, created = await sync_to_async(payments_service.finalize_payment)(
            payment_data.invoice_payload,
            user_id,
            payment_data.total_amount,
            payment_data.currency,
            payment_data.telegram_payment_charge_id,
            update.effective_user.full_name,
        )
    except (ValueError, payments_service.Payment.DoesNotExist):
        logger.error("Не удалось подтвердить платёж пользователя %s", user_id)
        await send_message_with_retry(
            update.message, "Не удалось подтвердить платёж. Обратитесь к организатору."
        )
        return STATE_MENU
    if not created:
        logger.info("Повторное уведомление об оплате %s", payment_data.telegram_payment_charge_id)
        return STATE_MENU
    logger.info("Пользователь %s успешно задонатил %s руб.", user_id, amount)
    await send_message_with_retry(
        update.message,
        f"Спасибо за донат! Ты поддержал митап на {amount} ₽ 🙏",
        reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
    )
    return STATE_MENU
