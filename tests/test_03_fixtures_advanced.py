# ============================================================
# tests/test_03_fixtures_advanced.py  --  DAY 3: Advanced Fixtures
# ============================================================
# LEARNING GOALS:
#   - fixture scope: function vs module vs session
#   - fixture chaining (fixture depending on fixture)
#   - yield fixtures (setup + teardown in one block)
#   - tmp_path built-in fixture
#   - capsys built-in fixture (capture stdout)
# Run: pytest tests/test_03_fixtures_advanced.py -v
# ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from vehicle_utils import validate_vin, parse_diagnostic_codes


# ----------------------------------------------------------
# FIXTURE CHAINING
# A fixture can depend on another fixture by name.
# pytest resolves the dependency chain automatically.
# ----------------------------------------------------------

@pytest.fixture(scope="module")
def vehicle_fleet():
    """Returns a list of raw vehicle records (module scope = once per file)."""
    return [
        {"vin": "1FTFW1ET0EKE12345", "make": "Ford", "model": "F-150"},
        {"vin": "1FMCU9GD0LUA12345", "make": "Ford", "model": "Escape"},
        {"vin": "3FADP4AJ1KM123456", "make": "Ford", "model": "Fiesta"},
    ]


@pytest.fixture(scope="module")
def valid_vins(vehicle_fleet):
    """
    Depends on vehicle_fleet -- pytest injects it automatically.
    Fixture chaining: valid_vins builds on vehicle_fleet.
    """
    return [v["vin"] for v in vehicle_fleet if validate_vin(v["vin"])]


def test_fleet_has_three_vehicles(vehicle_fleet):
    assert len(vehicle_fleet) == 3


def test_all_fleet_vins_are_valid(valid_vins):
    assert len(valid_vins) == 3


def test_fleet_makes_are_all_ford(vehicle_fleet):
    makes = [v["make"] for v in vehicle_fleet]
    assert all(m == "Ford" for m in makes)


# ----------------------------------------------------------
# YIELD FIXTURES  (setup + teardown in one block)
# Everything before yield = setup
# Everything after yield = teardown (runs even if test fails)
# Analogy: Suite Setup + Suite Teardown in one RF keyword
# ----------------------------------------------------------

@pytest.fixture
def diagnostic_session():
    """
    Simulates opening and closing a diagnostic session.
    yield passes the session object to the test.
    Teardown runs automatically after the test completes.
    """
    print("\n[SETUP] Opening diagnostic session")
    session = {"active": True, "codes": [], "session_id": "DIAG-001"}
    yield session
    # --- teardown ---
    session["active"] = False
    print("\n[TEARDOWN] Diagnostic session closed")


def test_session_starts_active(diagnostic_session):
    assert diagnostic_session["active"] is True


def test_session_can_collect_codes(diagnostic_session):
    diagnostic_session["codes"].append("P0300")
    assert "P0300" in diagnostic_session["codes"]


def test_each_test_gets_fresh_session(diagnostic_session):
    """
    This test proves scope=function gives a fresh fixture.
    The code list should be empty -- not carry over from previous test.
    """
    assert diagnostic_session["codes"] == []


# ----------------------------------------------------------
# BUILT-IN FIXTURE: tmp_path
# pytest provides this automatically -- no import needed.
# Creates a temporary directory that is cleaned up after the test.
# ----------------------------------------------------------

def test_write_diagnostic_report(tmp_path):
    """
    tmp_path is a built-in pytest fixture that provides a
    temporary Path object. Safe for file I/O in tests.
    """
    report_file = tmp_path / "diag_report.txt"
    codes = parse_diagnostic_codes("P0300, P0420, B1234")
    report_file.write_text("\n".join(codes))

    content = report_file.read_text()
    assert "P0300" in content
    assert "P0420" in content
    assert "B1234" in content


def test_report_file_exists(tmp_path):
    report_file = tmp_path / "test_output.txt"
    report_file.write_text("test data")
    assert report_file.exists()


# ----------------------------------------------------------
# BUILT-IN FIXTURE: capsys
# Captures stdout/stderr output from your code under test.
# ----------------------------------------------------------

def log_vin_result(vin):
    """Utility that prints to stdout -- we want to test its output."""
    result = validate_vin(vin)
    print(f"VIN {vin}: {'VALID' if result else 'INVALID'}")
    return result


def test_vin_log_output(capsys):
    log_vin_result("1FTFW1ET0EKE12345")
    captured = capsys.readouterr()
    assert "VALID" in captured.out
    assert "1FTFW1ET0EKE12345" in captured.out


def test_invalid_vin_log_output(capsys):
    log_vin_result("BADVIN")
    captured = capsys.readouterr()
    assert "INVALID" in captured.out
