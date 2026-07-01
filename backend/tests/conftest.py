import pytest
from app import create_app
from app.extensions import db
from app.models.farm import Farm
from app.models.reproduction_record import ReproductionRecord

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session

@pytest.fixture
def test_farm(app):
    farm = Farm(name='Test Farm')
    db.session.add(farm)
    db.session.commit()
    return farm