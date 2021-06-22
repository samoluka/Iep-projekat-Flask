from sqlalchemy import orm, Column, Integer, ForeignKey, String, Boolean, create_engine
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from configuration import Configuration

base = declarative_base()
engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URI)
base.metadata.bind = engine


# after this:
# base == db.Model
# session == db.session
# other db.* values are in sa.*
# ie: old: db.Column(db.Integer,db.ForeignKey('s.id'))
#     new: sa.Column(sa.Integer,sa.ForeignKey('s.id'))
# except relationship, and backref, those are in orm
# ie: orm.relationship, orm.backref
# so to define a simple model

class ElectionParticipants(base):
    __tablename__ = "electionparticipants"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    idelection = Column(Integer, ForeignKey("elections.idelection"), nullable=False)
    idparticipant = Column(Integer, ForeignKey("participants.idparticipant"), nullable=False)


class Participant(base):
    __tablename__ = "participants"

    idparticipant = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    individual = Column(Boolean, nullable=False)
    elections = relationship("Election", secondary=ElectionParticipants.__table__, back_populates="participants")

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


class Election(base):
    __tablename__ = "elections"

    idelection = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    start = Column(DATETIME, nullable=False)
    end = Column(DATETIME, nullable=False)
    individual = Column(Boolean, nullable=False)
    participants = relationship("Participant", secondary=ElectionParticipants.__table__, back_populates="elections")
    votes = relationship("Vote")

    def serialize(self):
        return {
            'id': self.idelection,
            'start': self.start.strftime('%Y-%m-%d'),
            'end': self.end.strftime('%Y-%m-%d'),
            'individual': self.individual,
            'participants': [p.serialize() for p in self.participants]
        }


class Vote(base):
    __tablename__ = "votes"

    idvote = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    guid = Column(String(256), nullable=False)
    pollnumber = Column(Integer, nullable=False)
    election = Column(Integer, ForeignKey('elections.idelection'))
    electionofficialjmbg = Column(String(14), nullable=False)
    valid = Column(Boolean, nullable=False)
    reason = Column(String(256), nullable=True)

    def __repr__(self):
        return "({}, {}, {})".format(self.guid, self.pollnumber)
