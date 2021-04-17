from flask import Flask


def create_app():
    app = Flask(__name__)

    from app import configurations, routes
    from app.configurations import database, migration

    configurations.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    routes.init_app(app)

    @app.route("/")
    def hello_flask():
        return {"msg": "Hello Flask!"}, 200

    return app
