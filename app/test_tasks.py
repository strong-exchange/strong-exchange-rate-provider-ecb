import pytest

from .tasks import update_daily_rates_from_ecb, load_history_from_ecb_file
from .data import rates, latest_daily_rate_for, history_data


@pytest.mark.anyio
async def test_update_daily_rates_from_ecb_task_works():
    assert not rates
    assert latest_daily_rate_for is None

    await update_daily_rates_from_ecb()

    assert rates
    assert "USD" in rates
    assert "THB" in rates


def test_load_history_from_ecb_file_works():
    assert not history_data

    load_history_from_ecb_file()

    assert history_data
