import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from bot.handlers.speaker import handle_speaker_start, handle_speaker_finish, handle_speaker_question
from bot.handlers.qna import qna_handler, qna_ask_text_handler
from bot.services import speaker_service
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.keyboards.speaker_app_keyboards import get_speaker_menu_keyboard, get_speaker_menu_speech_keyboard
from bot.constants import STATE_MENU, STATE_QNA_ASK_TEXT

@pytest.fixture(autouse=True)
def clear_data():
    speaker_service._FAKE_PERFORMANCES.clear()
    speaker_service._FAKE_QUESTIONS.clear()
    speaker_service.clear_active_speaker()

@pytest.mark.asyncio
async def test_questions_active_speaker_flow():
    speaker_id = 123456789  # Наш спикер
    user_id = 1111          # Обычный слушатель

    # --- Слушатель хочет задать вопрос, когда никто не выступает ---
    context = MagicMock()
    update = MagicMock()
    update.effective_user.id = user_id
    update.message.reply_text = AsyncMock()
    state = await qna_handler(update, context)
    assert state == STATE_MENU
    update.message.reply_text.assert_awaited_with(
        "В данный момент ни один спикер не выступает.\n"
        "Попробуйте отправить вопрос позже.",
        reply_markup=get_main_menu_keyboard()
    )

    # --- Спикер нажимает "Выступаю" ---
    context = MagicMock()
    update = MagicMock()
    update.effective_user.id = speaker_id
    update.message.reply_text = AsyncMock()
    state = await handle_speaker_start(update, context)
    assert state == STATE_MENU
    assert speaker_service.get_active_speaker() == speaker_id
    update.message.reply_text.assert_awaited_with(
        "Ты начал выступление! Теперь ты можешь просматривать вопросы.",
        reply_markup=get_speaker_menu_speech_keyboard()
    )

    # --- Слушатель снова заходит, может задать вопрос ---
    context = MagicMock()
    update = MagicMock()
    update.effective_user.id = user_id
    update.message.reply_text = AsyncMock()
    state = await qna_handler(update, context)
    assert state == STATE_QNA_ASK_TEXT
    # Симулируем ввод текста вопроса
    context.user_data = {"active_speaker_id": speaker_id, "active_speaker_name": "Иван Иванов"}
    update.message.text = "Ваш любимый язык?"
    state2 = await qna_ask_text_handler(update, context)
    assert state2 == STATE_MENU
    update.message.reply_text.assert_awaited_with(
        "Спасибо, твой вопрос отправлен текущему спикеру!\n\nТы в главном меню:",
        reply_markup=get_main_menu_keyboard(),
    )
    # Вопрос действительно появился у нужного спикера
    questions = speaker_service.get_questions_for_speaker(speaker_id)
    assert len(questions) == 1
    assert questions[0]['question_text'] == "Ваш любимый язык?"

    # --- Спикер смотрит свои вопросы ---
    context = MagicMock()
    update = MagicMock()
    update.effective_user.id = speaker_id
    update.message.reply_text = AsyncMock()
    state = await handle_speaker_question(update, context)
    assert state == STATE_MENU
    update.message.reply_text.assert_awaited_with(
        "Вопрос от пользователя 1111:\nВаш любимый язык?"
    )

    # --- Спикер завершает выступление ---
    context = MagicMock()
    update = MagicMock()
    update.effective_user.id = speaker_id
    update.message.reply_text = AsyncMock()
    state = await handle_speaker_finish(update, context)
    assert state == STATE_MENU
    assert speaker_service.get_active_speaker() is None
    update.message.reply_text.assert_awaited_with(
        "Спасибо за выступление! Ждём тебя снова.",
        reply_markup=get_speaker_menu_keyboard()
    )

    # --- Теперь слушатель снова НЕ может задать вопрос ---
    context = MagicMock()
    update = MagicMock()
    update.effective_user.id = user_id
    update.message.reply_text = AsyncMock()
    state = await qna_handler(update, context)
    assert state == STATE_MENU
    update.message.reply_text.assert_awaited_with(
        "В данный момент ни один спикер не выступает.\n"
        "Попробуйте отправить вопрос позже.",
        reply_markup=get_main_menu_keyboard()
    )
