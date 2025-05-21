import pytest
from bot.services import schedule_service

@pytest.fixture(autouse=True)
def clear_events():
    schedule_service.clear_events()

def test_add_and_get_schedule():
    ev1 = {
        'time': '11:00',
        'speaker': 'Алексей',
        'topic': 'DevOps для питонистов',
        'description': 'Инфраструктура как код и лучшие практики.',
    }
    ev2 = {
        'time': '10:00',
        'speaker': 'Ирина',
        'topic': 'Data Science Starter',
        'description': 'Введение в машинное обучение на Python.',
    }
    schedule_service.add_event(ev1)
    schedule_service.add_event(ev2)
    schedule = schedule_service.get_schedule()
    assert schedule[0]['time'] == '10:00'
    assert schedule[1]['time'] == '11:00'

def test_get_event_by_time():
    event = {
        'time': '16:00',
        'speaker': 'Пётр',
        'topic': 'Питон в автоматизации',
        'description': 'Практические кейсы.',
    }
    schedule_service.add_event(event)
    found = schedule_service.get_event_by_time('16:00')
    assert found is not None
    assert found['speaker'] == 'Пётр'
    assert schedule_service.get_event_by_time('17:00') is None
