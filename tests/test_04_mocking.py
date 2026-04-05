# ============================================================
# tests/test_04_mocking.py  --  DAY 4: pytest-mock + Coverage
# ============================================================
# LEARNING GOALS:
#   - mocker fixture (from pytest-mock)
#   - mock.patch vs mocker.patch
#   - MagicMock: return_value, side_effect
#   - Verifying calls: assert_called_once_with
#   - Running with coverage: pytest --cov=src --cov-report=html
# Run: pytest tests/test_04_mocking.py -v
# ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest


# ----------------------------------------------------------
# WHY MOCK?
# Tests should not depend on external systems (DBs, APIs, files).
# Mocking replaces a real dependency with a controlled fake.
# Analogy: RF's Run Keyword If + a stub keyword that returns canned data.
# ----------------------------------------------------------

# ----------------------------------------------------------
# MOCKING A FUNCTION RETURN VALUE
# mocker.patch replaces the target for the duration of the test.
# After the test, the original is restored automatically.
# ----------------------------------------------------------

def fetch_vehicle_recall_status(vin: str) -> dict:
    """Simulates a call to an external recall API."""
    # In reality this would call requests.get(...)
    raise NotImplementedError("Real API not available in test env")


def check_recall_and_notify(vin: str) -> str:
    """Business logic that calls the external API."""
    status = fetch_vehicle_recall_status(vin)
    if status.get("recall_active"):
        return f"RECALL ACTIVE: {status['recall_id']}"
    return "NO_RECALL"


def test_recall_active(mocker):
    """
    Mock fetch_vehicle_recall_status to return a canned recall response.
    The real API is never called.
    """
    # Patch the function within this module's namespace (correct approach)
    mocker.patch.object(
        sys.modules[__name__],
        "fetch_vehicle_recall_status",
        return_value={"recall_active": True, "recall_id": "NHTSA-2024-001"}
    )
    result = check_recall_and_notify("1FTFW1ET0EKE12345")
    assert result == "RECALL ACTIVE: NHTSA-2024-001"


def test_no_recall(mocker):
    mocker.patch.object(
        sys.modules[__name__],
        "fetch_vehicle_recall_status",
        return_value={"recall_active": False}
    )
    result = check_recall_and_notify("1FTFW1ET0EKE12345")
    assert result == "NO_RECALL"


# ----------------------------------------------------------
# VERIFYING CALL COUNT + ARGUMENTS
# ----------------------------------------------------------

def send_alert(recipient: str, message: str) -> None:
    """Simulates sending an alert email/notification."""
    pass  # Real impl would call an email API


def process_critical_code(code: str, notify_email: str) -> None:
    """Business logic: if code is critical, send alert."""
    critical_codes = {"P0700", "B1000", "U0100"}
    if code in critical_codes:
        send_alert(notify_email, f"Critical DTC detected: {code}")


def test_alert_sent_for_critical_code(mocker):
    """Verify send_alert is called with the right arguments."""
    mock_alert = mocker.patch.object(sys.modules[__name__], "send_alert")

    process_critical_code("P0700", "qa@ford.com")

    mock_alert.assert_called_once_with("qa@ford.com", "Critical DTC detected: P0700")


def test_no_alert_for_normal_code(mocker):
    """Verify send_alert is NOT called for a non-critical code."""
    mock_alert = mocker.patch.object(sys.modules[__name__], "send_alert")

    process_critical_code("P0300", "qa@ford.com")

    mock_alert.assert_not_called()


# ----------------------------------------------------------
# SIDE_EFFECT: simulate exceptions from dependencies
# ----------------------------------------------------------

def get_telemetry(vehicle_id: str) -> dict:
    """Would call a telemetry service in production."""
    raise ConnectionError("Telemetry service unreachable")
# Key Interview Statement
#   "We're at 98% coverage. The 5 missed lines are all intentional — one skipped test placeholder, one deliberately untested branch to demonstrate gap detection, and three stub bodies that mocks replace by design. I track coverage as a quality gate in CI with --cov-fail-under=80, not as a target to game."

def safe_telemetry_fetch(vehicle_id: str) -> dict:
    """Wraps get_telemetry with error handling."""
    try:
        return get_telemetry(vehicle_id)
    except ConnectionError:
        return {"status": "unavailable", "vehicle_id": vehicle_id}


def test_telemetry_unavailable_handled(mocker):
    """
    Use side_effect to make the mock raise an exception.
    Verifies our error handling works correctly.
    """
    mocker.patch.object(
        sys.modules[__name__],
        "get_telemetry",
        side_effect=ConnectionError("Telemetry service unreachable")
    )
    result = safe_telemetry_fetch("VH-001")
    assert result["status"] == "unavailable"
    assert result["vehicle_id"] == "VH-001"


# ----------------------------------------------------------
# PARAMETRIZE + MOCK COMBINED
# ----------------------------------------------------------

@pytest.mark.parametrize("code,should_alert", [
    ("P0700", True),
    ("B1000", True),
    ("U0100", True),
    ("P0300", False),
    ("C1234", False),
])
def test_alert_logic_parametrized(mocker, code, should_alert):
    mock_alert = mocker.patch.object(sys.modules[__name__], "send_alert")
    process_critical_code(code, "qa@ford.com")
    if should_alert:
        mock_alert.assert_called_once()
    else:
        mock_alert.assert_not_called()
