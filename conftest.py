import pytest

# ── Global fixtures available to all tests ──────────────────────────────────

@pytest.fixture(scope="session")
def app_config():
    """Session-scoped config. Runs once for the entire test session."""
    return {
        "base_url": "https://api.example.com",
        "timeout": 10,
        "env": "test"
    }

@pytest.fixture(scope="module")
def api_headers():
    """Module-scoped headers. Shared across all tests in a module."""
    return {"Authorization": "Bearer test-token", "Content-Type": "application/json"}

@pytest.fixture(scope="function")
def sample_vehicle():
    """Function-scoped fixture. Fresh data per test."""
    return {"vin": "1FTFW1ET0EKE12345", "make": "Ford", "model": "F-150", "year": 2024}

# ── Custom mark registration (avoids PytestUnknownMarkWarning) ───────────────
def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: fast, critical-path tests")
    config.addinivalue_line("markers", "regression: full regression suite")
    config.addinivalue_line("markers", "ford: Ford diagnostics-specific tests")
    config.addinivalue_line("markers", "api: live HTTP API tests (requires network)")

# ── DAY 6: Pipeline-style pass/fail hook ─────────────────────────────────────
# pytest_runtest_logreport is called after each test phase (setup/call/teardown).
# We only care about the "call" phase — that's the actual test body.
# This is equivalent to a Robot Framework listener's end_test() method.

def pytest_runtest_logreport(report):
    """
    Custom hook: logs PASSED / FAILED / SKIPPED to logs/pytest.log
    in a structured format suitable for CI log parsing.

    In a Ford/Jenkins pipeline context, this output is ingested by
    a log aggregator to build pass-rate dashboards.
    """
    if report.when != "call":
        return  # ignore setup and teardown phases

    import logging
    logger = logging.getLogger("ci_pipeline")

    if report.passed:
        logger.info(f"[PASS] {report.nodeid}")
    elif report.failed:
        logger.error(f"[FAIL] {report.nodeid}  →  {report.longreprtext[:120] if hasattr(report, 'longreprtext') else 'see output'}")
    elif report.skipped:
        logger.warning(f"[SKIP] {report.nodeid}")
