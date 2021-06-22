from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class ElectionParticipants(database.Model):
    __tablename__ = "electionparticipants"

    id = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    idelection = database.Column(database.Integer, database.ForeignKey("elections.idelection"), nullable=False)
    idparticipant = database.Column(database.Integer, database.ForeignKey("participants.idparticipant"), nullable=False)


class Participant(database.Model):
    __tablename__ = "participants"

    idparticipant = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = database.Column(database.String(256), nullable=False)
    individual = database.Column(database.Boolean, nullable=False)
    elections = database.relationship("Election", secondary=ElectionParticipants.__table__, back_populates="participants")

    def __repr__(self):
        return "({}, {}, {})".format(self.idparticipant, self.name, self.individual)

    def serializeFull(self):
        return {
            'id': self.idparticipant,
            'name': self.name,
            'individual': self.individual,
        }

    def serialize(self):
        return {
            'id': self.idparticipant,
            'name': self.name,
        }


class Election(database.Model):
    __tablename__ = "elections"

    idelection = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    start = database.Column(database.DATETIME, nullable=False)
    end = database.Column(database.DATETIME, nullable=False)
    individual = database.Column(database.Boolean, nullable=False)
    participants = database.relationship("Participant", secondary=ElectionParticipants.__table__, back_populates="elections")
    votes = database.relationship("Vote")

    def serialize(self):
        return {
            'id': self.idelection,
            'start': self.start.strftime('%Y-%m-%d %H:%M:%S'),
            'end': self.end.strftime('%Y-%m-%d %H:%M:%S'),
            'individual': self.individual,
            'participants': [p.serialize() for p in self.participants]
        }

    def serializeParticipant(self, pollnumber, name, result, votes):
        return {
            "pollNumber": pollnumber,
            "name": name,
            "result": result,
            "votes": votes
        }

    def participantsResults(self):
        if (not self.individual):
            return self.participantsResultsParlament()
        return self.participantsResultsPresident()

    def participantsResultsParlament(self):
        votes = self.votes
        okVotes = [v for v in votes if v.valid == True]
        results = []
        for p in self.participants:
            results.append([p.name, 0, -1, 0])
        for vote in okVotes:
            results[vote.pollnumber - 1][1] += 1
        ret = []
        index = 1;
        mandats = 240
        map = {}
        while (mandats > 0):
            div = []
            index = 0
            max = -1
            maxInd = 0
            for r in results:
                if (r[1] > (0.05 * len(votes))):
                    r[2] = r[1] / (1 + r[3])
                    if (r[2] > max):
                        max = r[2]
                        maxInd = index
                index += 1
            results[maxInd][3] += 1
            mandats -= 1
        index = 1
        for result in results:
            ret.append(self.serializeParticipant(index, result[0], result[3], result[1]))
            index += 1
        return ret

    def participantsResultsPresident(self):
        votes = self.votes
        okVotes = [v for v in votes if v.valid == True]
        results = []
        for p in self.participants:
            results.append([p.name, 0])
        for vote in okVotes:
            results[vote.pollnumber - 1][1] += 1
        ret = []
        index = 1
        for result in results:
            ret.append(self.serializeParticipant(index, result[0], "{:.2f}".format(result[1] / len(votes)), result[1]))
            index += 1
        return ret

    def invalidVotes(self):
        votes = self.votes
        invalidVotes = [v for v in votes if v.valid == False]
        ret = []
        for vote in invalidVotes:
            ret.append(vote.serializeInvalid())
        return ret


class Vote(database.Model):
    __tablename__ = "votes"

    idvote = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    guid = database.Column(database.String(256), nullable=False)
    pollnumber = database.Column(database.Integer, nullable=False)
    electionofficialjmbg = database.Column(database.String(14), nullable=False)
    election = database.Column(database.Integer, database.ForeignKey('elections.idelection'))

    valid = database.Column(database.Boolean, nullable=False)
    reason = database.Column(database.String(256), nullable=True)

    def __repr__(self):
        return "({}, {}, {})".format(self.guid, self.pollnumber)

    def serializeInvalid(self):
        return {
            "electionOfficialJmbg": self.electionofficialjmbg,
            "ballotGuid": self.guid,
            "pollNumber": self.pollnumber,
            "reason": self.reason
        }
