from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)

    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80),
        error_messages={"required": "Username is required."}
    )

    # Nested workouts
    workouts = fields.List(
        fields.Nested(lambda: __import__('server.schemas.workout_schema', fromlist=[
                      'WorkoutSchema']).WorkoutSchema(exclude=("user",)))
    )

    class Meta:
        unknown = "exclude"
