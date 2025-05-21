from telegram import Update
from telegram.ext import ContextTypes
from bot.constants import (
    STATE_MENU, STATE_NETW_NAME, STATE_NETW_CONTACTS, STATE_NETW_STACK,
    STATE_NETW_ROLE, STATE_NETW_GRADE, STATE_NETW_SHOW,
)
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.keyboards.networking_keyboards import get_next_profile_keyboard, get_profiles_finished_keyboard
from bot.services import networking_service

async def networking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['profile'] = {}
    await update.message.reply_text("Давай познакомимся!\n\nВведи свои ФИО:")
    return STATE_NETW_NAME

async def netw_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['profile']['name'] = update.message.text.strip()
    await update.message.reply_text("Укажи контакт для связи (Telegram, телефон):")
    return STATE_NETW_CONTACTS

async def netw_contacts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['profile']['contacts'] = update.message.text.strip()
    await update.message.reply_text("Опиши свой технологический стек (например: Python, Django, PostgreSQL):")
    return STATE_NETW_STACK

async def netw_stack_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['profile']['stack'] = update.message.text.strip()
    await update.message.reply_text("Твоя роль (например: Backend, Frontend, DevOps):")
    return STATE_NETW_ROLE

async def netw_role_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['profile']['role'] = update.message.text.strip()
    await update.message.reply_text("Твой грейд (например: Junior, Middle, Senior):")
    return STATE_NETW_GRADE

async def netw_grade_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['profile']['grade'] = update.message.text.strip()
    profile = context.user_data['profile']
    print(f"[NETWORKING] Новая анкета: {profile}")
    await update.message.reply_text(
        "Спасибо! Твоя анкета сохранена. В будущем ты сможешь знакомиться с другими участниками.\n\n"
        "Ты в главном меню.",
        reply_markup=get_main_menu_keyboard(),
    )
    return STATE_MENU

async def netw_show_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    telegram_id = update.effective_user.id
    viewed = context.user_data.get('viewed_profiles', [])

    if text == "➡️ Дальше":
        current = context.user_data.get('current_profile_id')
        if current and current not in viewed:
            viewed.append(current)
        context.user_data['viewed_profiles'] = viewed
        return await show_next_profile(update, context)
    if text == "🔄 Начать сначала":
        context.user_data['viewed_profiles'] = []
        return await show_next_profile(update, context)
    if text == "⬅️ В меню":
        await update.message.reply_text(
            "Ты в главном меню.",
            reply_markup=get_main_menu_keyboard(),
        )
        return STATE_MENU

    await update.message.reply_text(
        "Пожалуйста, пользуйтесь кнопками!",
        reply_markup=get_next_profile_keyboard(),
    )
    return STATE_NETW_SHOW