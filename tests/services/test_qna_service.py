import pytest
from bot.services import qna_service

@pytest.fixture(autouse=True)
def clear_questions():
    qna_service.clear_questions()

def test_save_and_get_question_success():
    data = {
        'telegram_id': 12345,
        'speaker_name': 'Иван Иванов',
        'question_text': 'Как начать работать с асинхронностью?',
    }
    saved = qna_service.save_question(data)
    assert saved['telegram_id'] == 12345
    assert saved['speaker_name'] == 'Иван Иванов'
    assert saved['question_text'].startswith('Как начать')
    assert saved['is_answered'] is False

    # Получить все вопросы для Иван Иванов
    questions = qna_service.get_questions_for_speaker('Иван Иванов')
    assert len(questions) == 1
    assert questions[0]['question_text'] == data['question_text']

def test_save_question_invalid_missing_field():
    data = {
        'telegram_id': 222,
        'speaker_name': '',  # Не заполнено
        'question_text': 'Что такое async?',
    }
    with pytest.raises(ValueError) as exc:
        qna_service.save_question(data)
    assert "обязательно" in str(exc.value)

def test_save_question_too_short():
    data = {
        'telegram_id': 333,
        'speaker_name': 'Мария Петрова',
        'question_text': 'OK',
    }
    with pytest.raises(ValueError) as exc:
        qna_service.save_question(data)
    assert "слишком короткий" in str(exc.value) or "короткий" in str(exc.value)

def test_mark_question_answered():
    data = {
        'telegram_id': 444,
        'speaker_name': 'Иван Иванов',
        'question_text': 'Какой ваш любимый фреймворк?',
    }
    qna_service.save_question(data)
    qna_service.mark_question_answered(0, "Django!")
    questions = qna_service.get_questions_for_speaker('Иван Иванов')
    assert questions[0]['is_answered']
    assert questions[0]['answer_text'] == "Django!"
