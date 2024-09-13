from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from . import app
from .models import Character, User, db


# Função de verificação de token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]  # O token está no formato "Bearer <token>"
        if not token:
            return jsonify({"message": "Token não encontrado."}), 401

        try:
            data = jwt.decode(token, "how-to-find-true-love-and-happiness", algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["id"]).first()
        except Exception as e:
            print(e)
            return jsonify({"message": "Token inválido."}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# Rota para criar um novo usuário
@app.route("/users", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user:
            return (
                jsonify({"message": "Usuário já existe. Por favor, faça login."}),
                200,
            )
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id, "username": user.username}), 201
    return jsonify({"message": "Usuário ou senha inválidos."}), 400


# Rota para fazer login
@app.route("/login", methods=["POST"])
def login():
    auth = request.json

    if not auth or not auth.get("username") or not auth.get("password"):
        return (
            jsonify({"message": "Usuário ou senha inválidos."}),
            401,
        )

    user = User.query.filter_by(username=auth.get("username")).first()

    if not user:
        return (
            jsonify({"message": "Usuário ou senha inválidos."}),
            401,
        )
    if check_password_hash(user.password, auth.get("password")):
        token = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            },
            "how-to-find-true-love-and-happiness",
            "HS256",
        )
        return jsonify({"token": token}, 201)
    return jsonify({"message": "Usuário ou senha inválidos."}), 401


# Rota para criar um novo personagem (agora vinculado ao usuário)
@app.route("/characters", methods=["POST"])
@token_required
def create_character(current_user):
    data = request.get_json()
    new_character = Character(
        name=data["name"],
        race=data["race"],
        class_=data["class_"],
        level=data["level"],
        user_id=current_user.id,
    )
    db.session.add(new_character)
    db.session.commit()

    return (
        jsonify(
            {
                "id": new_character.id,
                "name": new_character.name,
                "race": new_character.race,
                "class": new_character.class_,
                "level": new_character.level,
                "user_id": new_character.user_id,
            }
        ),
        201,
    )


# Rota para listar todos os personagens do usuário logado
@app.route("/characters", methods=["GET"])
@token_required
def get_characters(current_user):
    characters = current_user.characters

    if not characters:
        return jsonify({"message": "Usuário não possui personagens."}), 404

    return (
        jsonify(
            [
                {
                    "id": character.id,
                    "name": character.name,
                    "race": character.race,
                    "class": character.class_,
                    "level": character.level,
                }
                for character in characters
            ]
        ),
        200,
    )


# Rota para buscar um personagem específico do usuário logado por ID
@app.route("/characters/<int:id>", methods=["GET"])
@token_required
def get_character(current_user, id):
    character = Character.query.filter_by(id=id, user_id=current_user.id).first()

    if not character:
        return jsonify({"message": "Personagem não encontrado."}), 404

    return (
        jsonify(
            {
                "id": character.id,
                "name": character.name,
                "race": character.race,
                "class": character.class_,
                "level": character.level,
            }
        ),
        200,
    )


# Rota para editar um personagem existente
@app.route("/characters/<int:id>", methods=["PUT"])
@token_required
def update_character(current_user, id):
    character = Character.query.filter_by(id=id, user_id=current_user.id).first()

    if not character:
        return jsonify({"message": "Personagem não encontrado."}), 404

    data = request.get_json()

    character.name = data.get("name", character.name)
    character.race = data.get("race", character.race)
    character.class_ = data.get("class_", character.class_)
    character.level = data.get("level", character.level)

    db.session.commit()
    return (
        jsonify(
            {
                "id": character.id,
                "name": character.name,
                "race": character.race,
                "class": character.class_,
                "level": character.level,
            }
        ),
        200,
    )


# Rota para deletar um personagem do usuário
@app.route("/characters/<int:id>", methods=["DELETE"])
@token_required
def delete_character(current_user, id):
    character = Character.query.filter_by(id=id, user_id=current_user.id).first()

    if not character:
        return jsonify({"message": "Personagem não encontrado."}), 404

    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": "Personagem deletado com sucesso."}), 200
