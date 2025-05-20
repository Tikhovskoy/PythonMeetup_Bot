import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.handlers.qna import (
    qna_handler, qna_select_speaker_handler, qna_ask_text_handler
)
from bot.constants import (
    STATE_QNA_SELECT_SPEAKER, STATE_QNA_ASK_TEXT, STATE_MENU
)

@pytest.mark.asyncio
async def test_qna_flow_with_active_session():
    update = MagicMock()
    update.message = AsyncMock()
    context = MagicMock()
    context.user_data = {}

    # Эмулируем активную сессию — пользователь сразу пишет вопрос текущему спикеру
    active_session = {"speaker": {"name": "Иван Иванов"}}
    state = await qna_handler(update, context, active_session=active_session)
    assert state == STATE_QNA_ASK_TEXT

    update.message.text = "Мой вопрос Ивану"
    state = await qna_ask_text_handler(update, context)
    assert state == STATE_MENU

@pytest.mark.asyncio
async def test_qna_flow_with_speaker_selection():
    update = MagicMock()
    update.message = AsyncMock()
    context = MagicMock()
    context.user_data = {}

    # Нет активной сессии — пользователь должен выбрать спикера
    state = await qna_handler(update, context, active_session=None)
    assert state == STATE_QNA_SELECT_SPEAKER

    update.message.text = "Иван Иванов"
    state = await qna_select_speaker_handler(update, context)
    assert state == STATE_QNA_ASK_TEXT

    update.message.text = "Мой вопрос после выбора спикера"
    state = await qna_ask_text_handler(update, context)
    assert state == STATE_MENU
