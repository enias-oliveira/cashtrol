from flask import Flask


def create_app():
    app = Flask(__name__)

    from app import configurations
    from app.configurations import database, migration, views, authentication

    configurations.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    authentication.init_app(app)
    views.init_app(app)

    @app.route("/")
    def hello_flask():
        return {"msg": "Hello Flask!"}, 200

    return app
