from asgiref.sync import sync_to_async
from django.utils import timezone

from apps.events.models import Question, Speaker, SpeakerTalk
from bot.logging_tools import logger


def is_speaker_sync(telegram_id: int) -> bool:
    result = Speaker.objects.filter(telegram_id=telegram_id).exists()
    logger.info("Проверка: %s — докладчик: %s", telegram_id, result)
    return result

def get_speakers_sync() -> dict:
    logger.info("Получен список всех спикеров")
    return {s.telegram_id: s.name for s in Speaker.objects.all()}

def get_active_speaker_talk_sync() -> dict | None:
    talk = SpeakerTalk.objects.select_related('speaker').filter(is_active=True).first()
    if not talk or not talk.speaker:
        logger.info("Нет активного спикера")
        return None
    logger.info("Активный спикер: %s (talk_id=%s)", talk.speaker.name, talk.id)
    return {
        "id": talk.id,
        "speaker_name": talk.speaker.name,
    }

def get_active_speaker_name_sync() -> str | None:
    talk = SpeakerTalk.objects.select_related('speaker').filter(is_active=True).first()
    if not talk or not talk.speaker:
        logger.info("Нет активного спикера")
        return None
    logger.info("Имя активного спикера: %s", talk.speaker.name)
    return talk.speaker.name

def set_active_speaker_talk_sync(speaker_talk_id: int):
    SpeakerTalk.objects.update(is_active=False)
    SpeakerTalk.objects.filter(id=speaker_talk_id).update(is_active=True)
    logger.info("Назначен активный доклад: %s", speaker_talk_id)

def clear_active_speaker_talk_sync():
    SpeakerTalk.objects.update(is_active=False)
    logger.info("Сняты все флаги активности с докладов")

def start_performance_sync(speaker_telegram_id: int):
    talk = SpeakerTalk.objects.filter(speaker__telegram_id=speaker_telegram_id).order_by('start_performance').first()
    if talk:
        set_active_speaker_talk_sync(talk.id)
        if not talk.start_performance:
            talk.start_performance = timezone.now()
            talk.save(update_fields=["start_performance"])
        logger.info("Старт выступления: %s (talk_id=%s)", speaker_telegram_id, talk.id)
    else:
        logger.info("Не найден talk для старта выступления: %s", speaker_telegram_id)

def finish_performance_sync(speaker_telegram_id: int):
    talk = SpeakerTalk.objects.filter(speaker__telegram_id=speaker_telegram_id, is_active=True).first()
    if talk:
        talk.is_active = False
        talk.end_performance = timezone.now()
        talk.save(update_fields=["is_active", "end_performance"])
        logger.info("Завершено выступление: %s (talk_id=%s)", speaker_telegram_id, talk.id)
    else:
        logger.info("Не найден talk для завершения выступления: %s", speaker_telegram_id)

def save_question_for_active_speaker_sync(question_text: str, from_user_id: int, from_user_name: str = ''):
    active_talk = SpeakerTalk.objects.filter(is_active=True).first()
    if not active_talk:
        logger.warning("Попытка задать вопрос без активного спикера (user_id=%s)", from_user_id)
        raise ValueError("Нет активного спикера")
    Question.objects.create(
        telegram_id=from_user_id,
        name=from_user_name,
        speaker=active_talk,
        question_text=question_text.strip(),
    )
    logger.info("Пользователь %s задал вопрос активному спикеру %s", from_user_id, active_talk.speaker.name if active_talk.speaker else "None")

def get_questions_for_speaker_sync(speaker_telegram_id: int) -> list:
    talks = SpeakerTalk.objects.filter(speaker__telegram_id=speaker_telegram_id)
    questions = Question.objects.filter(speaker__in=talks)
    logger.info("Запрошены вопросы для спикера %s", speaker_telegram_id)
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
