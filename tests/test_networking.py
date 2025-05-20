import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from bot.handlers.networking import (
    networking_handler,
    netw_name_handler,
    netw_contacts_handler,
    netw_stack_handler,
    netw_role_handler,
    netw_grade_handler,
)
from bot.constants import (
    STATE_NETW_NAME, STATE_NETW_CONTACTS, STATE_NETW_STACK, STATE_NETW_ROLE, STATE_NETW_GRADE, STATE_MENU
)

@pytest.mark.asyncio
async def test_networking_full_flow():
    update = MagicMock()
    update.message = AsyncMock()
    context = MagicMock()
    context.user_data = {}

    # Запускаем анкету
    state = await networking_handler(update, context)
    assert state == STATE_NETW_NAME
    update.message.reply_text.assert_awaited_with("Давай познакомимся!\n\nВведи свои ФИО:")

    # ФИО
    update.message.text = "Иван Иванов"
    state = await netw_name_handler(update, context)
    assert state == STATE_NETW_CONTACTS
    update.message.reply_text.assert_awaited_with("Укажи контакт для связи (Telegram, телефон):")

    # Контакты
    update.message.text = "@ivan"
    state = await netw_contacts_handler(update, context)
    assert state == STATE_NETW_STACK
    update.message.reply_text.assert_awaited_with(
        "Опиши свой технологический стек (например: Python, Django, PostgreSQL):"
    )

    # Стек
    update.message.text = "Python"
    state = await netw_stack_handler(update, context)
    assert state == STATE_NETW_ROLE
    update.message.reply_text.assert_awaited_with(
        "Твоя роль (например: Backend, Frontend, DevOps):"
    )

    # Роль
    update.message.text = "Backend"
    state = await netw_role_handler(update, context)
    assert state == STATE_NETW_GRADE
    update.message.reply_text.assert_awaited_with(
        "Твой грейд (например: Junior, Middle, Senior):"
    )

    # Грейд
    update.message.text = "Junior"
    state = await netw_grade_handler(update, context)
    assert state == STATE_MENU
    assert context.user_data["profile"] == {
        "name": "Иван Иванов",
        "contacts": "@ivan",
        "stack": "Python",
        "role": "Backend",
        "grade": "Junior"
    }
    update.message.reply_text.assert_awaited()  # главное меню

