from flask import Blueprint, request
from .services import get_invitation_code
from .model import GroupModel
from ..accounts.model import AccountModel
from ..configurations.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

groups_bp = Blueprint("groups", __name__, url_prefix="/api/groups")

@groups_bp.route("/", methods=["GET"])
def hello_groups():
    return {"msg": "Hello groups"}

@groups_bp.route("/members", methods=["POST"])
@jwt_required()
def adding_new_member_to_group():    
    data = request.get_json()

    jwt_id = get_jwt_identity()

    code = get_invitation_code(data)
    table_group = db.session.query(GroupModel)
    group = table_group.filter(GroupModel.access_code == code).first()

    if not group:
        return {"error": "Group not found."}

    if group.is_member(jwt_id):
        return {"error": "User already in group."}

    new_account = AccountModel(group_id=group.id, user_id=jwt_id)
    db.session.add(new_account)

    db.session.commit()

    return {
        "id": group.id,
        "name": group.name,
        "invite_code": group.access_code,
        "members": [user.id for user in group.members_list]
    }