import pytest

from apps.events.models import BotUser, Event, Speaker, SpeakerTalk
from bot.services.core_service import register_user_sync
from bot.services.speaker_service import save_question_for_active_speaker_sync


@pytest.mark.django_db
def test_register_user_creates_and_updates_record():
    register_user_sync(100, "Первое имя")
    register_user_sync(100, "Обновлённое имя")

    assert BotUser.objects.count() == 1
    assert BotUser.objects.get(telegram_id=100).name == "Обновлённое имя"


@pytest.mark.django_db
def test_question_rejects_empty_and_long_text():
    speaker = Speaker.objects.create(name="Спикер", telegram_id=100)
    event = Event.objects.create(title="Митап")
    SpeakerTalk.objects.create(speaker=speaker, event=event, is_active=True)

    with pytest.raises(ValueError, match="пустым"):
        save_question_for_active_speaker_sync("   ", 1, "Участник")
    with pytest.raises(ValueError, match="1000"):
        save_question_for_active_speaker_sync("x" * 1001, 1, "Участник")
