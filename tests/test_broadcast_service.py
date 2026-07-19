from unittest.mock import patch

import pytest

from apps.events.models import BroadcastDelivery, SendMessage, Speaker, UserProfile
from apps.events.tasks import send_broadcast_delivery
from bot.services.broadcast_service import enqueue_broadcast, prepare_broadcast


@pytest.mark.django_db
def test_prepare_broadcast_creates_one_delivery_per_recipient():
    Speaker.objects.create(name="Спикер", telegram_id=1)
    UserProfile.objects.create(name="Участник", telegram_id=2)
    broadcast = SendMessage.objects.create(group="all", message="Новости")

    deliveries = prepare_broadcast(broadcast)

    assert {delivery.telegram_id for delivery in deliveries} == {1, 2}
    assert BroadcastDelivery.objects.filter(broadcast=broadcast).count() == 2


@pytest.mark.django_db
@patch("apps.events.tasks.send_broadcast_delivery.delay")
def test_enqueue_broadcast_queues_all_deliveries(mock_delay):
    Speaker.objects.create(name="Спикер", telegram_id=1)
    broadcast = SendMessage.objects.create(group="speakers", message="Новости")

    enqueue_broadcast(broadcast.pk)

    assert mock_delay.call_count == 1


@pytest.mark.django_db
@patch("apps.events.tasks.send_telegram_message", return_value=True)
def test_delivery_task_marks_successful_delivery(mock_send):
    broadcast = SendMessage.objects.create(group="speakers", message="Новости")
    delivery = BroadcastDelivery.objects.create(broadcast=broadcast, telegram_id=1)

    send_broadcast_delivery.apply(args=[delivery.pk])

    delivery.refresh_from_db()
    broadcast.refresh_from_db()
    assert delivery.status == BroadcastDelivery.STATUS_SENT
    assert delivery.attempts == 1
    assert broadcast.delivered_count == 1
    assert broadcast.is_sent
    mock_send.assert_called_once_with(1, "Новости")


@pytest.mark.django_db
@patch("apps.events.tasks.send_telegram_message", return_value=False)
def test_delivery_task_marks_delivery_failed_after_retries(mock_send):
    broadcast = SendMessage.objects.create(group="speakers", message="Новости")
    delivery = BroadcastDelivery.objects.create(broadcast=broadcast, telegram_id=1)

    send_broadcast_delivery.apply(args=[delivery.pk])

    delivery.refresh_from_db()
    broadcast.refresh_from_db()
    assert delivery.status == BroadcastDelivery.STATUS_FAILED
    assert delivery.attempts == 3
    assert broadcast.failed_count == 1
    assert not broadcast.is_sent
    assert mock_send.call_count == 3
