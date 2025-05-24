from typing import Optional

from apps.events.models import SpeakerApplication
from bot.logging_tools import logger


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
        logger.warning("Ошибка валидации заявки спикера %s: %s", data.get('telegram_id'), error)
        raise ValueError(error)
    app = SpeakerApplication.objects.create(
        telegram_id=data['telegram_id'],
        topic=data['topic'].strip(),
        desc=data['desc'].strip(),
        status="new",
    )
    logger.info("Сохранена заявка спикера %s, тема: %s", data['telegram_id'], data['topic'].strip())
    return app

def get_all_speaker_apps():
    logger.info("Запрошен список всех заявок спикеров")
    return list(SpeakerApplication.objects.all())

def clear_speaker_apps() -> None:
    SpeakerApplication.objects.all().delete()
    logger.warning("Администратор удалил все заявки спикеров")
