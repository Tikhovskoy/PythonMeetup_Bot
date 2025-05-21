import pytest
from bot.services import donations_service

@pytest.fixture(autouse=True)
def clear_donations():
    donations_service.clear_donations()

def test_save_and_get_donation_success():
    data = {
        'telegram_id': 111,
        'amount': 1500,
    }
    saved = donations_service.save_donation(data)
    assert saved['telegram_id'] == 111
    assert saved['amount'] == 1500

    donations = donations_service.get_all_donations()
    assert len(donations) == 1
    assert donations[0]['amount'] == 1500

def test_validate_donation_bad_amount():
    bad_data = {
        'telegram_id': 111,
        'amount': 0,
    }
    with pytest.raises(ValueError) as exc:
        donations_service.save_donation(bad_data)
    assert "больше нуля" in str(exc.value)

    bad_data2 = {
        'telegram_id': 222,
        'amount': 'notanumber',
    }
    with pytest.raises(ValueError):
        donations_service.save_donation(bad_data2)

def test_total_amount():
    donations_service.save_donation({'telegram_id': 1, 'amount': 100})
    donations_service.save_donation({'telegram_id': 2, 'amount': 200})
    assert donations_service.get_total_amount() == 300

def test_save_without_telegram_id():
    data = {'amount': 100}
    with pytest.raises(ValueError):
        donations_service.save_donation(data)
