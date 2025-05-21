import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from bot.handlers import speaker as speaker_handlers
from bot.services import speaker_service
from bot.keyboards import speaker_app_keyboards
from bot.handlers.start import switch_to_user_mode
from bot.keyboards.main_menu import get_main_menu_keyboard

@pytest.fixture(autouse=True)
def clear_data():
    # Очищаем in-memory данные перед каждым тестом
    speaker_service._FAKE_PERFORMANCES.clear()
    speaker_service._FAKE_QUESTIONS.clear()

@pytest.mark.asyncio
async def test_speaker_full_flow():
    # Допустим, у нас есть такой спикер
    speaker_id = 123456789
    user_id = 4444  # слушатель

    # Проверяем, что это спикер
    assert speaker_service.is_speaker(speaker_id)
    assert not speaker_service.is_speaker(user_id)

    # --- Проверка event_schedule (заглушка) ---
    schedule = speaker_service.event_schedule("Иван Иванов")
    assert "15:00" in schedule

    # --- Проверка старта выступления ---
    context = MagicMock()
    update = MagicMock(spec=Update)
    update.effective_user.id = speaker_id
    update.effective_user.first_name = "Иван"
    update.message.reply_text = AsyncMock()

    # Хендлер: начал выступление (клавиатура для доклада)
    result = await speaker_handlers.handle_speaker_start(update, context)
    assert result == "STATE_MENU"
    assert speaker_service._FAKE_PERFORMANCES[-1]["speaker_id"] == speaker_id
    assert speaker_service._FAKE_PERFORMANCES[-1]["end"] is None
    update.message.reply_text.assert_awaited_with(
        "Ты начал выступление! Теперь ты можешь просматривать вопросы.",
        reply_markup=speaker_app_keyboards.get_speaker_menu_speech_keyboard()
    )

    # --- Проверка добавления вопросов ---
    speaker_service.save_question(speaker_id, "Первый вопрос?", from_user_id=user_id)
    speaker_service.save_question(speaker_id, "Второй вопрос!", from_user_id=user_id)

    # --- Проверка получения вопросов ---
    questions = speaker_service.get_questions(speaker_id)
    assert len(questions) == 2
    assert questions[0]["question_text"] == "Первый вопрос?"

    # Хендлер: просмотр вопросов (должны выводиться оба вопроса)
    update.message.reply_text = AsyncMock()
    result = await speaker_handlers.handle_speaker_question(update, context)
    assert result == "STATE_MENU"
    expected = [
        f"Вопрос от пользователя {q['from_user_id']}:\n{q['question_text']}"
        for q in questions
    ]
    actual = [call.args[0] for call in update.message.reply_text.await_args_list]
    for msg in expected:
        assert msg in actual

    # --- Проверка завершения выступления ---
    update.message.reply_text = AsyncMock()
    result = await speaker_handlers.handle_speaker_finish(update, context)
    assert result == "STATE_MENU"
    assert speaker_service._FAKE_PERFORMANCES[-1]["end"] is not None
    update.message.reply_text.assert_awaited_with(
        "Спасибо за выступление! Ждём тебя снова.",
        reply_markup=speaker_app_keyboards.get_speaker_menu_keyboard()
    )

    # --- Проверка кнопки "Войти как пользователь" (имитация через start.py) ---
    update.message.reply_text = AsyncMock()
    result = await switch_to_user_mode(update, context)
    assert result == "STATE_MENU"
    update.message.reply_text.assert_awaited_with(
        "Теперь вы используете приложение как обычный пользователь.",
        reply_markup=get_main_menu_keyboard()
    )

    # --- Проверяем, что обычный пользователь не считается спикером ---
    assert not speaker_service.is_speaker(user_id)
    # Вопросы такому пользователю не выводятся
    assert speaker_service.get_questions(user_id) == []
