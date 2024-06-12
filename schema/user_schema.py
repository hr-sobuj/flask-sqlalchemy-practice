from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    profile = fields.Nested('ProfileSchema', dump_only=True)

class ProfileSchema(Schema):
    bio = fields.Str()

class CreateUserRequestSchema(Schema):
    name = fields.Str(required=True)
    bio = fields.Str()
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class CreateUserResponseSchema(Schema):
    message = fields.Str()
    user = fields.Nested(UserSchema)


class LoginRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class LoginResponseSchema(Schema):
    message = fields.Str(dump_only=True)
    token = fields.Str(dump_only=True)
