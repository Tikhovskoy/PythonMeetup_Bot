import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from bot.handlers import donations
from bot.services import donations_service

@pytest.fixture(autouse=True)
def clear_donations():
    donations_service.clear_donations()

@pytest.mark.asyncio
async def test_donation_flow(monkeypatch):
    user_id = 4444
    context = MagicMock()
    context.user_data = {}

    update = MagicMock(spec=Update)
    update.effective_user.id = user_id
    update.message.reply_text = AsyncMock()
    update.message.reply_invoice = AsyncMock()
    update.message.text = "1000"

    # monkeypatch provider_token для теста
    monkeypatch.setenv("PAYMENTS_PROVIDER_TOKEN", "test_provider_token")

    await donations.donate_wait_amount_handler(update, context)

    donations_list = donations_service.get_all_donations()
    assert donations_list
    assert donations_list[0]['telegram_id'] == user_id
    assert donations_list[0]['amount'] == 1000
