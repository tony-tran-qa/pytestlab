# ============================================================
# src/vehicle_utils.py  --  Sample business logic module
# This is the CODE UNDER TEST -- not the tests themselves.
# Ford context: VIN validation, status checks, diagnostics
# ============================================================


def validate_vin(vin: str) -> bool:
    """
    Validates a Vehicle Identification Number (VIN).
    Rules: exactly 17 chars, alphanumeric, no I/O/Q.
    """
    if not vin or not isinstance(vin, str):
        return False
    vin = vin.strip().upper()
    if len(vin) != 17:
        return False
    forbidden = set("IOQ")
    return all(c.isalnum() and c not in forbidden for c in vin)


def get_vehicle_status(odometer: int, last_service_km: int) -> str:
    """
    Returns service status based on km since last service.
    Business rule: service every 8,000 km.
    """
    if not isinstance(odometer, int) or not isinstance(last_service_km, int):
        raise TypeError("Odometer values must be integers")
    if odometer < last_service_km:
        raise ValueError("Odometer cannot be less than last service reading")

    km_since_service = odometer - last_service_km

    if km_since_service < 6000:
        return "OK"
    elif km_since_service < 8000:
        return "DUE_SOON"
    else:
        return "OVERDUE"


def parse_diagnostic_codes(raw: str) -> list:
    """
    Parses a comma-separated string of OBD-II diagnostic codes.
    Returns a cleaned list. Empty string returns empty list.
    """
    if not raw or not raw.strip():
        return []
    return [code.strip().upper() for code in raw.split(",") if code.strip()]


def calculate_fuel_efficiency(km: float, litres: float) -> float:
    """
    Returns fuel efficiency in L/100km.
    Raises ValueError on invalid inputs.
    """
    if litres <= 0 or km <= 0:
        raise ValueError("Distance and fuel must be positive values")
    return round((litres / km) * 100, 2)
