from flask_restful import Resource
from .models import Author, Tag, Post, HandleDB
from flask import request
from .schemas import AuthorSchema, TagSchema, PostSchema
import json
from marshmallow import ValidationError


class PostResource(Resource):

    def get(self, id=None):
        if id:
            # when a specific post is requested, increase its views
            HandleDB().add_views(id)
            posts = Post.objects(id=id)
        else:
            posts = Post.objects.all()
        return PostSchema(many=True).dump(posts)

    def post(self):
        json_data = json.dumps(request.json)
        try:
            validated = PostSchema(many=True).loads(json_data)
            errors = validated._asdict().get('errors')
            if errors:
                return errors
            validated_data = validated._asdict().get('data')
            res = HandleDB().fill_post_collection(validated_data)
            return res
        except ValidationError as error:
            return error.messages

    def put(self, id):
        json_data = json.dumps(request.json)
        try:
            validated = PostSchema().loads(json_data)
            errors = validated._asdict().get('errors')
            if errors:
                return errors
            validated_data = validated._asdict().get('data')
            res = HandleDB().update_post_by_id(id, validated_data)
            return res
        except ValidationError as error:
            return error.messages

    def delete(self, id):
        try:
            res = HandleDB().delete_object_by_id(object_type="post", id_in=id)
        except ValidationError as error:
            res = error.messages
        return res


class AuthorResource(Resource):

    def get(self, id=None):
        if id:
            # when author is requested, return their posts
            posts = HandleDB().get_posts_by_author(author_id=id)
            return PostSchema(many=True).dump(posts)

        else:
            authors = Author.objects.all()
            return AuthorSchema(many=True).dump(authors)

    def post(self):
        json_data = json.dumps(request.json)
        try:
            validated = AuthorSchema(many=True).loads(json_data)
            errors = validated._asdict().get('errors')
            if errors:
                return errors
            validated_data = validated._asdict().get('data')
            res = HandleDB().fill_author_collection(validated_data)
            return res
        except ValidationError as error:
            return error.messages

    def put(self, id):
        json_data = json.dumps(request.json)
        try:
            validated = AuthorSchema().loads(json_data)
            errors = validated._asdict().get('errors')
            if errors:
                return errors
            validated_data = validated._asdict().get('data')
            res = HandleDB().update_author_by_id(id, validated_data)
            return res
        except ValidationError as error:
            return error.messages

    def delete(self, id):
        try:
            res = HandleDB().delete_object_by_id(object_type="author", id_in=id)
        except ValidationError as error:
            res = error.messages
        return res


class TagResource(Resource):

    def get(self, id=None):
        if id:
            tags = Tag.objects(id=id)
        else:
            tags = Tag.objects.all()
        return TagSchema(many=True).dump(tags)

    def post(self):
        json_data = json.dumps(request.json)
        try:
            validated = TagSchema(many=True).loads(json_data)
            errors = validated._asdict().get('errors')
            if errors:
                return errors
            validated_data = validated._asdict().get('data')
            res = HandleDB().fill_tag_collection(validated_data)
            return res
        except ValidationError as error:
            return error.messages

    def put(self, id):
        json_data = json.dumps(request.json)
        try:
            validated = TagSchema().loads(json_data)
            errors = validated._asdict().get('errors')
            if errors:
                return errors
            validated_data = validated._asdict().get('data')
            res = HandleDB().update_tag_by_id(id, validated_data)
            return res
        except ValidationError as error:
            return error.messages

    def delete(self, id):
        try:
            res = HandleDB().delete_object_by_id(object_type="tag", id_in=id)
        except ValidationError as error:
            res = error.messages
        return res


class PostsByTagResource(Resource):

    def get(self, id):
        matching_tag = Tag.objects.get(id=id)
        post = Post.objects(tag__in=[matching_tag])
        return PostSchema(many=True).dump(post)
