# PytestLab — Run Commands Reference

## Basic
```bash
pytest                              # all tests
pytest -v                           # verbose
pytest tests/test_01_basics.py -v   # single file
pytest -m smoke                     # by marker
pytest -m "not api"                 # exclude api tests (offline CI)
```

## By Day
```bash
pytest tests/test_01_basics.py -v
pytest tests/test_02_parametrize.py -v
pytest tests/test_03_fixtures_advanced.py -v
pytest tests/test_04_mocking.py -v
pytest tests/test_05_api.py -v
pytest tests/test_06_coverage_ci.py -v
```

## Coverage (Day 6)
```bash
# Terminal report — shows missing lines per file
pytest --cov=src --cov-report=term-missing

# HTML report — open reports/coverage/index.html in browser
pytest --cov=src --cov-report=html:reports/coverage

# CI gate — exits with code 1 if coverage < 85% (blocks merge)
pytest --cov=src --cov-fail-under=85

# Full CI command — terminal + HTML + gate combined
pytest --cov=src --cov-report=term-missing --cov-report=html:reports/coverage --cov-fail-under=85

# Demonstrate gate failure (intentionally too high)
pytest --cov=src --cov-fail-under=99

# XML output for Codecov / SonarQube ingestion
pytest --cov=src --cov-report=xml:reports/coverage.xml
```

## HTML Report
```bash
pytest --html=reports/report.html --self-contained-html
```

## Full CI Simulation (coverage + HTML report + gate)
```bash
pytest --cov=src --cov-report=term-missing --cov-report=html:reports/coverage --cov-fail-under=85 --html=reports/report.html --self-contained-html
```
