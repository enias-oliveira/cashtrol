from flask import Flask

from app.users.view import users_bp
from app.groups.view import groups_bp


def init_app(app: Flask):
    app.register_blueprint(users_bp)
    app.register_blueprint(groups_bp)
