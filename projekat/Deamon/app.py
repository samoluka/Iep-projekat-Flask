import threading
from datetime import date

from flask import Flask, Response
from redis import Redis
from sqlalchemy import and_

from models import Election, Vote, database
from configuration import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)


def deamon(id):
    with Redis(Configuration.REDIS_HOST) as redis:
        sub = redis.pubsub()
        sub.subscribe(Configuration.REDIS_SUBSCRIBE_CHANNEL)
        for item in sub.listen():
            bytes = redis.lpop(Configuration.REDIS_VOTES_KEY)
            while (bytes):
                print("stiglo")
                voteString = bytes.decode("utf-8").split(",")
                today = date.today()
                election = Election.query.filter(and_(Election.start <= today, Election.end >= today)).first()
                if (not election):
                    print("no election")
                    continue
                voteDuplicated = Vote.query.filter(Vote.guid == voteString[0]).first()
                validDuplciated = False if voteDuplicated else True
                validPollNumber = False if int(voteString[1]) > len(election.participants) else True
                valid = validDuplciated and validPollNumber
                vote = Vote(guid=voteString[0], pollnumber=int(voteString[1]), election=election.idelection, valid=valid, electionofficialjmbg=voteString[2])
                if (not validPollNumber):
                    vote.reason = "Invalid poll number."
                if (not validDuplciated):
                    vote.reason = "Duplicate ballot."
                database.session.add(vote)
                database.session.commit()
                print('poslao')
                bytes = redis.lpop(Configuration.REDIS_VOTES_KEY)


@app.route("/startDeamon")
def start():
    deamon(1)
    return Response("", status=200)


if __name__ == '__main__':
    database.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5004)
