from telegram import Update
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async

from bot.constants import STATE_MENU, STATE_SUBSCRIBE_CONFIRM
from bot.keyboards.subscriptions_keyboards import get_subscribe_keyboard
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.services import subscriptions_service
from bot.services.core_service import is_speaker
from bot.utils.telegram_utils import send_message_with_retry

async def subscribe_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    is_sub = await sync_to_async(subscriptions_service.is_subscribed)(telegram_id)
    await send_message_with_retry(
        update.message,
        "Хотите получать уведомления о будущих митапах?\n\n"
        "Выберите действие:",
        reply_markup=get_subscribe_keyboard(is_subscribed=is_sub),
    )
    return STATE_SUBSCRIBE_CONFIRM

async def subscribe_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    telegram_id = update.effective_user.id
    is_spk = await is_speaker(telegram_id)

    if text == "⬅️ Назад":
        await send_message_with_retry(
            update.message,
            "Вы в главном меню. Выберите действие:",
            reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
        )
        return STATE_MENU

    if text == "✅ Подписаться":
        await sync_to_async(subscriptions_service.subscribe)(telegram_id)
        await send_message_with_retry(
            update.message,
            "Спасибо, вы подписались на новости митапа!\n\n"
            "Вы в главном меню.",
            reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
        )
        return STATE_MENU

    if text == "❌ Отписаться":
        await sync_to_async(subscriptions_service.unsubscribe)(telegram_id)
        await send_message_with_retry(
            update.message,
            "Вы успешно отписались от новостей митапа.\n\n"
            "Вы в главном меню.",
            reply_markup=get_main_menu_keyboard(is_speaker=is_spk),
        )
        return STATE_MENU

    is_sub = await sync_to_async(subscriptions_service.is_subscribed)(telegram_id)
    await send_message_with_retry(
        update.message,
        "Пожалуйста, выберите действие из меню.",
        reply_markup=get_subscribe_keyboard(is_subscribed=is_sub),
    )
    return STATE_SUBSCRIBE_CONFIRM
