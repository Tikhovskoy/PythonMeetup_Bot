from unittest.mock import AsyncMock, patch

import pytest
from django.core.exceptions import ValidationError

from apps.events.models import Question, SendMessage, UserProfile
from bot.services import donations_service, speaker_app_service, subscriptions_service


# --- UserProfile edge-case ---
@pytest.mark.django_db
def test_userprofile_empty_fields():
    profile = UserProfile.objects.create(telegram_id=1, name="Тест")
    assert profile.contacts is None or profile.contacts == ""
    assert profile.stack is None or profile.stack == ""
    assert profile.grade is None or profile.grade == ""


# --- Donate edge-cases ---
@pytest.mark.django_db
def test_donation_negative_and_zero_amount():
    with pytest.raises(ValueError):
        donations_service.save_donation({"telegram_id": 2, "name": "X", "amount": 0})
    with pytest.raises(ValueError):
        donations_service.save_donation({"telegram_id": 2, "name": "X", "amount": -10})


# --- Subscription edge-cases ---
@pytest.mark.django_db
def test_double_subscribe_and_unsubscribe():
    tid = 555
    subscriptions_service.subscribe(tid)
    assert subscriptions_service.is_subscribed(tid)
    subscriptions_service.subscribe(tid)
    assert subscriptions_service.is_subscribed(tid)
    subscriptions_service.unsubscribe(tid)
    assert not subscriptions_service.is_subscribed(tid)
    subscriptions_service.unsubscribe(tid)
    assert not subscriptions_service.is_subscribed(tid)


# --- SpeakerApplication edge-cases ---
@pytest.mark.django_db
def test_invalid_speaker_app_fields():
    with pytest.raises(ValueError):
        speaker_app_service.save_speaker_app(
            {"telegram_id": 1, "topic": "", "desc": "Описание"}
        )
    with pytest.raises(ValueError):
        speaker_app_service.save_speaker_app(
            {"telegram_id": 1, "topic": "Тема", "desc": ""}
        )
    with pytest.raises(ValueError):
        speaker_app_service.save_speaker_app({"topic": "Тема", "desc": "Описание"})


# --- Question edge-cases ---
@pytest.mark.django_db
def test_question_without_speaker():
    with pytest.raises(Exception):
        Question.objects.create(
            telegram_id=999, name="Тест", speaker=None, question_text="?"
        )


# --- SendMessage edge-case ---
@pytest.mark.django_db
def test_sendmessage_invalid_group():
    msg = SendMessage(message="Hello", group="unknown_group")
    with pytest.raises(ValidationError):
        msg.full_clean()


# --- Async handler edge-case ---
@pytest.mark.asyncio
@pytest.mark.django_db
@patch("bot.services.subscriptions_service.is_subscribed", return_value=True)
@patch("bot.services.subscriptions_service.subscribe")
@patch("bot.handlers.subscriptions.send_message_with_retry", new_callable=AsyncMock)
async def test_double_subscribe_message(mock_send, mock_sub, mock_is_sub, mocker):
    from bot.handlers import subscriptions

    update = mocker.Mock()
    update.effective_user.id = 2
    update.message.text = "✅ Подписаться"
    context = mocker.Mock()
    await subscriptions.subscribe_confirm_handler(update, context)
    mock_send.assert_awaited()
