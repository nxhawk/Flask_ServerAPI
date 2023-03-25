import os
from flask import Flask
from dotenv import load_dotenv
from mongoengine import connect
import logging
from flask_cors import CORS

from routes.auth_routes import auth_routes
from routes.post_routes import post_routes

load_dotenv('.env')

MONGODB_URL = os.getenv("MONGODB_URL")
PORT = os.getenv("PORT")

connect(host=MONGODB_URL)
logging.warning(MONGODB_URL)

server_api = Flask(__name__)

server_api.register_blueprint(auth_routes)
server_api.register_blueprint(post_routes)

CORS(server_api)

if __name__ == "__main__":
    server_api.run(host='0.0.0.0', port=PORT, debug=True)
