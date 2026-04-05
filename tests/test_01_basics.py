"""
Phase 1 - Basic pytest patterns.
Run: pytest tests/test_01_basics.py -v
"""
import pytest


# ── 1. Simplest possible test ────────────────────────────────────────────────
def test_addition():
    assert 1 + 1 == 2


# ── 2. Test with fixture from conftest.py ────────────────────────────────────
def test_vehicle_has_vin(sample_vehicle):
    assert "vin" in sample_vehicle
    assert len(sample_vehicle["vin"]) == 17


def test_vehicle_is_ford(sample_vehicle):
    assert sample_vehicle["make"] == "Ford"


# ── 3. Markers ───────────────────────────────────────────────────────────────
@pytest.mark.smoke
def test_config_loaded(app_config):
    assert app_config["env"] == "test"
    assert app_config["timeout"] > 0


@pytest.mark.skip(reason="Placeholder -- implement when API is available")
def test_live_api_connection():
    pass


@pytest.mark.xfail(reason="Known edge case FORD-0001 -- not yet fixed")
def test_known_failing_edge_case():
    assert 1 == 2  # intentionally fails
