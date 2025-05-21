from typing import Optional, Dict, List
from datetime import datetime

# In-memory storage для моков и тестов (пока нет БД)
_FAKE_PROFILES: Dict[int, dict] = {}

def validate_profile_data(data: dict) -> Optional[str]:
    required_fields = ['name', 'contacts', 'stack', 'role', 'grade']
    for field in required_fields:
        value = data.get(field, '').strip()
        if not value:
            return f"Поле «{field}» обязательно для заполнения."
        if len(value) < 2:
            return f"Поле «{field}» слишком короткое."
    return None

def save_profile(telegram_id: int, data: dict) -> dict:
    error = validate_profile_data(data)
    if error:
        raise ValueError(error)
    profile = data.copy()
    profile['telegram_id'] = telegram_id
    profile['created_at'] = datetime.now().isoformat()
    _FAKE_PROFILES[telegram_id] = profile
    return profile

def get_profile(telegram_id: int) -> Optional[dict]:
    return _FAKE_PROFILES.get(telegram_id)

def get_random_profile(exclude_telegram_id: int) -> Optional[dict]:
    import random
    candidates = [p for tid, p in _FAKE_PROFILES.items() if tid != exclude_telegram_id]
    return random.choice(candidates) if candidates else None

def get_profiles_list(exclude_telegram_id: int, exclude_list: Optional[List[int]] = None) -> List[dict]:
    exclude_list = exclude_list or []
    return [
        p for tid, p in _FAKE_PROFILES.items()
        if tid != exclude_telegram_id and tid not in exclude_list
    ]

def get_profiles_count() -> int:
    return len(_FAKE_PROFILES)
