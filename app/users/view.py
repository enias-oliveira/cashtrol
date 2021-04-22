from flask import Blueprint, render_template, request, current_app
from app.users.model import UserModel
from http import HTTPStatus
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/", methods=["GET"])
def hello_users():
    return {"msg": "Hello Users"}


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

    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    new_user = UserModel(name=name, email=email)
    new_user.password = password

    session.add(new_user)
    session.commit()

    access_token = create_access_token(
        identity=new_user.id, expires_delta=timedelta(days=7)
    )

    return {"user": {'access_token': access_token, 'id': new_user.id, 'email': email, }}, HTTPStatus.CREATED
