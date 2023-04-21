from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:pass@localhost:5433/postgres_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "sadasdsdssadsadsadsadsadssaddas"

db.init_app(app)
manager = LoginManager(app)

with app.app_context():
    from routes import *
    # from models import User
    # db.create_all()
    migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)