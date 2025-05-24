from unittest.mock import AsyncMock, patch

import pytest

from bot.handlers import subscriptions


@pytest.mark.asyncio
@patch("bot.handlers.subscriptions.send_message_with_retry", new_callable=AsyncMock)
@patch("bot.services.subscriptions_service.is_subscribed", return_value=False)
async def test_subscribe_handler_shows_menu(mock_is_sub, mock_send, mocker):
    update = mocker.Mock()
    update.effective_user.id = 1
    context = mocker.Mock()
    await subscriptions.subscribe_handler(update, context)
    mock_send.assert_awaited()
    args = mock_send.call_args[0]
    assert "Хотите получать уведомления" in args[1]


@pytest.mark.asyncio
@pytest.mark.django_db
@patch("bot.handlers.subscriptions.send_message_with_retry", new_callable=AsyncMock)
@patch("bot.services.subscriptions_service.subscribe")
@patch("bot.services.subscriptions_service.is_subscribed", return_value=False)
async def test_subscribe_confirm_handler_subscribe(
    mock_is_sub, mock_sub, mock_send, mocker
):
    update = mocker.Mock()
    update.effective_user.id = 2
    update.message.text = "✅ Подписаться"
    context = mocker.Mock()
    await subscriptions.subscribe_confirm_handler(update, context)
    mock_sub.assert_called_with(2)
    mock_send.assert_awaited()
