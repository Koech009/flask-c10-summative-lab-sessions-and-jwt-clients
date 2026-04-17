import pytest
from marshmallow import ValidationError
from server.schemas import WorkoutSchema, UserSchema


def test_valid_workout():
    schema = WorkoutSchema()
    data = {"title": "Morning Run", "date": "2026-04-17", "duration": 60}
    result = schema.load(data)
    assert result["title"] == "Morning Run"


def test_invalid_duration():
    schema = WorkoutSchema()
    data = {"title": "Ultra Marathon", "date": "2026-04-17", "duration": 200}
    with pytest.raises(ValidationError):
        schema.load(data)


def test_user_with_workouts():
    schema = UserSchema()
    data = {"username": "koech", "workouts": [
        {"title": "Gym", "date": "2026-04-17", "duration": 90}]}
    result = schema.load(data)
    assert result["username"] == "koech"
