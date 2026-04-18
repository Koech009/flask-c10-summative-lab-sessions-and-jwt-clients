def test_register_and_login(client):
    res = client.post("/signup", json={
        "username": "tester",
        "password": "password123",
        "password_confirmation": "password123"
    })
    assert res.status_code == 201
    assert res.json["user"]["username"] == "tester"

    res = client.post("/login", json={
        "username": "tester",
        "password": "password123"
    })
    assert res.status_code == 200
    assert "token" in res.json


def test_me_requires_jwt(client):
    res = client.get("/me")
    assert res.status_code == 401
