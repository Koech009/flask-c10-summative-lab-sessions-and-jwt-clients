from extensions import db
from datetime import date
# Workout model representing a workout session


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    duration = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    # Foreign key to associate workout with a user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Relationship to access the user who created the workout
    user = db.relationship("User", back_populates="workouts")

    def __repr__(self):
        return f"<Workout {self.title} on {self.date} for {self.duration} mins>"
