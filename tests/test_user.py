from os import name
from app.users.model import UserModel
from app.app import create_app
import app
from pytest import fixture

# from  app.app import create_app
# from  app.users.model import UserModel

# @fixture()
# def test_app(scope="module"):
#     app = create_app()
#     app.app_context().push()
#     app.db.create_all()

#     yield app

#     app.db.session.remove()
#     app.db.drop_all()

# @fixture(scope="module")
# def test_client(test_app):
#     return test_app.test_client()

# def test_standard_user_create(test_client)

#     user_bory{

#     }


# Exemplo Guilherme

@fixture
def app():
    return create_app()

@fixture
def db(app):
    from app.configurations.database import db

    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()


@fixture
def user_data():

    return{
	"name" : "Fulano Rodrigues",
	"email" : "fulano@email.com",
	"password" : "EuSouFulano123"
    }

def create_users(db, user_data):

    user = UserModel(name=user_data['name'])

    db.session.add(user)
    db.session.commit()

    expected_name = "Fulano Rodrigues"
    actual = UserModel.query.get(1)

    assert actual.name == expected_name





    