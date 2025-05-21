from typing import List, Dict, Optional
from datetime import datetime

_FAKE_EVENTS: List[dict] = [
    {
        'time': '12:00',
        'speaker': 'Иван Иванов',
        'topic': 'Python и нейросети',
        'description': 'Как использовать Python для работы с нейросетями.',
    },
    {
        'time': '13:00',
        'speaker': 'Мария Петрова',
        'topic': 'Асинхронность в Python',
        'description': 'Практика asyncio и параллелизм в реальных проектах.',
    },
    {
        'time': '14:00',
        'speaker': '',
        'topic': 'Пицца и нетворкинг 🍕',
        'description': 'Неофициальное общение за пиццей.',
    },
]

def add_event(event: dict) -> dict:
    """
    Добавляет новое событие (расширяемо для админки или миграции).
    """
    _FAKE_EVENTS.append(event)
    return event

def get_schedule() -> List[dict]:
    """
    Возвращает все события расписания, отсортированные по времени.
    """
    def parse_time(ev):
        try:
            return datetime.strptime(ev['time'], '%H:%M')
        except Exception:
            return datetime.min
    return sorted(_FAKE_EVENTS, key=parse_time)

def get_event_by_time(time_str: str) -> Optional[dict]:
    """
    Возвращает событие по времени (например, для поиска).
    """
    for ev in _FAKE_EVENTS:
        if ev['time'] == time_str:
            return ev
    return None

def clear_events() -> None:
    """
    Очищает расписание (для тестов).
    """
    _FAKE_EVENTS.clear()
