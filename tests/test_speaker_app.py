import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.handlers.speaker_app import (
    speaker_app_handler, speaker_topic_handler, speaker_desc_handler
)
from bot.constants import (
    STATE_APPLY_TOPIC, STATE_APPLY_DESC, STATE_MENU
)

@pytest.mark.asyncio
async def test_speaker_app_full_flow():
    update = MagicMock()
    update.message = AsyncMock()
    context = MagicMock()
    context.user_data = {}

    state = await speaker_app_handler(update, context)
    assert state == STATE_APPLY_TOPIC

    # Ввод темы
    update.message.text = "Моя тема"
    state = await speaker_topic_handler(update, context)
    assert state == STATE_APPLY_DESC
    assert context.user_data["speaker_app"]["topic"] == "Моя тема"

    # Ввод описания
    update.message.text = "Описание"
    state = await speaker_desc_handler(update, context)
    assert state == STATE_MENU
    assert context.user_data["speaker_app"]["desc"] == "Описание"
