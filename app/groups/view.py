from flask import Blueprint, request, current_app
from app.journal.model import JournalModel
from .services import create_invitation_code
from .model import GroupModel
from ..accounts.model import AccountModel
from ..configurations.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

groups_bp = Blueprint("groups", __name__, url_prefix="/api/groups")


@groups_bp.route("/", methods=["GET"])
def hello_groups():
    return {"msg": "Hello groups"}


@groups_bp.route("", methods=["POST"])
@jwt_required()
def create_group():
    session = current_app.db.session
    group_data = request.get_json()
    jwt_id = get_jwt_identity()

    invite_code = create_invitation_code()

    group = GroupModel(
        name=group_data["name"],
        access_code=invite_code,
        created_by=jwt_id,
    )
    session.add(group)
    session.commit()

    creator_account = AccountModel(user_id=jwt_id, group_id=group.id)

    session.add(creator_account)
    session.commit()

    return {"invite_code": invite_code}, HTTPStatus.CREATED


@groups_bp.route("/members", methods=["POST"])
@jwt_required()
def adding_new_member_to_group(invite=None):
    data = request.get_json()

    jwt_id = get_jwt_identity()

    code = data["invite_code"]
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
        "members": [user.id for user in group.members_list],
    }


@groups_bp.route("/<int:group_id>/expenses", methods=["POST"])
@jwt_required()
def add_expense_to_group(group_id):
    data = request.get_json()
    group: GroupModel = GroupModel.query.get_or_404(group_id)

    expense: JournalModel = group.create_expense(
        name=data["name"],
        amount=data["amount"],
        description=data["description"],
        splitted=data["splitted"],
        created_by=get_jwt_identity(),
    )

    from ..transactions.services import transaction_serializer

    return transaction_serializer(expense), HTTPStatus.CREATED


@groups_bp.route("/<int:group_id>/payments", methods=["POST"])
@jwt_required()
def add_payment_to_group(group_id):
    data = request.get_json()
    group: GroupModel = GroupModel.query.get_or_404(group_id)

    payment = group.create_payment(
        sender_id=get_jwt_identity(), receiver_id=data["paid_to"], amount=data["amount"]
    )

    from ..transactions.services import transaction_serializer

    return transaction_serializer(payment["entry"]), HTTPStatus.CREATED


@groups_bp.route("/<int:group_id>/suggested_payments", methods=["GET"])
@jwt_required()
def list_suggested_payments(group_id):
    group: GroupModel = GroupModel.query.get_or_404(group_id)

    return group.suggested_payments(), HTTPStatus.OK
