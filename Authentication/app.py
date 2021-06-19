from email.utils import parseaddr

from flask import Flask, request, Response, jsonify
from configuration import Configuration
from models import database, User
from sqlalchemy import or_
from formatChecker import FormatChecker

app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/proba', methods=["GET"])
def proba():
    svi = User.query.all()
    return str(svi)


@app.route('/register', methods=["POST"])
def registration():
    jmbg = request.json.get("jmbg", "");
    password = request.json.get("password", "");
    forename = request.json.get("forename", "");
    surname = request.json.get("surname", "");
    email = request.json.get("email", "");

    # provera uslova
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
        return Response("Email already exists.", status=400);

    user = User(jmbg=jmbg, forename=forename, surname=surname, email=email, password=password)
    database.session.add(user)
    database.session.commit()

    return Response(status=200);


if __name__ == '__main__':
    database.init_app(app)
    app.run(debug=True, port=5000)
