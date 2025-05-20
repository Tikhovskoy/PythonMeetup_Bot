import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.handlers.subscriptions import (
    subscribe_handler, subscribe_confirm_handler
)
from bot.constants import (
    STATE_SUBSCRIBE_CONFIRM, STATE_MENU
)

@pytest.mark.asyncio
async def test_subscription_flow():
    update = MagicMock()
    update.message = AsyncMock()
    context = MagicMock()

    state = await subscribe_handler(update, context)
    assert state == STATE_SUBSCRIBE_CONFIRM

    # Подтвердить подписку
    update.message.text = "✅ Подписаться"
    state = await subscribe_confirm_handler(update, context)
    assert state == STATE_MENU
