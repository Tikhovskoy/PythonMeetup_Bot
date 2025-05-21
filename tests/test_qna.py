import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from bot.handlers import qna
from bot.services import qna_service

@pytest.fixture(autouse=True)
def clear_questions():
    qna_service.clear_questions()

@pytest.mark.asyncio
async def test_qna_flow():
    user_id = 3333
    context = MagicMock()
    context.user_data = {}

    update = MagicMock(spec=Update)
    update.effective_user.id = user_id
    update.message.reply_text = AsyncMock()

    # Выбор спикера
    update.message.text = "Иван Иванов"
    await qna.qna_select_speaker_handler(update, context)
    context.user_data["qna_speaker"] = "Иван Иванов"

    # Ввод вопроса
    update.message.text = "Как стать мидлом?"
    await qna.qna_ask_text_handler(update, context)

    questions = qna_service.get_questions_for_speaker("Иван Иванов")
    assert questions
    assert questions[0]['question_text'] == "Как стать мидлом?"
    assert questions[0]['telegram_id'] == user_id
