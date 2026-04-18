from datetime import date


def register_and_login(client):
    client.post("/signup",
                json={"username": "tester", "password": "pass", "password_confirmation": "pass"})
    res = client.post("/login",
                      json={"username": "tester", "password": "pass"})
    return res.json["token"]


def test_create_and_list_workouts(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create workout
    res = client.post("/api/workouts/", json={
        "title": "Pushups",
        "date": "2026-04-17",
        "duration": 30,
        "notes": "Morning routine"
    }, headers=headers)
    assert res.status_code == 201
    assert res.json["title"] == "Pushups"

    # List workouts
    res = client.get("/api/workouts/", headers=headers)
    assert res.status_code == 200
    assert len(res.json["workouts"]) == 1


def test_update_and_delete_workout(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create workout
    res = client.post("/api/workouts/", json={
        "title": "Situps",
        "date": "2026-04-17",
        "duration": 20
    }, headers=headers)
    workout_id = res.json["id"]

    # Update workout
    res = client.patch(
        f"/api/workouts/{workout_id}", json={"duration": 25}, headers=headers)
    assert res.status_code == 200
    assert res.json["duration"] == 25

    # Delete workout
    res = client.delete(f"/api/workouts/{workout_id}", headers=headers)
    assert res.status_code == 200
    assert res.json["msg"] == "Workout deleted"
