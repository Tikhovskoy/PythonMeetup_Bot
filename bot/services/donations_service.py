from typing import List, Optional

from apps.events.models import Donate
from bot.logging_tools import logger


def validate_donation_data(data: dict) -> Optional[str]:
    if not data.get("telegram_id"):
        return "Не указан Telegram ID."
    amount = data.get("amount")
    if amount is None:
        return "Не указана сумма."
    try:
        amount = int(amount)
        if amount <= 0:
            return "Сумма должна быть больше нуля."
    except Exception:
        return "Сумма должна быть целым числом."
    return None


def save_donation(data: dict) -> Donate:
    error = validate_donation_data(data)
    if error:
        logger.warning("Ошибка валидации доната: %s | Данные: %s", error, data)
        raise ValueError(error)
    donation = Donate.objects.create(
        telegram_id=data["telegram_id"],
        name=data.get("name", ""),
        amount=int(data["amount"]),
    )
    logger.info(
        "Сохранён донат пользователя %s на сумму %s",
        data["telegram_id"],
        data["amount"],
    )
    return donation


def get_all_donations() -> List[Donate]:
    logger.info("Запрошен список всех донатов")
    return list(Donate.objects.all())


def get_total_amount() -> int:
    total = sum(d.amount for d in Donate.objects.all())
    logger.info("Запрошена общая сумма донатов: %s", total)
    return total


def clear_donations() -> None:
    Donate.objects.all().delete()
    logger.warning("Все донаты были удалены администратором")
