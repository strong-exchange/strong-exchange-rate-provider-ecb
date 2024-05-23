from .tasks import update_daily_rates_from_ecb
from .data import rates, latest_daily_rate_for


def test_update_daily_rates_from_ecb_task_work():
    assert not rates
    assert latest_daily_rate_for is None

    update_daily_rates_from_ecb()

    assert rates
    assert 'USD' in rates
    assert 'THB' in rates
    