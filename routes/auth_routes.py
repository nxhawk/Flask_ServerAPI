from flask import Blueprint, jsonify, request
from models.users import User
from middleware.authen import check_password, bcrypt_password, create_token, token_required
import json

auth_routes = Blueprint('auth_routes', __name__, url_prefix='/api')


@auth_routes.route('/home', methods=['GET'])
def home_api():
    return jsonify({
        'message': "Hello guy!"
    })


@auth_routes.route('/signup', methods=["POST"])
def sign_up():
    try:
        payload = request.json
        username = payload.get('username')
        email = payload.get('email')
        password = bcrypt_password(payload.get('password'))
        if not username or not email or not password:
            return jsonify({
                'message': "hmmm...."
            })
        new_user = User(
            username=username,
            email=email,
            password=password
        )
        new_user.save()
        return jsonify({
            'token': create_token({
                'username': payload.get('username'),
                'email': payload.get('email')
            }),
            'message': 'signed successfully!!!'
        })
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'some thing wrong!'
        })


@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        payload = request.json
        username = payload.get('username')
        password = payload.get('password')
        user = User.objects.get(username=username)
        if not check_password(password, user['password']):
            raise Exception('Password wrong!')

        return jsonify({
            'token': create_token({
                'username': username,
                'email': user['email']
            }),
            'message': 'ok login'
        })
    except:
        return jsonify({
            'message': 'dont have account'
        })


@auth_routes.route('/profile', methods=["GET"])
@token_required
def profile(*args, **kwargs):
    user = kwargs.get('user_info')
    user_profile = json.loads(user.to_json())
    del user_profile['_id']
    del user_profile['password']
    return jsonify({
        'data': user_profile
    })
