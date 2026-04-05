"""
Phase 2 - Parametrize (Ford explicitly requires this).
Run: pytest tests/test_02_parametrize.py -v
"""
import pytest

def validate_vin(vin: str) -> bool:
    if not vin or len(vin) != 17:
        return False
    invalid_chars = set("IOQ")
    return all(c.isalnum() and c not in invalid_chars for c in vin.upper())

@pytest.mark.parametrize("vin, expected", [
    ("1FTFW1ET0EKE12345", True),
    ("INVALID_VIN",       False),
    ("",                  False),
    ("1FTFW1ET0EKE1234I", False),
    ("1FTFW1ET0EKE12340", True),
])
def test_vin_validation(vin, expected):
    assert validate_vin(vin) == expected

@pytest.mark.parametrize("year, make, valid", [
    (2024, "Ford",    True),
    (1899, "Ford",    False),
    (2024, "",        False),
    (2024, "Lincoln", True),
])
def test_vehicle_record_valid(year, make, valid):
    is_valid = year >= 1900 and len(make) > 0
    assert is_valid == valid

@pytest.mark.smoke
@pytest.mark.parametrize("status_code, expected_pass", [
    (200, True),(201, True),(400, False),(500, False),
])
def test_http_status_handling(status_code, expected_pass):
    is_success = 200 <= status_code < 300
    assert is_success == expected_pass
