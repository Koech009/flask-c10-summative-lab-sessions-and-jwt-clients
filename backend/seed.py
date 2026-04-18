from faker import Faker
import random
from app import create_app
from extensions import db
from server.models.user import User
from server.models.workout import Workout
from datetime import date

fake = Faker()
app = create_app()

with app.app_context():
    # RESET DATABASE
    db.drop_all()
    db.create_all()

    # SEED SPECIFIC USERS
    specific_users = [
        {"username": "george", "password": "password123"},
        {"username": "ian12", "password": "password123"},
    ]

    named_users = []
    for u in specific_users:
        user = User(username=u["username"])
        user.password = u["password"]
        db.session.add(user)
        named_users.append(user)

    # SEED FAKE USERS
    fake_users = []
    for _ in range(20):
        user = User(username=fake.user_name())
        user.password = "password123"
        db.session.add(user)
        fake_users.append(user)

    db.session.commit()

    # SEED WORKOUTS FOR ALL USERS
    all_users = named_users + fake_users
    workout_titles = ["Morning Run", "Pushups", "Situps",
                      "Squats", "Cycling", "Yoga", "Swimming"]

    for user in all_users:
        for _ in range(3):
            workout = Workout(
                title=random.choice(workout_titles),
                date=fake.date_this_year(),
                duration=random.randint(10, 90),
                notes=fake.sentence(),
                user_id=user.id
            )
            db.session.add(workout)

    db.session.commit()
    print("Database seeded with fake users and workouts")
    print("Specific users: george / ian12 — password: password123")
