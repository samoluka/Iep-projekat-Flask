import datetime
import os
import threading
import time
from datetime import datetime

from redis import Redis
from sqlalchemy import and_, orm

from models import Election, Vote, engine
from configuration import Configuration


def deamon():
    while (1):
        try:
            with Redis(Configuration.REDIS_HOST) as redis:
                sub = redis.pubsub()
                sub.subscribe(Configuration.REDIS_SUBSCRIBE_CHANNEL)
                for item in sub.listen():
                    print('primio Poruku')
                    bytes = redis.lpop(Configuration.REDIS_VOTES_KEY)
                    while (bytes):
                        print('primio')
                        voteString = bytes.decode("utf-8").split(",")
                        today = datetime.today()
                        session = orm.scoped_session(orm.sessionmaker())(bind=engine)
                        election = session.query(Election).filter(and_(Election.start <= today, Election.end >= today)).first()
                        if (not election):
                            print(today.strftime('%Y-%m-%d %H:%M:%S'))
                            print("no election")
                            continue
                        voteDuplicated = session.query(Vote).filter(Vote.guid == voteString[0]).first()
                        validDuplciated = False if voteDuplicated else True
                        validPollNumber = False if int(voteString[1]) > len(election.participants) else True
                        valid = validDuplciated and validPollNumber
                        vote = Vote(guid=voteString[0], pollnumber=int(voteString[1]), election=election.idelection, valid=valid, electionofficialjmbg=voteString[2])
                        if (not validPollNumber):
                            vote.reason = "Invalid poll number."
                        if (not validDuplciated):
                            vote.reason = "Duplicate ballot."
                        session.add(vote)
                        session.commit()
                        print('sacuvao')
                        bytes = redis.lpop(Configuration.REDIS_VOTES_KEY)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    os.environ['TZ'] = 'Europe/Belgrade'
    time.tzset()
    threading.Thread(target=deamon, args=()).start()
