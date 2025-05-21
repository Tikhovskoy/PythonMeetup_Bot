from typing import List, Dict, Optional
from datetime import datetime

_FAKE_DONATIONS: List[dict] = []

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

def save_donation(data: dict) -> dict:
    error = validate_donation_data(data)
    if error:
        raise ValueError(error)
    donation = {
        'telegram_id': data['telegram_id'],
        'amount': int(data['amount']),
        'created_at': datetime.now().isoformat(),
    }
    _FAKE_DONATIONS.append(donation)
    return donation

def get_all_donations() -> List[dict]:
    return list(_FAKE_DONATIONS)

def get_total_amount() -> int:
    return sum(d['amount'] for d in _FAKE_DONATIONS)

def clear_donations() -> None:
    _FAKE_DONATIONS.clear()
