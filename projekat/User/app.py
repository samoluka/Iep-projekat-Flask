import csv
from datetime import datetime
import io

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from redis import Redis

from decorators import roleCheck
from configuration import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
jwt = JWTManager(app)


# Funkcionalnosti kontejnera koji namenjen za rad sa zvaničnicima su date u nastavku.
#  Unošenje glasova
# Adresa /vote
# Tip POST
# Zaglavlja Zaglavlja i njihov sadržaj su: {
# "Authorization": "Bearer <ACCESS_TOKEN>"
# }
# Vrednost <ACCESS_TOKEN> je string koji predstavlja JSON veb token za pristup
# koji je izdat zvaničniku prilikom prijave.
# Telo U telu zahteva se nalazi polje sa nazivom file čija vrednost predstavlja CSV datoteku
# sa glasovima. Svaki red datoteke je sadrži sledeće vrednosti:
#  Jedinstveni globalni identifikator (GUID) glasačkog listića;
#  Redni broj učesnika na glasačkom listiću;
# Odgovor Ukoliko su svi podaci prisutni i ispunjavaju sva navedena ograničenja, glasovi se
# smeštaju na Redis servis i rezultat zahteva je odgovor sa statusnim kodom 200 bez
# dodatnog sadržaja.
# U slučaju da neko polje tela nedostaje, rezultat zahteva je odgovor sa statusnim
# kodom 400 i JSON objektom sledećeg formata:
# {
# "message": "....."
# }
# Sadržaj polja message je:
#  “Field file missing.” ukoliko polje nije prisutno u telu zahteva;
#  “Incorrect number of values on line 2.” ukoliko neka od linija u
# datoteci ne sadrži tačno dve vrednost, poruka treba da sadrži i broj linije koja
# ne zadovoljava uslov, numeracija linija kreće od 0;
#  “Incorrect poll number on line 2.” ukoliko neka od linija u datoteci
# ne sadrži odgovarajući redni broj, redni broj je ceo broj veći od 0, numeracija
# linija kreće od 0;
# Odgovarajuće provere se vrše u navedenom redosledu.
@app.route('/vote', methods=['POST'])
@roleCheck('user')
def vote():
    additionalClaims = get_jwt();
    try:
        content = request.files["file"].stream.read().decode("utf-8")
    except Exception:
        return jsonify(message="Field file missing."), 400
    stream = io.StringIO(content)
    reader = csv.reader(stream)
    votes = []
    index = 0
    for row in reader:
        if (len(row) != 2):
            return jsonify(message="Incorrect number of values on line {}.".format(index)), 400
        if (not row[1].isdecimal() or int(row[1]) <= 0):
            return jsonify(message="Incorrect poll number on line {}.".format(index)), 400
        votes.append((row[0], row[1]))
        index += 1
    done = False
    br = 0
    while (not done):
        try:
            with Redis(host=Configuration.REDIS_HOST) as redis:
                for vote in votes:
                    redis.lpush(Configuration.REDIS_VOTES_KEY, "{},{},{}".format(vote[0], vote[1], additionalClaims['jmbg']))
                    print('poslao')
                    br += 1
                redis.publish(Configuration.REDIS_SUBSCRIBE_CHANNEL, "poruka")
            done = True
        except Exception as e:
            print(e)
    return Response("", status=200)


@app.route('/')
def hello():
    return "hello", 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
