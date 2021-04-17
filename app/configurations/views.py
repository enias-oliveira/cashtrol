from flask import Flask

from app.users.view import users_bp


def init_app(app: Flask):
    app.register_blueprint(users_bp)
