from typing import Optional, List, Dict
from datetime import datetime

_FAKE_QUESTIONS: List[dict] = []

def validate_question_data(data: dict) -> Optional[str]:
    required_fields = ['telegram_id', 'speaker_name', 'question_text']
    for field in required_fields:
        value = data.get(field, '').strip() if isinstance(data.get(field), str) else data.get(field)
        if not value:
            return f"Поле «{field}» обязательно для заполнения."
        if field == "question_text" and len(data[field].strip()) < 4:
            return "Вопрос слишком короткий."
    return None

def save_question(data: dict) -> dict:
    """
    Сохраняет вопрос. Возвращает dict вопроса.
    """
    error = validate_question_data(data)
    if error:
        raise ValueError(error)
    question = {
        'telegram_id': data['telegram_id'],
        'speaker_name': data['speaker_name'],
        'question_text': data['question_text'].strip(),
        'created_at': datetime.now().isoformat(),
        'is_answered': False,
        'answer_text': '',
    }
    _FAKE_QUESTIONS.append(question)
    return question

def get_questions_for_speaker(speaker_name: str) -> List[dict]:
    """
    Возвращает все вопросы для данного спикера.
    """
    return [q for q in _FAKE_QUESTIONS if q['speaker_name'] == speaker_name]

def mark_question_answered(question_idx: int, answer_text: str) -> None:
    """
    Помечает вопрос как отвеченный и добавляет ответ.
    """
    if 0 <= question_idx < len(_FAKE_QUESTIONS):
        _FAKE_QUESTIONS[question_idx]['is_answered'] = True
        _FAKE_QUESTIONS[question_idx]['answer_text'] = answer_text.strip()

def clear_questions():
    """
    Очищает список вопросов (для тестов).
    """
    _FAKE_QUESTIONS.clear()
