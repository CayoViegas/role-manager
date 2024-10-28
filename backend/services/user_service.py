from datetime import datetime, timedelta, timezone

import jwt
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash

from backend import db
from backend.models.user import User


def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    is_superuser = data.get("is_superuser", False)  # O campo is_superuser é opcional e tem False como valor padrão

    if not isinstance(username, str) or len(username) < 3 or len(username) > 50:
        return {"message": "Nome de usuário inválido. Deve conter entre 3 e 50 caracteres."}, 400
    if not isinstance(password, str) or len(password) < 6 or len(password) > 12:
        return {"message": "Senha inválida. Deve conter entre 6 e 12 caracteres."}, 400

    if username and password:
        user_ = User.query.filter_by(username=username).first()
        if user_:
            return (
                {"message": "Usuário já existe. Por favor, faça login."},
                200,
            )
        user_ = User(username=username, password=generate_password_hash(password), is_superuser=is_superuser)
        db.session.add(user_)
        db.session.commit()
        return {"id": user_.id, "username": user_.username, "is_superuser": user_.is_superuser}, 201
    return {"message": "Usuário ou senha inválidos."}, 400


def login():
    auth = request.json

    if not auth or not auth.get("username") or not auth.get("password"):
        return (
            {"message": "Usuário ou senha inválidos."},
            401,
        )

    user_ = User.query.filter_by(username=auth.get("username")).first()

    if not user_:
        return (
            {"message": "Usuário ou senha inválidos."},
            401,
        )
    if check_password_hash(user_.password, auth.get("password")):
        token = jwt.encode(
            {
                "id": user_.id,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24),
            },
            "how-to-find-true-love-and-happiness",
            "HS256",
        )
        return {"token": token, "username": user_.username}, 201
    return {"message": "Usuário ou senha inválidos."}, 401


def delete_user(current_user, id):
    if current_user.id != id:
        return {"message": "Você só pode deletar sua própria conta."}, 403

    user_ = User.query.filter_by(id=id).first()

    if not user_:
        return {"message": "Usuário não encontrado."}, 404

    db.session.delete(user_)
    db.session.commit()

    return {"message": "Usuário e seus personagens foram deletados com sucesso."}, 200
