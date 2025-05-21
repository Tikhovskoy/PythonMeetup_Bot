import pytest
from bot.services import networking_service

@pytest.fixture(autouse=True)
def clear_profiles():
    # Очищает "базу" перед каждым тестом
    networking_service._FAKE_PROFILES.clear()

def test_save_and_get_profile_success():
    telegram_id = 12345
    profile_data = {
        'name': 'Василий Петров',
        'contacts': '@vasya',
        'stack': 'Python, Django',
        'role': 'Backend',
        'grade': 'Middle',
    }

    saved = networking_service.save_profile(telegram_id, profile_data)
    assert saved['name'] == 'Василий Петров'
    assert saved['telegram_id'] == telegram_id
    assert 'created_at' in saved

    got = networking_service.get_profile(telegram_id)
    assert got['name'] == 'Василий Петров'

def test_validate_profile_missing_field():
    telegram_id = 777
    incomplete = {
        'name': 'Кот',
        'contacts': '',
        'stack': 'Python',
        'role': 'Backend',
        'grade': 'Junior',
    }
    with pytest.raises(ValueError) as exc:
        networking_service.save_profile(telegram_id, incomplete)
    assert "обязательно" in str(exc.value)

def test_validate_profile_too_short_field():
    telegram_id = 888
    bad = {
        'name': 'К',
        'contacts': '@k',
        'stack': 'P',
        'role': 'B',
        'grade': 'J',
    }
    with pytest.raises(ValueError) as exc:
        networking_service.save_profile(telegram_id, bad)
    assert "слишком короткое" in str(exc.value)

def test_get_random_profile():
    networking_service.save_profile(1, {
        'name': 'Один',
        'contacts': '@odin',
        'stack': 'Python',
        'role': 'Backend',
        'grade': 'Junior',
    })
    networking_service.save_profile(2, {
        'name': 'Два',
        'contacts': '@dva',
        'stack': 'Django',
        'role': 'Frontend',
        'grade': 'Middle',
    })

    random_profile = networking_service.get_random_profile(exclude_telegram_id=1)
    assert random_profile is not None
    assert random_profile['telegram_id'] == 2
