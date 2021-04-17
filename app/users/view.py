from flask import Blueprint


users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/", methods=["GET"])
def hello_users():
    return {"msg": "Hello Users"}
