import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.handlers.donations import (
    donate_handler, donate_init_handler, donate_confirm_handler
)
from bot.constants import (
    STATE_DONATE_INIT, STATE_DONATE_CONFIRM, STATE_MENU
)

@pytest.mark.asyncio
async def test_donate_full_flow():
    update = MagicMock()
    update.message = AsyncMock()
    context = MagicMock()
    context.user_data = {}

    state = await donate_handler(update, context)
    assert state == STATE_DONATE_INIT

    # Ввод суммы
    update.message.text = "500"
    state = await donate_init_handler(update, context)
    assert state == STATE_DONATE_CONFIRM
    assert context.user_data["donate_amount"] == 500

    # Подтверждение
    update.message.text = "500 ₽"
    state = await donate_confirm_handler(update, context)
    assert state == STATE_MENU
