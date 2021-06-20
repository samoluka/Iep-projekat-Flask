from email.utils import parseaddr

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from configuration import Configuration
from models import database, User
from sqlalchemy import or_, and_
from formatChecker import FormatChecker

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/proba', methods=["GET"])
def proba():
    svi = User.query.all()
    return str(svi)


@app.route('/register', methods=["POST"])
def register():
    jmbg = request.json.get("jmbg", "");
    password = request.json.get("password", "");
    forename = request.json.get("forename", "");
    surname = request.json.get("surname", "");
    email = request.json.get("email", "");

    formatChecker = FormatChecker(jmbg, email, forename, surname, password)
    ret = formatChecker.checkEmpty()
    if (ret != ""):
        return jsonify(message=ret), 400;
    ret = formatChecker.checkJmbg()
    if (ret != ""):
        return jsonify(message=ret), 400;
    ret = formatChecker.checkEmail()
    if (ret != ""):
        return jsonify(message=ret), 400;
    ret = formatChecker.checkPassword()
    if (ret != ""):
        return jsonify(message=ret), 400;

    user = User.query.filter(or_(User.jmbg == jmbg, User.email == email)).first()
    if (user):
        jsonify(message="Email already exists."), 400;

    user = User(jmbg=jmbg, forename=forename, surname=surname, email=email, password=password, role="user")
    database.session.add(user)
    database.session.commit()

    return Response(status=200);


@app.route('/login', methods=["POST"])
def login():
    password = request.json.get("password", "");
    email = request.json.get("email", "");

    formatChecker = FormatChecker("jmbg", email, "forename", "surname", password)
    ret = formatChecker.checkEmpty()
    if (ret != ""):
        return jsonify(message=ret), 400;
    ret = formatChecker.checkEmail()
    if (ret != ""):
        return jsonify(message=ret), 400;

    user = User.query.filter(and_(User.email == email, User.password == password)).first();
    if (not user):
        return jsonify(message="“Invalid credentials."), 400;

    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        "jmbg": user.jmbg,
        "role": user.role
    }
    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims);
    refreshToken = create_refresh_token(identity=user.email, additional_claims=additionalClaims);

    return jsonify(accessToken=accessToken, refreshToken=refreshToken);


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity();
    refreshClaims = get_jwt();

    additionalClaims = {
        "forename": refreshClaims["forename"],
        "surname": refreshClaims["surname"],
        "jmbg": refreshClaims["jmbg"],
        "role": refreshClaims["role"]
    };

    return jsonify(accessToken=create_access_token(identity=identity, additional_claims=additionalClaims)), 200


@app.route("/delete", methods=["POST"])
@jwt_required()
def delete():
    email = request.json.get("email", "");
    formatChecker = FormatChecker("jmbg", email, "forename", "surname", "password")
    ret = formatChecker.checkEmpty()
    if (ret != ""):
        return jsonify(message=ret), 400;
    ret = formatChecker.checkEmail()
    if (ret != ""):
        return jsonify(message=ret), 400;

    user = User.query.filter(User.email == email).first()
    if (not user):
        return jsonify(message="Unknown user."), 400;
    database.session.delete(user)
    database.session.commit()

    return Response(status=200);


if __name__ == '__main__':
    database.init_app(app)
    app.run(debug=True, port=5000)
