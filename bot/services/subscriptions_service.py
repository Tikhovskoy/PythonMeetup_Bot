from typing import Optional, Dict
from datetime import datetime

_FAKE_SUBSCRIPTIONS: Dict[int, dict] = {}

def subscribe(telegram_id: int) -> dict:
    sub = {
        'telegram_id': telegram_id,
        'is_subscribed': True,
        'created_at': datetime.now().isoformat(),
    }
    _FAKE_SUBSCRIPTIONS[telegram_id] = sub
    return sub

def unsubscribe(telegram_id: int) -> None:
    if telegram_id in _FAKE_SUBSCRIPTIONS:
        _FAKE_SUBSCRIPTIONS[telegram_id]['is_subscribed'] = False

def is_subscribed(telegram_id: int) -> bool:
    sub = _FAKE_SUBSCRIPTIONS.get(telegram_id)
    return bool(sub and sub['is_subscribed'])

def get_all_subscribed() -> list:
    return [tid for tid, sub in _FAKE_SUBSCRIPTIONS.items() if sub['is_subscribed']]

def clear_subscriptions() -> None:
    _FAKE_SUBSCRIPTIONS.clear()
