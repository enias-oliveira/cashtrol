from flask import Flask
from flask_login import LoginManager
from app.users.model import UserModel
from flask_jwt_extended import JWTManager


def init_app(app: Flask):
    login_manager = LoginManager(app)
    JWTManager(app)
    login_manager.login_view = 'users.login'

    @login_manager.user_loader
    def user_loader(user_id):
        return UserModel.query.get(user_id)
