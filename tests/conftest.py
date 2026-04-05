import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()


@pytest.fixture
def fresh_payload():
    return {
        "title": "Test Post",
        "body": "This is a test body.",
        "userId": 1
    }
