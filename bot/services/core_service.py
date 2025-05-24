from asgiref.sync import sync_to_async

from apps.events.models import SpeakerTalk
from bot.logging_tools import logger


def register_user_sync(telegram_id: int):
    logger.info("Регистрация пользователя %s", telegram_id)
    pass


def is_speaker_sync(telegram_id: int) -> bool:
    result = SpeakerTalk.objects.filter(speaker__telegram_id=telegram_id).exists()
    logger.info("Проверка докладчика %s — %s", telegram_id, result)
    return result


def event_schedule_sync(user_name: str) -> str:
    logger.info("Пользователь %s запросил своё расписание", user_name)
    return "Ваше выступление скоро начнётся!"


register_user = sync_to_async(register_user_sync)
is_speaker = sync_to_async(is_speaker_sync)
event_schedule = sync_to_async(event_schedule_sync)
