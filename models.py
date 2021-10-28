from typing import cast
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil.relativedelta import relativedelta
db = SQLAlchemy()


class CastModel(db.Model):
    def __init__(self) -> None:
        super().__init__()

    def insert(self):
        db.session.add(self)
        self.apply()

    def update(self):
        self.apply()

    def delete(self):
        db.session.delete(self)
        self.apply()

    def apply(self):
        db.session.commit()

    def refresh(self):
        db.session.refresh(self)

    def rollback(self):
        db.session.rollback()

    def dispose(self):
        db.session.close()


class Movie(CastModel):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False, unique=True)
    release_date = db.Column(db.DateTime, nullable=False)
    castings = db.relationship('Casting', backref='movie', lazy=True)

    def __init__(self, title, release_date) -> None:
        super().__init__()
        self.title = title
        self.release_date = release_date

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Actor(CastModel):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey(
        'gender.id'), nullable=False)
    castings = db.relationship('Casting', backref='actor', lazy=True)

    def __init__(self, name, dob, gender_id) -> None:
        super().__init__()
        self.name = name
        self.dob = dob
        self.gender_id = gender_id

    def age(self):
        now = datetime.now()
        today = now.date()
        age = relativedelta(self.dob, today).years
        return age

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'dob': self.dob,
            'age': self.age(),
            'gender': self.gender_id
        }


class Gender(CastModel):
    __tablename__ = 'gender'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    actors = db.relationship('Actor', backref='gender', lazy=True)

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def format(self):
        return{
            'id': self.id,
            'name': self.name
        }


class Casting(CastModel):
    __tablename__ = 'casting'
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    casting_date = db.Column(db.DateTime, nullable=False)
    recast_yn = db.Column(db.Boolean, nullable=False)
    db.UniqueConstraint(actor_id, movie_id, casting_date,
                        name='UX_actor_movie_date')

    def __init__(self, actor_id, movie_id, casting_date, recast_yn=False) -> None:
        super().__init__()
        self.actor_id = actor_id
        self.movie_id = movie_id
        self.casting_date = casting_date
        self.recast_yn = recast_yn

    def recast(self):
        if self.recast_yn:
            return 'Y'
        else:
            return 'N'

    def format(self):
        return{
            'id': self.id,
            'actor': self.actor.name,
            'movie': self.movie.name,
            'casting_date': self.casting_date,
            'recast_yn': self.recast_yn
        }
