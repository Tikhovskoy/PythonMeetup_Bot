import pytest
from bot.services import subscriptions_service

@pytest.fixture(autouse=True)
def clear_subs():
    subscriptions_service.clear_subscriptions()

def test_subscribe_and_check():
    telegram_id = 1001
    # Сначала пользователь не подписан
    assert not subscriptions_service.is_subscribed(telegram_id)
    # Подписываем
    subscriptions_service.subscribe(telegram_id)
    assert subscriptions_service.is_subscribed(telegram_id)

def test_unsubscribe():
    telegram_id = 2002
    subscriptions_service.subscribe(telegram_id)
    assert subscriptions_service.is_subscribed(telegram_id)
    # Отписываем
    subscriptions_service.unsubscribe(telegram_id)
    assert not subscriptions_service.is_subscribed(telegram_id)

def test_repeat_subscribe_unsubscribe():
    telegram_id = 3003
    subscriptions_service.subscribe(telegram_id)
    assert subscriptions_service.is_subscribed(telegram_id)
    subscriptions_service.unsubscribe(telegram_id)
    assert not subscriptions_service.is_subscribed(telegram_id)
    # Снова подписываем
    subscriptions_service.subscribe(telegram_id)
    assert subscriptions_service.is_subscribed(telegram_id)

def test_get_all_subscribed():
    ids = [1, 2, 3]
    for tid in ids:
        subscriptions_service.subscribe(tid)
    subscriptions_service.unsubscribe(2)
    all_subs = subscriptions_service.get_all_subscribed()
    assert set(all_subs) == {1, 3}

def test_unsubscribe_nonexistent():
    # Отписка несуществующего пользователя не вызывает ошибок
    telegram_id = 9009
    subscriptions_service.unsubscribe(telegram_id)  
    assert not subscriptions_service.is_subscribed(telegram_id)
