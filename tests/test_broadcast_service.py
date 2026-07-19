from unittest.mock import patch

import pytest

from apps.events.models import SendMessage, Speaker, UserProfile
from bot.services.broadcast_service import send_broadcast


@pytest.mark.django_db
@patch("bot.services.broadcast_service.send_telegram_message", side_effect=[True, False])
def test_broadcast_tracks_delivery_failures(mock_send):
    Speaker.objects.create(name="Спикер", telegram_id=1)
    UserProfile.objects.create(name="Участник", telegram_id=2)
    broadcast = SendMessage.objects.create(group="all", message="Новости")

    result = send_broadcast(broadcast)

    broadcast.refresh_from_db()
    assert result.delivered == 1
    assert result.failed == 1
    assert not broadcast.is_sent
    assert broadcast.delivered_count == 1
    assert broadcast.failed_count == 1
    assert mock_send.call_count == 2
