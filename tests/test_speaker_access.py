from unittest.mock import AsyncMock, patch

import pytest

from apps.events.models import Event, Speaker, SpeakerTalk
from bot.constants import STATE_MENU
from bot.handlers.speaker import handle_speaker_start
from bot.services import speaker_service


@pytest.mark.django_db
def test_speaker_starts_next_unfinished_talk():
    speaker = Speaker.objects.create(name="Докладчик", telegram_id=1001)
    event = Event.objects.create(title="Митап")
    first_talk = SpeakerTalk.objects.create(speaker=speaker, event=event, topic="Первый")
    second_talk = SpeakerTalk.objects.create(speaker=speaker, event=event, topic="Второй")

    started_first = speaker_service.start_performance_sync(speaker.telegram_id)
    finished_first = speaker_service.finish_performance_sync(speaker.telegram_id)
    started_second = speaker_service.start_performance_sync(speaker.telegram_id)

    assert started_first.id == first_talk.id
    assert finished_first.id == first_talk.id
    assert started_second.id == second_talk.id
    first_talk.refresh_from_db()
    second_talk.refresh_from_db()
    assert first_talk.end_performance is not None
    assert second_talk.is_active


@pytest.mark.asyncio
@patch("bot.handlers.speaker.send_message_with_retry", new_callable=AsyncMock)
@patch("bot.handlers.speaker.is_speaker", new_callable=AsyncMock, return_value=False)
async def test_non_speaker_cannot_start_talk(mock_is_speaker, mock_send, mocker):
    update = mocker.Mock()
    update.effective_user.id = 1002
    context = mocker.Mock()

    result = await handle_speaker_start(update, context)

    assert result == STATE_MENU
    mock_is_speaker.assert_awaited_once_with(1002)
    mock_send.assert_awaited_once()
