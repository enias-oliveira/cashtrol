from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello_flask():
        return {"msg": "Hello Flask!"}, 200

    return app
