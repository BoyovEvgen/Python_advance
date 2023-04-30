import hashlib

import flask
import sqlalchemy.exc
from app import app, db
from flask import render_template, request, redirect, session, url_for
from models import User, Article


@app.route("/")
def hello_world():
    articles = Article.query.all()
    return render_template("index.html", articles=articles)


@app.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")


@app.route("/save-user", methods=["POST"])
def register():
    data = request.form
    password_hash = hashlib.sha256(data.get("password").encode("utf-8"))
    try:
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password=password_hash.hexdigest(),
        )
        db.session.add(user)
        db.session.commit()
        session["user"] = user.serialize
        return redirect("/")
    except sqlalchemy.exc.IntegrityError:
        flask.flash('User with this email is already registered')
        return redirect(url_for('sign_up'))



@app.route("/sign-in")
def sign_in():
    return render_template("sign-in.html")


@app.route("/authorize", methods=["POST"])
def authorize():
    data = request.form
    user = User.query.filter(User.email == data.get("email")).first()
    if user:
        if hashlib.sha256(data.get("password").encode("utf-8")).hexdigest() == user.password:
            session["user"] = user.serialize
        else:
            flask.flash('Wrong password')
            return redirect(url_for('sign_in'))
    else:
        flask.flash('User with this email is not registered')
        return redirect(url_for('sign_in'))
    return redirect("/")


@app.route("/logout")
def logout():
    del session["user"]
    return redirect("/")
