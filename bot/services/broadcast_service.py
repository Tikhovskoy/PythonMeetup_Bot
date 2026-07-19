from dataclasses import dataclass

from apps.events.models import SendMessage, Speaker, UserProfile
from bot.services.send_message_service import send_telegram_message


@dataclass(frozen=True)
class BroadcastResult:
    delivered: int
    failed: int


def send_broadcast(broadcast: SendMessage) -> BroadcastResult:
    if broadcast.is_sent:
        return BroadcastResult(broadcast.delivered_count, broadcast.failed_count)

    telegram_ids = set()
    if broadcast.group in {"speakers", "all"}:
        telegram_ids.update(Speaker.objects.values_list("telegram_id", flat=True))
    if broadcast.group in {"listeners", "all"}:
        telegram_ids.update(
            UserProfile.objects.exclude(telegram_id__isnull=True).values_list("telegram_id", flat=True)
        )

    delivered = failed = 0
    for chat_id in telegram_ids:
        if send_telegram_message(chat_id, broadcast.message):
            delivered += 1
        else:
            failed += 1

    broadcast.delivered_count = delivered
    broadcast.failed_count = failed
    broadcast.is_sent = failed == 0
    broadcast.save(update_fields=["delivered_count", "failed_count", "is_sent"])
    return BroadcastResult(delivered, failed)
