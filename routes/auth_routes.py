from flask import Blueprint, jsonify, request, render_template
from models.users import User
from middleware.authen import check_password, bcrypt_password, create_token, token_required
import json

auth_routes = Blueprint('auth_routes', __name__, url_prefix='/api')


@auth_routes.route('/home', methods=['GET'])
def home_api():
    return jsonify({
        'message': "Hello guy!"
    })


@auth_routes.route('/signup', methods=['GET'])
def signup_views():
    return render_template('signup.html', title="Register Page", fileJS="signup")


@auth_routes.route('/signup', methods=["POST"])
def sign_up():
    try:
        payload = request.json
        username = payload.get('username')
        email = payload.get('email')
        password = bcrypt_password(payload.get('password'))
        if not username or not email or not password:
            return jsonify({
                'message': "You must fill all",
                'status': False
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
            'message': 'Register successfully, Hello new user',
            "status": True
        })
    except Exception as e:
        if e.__class__.__name__ == "NotUniqueError":
            return jsonify({
                'message': 'Email or Username is already existed!',
                'status': False
            })
        return jsonify({
            'message': 'Some thing wrong! Try signup again',
            "status": False
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
            'message': 'Login successfully, Hello guy',
            "status": True
        })
    except:
        return jsonify({
            'message': 'Some thing wrong, try login again!',
            "status": False
        })


@auth_routes.route('/login', methods=['GET'])
def login_views():
    return render_template('login.html', title="Login Page", fileJS="login")


@auth_routes.route('/getprofile', methods=["GET"])
@token_required
def profile(*args, **kwargs):
    user = kwargs.get('user_info')
    user_profile = json.loads(user.to_json())
    del user_profile['_id']
    del user_profile['password']
    return jsonify({
        'message': user_profile,
        'status': True
    })


@auth_routes.route('/profile', methods=["GET"])
def profile_views():
    return render_template("profile.html")
