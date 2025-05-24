from typing import Optional, List
from apps.events.models import Subscription

def subscribe(telegram_id: int) -> Subscription:
    sub, _ = Subscription.objects.update_or_create(
        telegram_id=telegram_id,
        defaults={'is_subscribed': True},
    )
    return sub

def unsubscribe(telegram_id: int) -> None:
    Subscription.objects.filter(telegram_id=telegram_id).update(is_subscribed=False)

def is_subscribed(telegram_id: int) -> bool:
    return Subscription.objects.filter(telegram_id=telegram_id, is_subscribed=True).exists()

def get_all_subscribed() -> list:
    return list(
        Subscription.objects.filter(is_subscribed=True)
        .values_list("telegram_id", flat=True)
    )

def clear_subscriptions() -> None:
    Subscription.objects.all().delete()
