import csv
from datetime import datetime
import io

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import or_, and_

from configuration import Configuration
from decorators import roleCheck
from models import database, Participant, Election

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


@app.route('/createParticipant', methods=["POST"])
@roleCheck('admin')
def createParticipant():
    name = request.json.get("name", "")
    individual = request.json.get("individual", "")

    if (name == "" or individual == ""):
        ret = ""
        if (name == ""):
            ret += "Field name is missing. "
        if (individual == ""):
            ret += "Field individual is missing. "
        ret = ret[:-1]
        return jsonify(message=ret), 400

    participant = Participant(name=name, individual=individual)
    database.session.add(participant)
    database.session.commit()
    database.session.refresh(participant)

    return jsonify(id=participant.idparticipant), 200


@app.route('/getParticipants', methods=["GET"])
@roleCheck('admin')
def getParticipants():
    return jsonify(participants=[p.serializeFull() for p in Participant.query.all()]), 200


@app.route('/createElection', methods=["POST"])
@roleCheck('admin')
def createElection():
    start = request.json.get("start", "")
    end = request.json.get("end", "")
    individual = request.json.get("individual", "")
    participantsKey = request.json.get("participants", "")

    if (start == "" or end == "" or individual == "" or participantsKey == ""):
        ret = ""
        if (start == ""):
            ret += "Field start is missing. "
        if (end == ""):
            ret += "Field end is missing. "
        if (individual == ""):
            ret += "Field individual is missing. "
        if (participantsKey == ""):
            ret += "Field participants is missing. "
        ret = ret[:-1]
        return jsonify(message=ret), 400

    def is_date(string):
        try:
            datetime.strptime(string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    if (not is_date(start) or not is_date(end) or start > end):
        return jsonify(message="Invalid date and time."), 400

    if (Election.query.filter(or_(
            or_(Election.start.between(start, end), Election.end.between(start, end)),
            and_(Election.start <= start, Election.end >= end)))
            .first()):
        return jsonify(message="Invalid date and time."), 400

    participants = Participant.query.filter(Participant.idparticipant.in_(participantsKey)).all()

    if (len(participants) < 2):
        return jsonify(message="Invalid participant."), 400
    if (len(participants) != len(participantsKey)):
        return jsonify(message="Invalid participant."), 400
    if (len([p for p in participants if p.individual != individual]) > 0):
        return jsonify(message="Invalid participant."), 400

    election = Election(start=start, end=end, individual=individual, participants=participants)
    database.session.add(election)
    database.session.commit()

    pollNumbers = list(range(1, len(participants) + 1))

    return jsonify(pollNumbers=pollNumbers), 200


@app.route('/getElections', methods=["GET"])
@roleCheck('admin')
def getElections():
    return jsonify(elections=[e.serialize() for e in Election.query.all()]), 200

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    database.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=5000)
