import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from bot.handlers import subscriptions
from bot.services import subscriptions_service

@pytest.fixture(autouse=True)
def clear_subs():
    subscriptions_service.clear_subscriptions()

@pytest.mark.asyncio
async def test_subscribe_and_unsubscribe_flow():
    user_id = 2222
    context = MagicMock()
    update = MagicMock(spec=Update)
    update.effective_user.id = user_id
    update.message.reply_text = AsyncMock()
    
    # Подписка
    update.message.text = "✅ Подписаться"
    await subscriptions.subscribe_confirm_handler(update, context)
    assert subscriptions_service.is_subscribed(user_id)

    # Отписка
    update.message.text = "❌ Отписаться"
    await subscriptions.subscribe_confirm_handler(update, context)
    assert not subscriptions_service.is_subscribed(user_id)
