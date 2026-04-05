# ============================================================
# tests/test_06_coverage_ci.py  --  DAY 6: Coverage & CI Readiness
# ============================================================
# LEARNING GOALS:
#   - pytest-cov: measuring code coverage per module
#   - Branch coverage: testing all if/elif/else paths
#   - Coverage thresholds as CI gates (--cov-fail-under=N)
#   - Why 100% line coverage != 100% branch coverage
#   - Structuring tests to close coverage gaps deliberately
#
# Run (basic):
#   pytest tests/test_06_coverage_ci.py -v
#
# Run with coverage (full suite):
#   pytest --cov=src --cov-report=term-missing --cov-report=html:reports/coverage
#
# Run with CI gate (fails build if coverage drops below 90%):
#   pytest --cov=src --cov-fail-under=90
#
# Ford interview context:
#   "Our pipeline runs pytest --cov=src --cov-fail-under=80 on every PR.
#    Any drop below threshold blocks the merge."
# ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from vehicle_utils import (
    validate_vin,
    get_vehicle_status,
    parse_diagnostic_codes,
    calculate_fuel_efficiency,
)


# ============================================================
# SECTION 1: validate_vin — branch coverage
# ============================================================
# The function has 4 distinct branches:
#   1. None / non-string input   → False
#   2. Wrong length (!=17)       → False
#   3. Contains I, O, or Q       → False
#   4. Valid VIN                 → True
#
# Line coverage alone would miss branch 3 if you only test valid + empty.
# ============================================================

class TestValidateVinCoverage:

    def test_valid_vin_passes(self):
        """Happy path — 17 chars, no I/O/Q."""
        assert validate_vin("1FTFW1ET0EKE12345") is True

    def test_none_input_returns_false(self):
        """Branch: falsy input guard."""
        assert validate_vin(None) is False

    def test_non_string_returns_false(self):
        """Branch: isinstance check fails."""
        assert validate_vin(12345678901234567) is False

    def test_wrong_length_short(self):
        """Branch: len != 17 (too short)."""
        assert validate_vin("1FTFW1ET0EKE123") is False

    def test_wrong_length_long(self):
        """Branch: len != 17 (too long)."""
        assert validate_vin("1FTFW1ET0EKE123456789") is False

    def test_forbidden_char_I(self):
        """Branch: forbidden char I present."""
        assert validate_vin("1FTFW1ET0EKE1234I") is False

    def test_forbidden_char_O(self):
        """Branch: forbidden char O present."""
        assert validate_vin("1FTFW1ET0OKE12345") is False

    def test_forbidden_char_Q(self):
        """Branch: forbidden char Q present."""
        assert validate_vin("1FTFW1ET0QKE12345") is False

    def test_lowercase_is_normalized(self):
        """Branch: lowercase input is stripped and uppercased before validation."""
        assert validate_vin("1ftfw1et0eke12345") is True

    def test_empty_string_returns_false(self):
        """Branch: empty string is falsy."""
        assert validate_vin("") is False


# ============================================================
# SECTION 2: get_vehicle_status — branch coverage
# ============================================================
# Branches:
#   1. TypeError: non-int inputs
#   2. ValueError: odometer < last_service_km
#   3. OK:        km_since_service < 6000
#   4. DUE_SOON:  6000 <= km_since < 8000
#   5. OVERDUE:   km_since >= 8000
#
# Boundary values matter here — this is where parametrize shines.
# ============================================================

class TestVehicleStatusCoverage:

    @pytest.mark.parametrize("odometer,last_service,expected", [
        (5000,  0,     "OK"),         # well under threshold
        (5999,  0,     "OK"),         # boundary: 1 km before DUE_SOON
        (6000,  0,     "DUE_SOON"),   # boundary: first km of DUE_SOON
        (7999,  0,     "DUE_SOON"),   # boundary: last km before OVERDUE
        (8000,  0,     "OVERDUE"),    # boundary: exactly at OVERDUE
        (15000, 5000,  "OVERDUE"),    # 15k odometer, 5k last service = 10k since → OVERDUE
        (10000, 5000,  "OK"),         # 10k odometer, 5k last service = 5k since → OK
    ], ids=[
        "well_under", "boundary_ok_max", "boundary_due_soon_min",
        "boundary_due_soon_max", "boundary_overdue_min",
        "relative_due_soon", "relative_overdue"
    ])
    def test_status_boundaries(self, odometer, last_service, expected):
        assert get_vehicle_status(odometer, last_service) == expected

    def test_type_error_on_float_odometer(self):
        """Branch: TypeError when non-int passed."""
        with pytest.raises(TypeError):
            get_vehicle_status(5000.5, 0)

    def test_type_error_on_string_input(self):
        """Branch: TypeError when string passed."""
        with pytest.raises(TypeError):
            get_vehicle_status("5000", 0)

    def test_value_error_when_odometer_less_than_service(self):
        """Branch: ValueError when odometer < last_service_km (impossible state)."""
        with pytest.raises(ValueError, match="cannot be less than"):
            get_vehicle_status(1000, 5000)


# ============================================================
# SECTION 3: parse_diagnostic_codes — branch coverage
# ============================================================
# Branches:
#   1. None / empty string / whitespace-only → []
#   2. Single code                           → [code]
#   3. Multiple codes                        → [code1, code2, ...]
#   4. Codes with extra whitespace           → stripped
#   5. Lowercase codes                       → uppercased
# ============================================================

class TestParseDiagnosticCodesCoverage:

    def test_empty_string_returns_empty_list(self):
        assert parse_diagnostic_codes("") == []

    def test_whitespace_only_returns_empty_list(self):
        """Branch: strip() catches whitespace-only strings."""
        assert parse_diagnostic_codes("   ") == []

    def test_single_code(self):
        assert parse_diagnostic_codes("P0700") == ["P0700"]

    def test_multiple_codes(self):
        assert parse_diagnostic_codes("P0700,B1000,U0100") == ["P0700", "B1000", "U0100"]

    def test_codes_with_extra_whitespace(self):
        """Branch: each token is stripped."""
        assert parse_diagnostic_codes("  P0700 , B1000 ") == ["P0700", "B1000"]

    def test_lowercase_codes_uppercased(self):
        """Branch: .upper() applied per token."""
        assert parse_diagnostic_codes("p0700,b1000") == ["P0700", "B1000"]

    def test_empty_tokens_filtered(self):
        """Branch: trailing comma produces empty token — filtered out."""
        assert parse_diagnostic_codes("P0700,,B1000") == ["P0700", "B1000"]


# ============================================================
# SECTION 4: calculate_fuel_efficiency — branch coverage
# ============================================================
# Branches:
#   1. ValueError: litres <= 0
#   2. ValueError: km <= 0
#   3. Valid: returns rounded float
# ============================================================

class TestFuelEfficiencyCoverage:

    def test_valid_calculation(self):
        """500km on 40L → 8.0 L/100km."""
        assert calculate_fuel_efficiency(500, 40) == 8.0

    def test_rounding_to_2_decimal_places(self):
        """300km on 25L → 8.33 L/100km."""
        assert calculate_fuel_efficiency(300, 25) == 8.33

    def test_zero_litres_raises(self):
        """Branch: litres=0 → ValueError."""
        with pytest.raises(ValueError, match="positive"):
            calculate_fuel_efficiency(500, 0)

    def test_negative_litres_raises(self):
        """Branch: litres<0 → ValueError."""
        with pytest.raises(ValueError):
            calculate_fuel_efficiency(500, -10)

    def test_zero_km_raises(self):
        """Branch: km=0 → ValueError."""
        with pytest.raises(ValueError, match="positive"):
            calculate_fuel_efficiency(0, 40)

    def test_negative_km_raises(self):
        """Branch: km<0 → ValueError."""
        with pytest.raises(ValueError):
            calculate_fuel_efficiency(-100, 40)


# ============================================================
# SECTION 5: CI GATE CONCEPT (no runnable test — just docs)
# ============================================================
#
# In a real CI pipeline (GitHub Actions, Jenkins, etc.) you'd have:
#
#   pytest --cov=src --cov-fail-under=85 --cov-report=xml
#
# --cov-fail-under=85  → pytest exits with code 1 if coverage < 85%
#                        This BLOCKS the pipeline / merge
# --cov-report=xml     → produces coverage.xml for Codecov / SonarQube
#
# Ford pipeline equivalent: Slash test runner with --threshold gate
#
# To see this in action:
#   pytest --cov=src --cov-fail-under=99   ← will FAIL (nothing is 99%)
#   pytest --cov=src --cov-fail-under=85   ← should PASS after Day 6 tests
#
# ============================================================

