from flask import Blueprint, request, current_app
from .services import get_invitation_code
from .model import GroupModel
from ..accounts.model import AccountModel
from ..configurations.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from http import HTTPStatus

groups_bp = Blueprint("groups", __name__, url_prefix="/api/groups")


@groups_bp.route("/", methods=["GET"])
def hello_groups():
    return {"msg": "Hello groups"}


@groups_bp.route("/create", methods=["POST"])
@jwt_required()
def create_group():
    session = current_app.db.session
    group_data = request.get_json()
    jwt_id = get_jwt_identity()

    group = GroupModel(name=group_data['name'],
                       access_code=group_data['access_code'],
                       created_by=jwt_id)
    print(adding_new_member_to_group(group_data['access_code']))
    session.add(group)
    session.commit()
    return {"msg": "Success"}, HTTPStatus.CREATED


@groups_bp.route("/members", methods=["POST"])
@jwt_required()
def adding_new_member_to_group(invite=None):
    data = request.get_json()

    jwt_id = get_jwt_identity()

    code = data['access_code']
    table_group = db.session.query(GroupModel)
    if code:
        group = table_group.filter(GroupModel.access_code == code).first()
    else:
        group = table_group.filter(GroupModel.access_code == invite).first()

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
