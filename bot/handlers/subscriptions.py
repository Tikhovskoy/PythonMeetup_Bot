from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import STATE_MENU, STATE_SUBSCRIBE_CONFIRM
from bot.keyboards.subscriptions_keyboards import get_subscribe_keyboard
from bot.keyboards.main_menu import get_main_menu_keyboard

async def subscribe_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Хотите получать уведомления о будущих митапах?\n\n"
        "Нажмите «✅ Подписаться» для подтверждения.",
        reply_markup=get_subscribe_keyboard(),
    )
    return STATE_SUBSCRIBE_CONFIRM

async def subscribe_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "⬅️ Назад":
        await update.message.reply_text(
            "Вы в главном меню. Выберите действие:",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU

    if text == "✅ Подписаться":
        print(f"[SUBSCRIBE] Пользователь {update.effective_user.id} подписался на новости")
        await update.message.reply_text(
            "Спасибо, вы подписались на новости митапа!\n\n"
            "Вы в главном меню.",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU

    await update.message.reply_text(
        "Пожалуйста, выберите «✅ Подписаться» или «⬅️ Назад».",
        reply_markup=get_subscribe_keyboard(),
    )
    return STATE_SUBSCRIBE_CONFIRM
