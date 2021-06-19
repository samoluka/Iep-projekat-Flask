from email.utils import parseaddr

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from configuration import Configuration
from decorators import roleCheck
app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


@app.route('/', methods=["POST"])
@roleCheck('admin')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, port=5001)
