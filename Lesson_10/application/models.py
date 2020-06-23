import mongoengine as me
from datetime import datetime

me.connect("posts")


class Author(me.Document):
    name = me.StringField(min_length=2, max_length=64)
    surname = me.StringField(min_length=2, max_length=128)
    publications = me.IntField(default=0)


class Tag(me.Document):
    tag = me.StringField(min_length=2, max_length=64, unique=True)


class Post(me.Document):
    title = me.StringField(min_length=2, max_length=64)
    body = me.StringField(min_length=2, max_length=4096)
    date = me.DateTimeField(default=datetime.now())
    author = me.ReferenceField(Author)
    tag = me.ListField(me.ReferenceField(Tag, required=False), required=False)
    views = me.IntField(default=0)


class HandleDB:

    # 'POST' object methods
    def prepare_tag_list_for_post_obj(self, post_obj):
        if post_obj['tag']:
            tags = post_obj['tag']
            tag_objects = list()
            for tag in tags:
                tag_obj = Tag.objects.get(id=tag['id'])
                tag_objects.append(tag_obj)
            return tag_objects
        else:
            return None

    def fill_post_collection(self, posts_list):
        for record in posts_list:
            try:
                author_id = record['author']['id']
                tag_objects = self.prepare_tag_list_for_post_obj(record)
                if tag_objects:
                    Post.objects.create(title=record['title'], body=record['body'], author=Author(id=author_id),
                                        tag=tag_objects)
                else:
                    Post.objects.create(title=record['title'], body=record['body'], author=Author(id=author_id), tag=[])
            except (KeyError, ValueError, me.ValidationError) as err:
                return str(err)
        return posts_list

    def update_post_by_id(self, id_in, post_data):
        try:
            record = Post.objects.get(id=id_in)
            author_id = post_data['author']['id']
            tag_objects = self.prepare_tag_list_for_post_obj(post_data)
            if tag_objects:
                record.update(title=record['title'], body=record['body'], author=Author(id=author_id),
                              tag=tag_objects)
            else:
                record.update(title=record['title'], body=record['body'], author=Author(id=author_id), tag=[])
        except (KeyError, ValueError, me.ValidationError) as err:
            return str(err)
        return post_data

    def add_views(self, id_in):
        post = Post.objects.get(id=id_in)
        views = post.views + 1
        post.update(views=views)

    def get_posts_by_author(self, author_id):
        author = Author.objects.get(id=author_id)
        posts = Post.objects(author__in=[author])
        return posts

    # AUTHOR methods
    def fill_author_collection(self, authors_list):
        for record in authors_list:
            try:
                Author.objects.create(name=record['name'], surname=record['surname'])
            except me.ValidationError as err:
                return str(err)
        return authors_list

    def update_author_by_id(self, id_in, author_data):
        try:
            record = Author.objects(id=id_in)
            record.update(name=author_data['name'], surname=author_data['surname'])
        except me.ValidationError as err:
            return str(err)
        return author_data

    # TAG methods
    def fill_tag_collection(self, tags_list):
        for record in tags_list:
            try:
                Tag.objects.create(tag=record['tag'])
            except me.ValidationError as err:
                return str(err)
        return tags_list

    def update_tag_by_id(self, id_in, tag_data):
        try:
            record = Tag.objects(id=id_in)
            record.update(tag=tag_data['tag'])
        except me.ValidationError as err:
            return str(err)
        return tag_data

    # delete method is common for all objects
    def delete_object_by_id(self, object_type, id_in):
        if object_type == 'tag':
            obj = Tag
        elif object_type == 'author':
            obj = Author
        elif object_type == 'post':
            obj = Post
        else:
            raise ValueError("object_type must be one of: tag/author/post")
        try:
            res = obj.objects(id=id_in).delete()
            if not res:
                return "no such id in the database"
        except me.ValidationError as err:
            return str(err)
        return "successfully deleted"

