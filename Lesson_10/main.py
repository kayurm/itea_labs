from flask import Flask
from flask_restful import Api
from application.resources import PostResource, TagResource, AuthorResource, PostsByTagResource

app = Flask(__name__)
api = Api(app)

api.add_resource(PostResource, '/post', '/post/<string:id>')
api.add_resource(AuthorResource, '/author', '/author/<string:id>')
api.add_resource(TagResource, '/tag', '/tag/<string:id>')
api.add_resource(PostsByTagResource, '/posts_by_tag/<string:id>')

if __name__ == "__main__":
    app.run(debug=True)
