
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template_string, request, redirect, url_for, render_template


from forms import RegisterForm
from models import db, Users, Profiles


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:pass@localhost:5433/postgres_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
db.init_app(app)


@app.route("/")
def index():
    info = []
    try:
        info = Users.query.all()
    except:
        app.logger.debug("database read error")
    return render_template('index.html', list=info)


@app.route("/register", methods=("POST", "GET"))
def register():
    print(request.method)
    if request.method == "POST":
        # ще треба валідувати данні
        try:
            hash = generate_password_hash(request.form['password'])
            u = Users(email=request.form['email'], password=hash)
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['username'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            app.logger.debug("error adding to database")
        return redirect(url_for('index'))
    form = RegisterForm()
    return render_template("register.html", form=form)


if __name__ == "__main__":
    import logging
    app.logger.setLevel(logging.DEBUG)
    with app.app_context():
        db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True)