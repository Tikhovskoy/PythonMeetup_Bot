from typing import Optional
from apps.events.models import SpeakerApplication

def validate_speaker_app(data: dict) -> Optional[str]:
    if not data.get('telegram_id'):
        return "Не указан Telegram ID."
    if not data.get('topic') or len(data['topic'].strip()) < 4:
        return "Тема доклада обязательна и должна быть не короче 4 символов."
    if not data.get('desc') or len(data['desc'].strip()) < 8:
        return "Описание обязательно и должно быть не короче 8 символов."
    return None

def save_speaker_app(data: dict) -> SpeakerApplication:
    error = validate_speaker_app(data)
    if error:
        raise ValueError(error)
    return SpeakerApplication.objects.create(
        telegram_id=data['telegram_id'],
        topic=data['topic'].strip(),
        desc=data['desc'].strip(),
        status="new",
    )

def get_all_speaker_apps():
    return list(SpeakerApplication.objects.all())

def clear_speaker_apps() -> None:
    SpeakerApplication.objects.all().delete()
