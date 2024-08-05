import pytest

from property_tracker.models.investor import InvestorType
from property_tracker.services.finance import calculate_stamp_duty


@pytest.mark.parametrize(
    "amount, investor_type, expected",
    [
        (250000, InvestorType.SOLE_TRADER, 7500),
        (600000, InvestorType.LIMITED_COMPANY, 38000),
    ],
)
def test_calculate_stamp_duty(amount, investor_type, expected):
    result = calculate_stamp_duty(amount, investor_type)
    assert result == expected
