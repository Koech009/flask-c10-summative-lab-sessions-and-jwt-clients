from sqlalchemy.ext.hybrid import hybrid_property
from extensions import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    workouts = db.relationship(
        "Workout",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # block direct access
    @hybrid_property
    def password(self):
        raise AttributeError("Password is not readable")

    # hash password on assignment
    @password.setter
    def password(self, value):
        self.password_hash = bcrypt.generate_password_hash(
            value).decode("utf-8")

    # check password
    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
