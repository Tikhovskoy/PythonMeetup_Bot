from typing import List, Dict, Optional
from apps.events.models import Donate

def validate_donation_data(data: dict) -> Optional[str]:
    if not data.get('telegram_id'):
        return "Не указан Telegram ID."
    amount = data.get('amount')
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
        raise ValueError(error)
    return Donate.objects.create(
        telegram_id=data['telegram_id'],
        name=data.get('name', ''),
        amount=int(data['amount'])
    )

def get_all_donations() -> List[Donate]:
    return list(Donate.objects.all())

def get_total_amount() -> int:
    return sum(d.amount for d in Donate.objects.all())

def clear_donations() -> None:
    Donate.objects.all().delete()
