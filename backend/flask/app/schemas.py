from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class TaskCreateSchema(Schema):
    title = fields.Str(required=True)
    prompt_body = fields.Str(required=True)
    description = fields.Str(load_default=None)
    is_reusable = fields.Bool(load_default=True)


class TaskUpdateSchema(TaskCreateSchema):
    pass


class ExecutionCreateSchema(Schema):
    task_id = fields.Int(required=True)
    input_payload = fields.Str(required=True)
    output_payload = fields.Str(required=True)
    meta = fields.Dict(load_default=None)


class RatingCreateSchema(Schema):
    execution_id = fields.Int(required=True)
    score = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(load_default=None)
