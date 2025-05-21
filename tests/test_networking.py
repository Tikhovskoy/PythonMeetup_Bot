import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from bot.handlers import networking
from bot.services import networking_service

@pytest.fixture(autouse=True)
def clear_profiles():
    networking_service._FAKE_PROFILES.clear()

@pytest.mark.asyncio
async def test_full_networking_flow():
    user_id = 5555
    context = MagicMock()
    context.user_data = {}

    update = MagicMock(spec=Update)
    update.effective_user.id = user_id
    update.message.reply_text = AsyncMock()
    await networking.networking_handler(update, context)

    update.message.text = "Иван Петров"
    await networking.netw_name_handler(update, context)
    update.message.text = "@ivan"
    await networking.netw_contacts_handler(update, context)
    update.message.text = "Python"
    await networking.netw_stack_handler(update, context)
    update.message.text = "Backend"
    await networking.netw_role_handler(update, context)
    update.message.text = "Junior"
    await networking.netw_grade_handler(update, context)

    profile = networking_service.get_profile(user_id)
    assert profile is not None
    assert profile['name'] == "Иван Петров"
    assert profile['contacts'] == "@ivan"
    assert profile['stack'] == "Python"
    assert profile['role'] == "Backend"
    assert profile['grade'] == "Junior"
