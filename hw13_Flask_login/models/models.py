from app import db
from flask_login import UserMixin
from datetime import datetime


class Post(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    text = db.Column(db.String(1000), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.now)
    autor = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='posts', cascade='all, delete')


class Comment(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.now)
    autor = db.Column(db.Integer, db.ForeignKey('users.id'))
    post = db.Column(db.Integer, db.ForeignKey('posts.post_id', ondelete='CASCADE'))




class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)

    # @property
    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "email": self.email,
    #         "first_name": self.first_name,
    #         "last_name": self.last_name
    #     }


