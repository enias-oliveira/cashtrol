from environs import Env

env = Env()
env.read_env()

db_username = env.str("DB_USERNAME")
db_password = env.str("DB_PASSWORD")
db_host = env.str("DB_HOST")
db_uri = f"postgresql://{db_username}:{db_password}@{db_host}:5432/"


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = env.str("SECRET_KEY")
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    db_name_dev = env.str("DB_NAME_DEV")
    SQLALCHEMY_DATABASE_URI = f"{db_uri}{db_name_dev}"


class TestConfig(Config):
    db_name_test = env.str("DB_NAME_TEST")
    SQLALCHEMY_DATABASE_URI = f"{db_uri}{db_name_test}"
    TESTING = True


config_selector = {"development": DevelopmentConfig, "test": TestConfig}
