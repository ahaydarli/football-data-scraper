from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(140))
    leagues = db.relationship('Leagues')

    def __repr__(self):
        return '<Country {}>'.format(self.name)


class Leagues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'))
    country = db.relationship('Country')
    years = db.relationship('Year')
    name = db.Column(db.String(140))

    def __repr__(self):
        return '<League {}>'.format(self.name)


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'))
    league_id = db.Column(db.Integer, db.ForeignKey('leagues.league_id'))
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))
    league = db.relationship('Leagues')
    country = db.relationship('Country')
    name = db.Column(db.String(255))
    code = db.Column(db.String(100))
    url = db.Column(db.String(200))

    def __repr__(self):
        return '<Club {}>'.format(self.name)


class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey('leagues.league_id'))
    url = db.Column(db.String(200))
    name = db.Column(db.String(100))
    code = db.Column(db.String(50))
    weeks = db.relationship('Week')

    def __repr__(self):
        return '<Year {}>'.format(self.name)


class Week(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))
    name = db.Column(db.String(100))
    url = db.Column(db.String(100))
    year = db.relationship('Year')

    def __repr__(self):
        return '<Year {}'.format(self.name)


class WeekClubs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    code = db.Column(db.String(100))
    url = db.Column(db.String(200))
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))
    position = db.Column(db.Integer)
    game = db.Column(db.Integer)
    win = db.Column(db.Integer)
    draw = db.Column(db.Integer)
    lost = db.Column(db.Integer)
    f = db.Column(db.Integer)
    a = db.Column(db.Integer)
    home_win = db.Column(db.Integer)
    home_draw = db.Column(db.Integer)
    home_lost = db.Column(db.Integer)
    home_f = db.Column(db.Integer)
    home_a = db.Column(db.Integer)
    home_pound = db.Column(db.Integer)
    away_win = db.Column(db.Integer)
    away_draw = db.Column(db.Integer)
    away_lost = db.Column(db.Integer)
    away_f = db.Column(db.Integer)
    away_a = db.Column(db.Integer)
    away_pound = db.Column(db.Integer)
    pound = db.Column(db.Integer)
    week_id = db.Column(db.Integer, db.ForeignKey('week.id'))

    def __repr__(self):
        return '<Club {}>'.format(self.name)

