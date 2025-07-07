import pytest
from src.run import dms_to_decimal

@pytest.mark.parametrize("dms, expected", [
    ("176-38-32.9277W", -176.64248097222222),
    ("37-46-44.9277N", 37.77803547222222),
    ("122-25-9.9277W", -122.41942436111111),
    ("INVALID-DMS", None)
])
def test_dms_to_decimal(dms, expected):
    if expected is None:
        assert dms_to_decimal(dms) == expected
    else:
        assert dms_to_decimal(dms) - expected < 1e-2