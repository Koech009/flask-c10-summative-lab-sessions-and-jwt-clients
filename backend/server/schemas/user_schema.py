from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)

    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80),
        error_messages={"required": "Username is required."}
    )

    # Nested workouts (lazy reference, no direct import)
    workouts = fields.List(
        fields.Nested(lambda: WorkoutSchema(exclude=("user",)))
    )

    class Meta:
        unknown = "exclude"  # Ignore extra fields from input
