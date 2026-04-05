# PytestLab — QA Portfolio Project

## Project Purpose
Pytest skill-building using automotive-domain business logic as the code under test.
Demonstrates practical test automation skills for QA Engineer roles.

## Current State
- **96 total tests** across 8 test files
- **80 passing** (non-API), 1 skipped, 1 xfailed
- **98% coverage** on src/vehicle_utils.py
- All non-API tests green as of April 2026

## Structure
```
PytestLab/
├── src/                              # Code under test
│   └── vehicle_utils.py              # VIN, service status, diagnostics, fuel efficiency
├── tests/
│   ├── test_01_basics.py             # Assertions, fixtures, markers
│   ├── test_02_parametrize.py        # Data-driven with parametrize
│   ├── test_03_fixtures_advanced.py  # Scope, chaining, yield, tmp_path
│   ├── test_03_mocking.py            # Mock fundamentals
│   ├── test_04_coverage_demo.py      # Coverage gap identification
│   ├── test_04_mocking.py            # pytest-mock, MagicMock, side_effect
│   ├── test_05_api.py                # Live API tests (requires network)
│   └── test_06_coverage_ci.py        # Branch coverage, CI gates
├── conftest.py                       # Shared fixtures (global)
├── pytest.ini                        # Config: testpaths, markers, addopts
├── requirements.txt                  # pytest, pytest-cov, pytest-mock, pytest-html, requests
└── reports/                          # HTML reports (gitignored)
```

## Run Commands
```bash
# Standard run (skip live API tests)
pytest -m "not api" -v

# With coverage
pytest --cov=src --cov-report=html:reports/coverage --cov-fail-under=80

# By marker
pytest -m smoke
pytest -m "not api"

# Specific file
pytest tests/test_04_mocking.py -v

# HTML report (auto via pytest.ini addopts)
pytest
```

## Robot Framework Mapping
| RF Concept         | Pytest Equivalent              |
|--------------------|-------------------------------|
| Resource file      | conftest.py                   |
| Suite Setup        | fixture(scope="module")       |
| Test Setup         | fixture(scope="function")     |
| Suite Teardown     | yield fixture (after yield)   |
| Tags               | @pytest.mark.name             |
| Data-driven tables | @pytest.mark.parametrize      |
| Run Keyword        | mocker.patch                  |

## Interview Talking Points
- fixtures + conftest.py: shared infrastructure pattern across test files
- parametrize: boundary value analysis without duplication (5999/6000/7999/8000 km thresholds)
- pytest-cov: coverage gating (--cov-fail-under) as CI merge gate
- pytest-mock: isolating HTTP APIs, file I/O, and external dependencies
- markers: selective execution for smoke, regression, and API test tiers
- xfail: documenting known failures without blocking the suite
