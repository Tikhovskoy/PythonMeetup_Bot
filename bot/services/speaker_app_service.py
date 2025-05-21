from typing import List, Dict, Optional
from datetime import datetime

_FAKE_SPEAKER_APPS: List[dict] = []

def validate_speaker_app(data: dict) -> Optional[str]:
    if not data.get('telegram_id'):
        return "Не указан Telegram ID."
    if not data.get('topic') or len(data['topic'].strip()) < 4:
        return "Тема доклада обязательна и должна быть не короче 4 символов."
    if not data.get('desc') or len(data['desc'].strip()) < 8:
        return "Описание обязательно и должно быть не короче 8 символов."
    return None

def save_speaker_app(data: dict) -> dict:
    error = validate_speaker_app(data)
    if error:
        raise ValueError(error)
    app = {
        'telegram_id': data['telegram_id'],
        'topic': data['topic'].strip(),
        'desc': data['desc'].strip(),
        'created_at': datetime.now().isoformat(),
    }
    _FAKE_SPEAKER_APPS.append(app)
    return app

def get_all_speaker_apps() -> List[dict]:
    return list(_FAKE_SPEAKER_APPS)

def clear_speaker_apps() -> None:
    _FAKE_SPEAKER_APPS.clear()
