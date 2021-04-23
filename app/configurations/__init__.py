from flask import Flask
from environs import Env
from config import config_selector


def init_app(app: Flask):
    env = Env()
    env.read_env()

    config = config_selector[env.str("FLASK_ENV")]
    app.config.from_object(config)
