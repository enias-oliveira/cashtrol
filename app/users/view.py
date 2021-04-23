from flask import Blueprint, render_template, request, current_app
from app.users.model import UserModel
from http import HTTPStatus
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from app.transactions.model import TransactionType

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("", methods=["GET"])
@jwt_required()
def list_user_info():
    user_id = get_jwt_identity()
    user: UserModel = UserModel.query.get_or_404(user_id)

    groups = [
        {"group_name": group.name, "group_id": group.id} for group in user.groups_list
    ]

    return {"id": user_id, "email": user.email, "groups": groups}, HTTPStatus.OK


@users_bp.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    email = body.get("email")
    password = body.get("password")

    found_user: UserModel = UserModel.query.filter_by(email=email).first()

    if not found_user or not found_user.validate_password(password):
        return {"msg": "User not found"}, HTTPStatus.BAD_REQUEST

    access_token = create_access_token(
        identity=found_user.id, expires_delta=timedelta(days=7)
    )

    return {"access_token": access_token}, HTTPStatus.OK


@users_bp.route("/signup", methods=["POST"])
def signup():
    session = current_app.db.session

    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")

    new_user = UserModel(name=name, email=email)
    new_user.password = password

    session.add(new_user)
    session.commit()

    access_token = create_access_token(
        identity=new_user.id, expires_delta=timedelta(days=7)
    )

    return {
        "user": {
            "id": new_user.id,
            "email": new_user.email,
        }
    }, HTTPStatus.CREATED


@users_bp.route("/update", methods=["PATCH"])
@jwt_required()
def update():
    session = current_app.db.session
    table = session.query(UserModel)
    current_user_id = get_jwt_identity()
    user = table.filter(UserModel.id == current_user_id).first()

    if user:
        new_name = request.json.get("name")
        new_email = request.json.get("email")
        if request.json.get("name"):
            user.name = new_name

        if request.json.get("email"):
            user.email = new_email

        session.commit()

        return {
            "id": str(current_user_id),
            "name": user.name,
            "email": user.email,
        }, HTTPStatus.OK

    return {"Error": "User not found"}, HTTPStatus.NOT_FOUND


@users_bp.route("/transactions", methods=["GET"])
@jwt_required()
def list_user_transactions():
    user_id = get_jwt_identity()
    user: UserModel = UserModel.query.get_or_404(user_id)

    transactions = [
        {
            "id": transaction.id,
            "entry": {
                "entry_name": transaction.entry.name,
                "entry_id": transaction.entry_id,
            },
            "type": "CREDIT" if transaction.type == TransactionType.credit else "DEBIT",
            "created_at": transaction.entry.created_at,
            "group": {
                "group_id": transaction.entry.group.id,
                "group_name": transaction.entry.group.name,
            },
        }
        for transaction in user.transactions_list
    ]
    print(transactions)

    return {"transactions": transactions}, HTTPStatus.OK
