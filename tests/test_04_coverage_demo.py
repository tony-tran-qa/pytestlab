"""
Phase 4 - Coverage demo.
Run: pytest tests/test_04_coverage_demo.py --cov=tests --cov-report=term-missing
"""
def classify_diagnostic_code(code: str) -> str:
    if not code:
        return "invalid"
    prefix = code[0].upper()
    if prefix == "P":
        return "powertrain"
    elif prefix == "B":
        return "body"
    elif prefix == "C":
        return "chassis"
    elif prefix == "U":
        return "network"
    else:
        return "unknown"

def test_powertrain():
    assert classify_diagnostic_code("P0300") == "powertrain"

def test_body():
    assert classify_diagnostic_code("B1234") == "body"

def test_chassis():
    assert classify_diagnostic_code("C0035") == "chassis"

def test_network():
    assert classify_diagnostic_code("U0100") == "network"

def test_empty():
    assert classify_diagnostic_code("") == "invalid"
# NOTE: "unknown" branch intentionally NOT tested -- shows as missed in coverage report

#def test_unknown():
#    assert classify_diagnostic_code("X9999") == "unknown"