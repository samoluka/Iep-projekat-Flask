from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy();


class User(database.Model):
    __tablename__ = "users";

    iduser = database.Column(database.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True);
    jmbg = database.Column(database.String(14), nullable=False, unique=True);
    forename = database.Column(database.String(256), nullable=False);
    surname = database.Column(database.String(256), nullable=False);
    email = database.Column(database.String(256), nullable=False, unique=True);
    password = database.Column(database.String(256), nullable=False);

    def __repr__(self):
        return "({}, {}, {})".format(self.email, self.forename, self.surname)
