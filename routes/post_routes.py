from datetime import datetime
import json
from flask import Blueprint, jsonify, request

from models.posts import Post
from middleware.authen import token_required
from models.users import User

post_routes = Blueprint("post_routes", __name__, url_prefix='/api/v1')


@post_routes.route('/posts', methods=['GET'])
@token_required
def get_Posts(*args, **kwargs):
    user = kwargs['user_info']
    data = [
        {
            'id': str(post['id']),
            'post_name': post['post_name'],
            'description': post['description'],
            'link_image': post['link_image'],
            'created_time': datetime.timestamp(post['created_time']),
            'updated_time':datetime.timestamp(post['updated_time'])
        }
        for post in user['posts']
    ] if len(user['posts']) > 0 else []
    return jsonify({
        'Posts': data,
        'length': len(data)
    })


@post_routes.route('/newpost', methods=['POST'])
@token_required
def add_newPost(*args, **kwargs):
    payload = request.json
    post_name = payload.get('post_name')
    description = payload.get('description')
    user = kwargs['user_info']
    try:
        new_Post = Post(
            post_name=post_name,
            description=description
        )
        new_Post.save()
        saved_Post = Post.objects.get(id=new_Post.id)
        User.objects(id=user['id']).update_one(push__posts=saved_Post)

        return jsonify({
            "message": "new post ok!"
        })
    except Exception as e:
        print(e)
        return jsonify({
            'message': "some thing wrong"
        })


@post_routes.route('posts/<string:id_post>', methods=['DELETE'])
@token_required
def delete_post(id_post, *args, **kwargs):
    user = kwargs['user_info']
    deleted_post = None
    try:
        for post in user['posts']:
            if str(post.id) == id_post:
                deleted_post = post
                break
        if not deleted_post:
            return jsonify({
                'message': 'Not found post'
            }), 403
        User.objects(id=user['id']).update_one(pull__posts=deleted_post)
        Post.objects(id=id_post).delete()
        return jsonify({
            'message': "Delete post successfully"
        })
    except:
        return jsonify({
            'message': 'Delete post error!'
        })
