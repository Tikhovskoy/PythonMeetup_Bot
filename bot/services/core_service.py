from apps.events.models import SpeakerTalk
from asgiref.sync import sync_to_async

def register_user_sync(telegram_id: int):
    pass

def is_speaker_sync(telegram_id: int) -> bool:
    return SpeakerTalk.objects.filter(speaker__telegram_id=telegram_id).exists()

def event_schedule_sync(user_name: str) -> str:
    return "Ваше выступление скоро начнётся!"

register_user = sync_to_async(register_user_sync)
is_speaker = sync_to_async(is_speaker_sync)
event_schedule = sync_to_async(event_schedule_sync)
