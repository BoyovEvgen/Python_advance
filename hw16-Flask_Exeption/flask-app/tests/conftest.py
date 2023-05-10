
import pytest
from app import app, db, Category


@pytest.fixture(scope="session")
def test_app():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

        insert_test_category()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def client(test_app):
    with test_app.test_client() as client:
        yield client


def insert_test_category():
    category1 = Category(name="Test1", slug="test1")
    category2 = Category(name="Test2", slug="test2")
    db.session.add_all([category1, category2])
    db.session.commit()
