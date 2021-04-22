from flask import Blueprint, request
from .services import get_invitation_code
from .model import GroupModel
from ..accounts.model import AccountModel
from ..configurations.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

groups_bp = Blueprint("groups", __name__, url_pre   fix="/api/groups")

@groups_bp.route("/", methods=["GET"])
def hello_groups():
    return {"msg": "Hello groups"}

@groups_bp.route("/members", methods=["POST"])
@jwt_required()
def adding_new_member_to_group():
    data = request.get_json()
    headers = request.headers['Authorization']
    print('headers-----',headers.split()[1])
    jwt = get_jwt_identity()
    print('jwt---------', jwt)
    # Pegar token de autenticação e validar
        # --> como pegar o header pelo request?
    # Se existir aquele usuário, pegar o ID dentro do token de autenticação
        # --> se estivermos usando jwt, só decodificar e pegar a parte do ID
    code = get_invitation_code(data)
    table_group = db.session.query(GroupModel)
    group = table_group.filter(GroupModel.access_code == code).first()
    if not group:
        return {"error": "Group not found."}

    # if group.is_member(user_id):
        # return {"error": "User already in group."}
    
    # se nao existir, criar nova conta conectando grupo ao usuário
    # new_account = AccountModel(group_id=group.id, user_id='blabla')
    # db.session.add(new_account)
    # retornar os dados do grupo atualizados
    accepted = {
        "id": group.id,
        "name": group.name,
        "invite_code": group.access_code,
        "members": group.members_list
    }

    db.session.commit()

    return accepted, 204