from apps.events.models import Subscription
from bot.logging_tools import logger


def subscribe(telegram_id: int) -> Subscription:
    sub, _ = Subscription.objects.update_or_create(
        telegram_id=telegram_id,
        defaults={"is_subscribed": True},
    )
    logger.info("Пользователь %s оформил подписку", telegram_id)
    return sub


def unsubscribe(telegram_id: int) -> None:
    Subscription.objects.filter(telegram_id=telegram_id).update(is_subscribed=False)
    logger.info("Пользователь %s отписался от новостей", telegram_id)


def is_subscribed(telegram_id: int) -> bool:
    result = Subscription.objects.filter(
        telegram_id=telegram_id, is_subscribed=True
    ).exists()
    logger.info("Проверка подписки пользователя %s: %s", telegram_id, result)
    return result


def get_all_subscribed() -> list:
    logger.info("Запрошен список всех подписанных пользователей")
    return list(
        Subscription.objects.filter(is_subscribed=True).values_list(
            "telegram_id", flat=True
        )
    )


def clear_subscriptions() -> None:
    Subscription.objects.all().delete()
    logger.warning("Все подписки были удалены")
