from tests.conftest import client


def test_no_contact_post():
    response = client.post("/write_data", json={"phone_number": "", "address": ""})
    assert response.status_code == 422


def test_missing_contact_post():
    response = client.post(
        "/write_data", json={"phone_number": "+7 (111) 111 11-11", "address": ""}
    )
    assert response.status_code == 422


def test_invalid_contact_post():
    response = client.post(
        "/write_data",
        json={
            "phone_number": "+7 (111) 111 11-11",
            "address": "улица Пушкина, д. 3",
            "name": "Bob",
        },
    )
    assert response.status_code == 422


def test_valid_contact_post():
    response = client.post(
        "/write_data",
        params={
            "phone_number": "+7 (111) 111 11-11",
            "address": "улица Пушкина, д. 3",
        },
    )
    assert response.status_code == 201


def test_missing_phone_get():
    response = client.get("/check_data", params={"phone_number": ""})
    assert response.status_code == 404


def test_no_contact_get():
    response = client.get("/check_data", params={"phone_number": "123456"})
    assert response.status_code == 404


def test_valid_contact_get():
    response = client.get("/check_data", params={"phone_number": "+7 (111) 111 11-11"})
    assert response.status_code == 200


def test_no_contact_patch():
    response = client.patch("/write_data", json={"phone_number": "", "address": ""})
    assert response.status_code == 422


def test_missing_contact_patch():
    response = client.patch(
        "/write_data", json={"phone_number": "+7 (111) 111 11-11", "address": ""}
    )
    assert response.status_code == 422


def test_valid_contact_patch():
    response = client.patch(
        "/write_data",
        params={"phone_number": "+7 (111) 111 11-11", "address": "улица Пушкина, д. 3"},
    )
    assert response.status_code == 202
