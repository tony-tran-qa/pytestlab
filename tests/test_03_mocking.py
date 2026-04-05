"""
Phase 3 - Mocking with pytest-mock.
Run: pytest tests/test_03_mocking.py -v
"""
import pytest
import requests

def fetch_vehicle_data(vin: str) -> dict:
    response = requests.get(f"https://api.example.com/vehicles/{vin}")
    response.raise_for_status()
    return response.json()

def get_vehicle_year(vin: str) -> int:
    data = fetch_vehicle_data(vin)
    return data["year"]

def test_fetch_vehicle_data_success(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"vin": "1FTFW1ET0EKE12345", "year": 2024, "make": "Ford"}
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)
    result = fetch_vehicle_data("1FTFW1ET0EKE12345")
    assert result["make"] == "Ford"
    assert result["year"] == 2024

def test_fetch_vehicle_data_404(mocker):
    mocker.patch("requests.get", side_effect=requests.exceptions.HTTPError("404"))
    with pytest.raises(requests.exceptions.HTTPError):
        fetch_vehicle_data("BADVIN00000000000")

def test_get_vehicle_year(mocker):
    mocker.patch("tests.test_03_mocking.fetch_vehicle_data", return_value={"year": 2022})
    assert get_vehicle_year("1FTFW1ET0EKE12345") == 2022
