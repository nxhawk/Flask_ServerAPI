from flask import request, jsonify
from datetime import datetime, timedelta
from functools import wraps
import bcrypt
import jwt
from models.users import User
from os import environ
from dotenv import load_dotenv
load_dotenv('.env')

TIME_EXPIRE = 150
SECRET_JWT = environ.get("SECRET_JWT")


def token_required(f):
    @wraps(f)
    def __checking_token(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': "token missing!", "status": False}), 401
        try:
            data = jwt.decode(token, SECRET_JWT, algorithms=['HS256'])
            user = User.objects.get(
                username=data['username'],
                email=data['email']
            )
            if not user:
                raise Exception('username or email not found')
            kwargs['user_info'] = user
        except:
            return jsonify({
                'message': 'Check JWT token error !!',
                "status": False
            }), 401
        return f(*args, **kwargs)

    return __checking_token


def create_token(payload_arg):
    return jwt.encode(
        payload={
            **payload_arg,
            'exp': datetime.utcnow() + timedelta(days=TIME_EXPIRE),
            'iat': datetime.utcnow()
        },
        key=SECRET_JWT,
        algorithm="HS256"
    )


def bcrypt_password(password):
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')


def check_password(pwd_input, pwd_bcrypt):
    return bcrypt.checkpw(
        pwd_input.encode('utf-8'),
        pwd_bcrypt.encode('utf-8')
    )
