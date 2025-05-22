from apps.events.models import Speaker, SpeakerTalk, Question
from django.utils import timezone
from asgiref.sync import sync_to_async

def is_speaker_sync(telegram_id: int) -> bool:
    return Speaker.objects.filter(telegram_id=telegram_id).exists()

def get_speakers_sync() -> dict:
    return {s.telegram_id: s.name for s in Speaker.objects.all()}

def get_active_speaker_talk_sync() -> dict | None:
    talk = SpeakerTalk.objects.select_related('speaker').filter(is_active=True).first()
    if not talk or not talk.speaker:
        return None
    return {
        "id": talk.id,
        "speaker_name": talk.speaker.name,
    }

def get_active_speaker_name_sync() -> str | None:
    talk = SpeakerTalk.objects.select_related('speaker').filter(is_active=True).first()
    if not talk or not talk.speaker:
        return None
    return talk.speaker.name

def set_active_speaker_talk_sync(speaker_talk_id: int):
    SpeakerTalk.objects.update(is_active=False)
    SpeakerTalk.objects.filter(id=speaker_talk_id).update(is_active=True)

def clear_active_speaker_talk_sync():
    SpeakerTalk.objects.update(is_active=False)

def start_performance_sync(speaker_telegram_id: int):
    talk = SpeakerTalk.objects.filter(speaker__telegram_id=speaker_telegram_id).order_by('start_performance').first()
    if talk:
        set_active_speaker_talk_sync(talk.id)
        if not talk.start_performance:
            talk.start_performance = timezone.now()
            talk.save(update_fields=["start_performance"])

def finish_performance_sync(speaker_telegram_id: int):
    talk = SpeakerTalk.objects.filter(speaker__telegram_id=speaker_telegram_id, is_active=True).first()
    if talk:
        talk.is_active = False
        talk.end_performance = timezone.now()
        talk.save(update_fields=["is_active", "end_performance"])

def save_question_for_active_speaker_sync(question_text: str, from_user_id: int, from_user_name: str = ''):
    active_talk = SpeakerTalk.objects.filter(is_active=True).first()
    if not active_talk:
        raise ValueError("Нет активного спикера")
    Question.objects.create(
        telegram_id=from_user_id,
        name=from_user_name,
        speaker=active_talk,
        question_text=question_text.strip(),
    )

def get_questions_for_speaker_sync(speaker_telegram_id: int) -> list:
    talks = SpeakerTalk.objects.filter(speaker__telegram_id=speaker_telegram_id)
    questions = Question.objects.filter(speaker__in=talks)
    return [
        {
            "from_user_id": q.telegram_id,
            "question_text": q.question_text,
            "name": q.name,
            "created_at": q.created_at,
        }
        for q in questions
    ]

is_speaker = sync_to_async(is_speaker_sync)
get_speakers = sync_to_async(get_speakers_sync)
get_active_speaker_talk = sync_to_async(get_active_speaker_talk_sync)
get_active_speaker_name = sync_to_async(get_active_speaker_name_sync)
set_active_speaker_talk = sync_to_async(set_active_speaker_talk_sync)
clear_active_speaker_talk = sync_to_async(clear_active_speaker_talk_sync)
start_performance = sync_to_async(start_performance_sync)
finish_performance = sync_to_async(finish_performance_sync)
save_question_for_active_speaker = sync_to_async(save_question_for_active_speaker_sync)
get_questions_for_speaker = sync_to_async(get_questions_for_speaker_sync)
