import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from bot.handlers import speaker_app
from bot.services import speaker_app_service

@pytest.fixture(autouse=True)
def clear_apps():
    speaker_app_service.clear_speaker_apps()

@pytest.mark.asyncio
async def test_speaker_app_flow():
    user_id = 5555
    context = MagicMock()
    context.user_data = {"speaker_app": {}}

    update = MagicMock(spec=Update)
    update.effective_user.id = user_id
    update.message.reply_text = AsyncMock()

    update.message.text = "Python для всех"
    await speaker_app.speaker_topic_handler(update, context)
    update.message.text = "Расскажем, почему Python лучший язык для старта."
    await speaker_app.speaker_desc_handler(update, context)

    apps = speaker_app_service.get_all_speaker_apps()
    assert apps
    assert apps[0]['topic'] == "Python для всех"
    assert apps[0]['desc'].startswith("Расскажем")
    assert apps[0]['telegram_id'] == user_id
