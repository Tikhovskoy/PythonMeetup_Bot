import pytest

from apps.events.models import (Donate, SpeakerApplication, Subscription,
                                UserProfile)
from bot.services import (donations_service, speaker_app_service,
                          subscriptions_service)


@pytest.mark.django_db
def test_donations_service_save_and_total():
    donations_service.clear_donations()
    donations_service.save_donation({'telegram_id': 1, 'name': 'A', 'amount': 150})
    donations_service.save_donation({'telegram_id': 2, 'name': 'B', 'amount': 350})
    all_donates = donations_service.get_all_donations()
    assert len(all_donates) == 2
    assert donations_service.get_total_amount() == 500

@pytest.mark.django_db
def test_subscriptions_service_lifecycle():
    subscriptions_service.clear_subscriptions()
    tid = 42
    assert not subscriptions_service.is_subscribed(tid)
    subscriptions_service.subscribe(tid)
    assert subscriptions_service.is_subscribed(tid)
    subscriptions_service.unsubscribe(tid)
    assert not subscriptions_service.is_subscribed(tid)

@pytest.mark.django_db
def test_speaker_app_service_save_and_clear():
    speaker_app_service.clear_speaker_apps()
    speaker_app_service.save_speaker_app({'telegram_id': 100, 'topic': 'Тест', 'desc': 'Описание темы'})
    apps = speaker_app_service.get_all_speaker_apps()
    assert len(apps) == 1
    assert apps[0].topic == 'Тест'
    speaker_app_service.clear_speaker_apps()
    assert len(speaker_app_service.get_all_speaker_apps()) == 0
