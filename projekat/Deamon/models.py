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
            'start': self.start.strftime('%Y-%m-%d'),
            'end': self.end.strftime('%Y-%m-%d'),
            'individual': self.individual,
            'participants': [p.serialize() for p in self.participants]
        }


class Vote(database.Model):
    __tablename__ = "votes"

    idvote = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    guid = database.Column(database.String(256), nullable=False)
    pollnumber = database.Column(database.Integer, nullable=False)
    election = database.Column(database.Integer, database.ForeignKey('elections.idelection'))

    valid = database.Column(database.Boolean, nullable=False)
    reason = database.Column(database.String(256), nullable=True)


    def __repr__(self):
        return "({}, {}, {})".format(self.guid, self.pollnumber)
