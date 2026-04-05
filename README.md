# PytestLab

![Pytest CI](https://github.com/tony-tran-qa/pytestlab/actions/workflows/pytest.yml/badge.svg)

A structured Pytest skill-building project using automotive-domain business logic as the code under test. Built to develop and demonstrate practical test automation skills relevant to QA Engineer roles in the automotive and enterprise software sectors.

## Project Structure

```
PytestLab/
├── src/
│   └── vehicle_utils.py        # Code under test: VIN validation, service status, diagnostics
├── tests/
│   ├── test_01_basics.py       # Assertions, fixtures, markers
│   ├── test_02_parametrize.py  # Data-driven testing with @pytest.mark.parametrize
│   ├── test_03_fixtures_advanced.py  # Fixture scope, chaining, yield, tmp_path
│   ├── test_03_mocking.py      # Mocking fundamentals
│   ├── test_04_coverage_demo.py      # Coverage concepts
│   ├── test_04_mocking.py      # pytest-mock, MagicMock, side_effect
│   ├── test_05_api.py          # Live API tests via requests
│   └── test_06_coverage_ci.py  # Branch coverage, CI gates, coverage thresholds
├── conftest.py                 # Shared fixtures (global scope)
├── pytest.ini                  # Config: testpaths, markers, addopts
├── requirements.txt            # Dependencies
└── reports/                    # HTML test reports (gitignored)
```

## Test Coverage

| Module | Tests | Focus |
|---|---|---|
| test_01_basics | 6 | assert, fixtures, markers, xfail |
| test_02_parametrize | 13 | data-driven, edge cases, boundary values |
| test_03_fixtures_advanced | 10 | scope, chaining, yield teardown, tmp_path |
| test_03_mocking | 3 | mock fundamentals |
| test_04_coverage_demo | 5 | coverage gap identification |
| test_04_mocking | 10 | MagicMock, side_effect, patch, spy |
| test_05_api | 16 | live HTTP, status codes, schema validation |
| test_06_coverage_ci | 33 | branch coverage, CI gate, boundary values |

**96 total tests — 80 passing (non-API), 1 skipped, 1 xfailed**

## Run Commands

```bash
# All tests (excluding live API)
pytest -m "not api" -v

# Full suite with coverage report
pytest --cov=src --cov-report=html:reports/coverage --cov-fail-under=80

# By marker
pytest -m smoke
pytest -m regression
pytest -m "not api"

# Specific file
pytest tests/test_04_mocking.py -v

# HTML report (auto-generated via pytest.ini)
pytest
# report saved to reports/report.html
```

## Key Concepts Demonstrated

**Fixtures & conftest.py**
Shared test infrastructure across modules using function, module, and session scope — equivalent to Robot Framework resource files and suite setup/teardown.

**Parametrize**
Data-driven test coverage without duplication. Boundary value analysis applied directly to vehicle service status thresholds (5999/6000/7999/8000 km boundaries).

**Mocking**
`pytest-mock` and `MagicMock` for isolating external dependencies — HTTP APIs, file I/O, database calls. Demonstrates `side_effect` for simulating failures and `spy` for call verification.

**Coverage & CI Gates**
`pytest-cov` with `--cov-fail-under` threshold enforcement. Branch coverage vs. line coverage distinction. Structured to mirror CI pipeline behaviour (GitHub Actions / Jenkins).

**Markers**
`smoke`, `regression`, `api`, `slow` markers for selective test execution. Registered in `pytest.ini` to avoid warnings and enable clean CI filtering.

## Code Under Test

`vehicle_utils.py` simulates automotive domain logic:

| Function | Description |
|---|---|
| `validate_vin(vin)` | VIN validation — 17 chars, alphanumeric, no I/O/Q |
| `get_vehicle_status(odometer, last_service_km)` | Service status: OK / DUE_SOON / OVERDUE |
| `parse_diagnostic_codes(raw)` | OBD-II code parsing from comma-separated string |
| `calculate_fuel_efficiency(km, litres)` | L/100km calculation with input validation |

## Robot Framework Mapping

| RF Concept | Pytest Equivalent |
|---|---|
| Resource file | conftest.py |
| Suite Setup | fixture(scope="module") |
| Test Setup | fixture(scope="function") |
| Suite Teardown | yield fixture (after yield) |
| Tags | @pytest.mark.name |
| Data-driven tables | @pytest.mark.parametrize |
| Run Keyword | mocker.patch |

## Requirements

```
pytest
pytest-cov
pytest-mock
pytest-html
requests
```

Install: `pip install -r requirements.txt`
