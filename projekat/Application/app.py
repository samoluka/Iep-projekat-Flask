import csv
from datetime import datetime, date
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


@app.route("/getResults", methods=["GET"])
@jwt_required("admin")
def getResults():
    id = request.args.get("id")
    if (not id):
        return jsonify(message="Field id is missing."), 400
    election = Election.query.filter(Election.idelection == id).first()
    if (not election):
        return jsonify(message="Election does not exist."), 400
    today = datetime.today()
    # if (election.end > today):
    #     return jsonify(message="Election is ongoing."), 400
    participantsResults = election.participantsResults()
    invalidVotes = election.invalidVotes()
    return jsonify(participants=participantsResults, invalidVotes=invalidVotes);


#  Dohvatanje rezultata izbora
# Adresa /getResults?id=<ELECTION_ID>
# Vrednost <ELECTION_ID> je ceo broj koji predstavlja identifikator izbora.
# Tip GET
# Zaglavlja Zaglavlja i njihov sadržaj su:
# {
# "Authorization": "Bearer <ACCESS_TOKEN>"
# }
# Vrednost <ACCESS_TOKEN> je string koji predstavlja JSON veb token za pristup
# koji je izdat administratoru prilikom prijave.
# Telo -
# Odgovor Ukoliko su sva tražena zaglavlja prisutna i ispunjavaju navedena ograničenja, rezultat
# zahteva je odgovor sa statusnim kodom 200 čiji je sadržaj JSON objekat sledećeg
# formata:
# {
# "participants": [
#  {
#  "pollNumber": 1,
#  "name": ".....",
#  "result": 1
#  },
#  ......
# ],
# "invalidVotes": [
#  {
#  "electionOfficialJmbg": "....",
#  "ballotGuid": "....",
#  "pollNumber": 1,
#  "reason": "....."
#  },
#  .....
# ]
# }
# Polje participants predstavlja niz JSON objekata koji se odnose na učesnike na
# datim izborima. Svaki objekat sadrži sledeća polja:  pollNumber: ceo broj koji predstavlja redni broj učesnika na glasačkom
# listuću;
#  name: string koji predstavlja ime učesnika;
#  result: ceo broj ili realan broj koji predstavlja rezultat učesnika na datim
# izborima;
# Polje invalidVotes predstavlja niz JSON objekata koji se odnose na glasove koji
# nisu važeći. Svaki objekat sadrži sledeća polja:
#  electionOfficialJmbg: string koji predstavlja JMBG zvaničnika koji je
# zabeležio glas;
#  ballotGuid: string koji predstavlja jedinstveni globalni identifikator (GUID)
# glasačkog listića;
#  pollNumber: ceo broj koji predstavlja redni broj na glasačkom listiću koji je
# odabran;
#  reason: string koji predstavlja razlog zbog kojeg je glas odbijen;
# Rezultat parlamentarnih izbora se računa pomoću D’ontovog sistema raspodele
# mandata i u tom slučaju vrednost polja result je ceo broj koji predstavlja broj
# mandata koji osvojila odgovarajuća politička partija. Pretpostaviti da postoji 250
# mandata za narodne poslanike i je cenzus 5%.
# Rezultat predsedničkih izbora se računa kao odnos broja glasova koje je dobio
# učesnik i ukupnog broja glasova i u tom slučaju vrednost polja result je realan broj
# iz opsega [0, 1] zaokružen na dve decimale koji predstavlja procenat glasova koji je
# osvojio odgovarajući pojedinac.
# U slučaju da zaglavlje nedostaje, rezultat je odgovor sa statusnim kodom 401 i JSON
# objektom sledećeg formata i sadržaja:
# {
# "msg": "Missing Authorization Header"
# }
# U slučaju da neko polje tela nedostaje, rezultat zahteva je odgovor sa statusnim
# kodom 400 i JSON objektom sledećeg formata:
# {
# "message": "....."
# }
# Sadržaj polja message je:
#  “Field id is missing.” ukoliko polje id nije prisutno;
#  “Election does not exist.” ukoliko navedeni id ne predstavlja validni
# identifikator izbora;
#  “Election is ongoing.” ukoliko izbori nisu završeni;
# Odgovarajuće provere se vrše u navedenom redosledu.
if __name__ == '__main__':
    database.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=5001)
