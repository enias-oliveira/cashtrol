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
def group_data(client):

    return{
        "name": "AP da galera"
    }
@fixture
def group_data(client):

    return{
        "name": "AP da galera"
    }


def test_list_with_no_groups(client):

    response = client.get('/api/groups')

    assert response.json == None

def test_create_group(client, group_data):   

    client.post('/api/groups/', json=group_data)

    response = client.get('/api/groups/')

    assert len(response.json) == 1

def test_list_groups(client, group_data):   

    response = client.get('/api/groups/')    

    assert response.status_code == 200

# def test_update_groups(client, group_data):   

#     response = client.get('/api/groups/')    

#     assert response.status_code == 200




# def test_authenticated(client):
#     # Fazer login
#     response = client.post("/api/login", json=creadenicais)
#     token = response.json['token']

#     client.get('/api/products', header={Baerer:token})
