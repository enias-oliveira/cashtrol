from _pytest.compat import ascii_escaped
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

# @fixture
# def app():
#     return create_app()

# @fixture
# def db(app):
#     from app.configurations.database import db

#     with app.app_context():
#         db.create_all()
#         yield db
#         db.drop_all()
#         db.session.commit()


# @fixture
# def client(app,db):
#     return app.text_client()

# @fixture
# def user_data():

#     return{
# 	"name" : "Fulano Rodrigues",
# 	"email" : "fulano@email.com",
# 	"password" : "EuSouFulano123"
#     }

# def test_list_with_no_users(client)

#     response = client.get('/api/users')

#     assert response.json == []

# def test_create_user(client, user_data)

#     client.post('/api/useres', json=user_data)

#     response = client.get( '/api/users')

#     assert len(response.json) == 1


# def test_authenticated(client):
#     # Fazer login
#     response = client.post("/api/login", json=**creadenicais)
#     token = response.json['token']

#     client.get('/api/products', header={Baerer:token})
