import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from bot.handlers import schedule
from bot.services import schedule_service

@pytest.fixture(autouse=True)
def clear_events():
    schedule_service.clear_events()

@pytest.mark.asyncio
async def test_schedule_output():
    schedule_service.add_event({
        "time": "09:00",
        "speaker": "Вася",
        "topic": "Микросервисы",
        "description": "Про архитектуру микросервисов.",
    })
    schedule_service.add_event({
        "time": "10:00",
        "speaker": "Петя",
        "topic": "Тестирование",
        "description": "Юнит-тесты в Python.",
    })

    context = MagicMock()
    update = MagicMock(spec=Update)
    update.message.reply_text = AsyncMock()

    await schedule.schedule_handler(update, context)
    update.message.reply_text.assert_called()
    call_args = update.message.reply_text.call_args[0][0]
    assert "Микросервисы" in call_args
    assert "Тестирование" in call_args
