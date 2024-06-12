from marshmallow import Schema, fields

class TagSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class PostSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    user_id = fields.Int(dump_only=True) 
    tags = fields.List(fields.Nested(TagSchema), dump_only=True)

class PostRequestSchema(Schema):
    username = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    tags = fields.List(fields.Str(), required=False)
