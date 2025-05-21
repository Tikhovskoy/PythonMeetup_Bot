from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU, STATE_SUBSCRIBE_CONFIRM
from bot.keyboards.subscriptions_keyboards import get_subscribe_keyboard
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.services import subscriptions_service

async def subscribe_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    is_sub = subscriptions_service.is_subscribed(telegram_id)
    await update.message.reply_text(
        "Хотите получать уведомления о будущих митапах?\n\n"
        "Выберите действие:",
        reply_markup=get_subscribe_keyboard(is_subscribed=is_sub),
    )
    return STATE_SUBSCRIBE_CONFIRM

async def subscribe_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    telegram_id = update.effective_user.id

    if text == "⬅️ Назад":
        await update.message.reply_text(
            "Вы в главном меню. Выберите действие:",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU

    if text == "✅ Подписаться":
        subscriptions_service.subscribe(telegram_id)
        await update.message.reply_text(
            "Спасибо, вы подписались на новости митапа!\n\n"
            "Вы в главном меню.",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU

    if text == "❌ Отписаться":
        subscriptions_service.unsubscribe(telegram_id)
        await update.message.reply_text(
            "Вы успешно отписались от новостей митапа.\n\n"
            "Вы в главном меню.",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU

    is_sub = subscriptions_service.is_subscribed(telegram_id)
    await update.message.reply_text(
        "Пожалуйста, выберите действие из меню.",
        reply_markup=get_subscribe_keyboard(is_subscribed=is_sub),
    )
    return STATE_SUBSCRIBE_CONFIRM
