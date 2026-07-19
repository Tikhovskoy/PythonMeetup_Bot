from django.db import transaction
from django.utils import timezone

from apps.events.models import Donate, Payment


def create_payment(telegram_id: int, amount: int, currency: str) -> Payment:
    return Payment.objects.create(telegram_id=telegram_id, amount=amount, currency=currency)


def validate_precheckout(payload: str, telegram_id: int, amount: int, currency: str) -> bool:
    return Payment.objects.filter(
        payload=payload,
        telegram_id=telegram_id,
        amount=amount,
        currency=currency,
        status=Payment.STATUS_PENDING,
    ).exists()


@transaction.atomic
def finalize_payment(
    payload: str, telegram_id: int, amount: int, currency: str, charge_id: str, name: str
) -> tuple[Donate, bool]:
    payment = Payment.objects.select_for_update().get(payload=payload)
    if (payment.telegram_id, payment.amount, payment.currency) != (telegram_id, amount, currency):
        raise ValueError("Параметры платежа не совпадают с выставленным счётом.")
    if payment.status == Payment.STATUS_PAID:
        return payment.donation, False
    donation = Donate.objects.create(telegram_id=telegram_id, name=name, amount=amount // 100)
    payment.status = Payment.STATUS_PAID
    payment.telegram_payment_charge_id = charge_id
    payment.donation = donation
    payment.paid_at = timezone.now()
    payment.save(update_fields=["status", "telegram_payment_charge_id", "donation", "paid_at"])
    return donation, True
