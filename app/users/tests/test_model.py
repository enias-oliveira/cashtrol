from app.users.tests.test_view import user_deleted
from os import name
from app.users.model import UserModel
from app.app import create_app
import app
from pytest import fixture

@fixture
def app():
    return create_app()

@fixture
def db(app):
    from app.configurations.database import db

    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        # db.session.commit()
        db.drop_all()


@fixture
def user_data():

    return{
	"name":"Fulano Rodrigues",
	"email":"fulano@email.com",
	"password_hash":"EuSouFulano123"
    }

def test_create_users(db, user_data):

    user = UserModel(name=user_data['name'], email=user_data['email'], password_hash=user_data['password_hash'])

    db.session.add(user)    
    db.session.commit()

    expected_name = "Fulano Rodrigues"
    actual = UserModel.query.get(1)

    assert actual.name == expected_name

def test_delete_users(db, user_data):
    user = UserModel(name=user_data['name'], email=user_data['email'], password_hash=user_data['password_hash'])
    print("user",user)
    db.session.add(user)
    db.session.commit()

    # user_deleted = db.select([users]).where(users.column.id == 1)
    table = db.session.query(UserModel)
    user_deleted =  table.filter(UserModel.id == 1).first()
    print("deleted",user_deleted)
    db.session.delete(user)
    db.session.commit()

    expected_name = None
    
    actual = table.filter(UserModel.id == 1).first()

    assert actual == expected_name

def test_update_users(db, user_data):
    user = UserModel(name=user_data['name'], email=user_data['email'], password_hash=user_data['password_hash'])
    print("user",user)
    db.session.add(user)
    db.session.commit()

    # user_deleted = db.select([users]).where(users.column.id == 1)
    table = db.session.query(UserModel)
    user_updated =  table.filter(UserModel.id == 1).first()
    user_updated.name = "Adilson"

    db.session.add(user_updated)  
     
    user_atual = table.filter(UserModel.name == "Adilson").first().name
    
    print("updated",user_deleted)
    db.session.commit()

    expected_name = "Adilson"
    
    actual = user_atual

    assert actual == expected_name


# def test_select_users(db, user_data):
#     user = UserModel(name=user_data['name'], email=user_data['email'], password_hash=user_data['password_hash'])
#     print("user",user)
#     db.session.add(user)
#     db.session.commit()

#     table = db.session.query(UserModel)
#     users = table.filter(UserModel).all()


#     print("All users",users)
#     # db.session.commit()

#     expected_name = "Adilson"
    
#     actual = user_atual

#     assert actual == expected_name

