import pytest

from apps.events.models import Payment
from bot.services import payments_service


@pytest.mark.django_db
def test_precheckout_rejects_changed_payment_data():
    payment = payments_service.create_payment(telegram_id=100, amount=15_000, currency="RUB")

    assert payments_service.validate_precheckout(
        str(payment.payload), telegram_id=100, amount=15_000, currency="RUB"
    )
    assert not payments_service.validate_precheckout(
        str(payment.payload), telegram_id=101, amount=15_000, currency="RUB"
    )
    assert not payments_service.validate_precheckout(
        str(payment.payload), telegram_id=100, amount=20_000, currency="RUB"
    )


@pytest.mark.django_db
def test_payment_is_recorded_only_once():
    payment = payments_service.create_payment(telegram_id=100, amount=15_000, currency="RUB")

    donation, created = payments_service.finalize_payment(
        str(payment.payload), 100, 15_000, "RUB", "charge-1", "Тестовый Пользователь"
    )
    repeated_donation, repeated_created = payments_service.finalize_payment(
        str(payment.payload), 100, 15_000, "RUB", "charge-1", "Тестовый Пользователь"
    )

    payment.refresh_from_db()
    assert created
    assert not repeated_created
    assert repeated_donation.id == donation.id
    assert payment.status == Payment.STATUS_PAID
    assert payment.donation_id == donation.id
