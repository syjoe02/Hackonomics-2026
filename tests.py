import uuid

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer testtoken")
    return client


def assert_json_response(response, expected_status=200):
    assert response.status_code == expected_status
    assert response["Content-Type"].startswith("application/json")


# ===================== exchange =====================


@pytest.mark.django_db
def test_usd_to_currency_success(api_client):
    response = api_client.get("/api/exchange/usd-to/KRW/")
    assert_json_response(response, 200)


@pytest.mark.django_db
def test_usd_to_currency_invalid_method(api_client):
    response = api_client.post("/api/exchange/usd-to/KRW/", data={})
    assert response.status_code == 405


@pytest.mark.django_db
def test_exchange_history_success(api_client):
    response = api_client.get("/api/exchange/history/")
    assert_json_response(response, 200)


@pytest.mark.django_db
def test_exchange_history_invalid_method(api_client):
    response = api_client.post("/api/exchange/history/", data={})
    assert response.status_code == 405


# ===================== meta =====================


@pytest.mark.django_db
def test_country_list_success(api_client):
    response = api_client.get("/api/meta/countries/")
    assert_json_response(response, 200)


@pytest.mark.django_db
def test_country_list_invalid_method(api_client):
    response = api_client.post("/api/meta/countries/", data={})
    assert response.status_code == 405


@pytest.mark.django_db
def test_country_detail_success(api_client):
    response = api_client.get("/api/meta/countries/US/")
    assert_json_response(response, 200)


@pytest.mark.django_db
def test_country_detail_invalid_method(api_client):
    response = api_client.post("/api/meta/countries/US/", data={})
    assert response.status_code == 405


# ===================== simulation =====================


@pytest.mark.django_db
def test_compare_dca_vs_deposit_success(api_client):
    payload = {"amount": 1000}
    response = api_client.post(
        "/api/simulation/compare/dca-vs-deposit/",
        data=payload,
        format="json",
    )
    assert_json_response(response, 200)


@pytest.mark.django_db
def test_compare_dca_vs_deposit_empty_payload(api_client):
    response = api_client.post(
        "/api/simulation/compare/dca-vs-deposit/",
        data={},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_compare_dca_vs_deposit_invalid_method(api_client):
    response = api_client.get("/api/simulation/compare/dca-vs-deposit/")
    assert response.status_code == 405


# ===================== accounts =====================


@pytest.mark.django_db
def test_account_me_success(api_client):
    response = api_client.get("/api/account/me/")
    assert_json_response(response, 200)


@pytest.mark.django_db
def test_account_me_invalid_method(api_client):
    response = api_client.post("/api/account/me/", data={}, format="json")
    assert response.status_code == 405


@pytest.mark.django_db
def test_my_exchange_rate_success(api_client):
    response = api_client.get("/api/account/me/exchange-rate/")
    assert_json_response(response, 200)


@pytest.mark.django_db
def test_my_exchange_rate_invalid_method(api_client):
    response = api_client.post(
        "/api/account/me/exchange-rate/",
        data={},
        format="json",
    )
    assert response.status_code == 405


# ===================== user_calendar =====================


@pytest.mark.django_db
def test_calendar_init_empty_payload(api_client):
    response = api_client.post("/api/calendar/init/", data={}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_calendar_oauth_login_success(api_client):
    response = api_client.get("/api/calendar/oauth/login/")
    assert_json_response(response, 200)


@pytest.mark.django_db
def test_calendar_categories_delete_success(api_client):
    category_id = uuid.uuid4()
    response = api_client.delete(f"/api/calendar/categories/{category_id}/")
    assert response.status_code in (200, 404)


@pytest.mark.django_db
def test_calendar_event_delete_success(api_client):
    event_id = uuid.uuid4()
    response = api_client.delete(f"/api/calendar/events/{event_id}/")
    assert response.status_code in (200, 404)


@pytest.mark.django_db
def test_calendar_advisor_empty_payload(api_client):
    response = api_client.post(
        "/api/calendar/advisor/",
        data={},
        format="json",
    )
    assert response.status_code == 400


# ===================== authentication =====================


@pytest.mark.django_db
def test_login_empty_payload(api_client):
    response = api_client.post(
        "/api/auth/login/",
        data={},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_invalid_method(api_client):
    response = api_client.get("/api/auth/login/")
    assert response.status_code == 405


@pytest.mark.django_db
def test_google_login_success(api_client):
    response = api_client.get("/api/auth/google/login/")
    assert_json_response(response, 200)


@pytest.mark.django_db
def test_logout_empty_payload(api_client):
    response = api_client.post(
        "/api/auth/logout/",
        data={},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_signup_empty_payload(api_client):
    response = api_client.post(
        "/api/auth/signup/",
        data={},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_refresh_empty_payload(api_client):
    response = api_client.post(
        "/api/auth/refresh/",
        data={},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_auth_me_success(api_client):
    response = api_client.get("/api/auth/me/")
    assert_json_response(response, 200)
