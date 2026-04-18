import pytest
from extensions import db
from server.models.user import User
from server.models.workout import Workout


@pytest.fixture
def session(app):
    return db.session


def test_user_password_hashing(session):
    user = User(username="tester")
    user.password = "password123"  # triggers bcrypt setter
    session.add(user)
    session.commit()

    assert user.password_hash is not None
    assert user.password_hash.startswith("$2b$")  # bcrypt hash prefix


def test_workout_creation(session):
    user = User(username="tester")
    user.password = "password123"
    session.add(user)
    session.commit()

    workout = Workout(
        title="Pushups",
        duration=30,
        notes="Morning routine",
        user_id=user.id
    )
    session.add(workout)
    session.commit()

    assert workout.id is not None
    assert workout.user_id == user.id
    assert workout.title == "Pushups"


def test_relationship_user_workouts(session):
    user = User(username="tester")
    user.password = "password123"
    session.add(user)
    session.commit()

    workout1 = Workout(title="Situps", duration=20, user_id=user.id)
    workout2 = Workout(title="Squats", duration=40, user_id=user.id)
    session.add_all([workout1, workout2])
    session.commit()

    workouts = Workout.query.filter_by(user_id=user.id).all()
    assert len(workouts) == 2
    assert {w.title for w in workouts} == {"Situps", "Squats"}
