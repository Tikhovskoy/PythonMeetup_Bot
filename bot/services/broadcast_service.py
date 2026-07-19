from apps.events.models import BroadcastDelivery, SendMessage, Speaker, UserProfile


def get_recipient_ids(broadcast: SendMessage) -> set[int]:
    telegram_ids: set[int] = set()
    if broadcast.group in {"speakers", "all"}:
        telegram_ids.update(Speaker.objects.values_list("telegram_id", flat=True))
    if broadcast.group in {"listeners", "all"}:
        telegram_ids.update(
            UserProfile.objects.exclude(telegram_id__isnull=True).values_list(
                "telegram_id", flat=True
            )
        )
    return telegram_ids


def prepare_broadcast(broadcast: SendMessage) -> list[BroadcastDelivery]:
    deliveries = [
        BroadcastDelivery(broadcast=broadcast, telegram_id=telegram_id)
        for telegram_id in get_recipient_ids(broadcast)
    ]
    BroadcastDelivery.objects.bulk_create(deliveries, ignore_conflicts=True)
    return list(broadcast.deliveries.filter(status=BroadcastDelivery.STATUS_PENDING))


def refresh_broadcast_status(broadcast: SendMessage) -> None:
    deliveries = broadcast.deliveries
    delivered_count = deliveries.filter(status=BroadcastDelivery.STATUS_SENT).count()
    failed_count = deliveries.filter(status=BroadcastDelivery.STATUS_FAILED).count()
    has_pending = deliveries.filter(status=BroadcastDelivery.STATUS_PENDING).exists()

    broadcast.delivered_count = delivered_count
    broadcast.failed_count = failed_count
    broadcast.is_sent = not has_pending and failed_count == 0
    broadcast.save(update_fields=["delivered_count", "failed_count", "is_sent"])


def enqueue_broadcast(broadcast_id: int) -> None:
    broadcast = SendMessage.objects.get(pk=broadcast_id)
    deliveries = prepare_broadcast(broadcast)

    if not deliveries:
        refresh_broadcast_status(broadcast)
        return

    from apps.events.tasks import send_broadcast_delivery

    for delivery in deliveries:
        send_broadcast_delivery.delay(delivery.pk)
