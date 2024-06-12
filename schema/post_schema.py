from marshmallow import Schema, fields
from .user_schema import UserSchema


class TagSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class PostSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    user = fields.Nested(UserSchema, dump_only=True)
    tags = fields.List(fields.Nested(TagSchema), dump_only=True)


class PostRequestSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    tags = fields.List(fields.Str(), required=False)
