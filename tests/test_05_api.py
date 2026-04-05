# ============================================================
# tests/test_05_api.py  --  DAY 5: Live API Tests
# ============================================================
# LEARNING GOALS:
#   - requests + pytest (real HTTP calls)
#   - Session fixture from conftest.py (api_session, base_url)
#   - Validating response shape, status codes, data types
#   - @pytest.mark.api to tag and selectively run
#   - Skip pattern for CI environments without network access
#
# Uses: https://jsonplaceholder.typicode.com (free public REST API)
#
# Run all:        pytest tests/test_05_api.py -v
# Run api only:   pytest -m api -v
# Skip api in CI: pytest -m "not api"
# ============================================================

import pytest


# ----------------------------------------------------------
# BASIC STATUS CODE CHECKS
# api_session and base_url come from conftest.py -- auto-injected
# ----------------------------------------------------------

@pytest.mark.api
def test_get_posts_returns_200(api_session, base_url):
    response = api_session.get(f"{base_url}/posts")
    assert response.status_code == 200


@pytest.mark.api
def test_get_single_post_returns_200(api_session, base_url):
    response = api_session.get(f"{base_url}/posts/1")
    assert response.status_code == 200


@pytest.mark.api
def test_get_nonexistent_post_returns_404(api_session, base_url):
    response = api_session.get(f"{base_url}/posts/99999")
    assert response.status_code == 404


# ----------------------------------------------------------
# RESPONSE SCHEMA VALIDATION
# ----------------------------------------------------------

@pytest.mark.api
def test_post_response_has_required_fields(api_session, base_url):
    """Verify the response shape matches expected contract."""
    response = api_session.get(f"{base_url}/posts/1")
    data = response.json()

    required_fields = {"userId", "id", "title", "body"}
    assert required_fields.issubset(data.keys()), \
        f"Missing fields: {required_fields - data.keys()}"


@pytest.mark.api
def test_post_id_is_integer(api_session, base_url):
    data = api_session.get(f"{base_url}/posts/1").json()
    assert isinstance(data["id"], int)


@pytest.mark.api
def test_post_title_is_non_empty_string(api_session, base_url):
    data = api_session.get(f"{base_url}/posts/1").json()
    assert isinstance(data["title"], str)
    assert len(data["title"]) > 0


# ----------------------------------------------------------
# COLLECTION ENDPOINT CHECKS
# ----------------------------------------------------------

@pytest.mark.api
def test_posts_collection_returns_list(api_session, base_url):
    data = api_session.get(f"{base_url}/posts").json()
    assert isinstance(data, list)


@pytest.mark.api
def test_posts_collection_has_100_items(api_session, base_url):
    """jsonplaceholder always returns exactly 100 posts."""
    data = api_session.get(f"{base_url}/posts").json()
    assert len(data) == 100


# ----------------------------------------------------------
# POST (CREATE) REQUEST
# ----------------------------------------------------------

@pytest.mark.api
def test_create_post_returns_201(api_session, base_url, fresh_payload):
    """
    fresh_payload fixture from conftest.py provides clean data.
    jsonplaceholder accepts POSTs and echoes back with a fake id.
    """
    response = api_session.post(f"{base_url}/posts", json=fresh_payload)
    assert response.status_code == 201


@pytest.mark.api
def test_create_post_returns_id(api_session, base_url, fresh_payload):
    response = api_session.post(f"{base_url}/posts", json=fresh_payload)
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)


# ----------------------------------------------------------
# PARAMETRIZED API TEST
# ----------------------------------------------------------

@pytest.mark.api
@pytest.mark.parametrize("post_id,expected_status", [
    (1,     200),
    (50,    200),
    (100,   200),
    (101,   404),
    (9999,  404),
], ids=["first", "middle", "last", "just_over", "way_over"])
def test_post_ids_boundary(api_session, base_url, post_id, expected_status):
    """Boundary test: valid IDs 1-100, anything above = 404."""
    response = api_session.get(f"{base_url}/posts/{post_id}")
    assert response.status_code == expected_status


# ----------------------------------------------------------
# RESPONSE TIME CHECK (non-functional)
# ----------------------------------------------------------

@pytest.mark.api
def test_response_time_under_2_seconds(api_session, base_url):
    """Basic performance assertion -- flag if API is slow."""
    import time
    start = time.time()
    api_session.get(f"{base_url}/posts/1")
    elapsed = time.time() - start
    assert elapsed < 2.0, f"Response took {elapsed:.2f}s -- too slow"
