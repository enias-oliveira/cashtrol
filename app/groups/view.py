from flask import Blueprint


groups_bp = Blueprint("groups", __name__, url_prefix="/api/groups")


@groups_bp.route("/", methods=["GET"])
def hello_groups():
    return {"msg": "Hello groups"}
