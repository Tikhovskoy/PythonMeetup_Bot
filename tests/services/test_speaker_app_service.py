import pytest
from bot.services import speaker_app_service

@pytest.fixture(autouse=True)
def clear_apps():
    speaker_app_service.clear_speaker_apps()

def test_save_and_get_speaker_app_success():
    data = {
        'telegram_id': 10001,
        'topic': 'Python Async',
        'desc': 'Практика и подводные камни асинхронности в Python.',
    }
    saved = speaker_app_service.save_speaker_app(data)
    assert saved['telegram_id'] == 10001
    assert saved['topic'] == 'Python Async'
    assert saved['desc'].startswith('Практика')

    apps = speaker_app_service.get_all_speaker_apps()
    assert len(apps) == 1
    assert apps[0]['topic'] == data['topic']

def test_topic_required_and_length():
    bad_data = {
        'telegram_id': 123,
        'topic': '',
        'desc': 'Подробное описание.',
    }
    with pytest.raises(ValueError) as exc:
        speaker_app_service.save_speaker_app(bad_data)
    assert "Тема доклада обязательна" in str(exc.value)

    bad_data2 = {
        'telegram_id': 123,
        'topic': 'Py',
        'desc': 'Подробное описание.',
    }
    with pytest.raises(ValueError) as exc:
        speaker_app_service.save_speaker_app(bad_data2)
    assert "Тема доклада обязательна" in str(exc.value)

def test_desc_required_and_length():
    bad_data = {
        'telegram_id': 123,
        'topic': 'Python Async',
        'desc': '',
    }
    with pytest.raises(ValueError) as exc:
        speaker_app_service.save_speaker_app(bad_data)
    assert "Описание обязательно" in str(exc.value)

    bad_data2 = {
        'telegram_id': 123,
        'topic': 'Python Async',
        'desc': 'Коротко',
    }
    with pytest.raises(ValueError) as exc:
        speaker_app_service.save_speaker_app(bad_data2)
    assert "Описание обязательно" in str(exc.value)

def test_missing_telegram_id():
    bad_data = {
        'topic': 'Python Async',
        'desc': 'Описание достаточно длинное.',
    }
    with pytest.raises(ValueError) as exc:
        speaker_app_service.save_speaker_app(bad_data)
    assert "Telegram ID" in str(exc.value)
