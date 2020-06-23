from marshmallow import Schema, fields, validate, validates, ValidationError
from .models import Author, Tag


# for working with Author object
class AuthorSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=64))
    surname = fields.String(required=True, validate=validate.Length(min=2, max=128))


# for working with Author in the Post object
class AuthorSchemaPost(Schema):
    id = fields.String(required=True)
    name = fields.String(dump_only=True)
    surname = fields.String(dump_only=True)


# for working with the Tag object
class TagSchema(Schema):
    id = fields.String(dump_only=True)
    tag = fields.String(required=True, validate=validate.Length(min=2, max=64))


# for working with Tags in the Post object
class TagSchemaPost(Schema):
    id = fields.String(required=False)
    tag = fields.String(dump_only=True)


class PostSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=2, max=64))
    body = fields.String(required=True, validate=validate.Length(min=2, max=4096))
    author = fields.Nested(AuthorSchemaPost, required=True)
    tag = fields.List(fields.Nested(TagSchemaPost), required=False)

    @validates('author')
    def validate_author(self, author_obj):
        if Author.objects(id=author_obj['id']):
            return author_obj
        else:
            raise ValidationError(message="Author doesn't exist")

    @validates('tag')
    def validate_tag(self, tags_obj):
        for tag in tags_obj:
            if tag.get('id'):
                # validates if id exists in the db
                if not Tag.objects.get(id=tag['id']):
                    raise ValidationError(message="Tag doesn't exist")
        return tags_obj
