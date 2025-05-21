from datetime import datetime
from typing import List, Dict, Optional

_FAKE_SPEAKERS = {
    123456789: "Иван Иванов",
    987654321: "Мария Петрова",
}
_FAKE_PERFORMANCES = []
_FAKE_QUESTIONS = []
_ACTIVE_SPEAKER_ID: Optional[int] = None

def is_speaker(telegram_id: int) -> bool:
    return telegram_id in _FAKE_SPEAKERS

def event_schedule(speaker_name: str) -> str:
    return f"Ваше выступление в 15:00"

def set_active_speaker(speaker_id: int):
    global _ACTIVE_SPEAKER_ID
    _ACTIVE_SPEAKER_ID = speaker_id

def clear_active_speaker():
    global _ACTIVE_SPEAKER_ID
    _ACTIVE_SPEAKER_ID = None

def get_active_speaker() -> Optional[int]:
    return _ACTIVE_SPEAKER_ID

def start_performance(speaker_id: int):
    set_active_speaker(speaker_id)
    _FAKE_PERFORMANCES.append({
        "speaker_id": speaker_id,
        "start": datetime.now().isoformat(),
        "end": None,
    })

def finish_performance(speaker_id: int):
    clear_active_speaker()
    for perf in reversed(_FAKE_PERFORMANCES):
        if perf["speaker_id"] == speaker_id and perf["end"] is None:
            perf["end"] = datetime.now().isoformat()
            break

def save_question_for_active_speaker(question_text: str, from_user_id: int):
    speaker_id = get_active_speaker()
    if not speaker_id:
        raise ValueError("Нет активного спикера")
    _FAKE_QUESTIONS.append({
        "speaker_id": speaker_id,
        "question_text": question_text.strip(),
        "from_user_id": from_user_id,
        "created_at": datetime.now().isoformat(),
    })

def get_questions_for_speaker(speaker_id: int) -> List[Dict]:
    return [q for q in _FAKE_QUESTIONS if q["speaker_id"] == speaker_id]

def get_speakers() -> Dict[int, str]:
    return _FAKE_SPEAKERS
