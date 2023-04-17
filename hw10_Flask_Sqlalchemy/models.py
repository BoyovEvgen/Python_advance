from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class ReprMixin:
    def __repr__(self):
        d = {k: v for k, v in vars(self).items()
                if not k.startswith('_')}
        basic = super().__repr__()
        if not d:
            return basic
        basic, cut = basic[:-1], basic[-1]

        add = ', '.join([f'{k}={v!r}' for k, v in d.items()])

        res = f'{basic} ~ ({add}){cut}'
        return res


class Users(db.Model, ReprMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship('Profiles', backref='users', uselist=False)


class Profiles(db.Model, ReprMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))