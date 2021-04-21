from _pytest.compat import ascii_escaped
from flask import Flask
from app.app import create_app
import app
from pytest import fixture

@fixture
def app():
    return create_app()

@fixture
def db(app):
    from app.configurations.database import db
    # from ..app.configurations.database import db

    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()


@fixture
def client(app,db):
    return app.test_client()

@fixture
def user_data(client):

    return{
	"name" : "Fulano Rodrigues",
	"email" : "fulano@email.com",
	"password" : "EuSouFulano123"
    }

@fixture
def login_user(client):
    
    return {   
    "email" : "fulano@email.com",
	"password" : "EuSouFulano123"

}

@fixture
def user_updated(client):
    
    return {   
    "email" : "fulano@email.com",
	"password" : "EuSouFulano123"

}

@fixture
def user_deleted(client):
    
    return {   
    "email" : "fulano@email.com",
	"password" : "EuSouFulano123"

}



def test_list_with_no_users(client):

    response = client.get('/api/users')

    assert response.json == None

# def test_list_with_users(cliente):

#     response = client.get('/api/users')

#     assert response.status_code == 308


def test_create_user(client, user_data):

    client.post('/api/users/', json=user_data)

    response = client.get('/api/users/')

    assert len(response.json) == 1

# def test_login_user(client, login_user):

#     response = client.post('/api/login/',json=login_user)

#     assert response.status_code == 200

# def test_update_user(client, user_update):

#     response = client.path(/api/users/profile)


# def test_delete_user(client, ):

#     response = client.delete('/api/user/id',json=delete_user)

#     assert response.status_code == 200




# def test_authenticated(client):
#     # Fazer login
#     response = client.post("/api/login", json=creadenicais)
#     token = response.json['token']

#     client.get('/api/products', header={Baerer:token})
