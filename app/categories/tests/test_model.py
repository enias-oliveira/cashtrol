from app.users.tests.test_view import user_deleted
from os import name
from app.users.model import UserModel
from app.groups.model import GroupModel
from app.categories.model import CategoryModel
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

@fixture
def group_data():

    return{
	"name":"Praia",
	"access_code":"abc123",
	"created_by":"1"
    }
@fixture
def category_data():

    return{
	"name":"Casa",
	
    }


def test_create_account(db, group_data, user_data, category_data):

    user = UserModel(name=user_data['name'], email=user_data['email'], password_hash=user_data['password_hash'])

    db.session.add(user)    
    db.session.commit()


    group = GroupModel(name=group_data['name'], access_code=group_data['access_code'], created_by=group_data['created_by'])
    db.session.add(group)  
    category = CategoryModel(name=category_data['name'])

    db.session.add(category)    
    db.session.commit()

    expected_name = "Casa"
    actual = CategoryModel.query.get(1)

    assert actual.name == expected_name


def test_delete_category(db, group_data, user_data, category_data):

    user = UserModel(name=user_data['name'], email=user_data['email'], password_hash=user_data['password_hash'])

    db.session.add(user)    
    db.session.commit()


    group = GroupModel(name=group_data['name'], access_code=group_data['access_code'], created_by=group_data['created_by'])
    db.session.add(group)  
    
    category = CategoryModel(name=category_data['name'])

    db.session.add(category)    
    db.session.commit()


def test_update_category(db, group_data, user_data, category_data):

    user = UserModel(name=user_data['name'], email=user_data['email'], password_hash=user_data['password_hash'])

    db.session.add(user)
    db.session.commit()  
    
    group = GroupModel(name=group_data['name'], access_code=group_data['access_code'], created_by=group_data['created_by'])

    db.session.add(group) 
    db.session.commit()

    category = CategoryModel(name=category_data['name'])
    db.session.add(category)  
    db.session.commit()

    table = db.session.query(CategoryModel)
    updated_category = table.filter(CategoryModel.id == 1).first()
    updated_category.name = "Bebidas"

    db.session.add(updated_category)
    db.session.commit()
    
    category_atual = table.filter(CategoryModel.name == "Bebidas").first().name

    expected_name = category_atual    

    actual = table.filter(CategoryModel.name == "Bebidas").first().name  
    assert actual == expected_name
