from marshmallow import Schema, fields, validate, ValidationError, validates_schema


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    title = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=120),
        error_messages={"required": "Workout title is required."}
    )

    date = fields.Date(
        required=True,
        error_messages={"required": "Workout date is required."}
    )

    duration = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=300),
        error_messages={"invalid": "Duration must be a number."}
    )

    notes = fields.Str(validate=validate.Length(max=500))

    # Nested user (lazy reference, no direct import)
    user = fields.Nested(lambda: UserSchema(exclude=("workouts",)))

    @validates_schema
    def validate_duration_logic(self, data, **kwargs):
        if data.get("duration") and data["duration"] > 180:
            raise ValidationError(
                "Workout duration seems too long (max 180 mins recommended)."
            )
