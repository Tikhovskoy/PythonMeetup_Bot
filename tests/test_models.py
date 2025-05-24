import pytest

from apps.events.models import (
    Donate,
    Event,
    Question,
    SendMessage,
    Speaker,
    SpeakerApplication,
    SpeakerTalk,
    Subscription,
    UserProfile,
)


@pytest.mark.django_db
def test_create_userprofile():
    profile = UserProfile.objects.create(
        telegram_id=123,
        name="Вася Пупкин",
        contacts="@vasya",
        role="Backend",
        stack="Python, Django",
        grade="Middle",
    )
    assert profile.id is not None
    assert profile.name == "Вася Пупкин"


@pytest.mark.django_db
def test_create_event_and_speaker():
    event = Event.objects.create(title="Test Meetup")
    speaker = Speaker.objects.create(name="Докладчик 1")
    talk = SpeakerTalk.objects.create(
        speaker=speaker, event=event, topic="Async Django"
    )
    assert talk.topic == "Async Django"
    assert talk.event == event
    assert talk.speaker == speaker


@pytest.mark.django_db
def test_question_lifecycle():
    event = Event.objects.create(title="QnA Meetup")
    speaker = Speaker.objects.create(name="QnA Speaker")
    talk = SpeakerTalk.objects.create(speaker=speaker, event=event)
    question = Question.objects.create(
        telegram_id=456,
        name="Тестовый слушатель",
        speaker=talk,
        question_text="Как работает async?",
    )
    assert not question.is_answered
    question.answer_text = "Вот так!"
    question.is_answered = True
    question.save()
    assert Question.objects.get(id=question.id).is_answered


@pytest.mark.django_db
def test_donate_and_subscription():
    donate = Donate.objects.create(telegram_id=789, name="Жертвователь", amount=1000)
    sub = Subscription.objects.create(telegram_id=789, is_subscribed=True)
    assert donate.amount == 1000
    assert sub.is_subscribed


@pytest.mark.django_db
def test_speaker_application_and_send_message():
    app = SpeakerApplication.objects.create(
        telegram_id=999, topic="Мой доклад", desc="Описание доклада"
    )
    msg = SendMessage.objects.create(message="Тестовая рассылка", group="all")
    assert app.status == "new"
    assert msg.message == "Тестовая рассылка"
