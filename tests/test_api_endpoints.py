import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


# ===================== exchange =====================

@pytest.mark.django_db
def test_usd_to_currency_success(api_client):
    response = api_client.get("/api/exchange/usd-to/KRW/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_usd_to_currency_invalid_method(api_client):
    response = api_client.post("/api/exchange/usd-to/KRW/", data={})
    assert response.status_code in (400, 405)


@pytest.mark.django_db
def test_exchange_history_success(api_client):
    response = api_client.get("/api/exchange/history/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_exchange_history_invalid_method(api_client):
    response = api_client.post("/api/exchange/history/", data={})
    assert response.status_code in (400, 405)


# ===================== meta =====================

@pytest.mark.django_db
def test_country_list_success(api_client):
    response = api_client.get("/api/meta/countries/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_country_list_invalid_method(api_client):
    response = api_client.post("/api/meta/countries/", data={})
    assert response.status_code in (400, 405)


@pytest.mark.django_db
def test_country_detail_success(api_client):
    response = api_client.get("/api/meta/countries/US/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_country_detail_invalid_method(api_client):
    response = api_client.post("/api/meta/countries/US/", data={})
    assert response.status_code in (400, 405)


# ===================== simulation =====================

@pytest.mark.django_db
def test_compare_dca_vs_deposit_success(api_client):
    response = api_client.post(
        "/api/simulation/compare/dca-vs-deposit/",
        data={},
        format="json",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_compare_dca_vs_deposit_invalid_method(api_client):
    response = api_client.get("/api/simulation/compare/dca-vs-deposit/")
    assert response.status_code in (400, 405)


@pytest.mark.django_db
def test_compare_dca_vs_deposit_invalid_payload(api_client):
    response = api_client.post(
        "/api/simulation/compare/dca-vs-deposit/",
        data={"invalid": "payload"},
        format="json",
    )
    assert response.status_code == 400


# ===================== accounts =====================

@pytest.mark.django_db
def test_account_me_success(api_client):
    response = api_client.get("/api/account/me/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_account_me_invalid_method(api_client):
    response = api_client.post("/api/account/me/", data={}, format="json")
    assert response.status_code in (400, 405)


@pytest.mark.django_db
def test_my_exchange_rate_success(api_client):
    response = api_client.get("/api/account/me/exchange-rate/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_my_exchange_rate_invalid_method(api_client):
    response = api_client.post("/api/account/me/exchange-rate/", data={}, format="json")
    assert response.status_code in (400, 405)


# ===================== authentication =====================

@pytest.mark.django_db
def test_login_success(api_client):
    response = api_client.post("/api/auth/login/", data={}, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_invalid_method(api_client):
    response = api_client.get("/api/auth/login/")
    assert response.status_code in (400, 405)


@pytest.mark.django_db
def test_login_invalid_payload(api_client):
    response = api_client.post(
        "/api/auth/login/",
        data={"invalid": "payload"},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_google_login_success(api_client):
    response = api_client.get("/api/auth/google/login/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_google_login_invalid_method(api_client):
    response = api_client.post("/api/auth/google/login/", data={})
    assert response.status_code in (400, 405)


@pytest.mark.django_db
def test_google_callback_success(api_client):
    response = api_client.get("/api/auth/google/callback/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_google_callback_invalid_method(api_client):
    response = api_client.post("/api/auth/google/callback/", data={})
    assert response.status_code in (400, 405)


@pytest.mark.django_db
def test_logout_success(api_client):
    response = api_client.post("/api/auth/logout/", data={}, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_invalid_method(api_client):
    response = api_client.get("/api/auth/logout/")
    assert response.status_code in (400, 405)


@pytest.mark.django_db
def test_logout_invalid_payload(api_client):
    response = api_client.post(
        "/api/auth/logout/",
        data={"invalid": "payload"},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_signup_success(api_client):
    response = api_client.post("/api/auth/signup/", data={}, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_invalid_method(api_client):
    response = api_client.get("/api/auth/signup/")
    assert response.status_code in (400, 405)


@pytest.mark.django_db
def test_signup_invalid_payload(api_client):
    response = api_client.post(
        "/api/auth/signup/",
        data={"invalid": "payload"},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_refresh_success(api_client):
    response = api_client.post("/api/auth/refresh/", data={}, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_refresh_invalid_method(api_client):
    response = api_client.get("/api/auth/refresh/")
    assert response.status_code in (400, 405)


@pytest.mark.django_db
def test_refresh_invalid_payload(api_client):
    response = api_client.post(
        "/api/auth/refresh/",
        data={"invalid": "payload"},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_auth_me_success(api_client):
    response = api_client.get("/api/auth/me/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_auth_me_invalid_method(api_client):
    response = api_client.post("/api/auth/me/", data={}, format="json")
    assert response.status_code in (400, 405)