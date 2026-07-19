from celery import shared_task
from django.utils import timezone

from apps.events.models import BroadcastDelivery
from bot.services.broadcast_service import refresh_broadcast_status
from bot.services.send_message_service import send_telegram_message


@shared_task(bind=True, max_retries=2)
def send_broadcast_delivery(self, delivery_id: int) -> None:
    delivery = BroadcastDelivery.objects.select_related("broadcast").get(pk=delivery_id)
    if delivery.status == BroadcastDelivery.STATUS_SENT:
        return

    delivery.attempts += 1
    if send_telegram_message(delivery.telegram_id, delivery.broadcast.message):
        delivery.status = BroadcastDelivery.STATUS_SENT
        delivery.sent_at = timezone.now()
        delivery.last_error = ""
        delivery.save(update_fields=["attempts", "status", "sent_at", "last_error"])
        refresh_broadcast_status(delivery.broadcast)
        return

    if self.request.retries < self.max_retries:
        delivery.save(update_fields=["attempts"])
        raise self.retry(countdown=60)

    delivery.status = BroadcastDelivery.STATUS_FAILED
    delivery.last_error = "Telegram API не принял сообщение"
    delivery.save(update_fields=["attempts", "status", "last_error"])
    refresh_broadcast_status(delivery.broadcast)
